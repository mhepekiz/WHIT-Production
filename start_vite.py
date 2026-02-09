import subprocess
import sys
import os

# Navigate to frontend directory
frontend_dir = "/Users/mustafahepekiz/Desktop/whit-release/frontend"
os.chdir(frontend_dir)

print("Starting frontend server on port 5175...")
print(f"Working directory: {os.getcwd()}")

# Start npm dev server
try:
    result = subprocess.run(["npm", "run", "dev"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error starting frontend server: {e}")
    sys.exit(1)