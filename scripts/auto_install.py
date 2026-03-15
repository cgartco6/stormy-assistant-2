#!/usr/bin/env python3
"""
Stormy Mega Auto-Installer - Works on Windows, macOS, Linux
Autodetects everything and sets up Stormy in minutes!
"""

import os
import sys
import platform
import subprocess
import shutil
import json
import time
from pathlib import Path

# ==================== CONFIGURATION ====================
PROJECT_NAME = "stormy-assistant-2"
REQUIRED_PYTHON = (3, 8)
GITHUB_REPO = "yourusername/stormy-assistant-2"  # Change this!

# ==================== COLOR CODES ====================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg):
    print(f"\n{Colors.BLUE}🔹 {msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

# ==================== OS DETECTION ====================
def detect_os():
    system = platform.system().lower()
    if 'windows' in system:
        return 'windows'
    elif 'darwin' in system:
        return 'macos'
    elif 'linux' in system:
        return 'linux'
    return 'unknown'

def detect_arch():
    machine = platform.machine().lower()
    if '64' in machine or 'amd64' in machine or 'x86_64' in machine:
        return '64bit'
    return '32bit'

# ==================== COMMAND CHECKING ====================
def check_command(cmd, name):
    if shutil.which(cmd):
        print_success(f"{name} found")
        return True
    print_warning(f"{name} not found")
    return False

def get_command_path(cmd):
    return shutil.which(cmd) or cmd

# ==================== PYTHON CHECK ====================
def check_python():
    v = sys.version_info
    if v.major < REQUIRED_PYTHON[0] or (v.major == REQUIRED_PYTHON[0] and v.minor < REQUIRED_PYTHON[1]):
        print_error(f"Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ required. You have {v.major}.{v.minor}")
        return False
    print_success(f"Python {v.major}.{v.minor}.{v.micro}")
    return True

# ==================== RUN COMMAND ====================
def run_cmd(cmd, cwd=None, shell=False, check=False):
    print(f"  Running: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    try:
        if isinstance(cmd, list):
            result = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=True, text=True)
        
        if result.returncode != 0:
            if check:
                print_error(f"Command failed: {result.stderr}")
                return None
            print_warning(f"Command returned {result.returncode}")
        return result
    except Exception as e:
        print_error(f"Error running command: {e}")
        return None

# ==================== INSTALL PYTHON PACKAGES ====================
def install_packages(pip_cmd, req_file):
    print(f"  Installing from {req_file}...")
    if os.path.exists(req_file):
        return run_cmd([pip_cmd, 'install', '-r', req_file])
    return None

# ==================== MAIN INSTALLER ====================
def main():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("="*60)
    print("🌪️  STORMY ASSISTANT - MEGA AUTO-INSTALLER")
    print("="*60)
    print(f"{Colors.END}")

    # Detect system
    os_type = detect_os()
    arch = detect_arch()
    print_step(f"Detected System: {os_type.upper()} ({arch})")

    # Check Python
    if not check_python():
        sys.exit(1)

    # Check for required tools
    print_step("Checking required tools...")
    has_pip = check_command('pip', 'pip')
    has_venv = check_command('virtualenv', 'virtualenv/venv') or check_command('python3 -m venv', 'venv module')
    has_git = check_command('git', 'Git')
    has_docker = check_command('docker', 'Docker')
    has_node = check_command('node', 'Node.js')
    has_npm = check_command('npm', 'npm')
    has_curl = check_command('curl', 'curl')
    has_wget = check_command('wget', 'wget')

    # Set project paths
    project_path = Path.cwd()
    if project_path.name != PROJECT_NAME:
        project_path = project_path / PROJECT_NAME
    
    if not project_path.exists():
        print_step(f"Creating project directory: {project_path}")
        project_path.mkdir(parents=True, exist_ok=True)
    
    os.chdir(project_path)
    print_success(f"Working directory: {project_path}")

    # ==================== SETUP VIRTUAL ENVIRONMENT ====================
    print_step("Setting up Python virtual environment...")
    
    venv_path = project_path / 'venv'
    
    if os_type == 'windows':
        venv_cmd = [sys.executable, '-m', 'venv', 'venv']
        python_cmd = str(venv_path / 'Scripts' / 'python')
        pip_cmd = str(venv_path / 'Scripts' / 'pip')
        activate_cmd = str(venv_path / 'Scripts' / 'activate.bat')
    else:
        venv_cmd = [sys.executable, '-m', 'venv', 'venv']
        python_cmd = str(venv_path / 'bin' / 'python')
        pip_cmd = str(venv_path / 'bin' / 'pip')
        activate_cmd = f"source {venv_path}/bin/activate"
    
    if not venv_path.exists():
        run_cmd(venv_cmd)
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment already exists")

    # Upgrade pip
    print_step("Upgrading pip...")
    run_cmd([pip_cmd, 'install', '--upgrade', 'pip'])

    # ==================== INSTALL DEPENDENCIES ====================
    print_step("Installing Python dependencies...")
    
    # Install from different requirement files
    req_files = ['requirements.txt', 'web/requirements-web.txt', 'desktop/requirements-desktop.txt']
    for req_file in req_files:
        if os.path.exists(req_file):
            install_packages(pip_cmd, req_file)

    # Install additional packages based on OS
    if os_type == 'windows':
        print_step("Installing Windows-specific packages...")
        run_cmd([pip_cmd, 'install', 'pywin32'])
        # Try to install PyAudio (might need wheel)
        try:
            run_cmd([pip_cmd, 'install', 'pyaudio'])
        except:
            print_warning("PyAudio installation failed. You may need to install manually.")
    elif os_type == 'linux':
        print_step("Installing Linux system dependencies...")
        if check_command('apt-get', 'apt-get'):
            run_cmd(['sudo', 'apt-get', 'update'])
            run_cmd(['sudo', 'apt-get', 'install', '-y', 'portaudio19-dev', 'python3-pyaudio', 'espeak'])
        elif check_command('yum', 'yum'):
            run_cmd(['sudo', 'yum', 'install', '-y', 'portaudio-devel', 'python3-pyaudio', 'espeak'])
    elif os_type == 'macos':
        print_step("Installing macOS dependencies...")
        if check_command('brew', 'Homebrew'):
            run_cmd(['brew', 'install', 'portaudio', 'espeak'])

    # ==================== SETUP CONFIGURATION ====================
    print_step("Setting up configuration...")
    
    if os.path.exists('.env.example') and not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print_success("Created .env file from template")

    # ==================== CREATE DATA DIRECTORIES ====================
    print_step("Creating data directories...")
    data_dirs = ['data', 'data/logs', 'localization/stt_models', 'localization/tts_voices']
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path}")

    # ==================== TEST MICROPHONE ====================
    print_step("Testing microphone...")
    if os.path.exists('scripts/test_microphone.py'):
        run_cmd([python_cmd, 'scripts/test_microphone.py'])

    # ==================== DOCKER SETUP (if available) ====================
    if has_docker:
        print_step("Docker detected. Setting up containers...")
        if os.path.exists('Dockerfile'):
            choice = input(f"{Colors.YELLOW}Build Docker image? (y/n): {Colors.END}").lower()
            if choice == 'y':
                run_cmd(['docker', 'build', '-t', 'stormy', '.'])
                run_cmd(['docker-compose', 'up', '-d'])

    # ==================== GIT SETUP ====================
    if has_git and not os.path.exists('.git'):
        print_step("Initializing Git repository...")
        run_cmd(['git', 'init'])
        run_cmd(['git', 'add', '.'])
        run_cmd(['git', 'commit', '-m', 'Initial commit of Stormy Assistant'])
        
        if GITHUB_REPO != "yourusername/stormy-assistant-2":
            run_cmd(['git', 'remote', 'add', 'origin', f'https://github.com/{GITHUB_REPO}.git'])
            print_success(f"Remote added: https://github.com/{GITHUB_REPO}.git")

    # ==================== LAUNCH OPTIONS ====================
    print_step("Launch Options")
    print(f"{Colors.BOLD}Choose how to run Stormy:{Colors.END}")
    print("  1. Desktop version (full voice, local)")
    print("  2. Web version (Flask server)")
    print("  3. Docker container")
    print("  4. Deploy to Render")
    print("  5. Deploy to PythonAnywhere")
    print("  6. Exit")
    
    choice = input(f"{Colors.YELLOW}Enter choice (1-6): {Colors.END}").strip()
    
    if choice == '1':
        print_step("Launching Desktop Stormy...")
        run_cmd([python_cmd, 'desktop/main.py'])
    
    elif choice == '2':
        print_step("Launching Web Stormy...")
        port = input("Port (default 5000): ").strip() or '5000'
        host = '0.0.0.0'
        print(f"🌐 Server will be available at: http://{host}:{port}")
        print("📱 On your phone, use your computer's IP address")
        os.environ['FLASK_ENV'] = 'development'
        run_cmd([python_cmd, 'web/app.py', '--host', host, '--port', port])
    
    elif choice == '3' and has_docker:
        print_step("Launching Docker Stormy...")
        run_cmd(['docker-compose', 'up'])
    
    elif choice == '4':
        print_step("Deploying to Render...")
        if os.path.exists('scripts/deploy_render.py'):
            run_cmd([python_cmd, 'scripts/deploy_render.py'])
    
    elif choice == '5':
        print_step("Deploying to PythonAnywhere...")
        if os.path.exists('scripts/deploy_pythonanywhere.py'):
            run_cmd([python_cmd, 'scripts/deploy_pythonanywhere.py'])
    
    else:
        print_success("Installation complete! Run Stormy manually with:")
        if os_type == 'windows':
            print(f"\n  {venv_path}\\Scripts\\activate")
        else:
            print(f"\n  source {venv_path}/bin/activate")
        print(f"  python desktop/main.py  # Desktop version")
        print(f"  python web/app.py       # Web version")

    print(f"\n{Colors.GREEN}{Colors.BOLD}")
    print("="*60)
    print("🌪️  STORMY INSTALLATION COMPLETE!")
    print("="*60)
    print(f"{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Installation cancelled.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
