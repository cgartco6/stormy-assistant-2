#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Stormy Assistant Windows PowerShell Installer
.DESCRIPTION
    Auto-detects Windows environment and installs Stormy with all dependencies
#>

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors
$Green = [char]0x1b + "[92m"
$Yellow = [char]0x1b + "[93m"
$Red = [char]0x1b + "[91m"
$Blue = [char]0x1b + "[94m"
$Reset = [char]0x1b + "[0m"

Write-Host "$Blue========================================$Reset"
Write-Host "$Blue🌪️  STORMY WINDOWS INSTALLER$Reset"
Write-Host "$Blue========================================$Reset"

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "$Yellow⚠️  Not running as administrator. Some operations may fail.$Reset"
    $choice = Read-Host "Continue anyway? (y/n)"
    if ($choice -ne 'y') { exit }
}

# Check Python
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "$Green✅ Python found: $pythonVersion$Reset"
} catch {
    Write-Host "$Red❌ Python not found. Please install Python 3.8+ from python.org$Reset"
    exit 1
}

# Check pip
try {
    $pipVersion = & pip --version 2>&1
    Write-Host "$Green✅ pip found$Reset"
} catch {
    Write-Host "$Red❌ pip not found. Installing...$Reset"
    python -m ensurepip --upgrade
}

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "$Blue🔹 Creating virtual environment...$Reset"
    python -m venv venv
}

# Activate and install
Write-Host "$Blue🔹 Installing dependencies...$Reset"
& .\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
pip install -r web\requirements-web.txt
pip install -r desktop\requirements-desktop.txt

# Install PyAudio (special handling for Windows)
try {
    pip install pyaudio
} catch {
    Write-Host "$Yellow⚠️  PyAudio installation failed. Downloading wheel...$Reset"
    $pythonVersion = python -c "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')"
    $arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "win32" }
    $url = "https://download.lfd.uci.edu/pythonlibs/archived/cp$pythonVersion/PyAudio-0.2.11-cp$pythonVersion-cp$pythonVersion-win_$arch.whl"
    $output = "PyAudio.whl"
    Invoke-WebRequest -Uri $url -OutFile $output
    pip install $output
    Remove-Item $output
}

# Create data directories
New-Item -ItemType Directory -Force -Path data, data\logs, localization\stt_models, localization\tts_voices | Out-Null

# Test microphone
Write-Host "$Blue🔹 Testing microphone...$Reset"
python scripts\test_microphone.py

# Offer launch options
Write-Host "$Blue`nLaunch Options:$Reset"
Write-Host "1. Desktop version (full voice)"
Write-Host "2. Web version (Flask server)"
Write-Host "3. Exit"

$choice = Read-Host "Enter choice (1-3)"
switch ($choice) {
    '1' { python desktop\main.py }
    '2' { 
        $port = Read-Host "Port (default 5000)"
        if (-not $port) { $port = 5000 }
        $ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"} | Select-Object -First 1).IPAddress
        Write-Host "$Green🌐 Server: http://$ip`:$port$Reset"
        python web\app.py --host 0.0.0.0 --port $port
    }
}

Write-Host "$Green✅ Installation complete!$Reset"
