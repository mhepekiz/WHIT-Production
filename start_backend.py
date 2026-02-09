#!/usr/bin/env python3
"""
Script to start the Django backend server
"""
import os
import sys
import subprocess

# Change to the backend directory
backend_dir = '/Users/mustafahepekiz/Desktop/whit-release/backend'
os.chdir(backend_dir)

# Activate virtual environment
venv_path = '/Users/mustafahepekiz/Desktop/whit-release/.venv/bin/python'

print("🚀 Starting Django backend server...")
print(f"📂 Working directory: {os.getcwd()}")
print(f"🐍 Using Python: {venv_path}")

try:
    # Run Django server
    cmd = [venv_path, 'manage.py', 'runserver', '8000']
    print(f"🔧 Running command: {' '.join(cmd)}")
    
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
    sys.exit(0)