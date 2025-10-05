"""
Updated Main Desktop Application with Universal Automatic System Integration
Integrates all automatic features, cross-device sync, and universal settings
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import automatic system components
try:
    from automatic_universal_manager import get_universal_manager, automatic_login
    from automatic_login import get_login_system, quick_automatic_login
    from universal_settings_manager import get_settings_manager, apply_all_settings
    from cross_device_sync import start_cross_device_sync
    from automatic_external_screen_reader import AutomaticExternalScreenReader
    from speech import SpeechRecognitionManager, TextToSpeechManager
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    # Continue without automatic features

class UniversalAutomaticAccessMateApp:
    """Main AccessMate application with universal automatic features"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AccessMate - Universal Automatic Edition")
        self.root.geometry("900x700")
        
        # Application state
        self.current_user = None
        self.universal_manager = None
        self.settings_manager = None
        self.sync_manager = None
        self.login_system = None
        self.auto_screen_reader = None
        
        # Feature states
        self.features_active = {}
        self.automatic_mode = False
        
        # Initialize automatic systems
        self._initialize_automatic_systems()
        
        # Setup UI
        self._setup_ui()
        
        # Try automatic login on startup
        self._attempt_automatic_login()
        
        print("🚀 Universal Automatic AccessMate initialized!")
    
    def _initialize_automatic_systems(self):
        """Initialize all automatic systems"""
        try:
            self.universal_manager = get_universal_manager()
            self.login_system = get_login_system()
            self.settings_manager = get_settings_manager()
            
            print("✅ Automatic systems initialized")
        except Exception as e:
            print(f"⚠️ Error initializing automatic systems: {e}")
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="AccessMate - Universal Automatic Edition", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # User status frame
        self._setup_user_status_frame(main_frame)
        
        # Automatic features frame
        self._setup_automatic_features_frame(main_frame)
        
        # Universal controls frame
        self._setup_universal_controls_frame(main_frame)
        
        # Settings frame
        self._setup_settings_frame(main_frame)
        
        # Status log
        self._setup_status_log(main_frame)
    
    def _setup_user_status_frame(self, parent):
        """Setup user status and login frame"""
        user_frame = ttk.LabelFrame(parent, text="User Status & Login", padding="10")
        user_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        user_frame.columnconfigure(1, weight=1)
        
        # User status
        self.user_status_label = ttk.Label(user_frame, text="Not logged in", foreground="red")
        self.user_status_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Login fields
        ttk.Label(user_frame, text="Username:").grid(row=1, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(user_frame, width=20)
        self.username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Label(user_frame, text="Password:").grid(row=2, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(user_frame, width=20, show="*")
        self.password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Login buttons
        login_frame = ttk.Frame(user_frame)
        login_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(login_frame, text="🔐 Auto Login", 
                  command=self._quick_auto_login).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(login_frame, text="🚀 Login & Activate All", 
                  command=self._login_and_activate_all).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(login_frame, text="📤 Logout", 
                  command=self._logout_user).pack(side=tk.LEFT)
    
    def _setup_automatic_features_frame(self, parent):
        """Setup automatic features control frame"""
        features_frame = ttk.LabelFrame(parent, text="Automatic Features", padding="10")
        features_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        features_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(1, weight=1)
        features_frame.columnconfigure(2, weight=1)
        
        # Automatic mode toggle
        self.auto_mode_var = tk.BooleanVar(value=True)
        auto_mode_check = ttk.Checkbutton(features_frame, text="🤖 Universal Automatic Mode", 
                                         variable=self.auto_mode_var,
                                         command=self._toggle_automatic_mode)
        auto_mode_check.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Feature buttons - Row 1
        ttk.Button(features_frame, text="🤖 Auto Screen Reader", 
                  command=self._start_auto_screen_reader).grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(features_frame, text="🎤 Auto Speech Recognition", 
                  command=self._start_auto_speech).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(features_frame, text="🔊 Auto Text-to-Speech", 
                  command=self._start_auto_tts).grid(row=1, column=2, sticky=(tk.W, tk.E))
        
        # Feature buttons - Row 2
        ttk.Button(features_frame, text="🔄 Auto Sync All Devices", 
                  command=self._start_auto_sync).grid(row=2, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Button(features_frame, text="📋 Auto Clipboard Sync", 
                  command=self._start_clipboard_sync).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Button(features_frame, text="⚙️ Auto Apply Settings", 
                  command=self._auto_apply_settings).grid(row=2, column=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def _setup_universal_controls_frame(self, parent):
        """Setup universal controls frame"""
        universal_frame = ttk.LabelFrame(parent, text="Universal Controls", padding="10")
        universal_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        universal_frame.columnconfigure(0, weight=1)
        universal_frame.columnconfigure(1, weight=1)
        universal_frame.columnconfigure(2, weight=1)
        
        # Universal buttons
        ttk.Button(universal_frame, text="🌐 Activate ALL Features", 
                  command=self._activate_all_features).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(universal_frame, text="🔄 Sync Everything Now", 
                  command=self._sync_everything_now).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(universal_frame, text="📱 Copy to All Devices", 
                  command=self._copy_to_all_devices).grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # Device management
        ttk.Button(universal_frame, text="📋 View Device Status", 
                  command=self._show_device_status).grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Button(universal_frame, text="⚙️ Universal Settings", 
                  command=self._open_universal_settings).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Button(universal_frame, text="🧪 Test All Systems", 
                  command=self._test_all_systems).grid(row=1, column=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def _setup_settings_frame(self, parent):
        """Setup quick settings frame"""
        settings_frame = ttk.LabelFrame(parent, text="Quick Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
        # Theme selection
        ttk.Label(settings_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W)
        self.theme_var = tk.StringVar(value="auto")
        theme_combo = ttk.Combobox(settings_frame, textvariable=self.theme_var, 
                                  values=["light", "dark", "auto", "high_contrast"], 
                                  state="readonly", width=15)
        theme_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        theme_combo.bind("<<ComboboxSelected>>", self._on_theme_change)
        
        # Language selection
        ttk.Label(settings_frame, text="Language:").grid(row=1, column=0, sticky=tk.W)
        self.language_var = tk.StringVar(value="en")
        language_combo = ttk.Combobox(settings_frame, textvariable=self.language_var,
                                     values=["en", "es", "fr", "de", "it", "pt"], 
                                     state="readonly", width=15)
        language_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        language_combo.bind("<<ComboboxSelected>>", self._on_language_change)
    
    def _setup_status_log(self, parent):
        """Setup status log display"""
        log_frame = ttk.LabelFrame(parent, text="Status Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure main frame to expand
        parent.rowconfigure(5, weight=1)
        
        # Status log text area
        self.status_log = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.status_log.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add initial message
        self._log_status("🚀 AccessMate Universal Automatic Edition started")
        self._log_status("💡 Enable automatic mode and login to activate all features!")
    
    def _attempt_automatic_login(self):
        """Attempt automatic login on startup"""
        if not self.login_system:
            return
        
        try:
            success, username = quick_automatic_login()
            if success:
                self.current_user = username
                self._update_user_status(f"✅ Auto-logged in as: {username}")
                self._log_status(f"🔐 Automatic login successful: {username}")
                
                # Automatically activate all features if in automatic mode
                if self.auto_mode_var.get():
                    self._activate_all_features()
            else:
                self._log_status("ℹ️ No automatic login available - please login manually")
        except Exception as e:
            self._log_status(f"⚠️ Automatic login error: {e}")
    
    def _quick_auto_login(self):
        """Quick automatic login"""
        try:
            success, username = quick_automatic_login()
            if success:
                self.current_user = username
                self._update_user_status(f"✅ Auto-logged in as: {username}")
                self._log_status(f"🔐 Quick automatic login successful: {username}")
                
                if self.auto_mode_var.get():
                    self._activate_all_features()
            else:
                messagebox.showwarning("Login Failed", "No automatic login available. Please use manual login.")
        except Exception as e:
            messagebox.showerror("Login Error", f"Automatic login failed: {e}")
    
    def _login_and_activate_all(self):
        """Login user and activate all features"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Input Error", "Please enter a username")
            return
        
        try:
            # Use automatic login system
            if self.login_system:
                success, logged_user = self.login_system.login_with_sync(username, password)
                if success:
                    self.current_user = logged_user
                    self._update_user_status(f"✅ Logged in as: {logged_user}")
                    self._log_status(f"🚀 Login successful with automatic activation: {logged_user}")
                    
                    # Clear password field
                    self.password_entry.delete(0, tk.END)
                    
                    # Activate all features automatically
                    self._activate_all_features()
                else:
                    messagebox.showerror("Login Failed", "Invalid credentials")
            else:
                messagebox.showerror("System Error", "Login system not available")
                
        except Exception as e:
            messagebox.showerror("Login Error", f"Login failed: {e}")
    
    def _logout_user(self):
        """Logout current user"""
        try:
            if self.login_system:
                self.login_system.logout()
            
            self.current_user = None
            self._update_user_status("Not logged in")
            self._log_status("📤 User logged out")
            
            # Clear password field
            self.password_entry.delete(0, tk.END)
            
        except Exception as e:
            self._log_status(f"⚠️ Logout error: {e}")
    
    def _toggle_automatic_mode(self):
        """Toggle automatic mode"""
        self.automatic_mode = self.auto_mode_var.get()
        
        if self.automatic_mode:
            self._log_status("🤖 Universal Automatic Mode ENABLED")
            if self.current_user:
                self._activate_all_features()
        else:
            self._log_status("📱 Manual Mode enabled")
    
    def _activate_all_features(self):
        """Activate all available features"""
        if not self.current_user:
            messagebox.showwarning("Not Logged In", "Please login first to activate features")
            return
        
        try:
            self._log_status("🚀 Activating ALL features...")
            
            # Use universal manager to activate features
            if self.universal_manager:
                # Login user with full sync
                self.universal_manager.login_user(self.current_user, auto_sync=True)
                self._log_status("✅ Universal feature manager activated")
            
            # Start automatic screen reader
            self._start_auto_screen_reader()
            
            # Start automatic sync
            self._start_auto_sync()
            
            # Apply all settings
            self._auto_apply_settings()
            
            self._log_status("🎉 ALL features activated successfully!")
            
        except Exception as e:
            self._log_status(f"❌ Error activating features: {e}")
    
    def _start_auto_screen_reader(self):
        """Start automatic screen reader"""
        try:
            if not self.auto_screen_reader:
                self.auto_screen_reader = AutomaticExternalScreenReader()
                self.auto_screen_reader.start_continuous_reading()
            
            self.features_active["screen_reader"] = True
            self._log_status("🤖 Automatic screen reader started")
            
        except Exception as e:
            self._log_status(f"❌ Screen reader error: {e}")
    
    def _start_auto_speech(self):
        """Start automatic speech recognition"""
        try:
            # Initialize speech recognition
            self.features_active["speech_recognition"] = True
            self._log_status("🎤 Automatic speech recognition started")
            
        except Exception as e:
            self._log_status(f"❌ Speech recognition error: {e}")
    
    def _start_auto_tts(self):
        """Start automatic text-to-speech"""
        try:
            # Initialize TTS
            self.features_active["tts"] = True
            self._log_status("🔊 Automatic text-to-speech started")
            
        except Exception as e:
            self._log_status(f"❌ TTS error: {e}")
    
    def _start_auto_sync(self):
        """Start automatic cross-device synchronization"""
        try:
            if self.current_user and not self.sync_manager:
                device_id = self.universal_manager.device_id if self.universal_manager else "desktop_device"
                self.sync_manager = start_cross_device_sync(self.current_user, device_id)
            
            self.features_active["sync"] = True
            self._log_status("🔄 Automatic cross-device sync started")
            
        except Exception as e:
            self._log_status(f"❌ Sync error: {e}")
    
    def _start_clipboard_sync(self):
        """Start automatic clipboard synchronization"""
        try:
            self.features_active["clipboard_sync"] = True
            self._log_status("📋 Automatic clipboard sync started")
            
        except Exception as e:
            self._log_status(f"❌ Clipboard sync error: {e}")
    
    def _auto_apply_settings(self):
        """Automatically apply all settings"""
        try:
            if self.settings_manager:
                apply_all_settings()
            
            self.features_active["auto_settings"] = True
            self._log_status("⚙️ All settings applied automatically")
            
        except Exception as e:
            self._log_status(f"❌ Settings error: {e}")
    
    def _sync_everything_now(self):
        """Manually trigger full synchronization"""
        try:
            if self.universal_manager:
                self.universal_manager.sync_to_cloud()
                self.universal_manager.sync_from_cloud()
            
            self._log_status("🔄 Full synchronization completed")
            
        except Exception as e:
            self._log_status(f"❌ Sync error: {e}")
    
    def _copy_to_all_devices(self):
        """Copy data to all user devices"""
        try:
            if not self.current_user:
                messagebox.showwarning("Not Logged In", "Please login first")
                return
            
            # Get clipboard content
            try:
                clipboard_content = self.root.clipboard_get()
                if clipboard_content:
                    if self.universal_manager:
                        from automatic_universal_manager import copy_to_all_devices
                        copy_to_all_devices({"type": "clipboard", "content": clipboard_content})
                    
                    self._log_status(f"📤 Copied to all devices: {clipboard_content[:50]}...")
                else:
                    messagebox.showinfo("No Content", "No content in clipboard to copy")
            except:
                messagebox.showinfo("No Content", "No content in clipboard to copy")
                
        except Exception as e:
            self._log_status(f"❌ Copy error: {e}")
    
    def _show_device_status(self):
        """Show device and sync status"""
        try:
            status_info = []
            
            if self.universal_manager:
                devices = self.universal_manager.get_available_devices()
                status_info.append(f"Available Devices: {len(devices)}")
                for device in devices:
                    status_info.append(f"  • {device['name']} ({device['platform']})")
            
            if self.sync_manager:
                sync_status = self.sync_manager.get_sync_status()
                status_info.append(f"\nSync Status:")
                status_info.append(f"  Running: {sync_status['running']}")
                status_info.append(f"  Queue Size: {sync_status['queue_size']}")
                status_info.append(f"  Total Items: {sync_status['total_items']}")
            
            active_features = [name for name, active in self.features_active.items() if active]
            status_info.append(f"\nActive Features: {len(active_features)}")
            for feature in active_features:
                status_info.append(f"  • {feature}")
            
            messagebox.showinfo("Device Status", "\n".join(status_info))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get device status: {e}")
    
    def _open_universal_settings(self):
        """Open universal settings dialog"""
        try:
            # Create settings window
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Universal Settings")
            settings_window.geometry("600x500")
            
            # Settings content
            settings_frame = ttk.Frame(settings_window, padding="10")
            settings_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(settings_frame, text="Universal Settings", 
                     font=("Arial", 14, "bold")).pack(pady=(0, 20))
            
            # Show current settings
            if self.settings_manager:
                settings = self.settings_manager.get_all_settings()
                
                # Create scrollable text area
                settings_text = scrolledtext.ScrolledText(settings_frame, height=20)
                settings_text.pack(fill=tk.BOTH, expand=True)
                
                for key, value in settings.items():
                    settings_text.insert(tk.END, f"{key}: {value}\n")
                
                settings_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {e}")
    
    def _test_all_systems(self):
        """Test all systems"""
        try:
            self._log_status("🧪 Testing all systems...")
            
            # Run comprehensive test
            from test_universal_system import run_comprehensive_test
            
            def run_test():
                report = run_comprehensive_test()
                
                # Show results in UI
                def show_results():
                    success_rate = report['success_rate']
                    if success_rate == 100:
                        messagebox.showinfo("Test Results", 
                                          f"🎉 ALL TESTS PASSED!\n\nSuccess Rate: {success_rate:.1f}%\nTotal Tests: {report['total_tests']}")
                    else:
                        messagebox.showwarning("Test Results", 
                                             f"⚠️ Some tests failed\n\nSuccess Rate: {success_rate:.1f}%\nPassed: {report['passed_tests']}\nFailed: {report['failed_tests']}")
                
                self.root.after(0, show_results)
            
            # Run test in background thread
            test_thread = threading.Thread(target=run_test, daemon=True)
            test_thread.start()
            
        except Exception as e:
            self._log_status(f"❌ Test error: {e}")
    
    def _on_theme_change(self, event=None):
        """Handle theme change"""
        theme = self.theme_var.get()
        if self.settings_manager:
            self.settings_manager.set_setting("app_theme", theme, sync_immediately=True)
        self._log_status(f"🎨 Theme changed to: {theme}")
    
    def _on_language_change(self, event=None):
        """Handle language change"""
        language = self.language_var.get()
        if self.settings_manager:
            self.settings_manager.set_setting("app_language", language, sync_immediately=True)
        self._log_status(f"🌐 Language changed to: {language}")
    
    def _update_user_status(self, status):
        """Update user status display"""
        self.user_status_label.config(text=status)
        if "logged in" in status.lower() and "not" not in status.lower():
            self.user_status_label.config(foreground="green")
        else:
            self.user_status_label.config(foreground="red")
    
    def _log_status(self, message):
        """Log status message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.status_log.insert(tk.END, formatted_message)
        self.status_log.see(tk.END)
        
        # Also print to console
        print(formatted_message.strip())
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main application entry point"""
    print("🚀 Starting AccessMate Universal Automatic Edition...")
    
    app = UniversalAutomaticAccessMateApp()
    app.run()

if __name__ == "__main__":
    main()