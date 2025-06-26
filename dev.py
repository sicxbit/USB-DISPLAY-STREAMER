import os
import zipfile
import urllib.request
import subprocess
import time

# Constants
ADB_ZIP_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
ADB_ZIP_PATH = "platform-tools.zip"
ADB_DIR = "adb"
REQUIRED_FILES = ["adb.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll"]

#Checking if required ADB files are already extracted
def adb_files_present():
    return all(os.path.isfile(os.path.join(ADB_DIR, f)) for f in REQUIRED_FILES)

if not adb_files_present():
    print("⬇️ Downloading platform-tools (ADB)...")
    urllib.request.urlretrieve(ADB_ZIP_URL, ADB_ZIP_PATH)

    print("📦 Extracting required ADB files...")
    with zipfile.ZipFile(ADB_ZIP_PATH, 'r') as zip_ref:
        for file in zip_ref.namelist():
            filename = os.path.basename(file)
            if filename in REQUIRED_FILES:
                os.makedirs(ADB_DIR, exist_ok=True)
                with open(os.path.join(ADB_DIR, filename), "wb") as f:
                    f.write(zip_ref.read(file))

    os.remove(ADB_ZIP_PATH)
    print("✅ ADB files extracted to ./adb")
else:
    print("✔️ ADB already set up — skipping download.")


# checking if the dummy display driver is installed and if not, running the setup script
if not os.path.exists(os.path.join("tools", "SudoVDA")):
    print("🚀 Running dummy display setup...")
    subprocess.run(["python", "setupDummyDisplay.py"], shell=True)


print("🚀 Starting Flask server on localhost:8080...")
subprocess.Popen(["venv\\Scripts\\python.exe", "stream.py"], shell=True)

time.sleep(3)

adb_path = os.path.join(ADB_DIR, "adb.exe")
print("🔁 Setting up ADB reverse (USB tethering)...")

try:
    result = subprocess.run([adb_path, "reverse", "tcp:8080", "tcp:8080"], check=True)
    print("✅ Port reverse successful! Visit http://localhost:8080 on your phone browser.")
except subprocess.CalledProcessError:
    print("❌ Port reverse failed.")
    print("👉 Try checking your USB connection or authorize USB debugging on your phone.")
    input("Press Enter after authorizing USB debugging...")


input("🛑 Press Enter to quit...")
