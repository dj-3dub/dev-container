# Using the 2026 LTS version of PowerShell
FROM mcr.microsoft.com/powershell:lts-debian-13

# Avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Basics
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git ca-certificates jq && \
    rm -rf /var/lib/apt/lists/*

# 2. Install SRE Modules via PWSH
# We use -Scope AllUsers so they are available to any user in the container
RUN pwsh -Command "\
    Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted; \
    Install-Module -Name AWS.Tools.Installer -Force -Scope AllUsers; \
    Install-Module -Name Pester -Force -Scope AllUsers; \
    Install-Module -Name PSFramework -Force -Scope AllUsers; \
    Install-Module -Name powershell-yaml -Force -Scope AllUsers; \
    Install-Module -Name Terminal-Icons -Force -Scope AllUsers"

# 3. Pre-install specific AWS modules for SAA study
# This saves time during container startup
RUN pwsh -Command "Install-AWSToolsModule AWS.Tools.EC2,AWS.Tools.S3,AWS.Tools.IAM -CleanUp -Force"

WORKDIR /workspace

# Start PowerShell with the Terminal-Icons enabled in the profile
RUN echo 'Import-Module Terminal-Icons' >> $PSHOME/Microsoft.PowerShell_profile.ps1

CMD ["pwsh"]
