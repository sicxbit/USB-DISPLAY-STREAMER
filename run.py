import subprocess
import time
import os

adb_path = os.path.join("adb", "adb.exe")

print("✅ Starting Flask server...")
subprocess.Popen(["venv\\Scripts\\python.exe", "stream.py"], shell=True)

time.sleep(3)

print("🔁 Setting up ADB reverse...")
subprocess.run([adb_path, "reverse", "tcp:8080", "tcp:8080"])

print("✅ Done! Open http://localhost:8080 on your phone.")
input("Press Enter to exit...")