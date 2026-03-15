#!/usr/bin/env python3
"""
Stormy Render Deployment Script
Deploys to Render.com automatically
"""

import os
import sys
import subprocess
import json
import time
import requests

def check_render_cli():
    """Check if Render CLI is installed"""
    try:
        subprocess.run(['render', '--version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def deploy_to_render():
    print("🌪️  Deploying Stormy to Render...")
    
    # Check for render.yaml
    if not os.path.exists('render.yaml'):
        print("❌ render.yaml not found!")
        return False
    
    # Check if git repo exists
    if not os.path.exists('.git'):
        print("📦 Initializing git repository...")
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit for Render deployment'])
    
    # Check Render CLI
    if not check_render_cli():
        print("📦 Installing Render CLI...")
        subprocess.run(['npm', 'install', '-g', '@render/cli'])
    
    # Login to Render (interactive)
    print("🔑 Please log in to Render:")
    subprocess.run(['render', 'login'])
    
    # Deploy
    print("🚀 Deploying to Render...")
    result = subprocess.run(['render', 'deploy'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Deployment initiated!")
        print("📊 Check status at: https://dashboard.render.com")
        return True
    else:
        print(f"❌ Deployment failed: {result.stderr}")
        return False

if __name__ == '__main__':
    deploy_to_render()
