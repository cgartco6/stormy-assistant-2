#!/usr/bin/env python3
"""
Stormy Clean Installer - Fixed for Windows
"""

import os
import sys
import subprocess
import platform

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("="*50)
    print("🌪️  Stormy Clean Installer")
    print("="*50)
    
    # Get correct paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    print(f"📁 Project directory: {project_dir}")
    
    # Check Python version
    py_version = sys.version_info
    print(f"🐍 Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    # Activate venv or create if doesn't exist
    venv_path = os.path.join(project_dir, 'venv')
    if not os.path.exists(venv_path):
        print("🔹 Creating virtual environment...")
        run_cmd(f"{sys.executable} -m venv venv")
    
    # Get pip path
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_path, 'Scripts', 'pip')
        python_path = os.path.join(venv_path, 'Scripts', 'python')
    else:
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    # Upgrade pip
    print("🔹 Upgrading pip...")
    run_cmd(f'"{python_path}" -m pip install --upgrade pip')
    
    # Install pipwin first
    print("🔹 Installing pipwin...")
    run_cmd(f'"{pip_path}" install pipwin')
    
    # Use pipwin to install PyAudio
    print("🔹 Installing PyAudio via pipwin...")
    run_cmd(f'"{python_path}" -m pipwin install pyaudio')
    
    # Install requirements
    print("🔹 Installing requirements...")
    run_cmd(f'"{pip_path}" install -r requirements.txt')
    run_cmd(f'"{pip_path}" install -r web\\requirements-web.txt')
    run_cmd(f'"{pip_path}" install -r desktop\\requirements-desktop.txt')
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/logs', exist_ok=True)
    
    print("\n" + "="*50)
    print("✅ Installation Complete!")
    print("="*50)
    print("\nTo run Stormy:")
    print("  1. venv\\Scripts\\activate")
    print("  2. python desktop\\main.py")
    print("\nOr for web version:")
    print("  python web\\app.py")

if __name__ == "__main__":
    main()
