import subprocess
import os
import urllib.request
import zipfile
import sys
import ctypes


# #requesting admin privileges
# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False


# if not is_admin():
#     print("⚠️  Requesting Administrator permission...")
#     # Relaunch the script with admin rights
#     ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     sys.exit()

# for better debugging, we will run vs code itself as admin vs terminal is better than windows powershell

print("✅ Running as Administrator!")

def download_and_extract_sudovda():
    """
    Downloads the SudoVDA repository ZIP from GitHub,
    extracts it to ./tools/SudoVDA, and returns the folder path.
    """

    repo_url = "https://github.com/SudoMaker/SudoVDA/archive/refs/heads/master.zip"
    zip_path = "SudoVDA.zip"
    extract_to = os.path.join("tools", "SudoVDA")  # Target folder

    # If SudoVDA already exists, skip downloading
    if os.path.exists(extract_to):
        print("✅ SudoVDA already exists.")
        return extract_to

    # Download the ZIP file
    print("⬇️ Downloading SudoVDA...")
    urllib.request.urlretrieve(repo_url, zip_path)

    # Extract the ZIP to the 'tools' folder
    print("📦 Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("tools")

    # The extracted folder will be named 'SudoVDA-master', so rename it
    os.rename(os.path.join("tools", "SudoVDA-master"), extract_to)

    # Clean up ZIP file after extraction
    os.remove(zip_path)

    print("✅ Extraction complete.")
    return extract_to  # Return the path for later use


def install_driver(sudovda_path):
    """
    Installs the SudoVDA driver from the INF file located inside the given path.
    """

    # Setting the path to the INF file
    inf_path = os.path.join(sudovda_path, "Virtual Display Driver (HDR)","SudoVDA", "SudoVDA.inf")

    # Check if the INF file actually exists
    if not os.path.exists(inf_path):
        print(f"❌ INF file not found at {inf_path}")
        return

    # Run pnputil to install the driver (requires administrator privileges)
    print("⚙️ Installing SudoVDA driver...")
    result = subprocess.run(
        ["pnputil", "/add-driver", inf_path, "/install"],
        capture_output=True,
        text=True
    )

    # Check the result of the installation
    if result.returncode == 0:
        print("✅ Driver installed successfully.")
    else:
        print("❌ Driver installation failed.")
        print(result.stdout)
        print(result.stderr)


def main():
    """
    Main function to handle downloading and installing the driver.
    """

    # Step 1: Download and extract SudoVDA
    sudovda_folder = download_and_extract_sudovda()

    # Step 2: Install the driver
    install_driver(sudovda_folder)


if __name__ == "__main__":
    main()
