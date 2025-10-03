"""
auto_update.py - Automatic update and OS compatibility checker for Talkback Assistant (mobile)
"""
import sys
import platform
# pyright: ignore[reportMissingImports]
import requests
import os

def get_os_info():
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'python': platform.python_version(),
    }

def check_for_app_update(current_version, update_url):
    try:
        resp = requests.get(update_url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            latest = data.get('latest_version')
            if latest and latest != current_version:
                return data.get('download_url')
    except Exception:
        pass
    return None
def apply_update(download_url):
    
    try:
        resp = requests.get(download_url, timeout=10)
        if resp.status_code == 200:
            fname = os.path.join(os.getcwd(), 'update_package.zip')
            with open(fname, 'wb') as f:
                f.write(resp.content)
            # TODO: Unzip and replace files, restart app
            print("Update downloaded. Please restart the app to apply.")
            return True
    except Exception as e:
        print(f"Update failed: {e}")
    return False

def check_os_compatibility():
    info = get_os_info()
    # Example: warn if major OS update detected
    if info['system'] == 'Linux' and 'ANDROID_STORAGE' in os.environ:
        print("Detected Android. Checking compatibility...")
    elif info['system'] == 'Darwin':
        print("Detected iOS/macOS. Checking compatibility...")
    # TODO: Add more checks as needed

def auto_update_main(current_version, update_url):
    check_os_compatibility()
    url = check_for_app_update(current_version, update_url)
    if url:
        print("New version available. Downloading update...")
        apply_update(url)
    else:
        print("App is up to date.")
