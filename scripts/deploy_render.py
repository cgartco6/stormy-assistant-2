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
        subprocess.run(['git', '
