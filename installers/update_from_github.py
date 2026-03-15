#!/usr/bin/env python3
import os
import subprocess
import sys

def update_from_github():
    if not os.path.exists('.git'):
        print("Not a git repository. Please clone first.")
        return
    
    print("Pulling latest changes...")
    subprocess.run(['git', 'pull'])
    
    print("Updating dependencies...")
    if os.path.exists('venv'):
        if sys.platform == 'win32':
            pip = 'venv\\Scripts\\pip'
        else:
            pip = 'venv/bin/pip'
        subprocess.run([pip, 'install', '-r', 'requirements.txt'])
    
    print("✅ Update complete!")

if __name__ == '__main__':
    update_from_github()
