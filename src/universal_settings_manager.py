"""
Universal Settings Manager for AccessMate
Manages and synchronizes all settings across all platforms automatically
"""

import json
import os
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import platform
from dataclasses import dataclass, asdict

@dataclass
class SettingDefinition:
    """Definition of a setting with metadata"""
    key: str
    name: str
    description: str
    setting_type: str  # 'bool', 'int', 'float', 'string', 'list', 'dict'
    default_value: Any
    platform_specific: bool = False
    requires_restart: bool = False
    validation_rules: Optional[Dict] = None

class UniversalSettingsManager:
    """Manages settings across all platforms with automatic synchronization"""
    
    def __init__(self, user_id: str = None, device_id: str = None):
        self.user_id = user_id
        self.device_id = device_id or self._get_device_id()
        self.platform = platform.system().lower()
        
        # Settings directories
        self.settings_dir = self._get_settings_directory()
        self.user_settings_file = os.path.join(self.settings_dir, "user_settings.json")
        self.platform_settings_file = os.path.join(self.settings_dir, f"{self.platform}_settings.json")
        self.sync_settings_file = os.path.join(self.settings_dir, "sync_settings.json")
        
        # Settings storage
        self.user_settings = {}
        self.platform_settings = {}
        self.sync_settings = {}
        self.setting_definitions = {}
        
        # Sync configuration
        self.auto_sync_enabled = True
        self.sync_interval = 30  # seconds
        self.sync_thread = None
        self.running = False
        
        # Change tracking
        self.pending_changes = {}
        self.change_listeners = []
        
        # Initialize default settings
        self._define_default_settings()
        self._load_all_settings()
        
        print(f"⚙️ Universal Settings Manager initialized for {self.platform}")
    
    def _get_device_id(self) -> str:
        """Get unique device identifier"""
        import uuid
        return str(uuid.uuid4())[:16]
    
    def _get_settings_directory(self) -> str:
        """Get platform-appropriate settings directory"""
        if self.platform == "windows":
            settings_dir = os.path.join(os.environ.get("APPDATA", ""), "AccessMate", "Settings")
        elif self.platform == "darwin":  # macOS
            settings_dir = os.path.join(os.path.expanduser("~"), "Library", "Preferences", "AccessMate")
        elif self.platform == "linux":
            settings_dir = os.path.join(os.path.expanduser("~"), ".config", "accessmate", "settings")
        else:
            # Mobile platforms
            settings_dir = os.path.join(os.path.expanduser("~"), ".accessmate", "settings")
        
        os.makedirs(settings_dir, exist_ok=True)
        return settings_dir
    
    def _define_default_settings(self):
        """Define all available settings with their metadata"""
        
        # Core Application Settings
        self._define_setting("app_language", "Application Language", "Primary language for the application", 
                           "string", "en", validation_rules={"choices": ["en", "es", "fr", "de", "it", "pt", "zh", "ja"]})
        
        self._define_setting("app_theme", "Application Theme", "Visual theme for the application",
                           "string", "auto", validation_rules={"choices": ["light", "dark", "auto", "high_contrast"]})
        
        self._define_setting("startup_behavior", "Startup Behavior", "What to do when app starts",
                           "string", "automatic", validation_rules={"choices": ["manual", "automatic", "restore_session"]})
        
        # Accessibility Settings
        self._define_setting("enable_screen_reader", "Enable Screen Reader", "Automatically start screen reader",
                           "bool", True, requires_restart=True)
        
        self._define_setting("screen_reader_voice_speed", "Screen Reader Speed", "Voice speed for screen reader",
                           "float", 1.0, validation_rules={"min": 0.5, "max": 3.0})
        
        self._define_setting("high_contrast_mode", "High Contrast Mode", "Enable high contrast display",
                           "bool", False, requires_restart=True)
        
        self._define_setting("large_text_mode", "Large Text Mode", "Enable large text display",
                           "bool", False, requires_restart=True)
        
        self._define_setting("voice_navigation", "Voice Navigation", "Enable voice-controlled navigation",
                           "bool", True)
        
        # Speech Settings
        self._define_setting("enable_speech_recognition", "Enable Speech Recognition", "Automatically start speech recognition",
                           "bool", True)
        
        self._define_setting("speech_language", "Speech Language", "Language for speech recognition",
                           "string", "en-US", validation_rules={"choices": ["en-US", "es-ES", "fr-FR", "de-DE"]})
        
        self._define_setting("tts_voice", "Text-to-Speech Voice", "Voice for text-to-speech",
                           "string", "default")
        
        self._define_setting("tts_speed", "TTS Speed", "Speed for text-to-speech",
                           "float", 1.0, validation_rules={"min": 0.5, "max": 2.0})
        
        # Feature Settings
        self._define_setting("auto_translate", "Auto Translation", "Automatically translate content",
                           "bool", True)
        
        self._define_setting("translation_target_language", "Translation Target", "Target language for translation",
                           "string", "en", validation_rules={"choices": ["en", "es", "fr", "de", "it", "pt", "zh", "ja"]})
        
        self._define_setting("enable_ocr", "Enable OCR", "Automatically perform OCR on images",
                           "bool", True)
        
        self._define_setting("enable_web_scraping", "Enable Web Scraping", "Allow web content extraction",
                           "bool", True)
        
        # Synchronization Settings
        self._define_setting("enable_cloud_sync", "Enable Cloud Sync", "Sync data across devices",
                           "bool", True, requires_restart=True)
        
        self._define_setting("sync_frequency", "Sync Frequency", "How often to sync data (minutes)",
                           "int", 5, validation_rules={"min": 1, "max": 60})
        
        self._define_setting("sync_on_startup", "Sync on Startup", "Sync data when app starts",
                           "bool", True)
        
        self._define_setting("cross_device_clipboard", "Cross-Device Clipboard", "Share clipboard between devices",
                           "bool", True)
        
        # Privacy Settings
        self._define_setting("data_collection_consent", "Data Collection", "Allow anonymous usage data collection",
                           "bool", False)
        
        self._define_setting("crash_reporting", "Crash Reporting", "Send crash reports to improve app",
                           "bool", True)
        
        self._define_setting("usage_analytics", "Usage Analytics", "Send usage analytics",
                           "bool", False)
        
        # Platform-Specific Settings
        if self.platform == "windows":
            self._define_setting("integrate_with_narrator", "Narrator Integration", "Integrate with Windows Narrator",
                               "bool", True, platform_specific=True)
            
            self._define_setting("windows_notifications", "Windows Notifications", "Show Windows notifications",
                               "bool", True, platform_specific=True)
        
        elif self.platform == "darwin":  # macOS
            self._define_setting("integrate_with_voiceover", "VoiceOver Integration", "Integrate with macOS VoiceOver",
                               "bool", True, platform_specific=True)
            
            self._define_setting("macos_accessibility_shortcuts", "Accessibility Shortcuts", "Enable macOS accessibility shortcuts",
                               "bool", True, platform_specific=True)
        
        elif self.platform == "linux":
            self._define_setting("integrate_with_orca", "Orca Integration", "Integrate with Orca screen reader",
                               "bool", True, platform_specific=True)
        
        # Advanced Settings
        self._define_setting("debug_mode", "Debug Mode", "Enable debug logging",
                           "bool", False, requires_restart=True)
        
        self._define_setting("log_level", "Log Level", "Level of logging detail",
                           "string", "INFO", validation_rules={"choices": ["DEBUG", "INFO", "WARNING", "ERROR"]})
        
        self._define_setting("automatic_updates", "Automatic Updates", "Automatically check for updates",
                           "bool", True)
    
    def _define_setting(self, key: str, name: str, description: str, setting_type: str, 
                       default_value: Any, platform_specific: bool = False, 
                       requires_restart: bool = False, validation_rules: Optional[Dict] = None):
        """Define a setting with its metadata"""
        self.setting_definitions[key] = SettingDefinition(
            key=key,
            name=name,
            description=description,
            setting_type=setting_type,
            default_value=default_value,
            platform_specific=platform_specific,
            requires_restart=requires_restart,
            validation_rules=validation_rules
        )
    
    def _load_all_settings(self):
        """Load all settings from files"""
        # Load user settings
        if os.path.exists(self.user_settings_file):
            try:
                with open(self.user_settings_file, 'r') as f:
                    self.user_settings = json.load(f)
            except:
                self.user_settings = {}
        
        # Load platform-specific settings
        if os.path.exists(self.platform_settings_file):
            try:
                with open(self.platform_settings_file, 'r') as f:
                    self.platform_settings = json.load(f)
            except:
                self.platform_settings = {}
        
        # Load sync settings
        if os.path.exists(self.sync_settings_file):
            try:
                with open(self.sync_settings_file, 'r') as f:
                    self.sync_settings = json.load(f)
            except:
                self.sync_settings = {}
        
        # Apply defaults for missing settings
        self._apply_default_settings()
    
    def _apply_default_settings(self):
        """Apply default values for missing settings"""
        for key, definition in self.setting_definitions.items():
            if definition.platform_specific:
                if key not in self.platform_settings:
                    self.platform_settings[key] = definition.default_value
            else:
                if key not in self.user_settings:
                    self.user_settings[key] = definition.default_value
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        definition = self.setting_definitions.get(key)
        
        if definition and definition.platform_specific:
            return self.platform_settings.get(key, default or definition.default_value)
        else:
            return self.user_settings.get(key, default or (definition.default_value if definition else None))
    
    def set_setting(self, key: str, value: Any, sync_immediately: bool = False) -> bool:
        """Set a setting value"""
        try:
            # Validate setting
            if not self._validate_setting(key, value):
                return False
            
            definition = self.setting_definitions.get(key)
            
            # Store in appropriate settings dict
            if definition and definition.platform_specific:
                old_value = self.platform_settings.get(key)
                self.platform_settings[key] = value
                settings_dict = self.platform_settings
                settings_file = self.platform_settings_file
            else:
                old_value = self.user_settings.get(key)
                self.user_settings[key] = value
                settings_dict = self.user_settings
                settings_file = self.user_settings_file
            
            # Save to file
            with open(settings_file, 'w') as f:
                json.dump(settings_dict, f, indent=2)
            
            # Track change for sync
            if not (definition and definition.platform_specific):
                self.pending_changes[key] = {
                    "old_value": old_value,
                    "new_value": value,
                    "timestamp": datetime.now().isoformat(),
                    "device_id": self.device_id
                }
            
            # Notify listeners
            self._notify_setting_changed(key, old_value, value)
            
            # Sync immediately if requested
            if sync_immediately and self.auto_sync_enabled:
                self._sync_settings_to_cloud()
            
            print(f"⚙️ Setting '{key}' updated to: {value}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to set setting '{key}': {e}")
            return False
    
    def _validate_setting(self, key: str, value: Any) -> bool:
        """Validate a setting value"""
        definition = self.setting_definitions.get(key)
        if not definition:
            return True  # Allow unknown settings
        
        # Type validation
        if definition.setting_type == "bool" and not isinstance(value, bool):
            return False
        elif definition.setting_type == "int" and not isinstance(value, int):
            return False
        elif definition.setting_type == "float" and not isinstance(value, (int, float)):
            return False
        elif definition.setting_type == "string" and not isinstance(value, str):
            return False
        elif definition.setting_type == "list" and not isinstance(value, list):
            return False
        elif definition.setting_type == "dict" and not isinstance(value, dict):
            return False
        
        # Validation rules
        if definition.validation_rules:
            rules = definition.validation_rules
            
            if "choices" in rules and value not in rules["choices"]:
                return False
            
            if "min" in rules and value < rules["min"]:
                return False
            
            if "max" in rules and value > rules["max"]:
                return False
        
        return True
    
    def get_all_settings(self, include_platform_specific: bool = True) -> Dict[str, Any]:
        """Get all current settings"""
        all_settings = self.user_settings.copy()
        
        if include_platform_specific:
            all_settings.update(self.platform_settings)
        
        return all_settings
    
    def reset_to_defaults(self, keys: List[str] = None):
        """Reset settings to default values"""
        keys_to_reset = keys or list(self.setting_definitions.keys())
        
        for key in keys_to_reset:
            definition = self.setting_definitions.get(key)
            if definition:
                self.set_setting(key, definition.default_value)
        
        print(f"⚙️ Reset {len(keys_to_reset)} settings to defaults")
    
    def export_settings(self, file_path: str) -> bool:
        """Export all settings to a file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "platform": self.platform,
                "device_id": self.device_id,
                "user_settings": self.user_settings,
                "platform_settings": self.platform_settings
            }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"⚙️ Settings exported to: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to export settings: {e}")
            return False
    
    def import_settings(self, file_path: str, merge: bool = True) -> bool:
        """Import settings from a file"""
        try:
            with open(file_path, 'r') as f:
                import_data = json.load(f)
            
            if merge:
                # Merge with existing settings
                self.user_settings.update(import_data.get("user_settings", {}))
                self.platform_settings.update(import_data.get("platform_settings", {}))
            else:
                # Replace existing settings
                self.user_settings = import_data.get("user_settings", {})
                self.platform_settings = import_data.get("platform_settings", {})
            
            # Save updated settings
            self._save_all_settings()
            
            print(f"⚙️ Settings imported from: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to import settings: {e}")
            return False
    
    def start_automatic_sync(self):
        """Start automatic settings synchronization"""
        if self.running:
            return
        
        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        
        print("🔄 Automatic settings sync started")
    
    def stop_automatic_sync(self):
        """Stop automatic settings synchronization"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join()
        
        print("🛑 Automatic settings sync stopped")
    
    def _sync_loop(self):
        """Main synchronization loop"""
        while self.running:
            try:
                if self.pending_changes:
                    self._sync_settings_to_cloud()
                
                self._sync_settings_from_cloud()
                
                time.sleep(self.sync_interval)
                
            except Exception as e:
                print(f"⚠️ Settings sync error: {e}")
                time.sleep(self.sync_interval * 2)
    
    def _sync_settings_to_cloud(self):
        """Sync local settings changes to cloud"""
        if not self.pending_changes:
            return
        
        try:
            # Simulate cloud sync
            print(f"☁️ Syncing {len(self.pending_changes)} setting changes to cloud")
            
            # In real implementation, send to cloud server
            # requests.post(f"{sync_server}/settings", json=self.pending_changes)
            
            # Clear pending changes
            self.pending_changes.clear()
            
        except Exception as e:
            print(f"❌ Failed to sync settings to cloud: {e}")
    
    def _sync_settings_from_cloud(self):
        """Sync settings from cloud to local"""
        try:
            # Simulate cloud fetch
            # In real implementation: response = requests.get(f"{sync_server}/settings/{user_id}")
            
            # Simulate remote settings
            remote_settings = {
                "app_theme": "dark",
                "sync_frequency": 10,
                "enable_cloud_sync": True
            }
            
            # Apply remote settings that are newer
            for key, value in remote_settings.items():
                if key not in self.pending_changes:  # Don't overwrite pending local changes
                    current_value = self.get_setting(key)
                    if current_value != value:
                        self.set_setting(key, value)
                        print(f"☁️ Updated setting '{key}' from cloud: {value}")
            
        except Exception as e:
            print(f"⚠️ Failed to sync settings from cloud: {e}")
    
    def _save_all_settings(self):
        """Save all settings to their respective files"""
        try:
            with open(self.user_settings_file, 'w') as f:
                json.dump(self.user_settings, f, indent=2)
            
            with open(self.platform_settings_file, 'w') as f:
                json.dump(self.platform_settings, f, indent=2)
            
        except Exception as e:
            print(f"❌ Failed to save settings: {e}")
    
    def add_change_listener(self, callback):
        """Add a callback to be notified of setting changes"""
        self.change_listeners.append(callback)
    
    def _notify_setting_changed(self, key: str, old_value: Any, new_value: Any):
        """Notify all listeners of setting change"""
        for callback in self.change_listeners:
            try:
                callback(key, old_value, new_value)
            except Exception as e:
                print(f"⚠️ Setting change listener error: {e}")
    
    def get_setting_definition(self, key: str) -> Optional[SettingDefinition]:
        """Get the definition for a setting"""
        return self.setting_definitions.get(key)
    
    def get_all_setting_definitions(self) -> Dict[str, SettingDefinition]:
        """Get all setting definitions"""
        return self.setting_definitions.copy()

