#!/usr/bin/env python3
import os
import signal

print("Checking for existing processes...")

# Kill any existing npm/node processes
os.system("pkill -f npm 2>/dev/null")
os.system("pkill -f node 2>/dev/null") 
os.system("pkill -f vite 2>/dev/null")

print("Starting frontend server directly...")

# Change to frontend directory
os.chdir("/Users/mustafahepekiz/Desktop/whit-release/frontend")

# Start the server
os.system("npm run dev &")

print("Frontend server started in background")