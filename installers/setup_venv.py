#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def setup_venv():
    system = platform.system().lower()
    
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    if system == 'windows':
        pip_path = 'venv\\Scripts\\pip'
        activate = 'venv\\Scripts\\activate'
    else:
        pip_path = 'venv/bin/pip'
        activate = 'source venv/bin/activate'
    
    print("Installing dependencies...")
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    
    print(f"\n✅ Setup complete! Activate with: {activate}")

if __name__ == '__main__':
    setup_venv()
