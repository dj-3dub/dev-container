use clap::{Parser, Subcommand};
use std::fs::File;
use std::io::Write;
use std::process::Command;

const ZABBIX_SENDER_PATH: &str = "/workspace/homelab-helper/zabbix_sender.txt";

#[derive(Parser)]
#[command(
    name = "homelab-helper",
    version,
    about = "Rust CLI for homelab health checks and Zabbix integration"
)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Simple ICMP ping check
    Ping {
        /// Host to ping
        host: String,
        /// Number of echo requests
        #[arg(short, long, default_value_t = 2)]
        count: u32,
    },
    /// Summary health check + Zabbix sender file
    Summary {
        /// Host to check (via ping)
        host: String,
        /// Zabbix logical host name to use when writing metrics
        #[arg(long, default_value = "lab-health-rust")]
        zabbix_host: String,
    },
}

fn run_ping(host: &str, count: u32) -> bool {
    // Uses the container's ping utility
    let output = Command::new("ping")
        .arg("-c")
        .arg(count.to_string())
        .arg(host)
        .output();

    match output {
        Ok(out) => out.status.success(),
        Err(_) => false,
    }
}

fn write_zabbix_sender_file(zabbix_host: &str, metrics: &[(&str, i64)]) -> std::io::Result<()> {
    let mut file = File::create(ZABBIX_SENDER_PATH)?;
    for (key, value) in metrics {
        writeln!(file, "{host} {key} {value}", host = zabbix_host, key = key, value = value)?;
    }
    Ok(())
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Ping { host, count } => {
            println!("Pinging {} ({} packets)...", host, count);
            let ok = run_ping(&host, count);
            if ok {
                println!("PING OK");
                std::process::exit(0);
            } else {
                println!("PING FAILED");
                std::process::exit(1);
            }
        }
        Commands::Summary { host, zabbix_host } => {
            println!("Running summary health check for host: {}", host);

            // For now, summary = just ping. You can expand this later.
            let ping_ok = run_ping(&host, 2);

            let total_checks: i64 = 1;
            let fail_checks: i64 = if ping_ok { 0 } else { 1 };
            let overall_ok: i64 = if ping_ok { 1 } else { 0 };

            println!("Summary:");
            println!("  Total checks : {}", total_checks);
            println!("  Failed checks: {}", fail_checks);
            println!("  Overall OK   : {}", overall_ok);

            // Build Zabbix metrics (mirror Python pattern)
            let metrics = vec![
                ("lab.rust_checks.total", total_checks),
                ("lab.rust_checks.fail", fail_checks),
                ("lab.rust_health.ok", overall_ok),
            ];

            match write_zabbix_sender_file(&zabbix_host, &metrics) {
                Ok(_) => {
                    println!(
                        "Wrote Zabbix sender file to {} for host '{}'.",
                        ZABBIX_SENDER_PATH, zabbix_host
                    );
                    // exit code still reflects health
                    std::process::exit(if overall_ok == 1 { 0 } else { 1 });
                }
                Err(e) => {
                    eprintln!("Failed to write Zabbix sender file: {}", e);
                    std::process::exit(1);
                }
            }
        }
    }
}
