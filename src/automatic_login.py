"""
Automatic Login System for AccessMate
Handles automatic user authentication and feature activation across all platforms
"""

import json
import os
import hashlib
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import platform

class AutomaticLoginSystem:
    """Manages automatic login and authentication across devices"""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.login_data_dir = self._get_login_data_directory()
        self.session_file = os.path.join(self.login_data_dir, "active_session.json")
        self.credentials_file = os.path.join(self.login_data_dir, "secure_credentials.json")
        
        # Session management
        self.current_session = None
        self.auto_login_enabled = True
        self.remember_credentials = True
        self.session_timeout = 24 * 60 * 60  # 24 hours
        
        # Security settings
        self.require_biometric = False  # Can be enabled for enhanced security
        self.max_failed_attempts = 3
        self.lockout_duration = 300  # 5 minutes
        
        # Multi-device support
        self.device_trust_enabled = True
        self.trusted_devices = self._load_trusted_devices()
        
        print(f"🔐 Automatic Login System initialized for {self.platform}")
    
    def _get_login_data_directory(self) -> str:
        """Get secure directory for login data"""
        if self.platform == "windows":
            login_dir = os.path.join(os.environ.get("APPDATA", ""), "AccessMate", "Login")
        elif self.platform == "darwin":  # macOS
            login_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "AccessMate", "Login")
        elif self.platform == "linux":
            login_dir = os.path.join(os.path.expanduser("~"), ".config", "accessmate", "login")
        else:
            # Mobile platforms
            login_dir = os.path.join(os.path.expanduser("~"), ".accessmate", "login")
        
        os.makedirs(login_dir, exist_ok=True)
        
        # Set restrictive permissions on login directory
        try:
            os.chmod(login_dir, 0o700)  # Owner read/write/execute only
        except:
            pass  # Permissions may not be supported on all platforms
        
        return login_dir
    
    def enable_automatic_login(self, username: str, password: str = None, use_biometric: bool = False) -> bool:
        """Enable automatic login for user"""
        try:
            # Create secure credential storage
            credentials = {
                "username": username,
                "password_hash": hashlib.sha256(password.encode()).hexdigest() if password else None,
                "use_biometric": use_biometric,
                "created_at": datetime.now().isoformat(),
                "device_id": self._get_device_id(),
                "platform": self.platform
            }
            
            # Save encrypted credentials
            self._save_encrypted_credentials(credentials)
            
            # Create persistent session
            session_data = {
                "username": username,
                "login_time": datetime.now().isoformat(),
                "device_id": credentials["device_id"],
                "auto_login": True,
                "expires_at": (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat()
            }
            
            self._save_session(session_data)
            self.current_session = session_data
            
            print(f"✅ Automatic login enabled for {username}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to enable automatic login: {e}")
            return False
    
    def automatic_login(self) -> Tuple[bool, Optional[str]]:
        """Attempt automatic login using saved credentials"""
        try:
            # Check for existing valid session
            if self._has_valid_session():
                username = self.current_session["username"]
                print(f"✅ Automatic login successful using existing session: {username}")
                return True, username
            
            # Try to load saved credentials
            credentials = self._load_encrypted_credentials()
            if not credentials:
                print("ℹ️ No saved credentials found")
                return False, None
            
            username = credentials["username"]
            
            # Verify device trust
            if self.device_trust_enabled and not self._is_trusted_device():
                print("⚠️ Device not trusted - manual login required")
                return False, None
            
            # Attempt biometric authentication if enabled
            if credentials.get("use_biometric", False):
                if not self._verify_biometric():
                    print("❌ Biometric verification failed")
                    return False, None
            
            # Create new session
            session_data = {
                "username": username,
                "login_time": datetime.now().isoformat(),
                "device_id": credentials["device_id"],
                "auto_login": True,
                "expires_at": (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat()
            }
            
            self._save_session(session_data)
            self.current_session = session_data
            
            # Add device to trusted devices
            self._add_trusted_device()
            
            print(f"✅ Automatic login successful: {username}")
            return True, username
            
        except Exception as e:
            print(f"❌ Automatic login failed: {e}")
            return False, None
    
    def login_with_sync(self, username: str, password: str = None) -> Tuple[bool, Optional[str]]:
        """Login user and automatically activate all features with sync"""
        try:
            # First try automatic login
            success, logged_in_user = self.automatic_login()
            
            if success and logged_in_user == username:
                # Activate automatic features
                self._activate_all_features_automatically(username)
                return True, username
            
            # Manual login if automatic failed
            if password:
                if self._verify_password(username, password):
                    # Enable automatic login for next time
                    self.enable_automatic_login(username, password)
                    
                    # Activate all features
                    self._activate_all_features_automatically(username)
                    
                    print(f"✅ Manual login successful with auto-features: {username}")
                    return True, username
                else:
                    print("❌ Invalid credentials")
                    return False, None
            
            print("❌ Login failed - no valid credentials")
            return False, None
            
        except Exception as e:
            print(f"❌ Login with sync failed: {e}")
            return False, None
    
    def _activate_all_features_automatically(self, username: str):
        """Activate all features and start synchronization"""
        try:
            # Import and initialize automatic universal manager
            from automatic_universal_manager import get_universal_manager
            manager = get_universal_manager()
            
            # Login user with full sync
            manager.login_user(username, auto_sync=True)
            
            print(f"🚀 All features activated automatically for {username}")
            
        except Exception as e:
            print(f"⚠️ Feature activation error: {e}")
    
    def _has_valid_session(self) -> bool:
        """Check if there's a valid active session"""
        if not os.path.exists(self.session_file):
            return False
        
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check expiration
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            if datetime.now() > expires_at:
                # Session expired
                os.remove(self.session_file)
                return False
            
            self.current_session = session_data
            return True
            
        except Exception:
            return False
    
    def _save_session(self, session_data: Dict):
        """Save session data securely"""
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)
        
        # Set restrictive permissions
        try:
            os.chmod(self.session_file, 0o600)  # Owner read/write only
        except:
            pass
    
    def _save_encrypted_credentials(self, credentials: Dict):
        """Save encrypted credentials (simplified encryption)"""
        # In production, use proper encryption like cryptography library
        encrypted_data = self._simple_encrypt(json.dumps(credentials))
        
        with open(self.credentials_file, 'w') as f:
            f.write(encrypted_data)
        
        # Set restrictive permissions
        try:
            os.chmod(self.credentials_file, 0o600)
        except:
            pass
    
    def _load_encrypted_credentials(self) -> Optional[Dict]:
        """Load and decrypt saved credentials"""
        if not os.path.exists(self.credentials_file):
            return None
        
        try:
            with open(self.credentials_file, 'r') as f:
                encrypted_data = f.read()
            
            decrypted_json = self._simple_decrypt(encrypted_data)
            return json.loads(decrypted_json)
            
        except Exception:
            return None
    
    def _simple_encrypt(self, data: str) -> str:
        """Simple encryption (use proper encryption in production)"""
        import base64
        # This is a simplified example - use proper encryption in production
        encoded = base64.b64encode(data.encode()).decode()
        return encoded
    
    def _simple_decrypt(self, encrypted_data: str) -> str:
        """Simple decryption (use proper decryption in production)"""
        import base64
        # This is a simplified example - use proper decryption in production
        decoded = base64.b64decode(encrypted_data.encode()).decode()
        return decoded
    
    def _get_device_id(self) -> str:
        """Get unique device identifier"""
        import uuid
        device_file = os.path.join(self.login_data_dir, "device_id")
        
        if os.path.exists(device_file):
            with open(device_file, 'r') as f:
                return f.read().strip()
        
        device_id = str(uuid.uuid4())[:16]
        with open(device_file, 'w') as f:
            f.write(device_id)
        
        return device_id
    
    def _is_trusted_device(self) -> bool:
        """Check if current device is trusted"""
        device_id = self._get_device_id()
        return device_id in self.trusted_devices
    
    def _add_trusted_device(self):
        """Add current device to trusted devices"""
        device_id = self._get_device_id()
        if device_id not in self.trusted_devices:
            self.trusted_devices.append(device_id)
            self._save_trusted_devices()
    
    def _load_trusted_devices(self) -> List[str]:
        """Load list of trusted devices"""
        trusted_file = os.path.join(self.login_data_dir, "trusted_devices.json")
        
        if os.path.exists(trusted_file):
            try:
                with open(trusted_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return []
    
    def _save_trusted_devices(self):
        """Save list of trusted devices"""
        trusted_file = os.path.join(self.login_data_dir, "trusted_devices.json")
        
        with open(trusted_file, 'w') as f:
            json.dump(self.trusted_devices, f)
    
    def _verify_biometric(self) -> bool:
        """Verify biometric authentication (platform-specific)"""
        if self.platform == "windows":
            return self._verify_windows_hello()
        elif self.platform == "darwin":
            return self._verify_touch_id()
        elif self.platform == "linux":
            return self._verify_linux_biometric()
        else:
            # Mobile platforms would use their respective biometric APIs
            return True  # Simplified for testing
    
    def _verify_windows_hello(self) -> bool:
        """Verify Windows Hello authentication"""
        try:
            # In production, integrate with Windows Hello API
            print("🔐 Windows Hello verification (simulated)")
            return True
        except:
            return False
    
    def _verify_touch_id(self) -> bool:
        """Verify Touch ID on macOS"""
        try:
            # In production, integrate with Touch ID API
            print("👆 Touch ID verification (simulated)")
            return True
        except:
            return False
    
    def _verify_linux_biometric(self) -> bool:
        """Verify biometric on Linux"""
        try:
            # In production, integrate with PAM or fprintd
            print("🔐 Linux biometric verification (simulated)")
            return True
        except:
            return False
    
    def _verify_password(self, username: str, password: str) -> bool:
        """Verify username and password"""
        credentials = self._load_encrypted_credentials()
        if not credentials:
            return False
        
        stored_username = credentials.get("username")
        stored_password_hash = credentials.get("password_hash")
        
        if stored_username != username:
            return False
        
        if stored_password_hash:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            return password_hash == stored_password_hash
        
        return True  # If no password stored, allow login
    
    def logout(self):
        """Logout current user"""
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        
        self.current_session = None
        print("✅ User logged out")
    
    def disable_automatic_login(self):
        """Disable automatic login"""
        if os.path.exists(self.credentials_file):
            os.remove(self.credentials_file)
        
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        
        self.auto_login_enabled = False
        print("✅ Automatic login disabled")
    
    def get_login_status(self) -> Dict:
        """Get current login status"""
        return {
            "logged_in": self.current_session is not None,
            "username": self.current_session["username"] if self.current_session else None,
            "auto_login_enabled": self.auto_login_enabled,
            "session_expires": self.current_session["expires_at"] if self.current_session else None,
            "trusted_device": self._is_trusted_device(),
            "platform": self.platform
        }

# Global login system instance
_login_system = None

def get_login_system():
    """Get global login system instance"""
    global _login_system
    if _login_system is None:
        _login_system = AutomaticLoginSystem()
    return _login_system

def quick_automatic_login() -> Tuple[bool, Optional[str]]:
    """Quick automatic login attempt"""
    login_system = get_login_system()
    return login_system.automatic_login()

def setup_automatic_login(username: str, password: str) -> bool:
    """Setup automatic login for user"""
    login_system = get_login_system()
    return login_system.enable_automatic_login(username, password)

def login_and_activate_all(username: str, password: str = None) -> bool:
    """Login user and automatically activate all features"""
    login_system = get_login_system()
    success, logged_user = login_system.login_with_sync(username, password)
    return success

if __name__ == "__main__":
    # Test automatic login system
    print("🧪 Testing Automatic Login System...")
    
    login_system = AutomaticLoginSystem()
    
    # Test setup
    success = login_system.enable_automatic_login("testuser", "testpass")
    if success:
        print("✅ Automatic login setup successful")
        
        # Test automatic login
        login_success, username = login_system.automatic_login()
        if login_success:
            print(f"✅ Automatic login test successful for {username}")
            
            # Test status
            status = login_system.get_login_status()
            print(f"📊 Login status: {status}")
        else:
            print("❌ Automatic login test failed")
    else:
        print("❌ Automatic login setup failed")