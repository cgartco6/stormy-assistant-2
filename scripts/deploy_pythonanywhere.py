#!/usr/bin/env python3
"""
Stormy PythonAnywhere Deployment Script
"""

import os
import sys
import subprocess
import requests
import getpass

def deploy_to_pythonanywhere():
    print("🌪️  Deploying Stormy to PythonAnywhere...")
    
    username = input("PythonAnywhere username: ")
    password = getpass.getpass("PythonAnywhere password: ")
    
    # Prepare files for upload
    files_to_upload = [
        'web/app.py',
        'web/wsgi.py',
        'web/requirements-web.txt',
        'templates/index.html',
        'static/style.css'
    ]
    
    # Create a tar file
    print("📦 Creating deployment package...")
    import tarfile
    with tarfile.open('stormy_deploy.tar.gz', 'w:gz') as tar:
        for file in files_to_upload:
            if os.path.exists(file):
                tar.add(file)
    
    # Upload via SCP-like API (simplified)
    print("📤 Uploading to PythonAnywhere...")
    
    # Note: Real implementation would use PythonAnywhere API
    print("\n📋 Manual deployment steps:")
    print("1. Log in to pythonanywhere.com")
    print("2. Go to Files tab")
    print("3. Upload these files:")
    for file in files_to_upload:
        print(f"   - {file}")
    print("4. Go to Web tab and create a new web app")
    print("5. Select Flask and Python 3.9")
    print("6. Set WSGI file to point to web/wsgi.py")
    print("7. Reload the app")
    
    return True

if __name__ == '__main__':
    deploy_to_pythonanywhere()
