import os
import sys
import zipfile
import requests
import shutil

def get_chrome_version():
    import subprocess
    try:
        if sys.platform == "win32":
            process = subprocess.Popen([r"reg", "query", r"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon", "/v", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if b"version" in out:
                version = out.decode().split()[-1]
                return version
        # For other OS, add logic as needed
    except Exception:
        pass
    return None

def download_chromedriver(version=None, dest_folder="."):
    if not version:
        version = "latest"
    # Get latest version if not specified
    if version == "latest":
        resp = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        version = resp.text.strip()
    # Download chromedriver zip
    url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
    zip_path = os.path.join(dest_folder, "chromedriver_win32.zip")
    resp = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(resp.content)
    # Extract
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    os.remove(zip_path)
    # Optionally move to PATH
    chromedriver_path = os.path.join(dest_folder, "chromedriver.exe")
    system32 = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "System32")
    try:
        shutil.copy(chromedriver_path, system32)
        print(f"chromedriver.exe copied to {system32}")
    except Exception as e:
        print(f"Could not copy to System32: {e}")
    print(f"chromedriver.exe is ready at {chromedriver_path}")

if __name__ == "__main__":
    chrome_version = get_chrome_version()
    print(f"Detected Chrome version: {chrome_version}")
    download_chromedriver()
