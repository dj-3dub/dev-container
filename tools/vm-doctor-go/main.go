package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

type CmdResult struct {
	Cmd    string `json:"cmd"`
	RC     int    `json:"rc"`
	Stdout string `json:"stdout"`
	Stderr string `json:"stderr"`
}

type Report struct {
	Meta   map[string]any       `json:"meta"`
	Checks map[string]CmdResult `json:"checks"`
	Docker map[string]CmdResult `json:"docker"`
	Fixes  map[string]CmdResult `json:"fixes,omitempty"`
}

func run(cmd string, timeout time.Duration) CmdResult {
	c := exec.Command("bash", "-lc", cmd)
	outB, errB := new(strings.Builder), new(strings.Builder)
	c.Stdout = outB
	c.Stderr = errB

	rc := 0
	done := make(chan error, 1)
	go func() { done <- c.Run() }()

	select {
	case e := <-done:
		if e != nil {
			if ee, ok := e.(*exec.ExitError); ok {
				rc = ee.ExitCode()
			} else {
				rc = 1
			}
		}
	case <-time.After(timeout):
		_ = c.Process.Kill()
		rc = 124
		errB.WriteString("\nTIMEOUT\n")
	}

	return CmdResult{Cmd: cmd, RC: rc, Stdout: strings.TrimSpace(outB.String()), Stderr: strings.TrimSpace(errB.String())}
}

func have(bin string) bool { _, err := exec.LookPath(bin); return err == nil }
func sudo(cmd string) string { return "sudo -n " + cmd }

func hostname() string {
	r := run("hostname", 2*time.Second)
	if r.Stdout != "" {
		return r.Stdout
	}
	return "host"
}

func stamp() string { return time.Now().Format("20060102_150405") }

func main() {
	outdir := flag.String("outdir", filepath.Join(os.Getenv("HOME"), "vm-doctor-reports"), "Report output dir")
	fix := flag.Bool("fix", false, "Safe cleanup: apt clean/autoremove + journal vacuum")
	dockerCachePrune := flag.Bool("docker-cache-prune", false, "Prune Docker build cache (builder prune)")
	dockerPrune := flag.Bool("docker-prune", false, "DANGEROUS: docker system prune -af --volumes")
	flag.Parse()

	ts := stamp()
	host := hostname()
	dockerPresent := have("docker")

	rep := Report{
		Meta: map[string]any{
			"host":               host,
			"timestamp":          ts,
			"fix":                *fix,
			"docker_cache_prune": *dockerCachePrune,
			"docker_prune":       *dockerPrune,
			"docker_present":     dockerPresent,
		},
		Checks: map[string]CmdResult{},
		Docker: map[string]CmdResult{},
		Fixes:  map[string]CmdResult{},
	}

	checks := []struct {
		k string
		c string
		t time.Duration
	}{
		{"date", "date", 3 * time.Second},
		{"uptime", "uptime", 3 * time.Second},
		{"df", "df -hT", 10 * time.Second},
		{"lsblk", "lsblk -f || true", 10 * time.Second},
		{"free", "free -h", 3 * time.Second},
		{"swap", "swapon --show || true", 3 * time.Second},
		{"top_mem", "ps aux --sort=-%mem | head -25", 5 * time.Second},
		{"top_cpu", "ps aux --sort=-%cpu | head -25", 5 * time.Second},
		{"du_root", sudo("du -xh / --max-depth=1 2>/dev/null | sort -h"), 3 * time.Minute},
		{"du_var", sudo("du -xh /var --max-depth=2 2>/dev/null | sort -h | tail -80"), 4 * time.Minute},
		{"journal_usage", sudo("journalctl --disk-usage || true"), 10 * time.Second},
		{"log_sizes", sudo("du -sh /var/log/* 2>/dev/null | sort -h | tail -40"), 20 * time.Second},
		{"apt_cache", sudo("du -sh /var/cache/apt/archives 2>/dev/null || true"), 10 * time.Second},
		{"apt_autoremove_dry", sudo("apt-get -s autoremove --purge | sed -n '1,160p' || true"), 20 * time.Second},
		{"largest_pkgs", "dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n | tail -60 || true", 20 * time.Second},
		{"running_services", "systemctl --type=service --state=running | sed -n '1,220p' || true", 10 * time.Second},
	}

	for _, x := range checks {
		rep.Checks[x.k] = run(x.c, x.t)
	}

	if dockerPresent {
		dchecks := []struct {
			k string
			c string
			t time.Duration
		}{
			{"df", "docker system df -v", 30 * time.Second},
			{"ps", "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'", 15 * time.Second},
			{"exited", "docker ps -a --filter status=exited --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'", 15 * time.Second},
			{"dangling_images", "docker images -f dangling=true --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}'", 15 * time.Second},
			{"dangling_vols", "docker volume ls -qf dangling=true", 10 * time.Second},
			{"build_cache", "docker builder du 2>/dev/null || true", 15 * time.Second},
		}
		for _, x := range dchecks {
			rep.Docker[x.k] = run(x.c, x.t)
		}
	} else {
		rep.Docker["note"] = CmdResult{Cmd: "docker", RC: 1, Stderr: "docker not installed"}
	}

	if *fix {
		rep.Fixes["apt_clean"] = run(sudo("apt-get clean"), 2*time.Minute)
		rep.Fixes["apt_autoremove"] = run(sudo("apt-get autoremove --purge -y"), 10*time.Minute)
		rep.Fixes["journal_vacuum_7d"] = run(sudo("journalctl --vacuum-time=7d || true"), 3*time.Minute)
	}
	if *dockerCachePrune && dockerPresent {
		rep.Fixes["docker_cache_prune"] = run("docker builder prune -a -f", 10*time.Minute)
	}
	if *dockerPrune && dockerPresent {
		rep.Fixes["docker_prune"] = run("docker system prune -af --volumes", 15*time.Minute)
	}

	_ = os.MkdirAll(*outdir, 0o755)
	base := fmt.Sprintf("vm_doctor_%s_%s", host, ts)
	txtPath := filepath.Join(*outdir, base+".txt")
	jsonPath := filepath.Join(*outdir, base+".json")

	jb, _ := json.MarshalIndent(rep, "", "  ")
	_ = os.WriteFile(jsonPath, jb, 0o644)

	var b strings.Builder
	b.WriteString(fmt.Sprintf("VM DOCTOR REPORT: %s @ %s\n", host, ts))
	b.WriteString(fmt.Sprintf("docker_present=%v fix=%v docker_cache_prune=%v docker_prune=%v\n",
		dockerPresent, *fix, *dockerCachePrune, *dockerPrune))

	writeBlock := func(title string, r CmdResult) {
		b.WriteString("\n== " + title + " ==\n")
		if r.Stdout != "" {
			b.WriteString(r.Stdout + "\n")
		}
		if r.Stderr != "" {
			b.WriteString("\n-- stderr --\n" + r.Stderr + "\n")
		}
		b.WriteString(fmt.Sprintf("\n(rc=%d)\n", r.RC))
	}
	for k, v := range rep.Checks {
		writeBlock(k, v)
	}
	for k, v := range rep.Docker {
		writeBlock("docker/"+k, v)
	}
	for k, v := range rep.Fixes {
		writeBlock("fix/"+k, v)
	}

	_ = os.WriteFile(txtPath, []byte(b.String()), 0o644)
	fmt.Println("Wrote:")
	fmt.Println(" ", txtPath)
	fmt.Println(" ", jsonPath)
}