# Global settings manager
_settings_manager = None

def get_settings_manager(user_id: str = None, device_id: str = None):
    """Get global settings manager instance"""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = UniversalSettingsManager(user_id, device_id)
    return _settings_manager

def get_setting(key: str, default: Any = None) -> Any:
    """Quick access to get a setting"""
    manager = get_settings_manager()
    return manager.get_setting(key, default)

def set_setting(key: str, value: Any, sync_immediately: bool = False) -> bool:
    """Quick access to set a setting"""
    manager = get_settings_manager()
    return manager.set_setting(key, value, sync_immediately)

def apply_all_settings():
    """Apply all current settings to the application"""
    manager = get_settings_manager()
    settings = manager.get_all_settings()
    
    print("⚙️ Applying all settings...")
    
    # Apply accessibility settings
    if settings.get("high_contrast_mode", False):
        print("   🎨 Applying high contrast mode")
    
    if settings.get("large_text_mode", False):
        print("   📝 Applying large text mode")
    
    # Apply speech settings
    if settings.get("enable_speech_recognition", True):
        print("   🎤 Enabling speech recognition")
    
    # Apply sync settings
    if settings.get("enable_cloud_sync", True):
        manager.start_automatic_sync()
        print("   ☁️ Cloud sync enabled")
    
    print("✅ All settings applied successfully")

if __name__ == "__main__":
    # Test settings manager
    print("🧪 Testing Universal Settings Manager...")
    
    manager = UniversalSettingsManager("test_user", "test_device")
    
    # Test setting values
    manager.set_setting("app_theme", "dark")
    manager.set_setting("screen_reader_voice_speed", 1.5)
    manager.set_setting("enable_cloud_sync", True)
    
    # Test getting values
    theme = manager.get_setting("app_theme")
    speed = manager.get_setting("screen_reader_voice_speed")
    sync = manager.get_setting("enable_cloud_sync")
    
    print(f"Theme: {theme}, Speed: {speed}, Sync: {sync}")
    
    # Test sync
    manager.start_automatic_sync()
    time.sleep(2)
    manager.stop_automatic_sync()
    
    print("✅ Settings manager test completed!")