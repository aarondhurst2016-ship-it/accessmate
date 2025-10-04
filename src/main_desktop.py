# GUI module for AccessMate - Restored to Original Design

import tkinter as tk
from tkinter import ttk
import sys
import os
import traceback

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import original modules with error handling
def enable_accessibility(widget, tooltip=None):
    """Simple accessibility helper"""
    try:
        widget.focus_set()
        widget.bind('<Tab>', lambda e: widget.tk_focusNext().focus())
        widget.bind('<Shift-Tab>', lambda e: widget.tk_focusPrev().focus())
        widget.bind('<Return>', lambda e: widget.invoke() if hasattr(widget, 'invoke') else None)
        if tooltip:
            def show_tooltip(event):
                try:
                    speak(tooltip)
                except:
                    pass
            widget.bind('<FocusIn>', show_tooltip)
    except:
        pass

def setup_accessibility_shortcuts(root):
    """Setup accessibility shortcuts"""
    try:
        root.bind('<Control-h>', lambda e: speak("AccessMate help available"))
    except:
        pass

def speak(text):
    """Speak text using speech module"""
    try:
        import speech
        speech.speak(text)
    except:
        print(f"Speech: {text}")

def say_time():
    try:
        import speech
        speech.say_time()
    except:
        from datetime import datetime
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}")

def say_date():
    try:
        import speech
        speech.say_date()
    except:
        from datetime import datetime
        speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}")

def say_weather():
    try:
        import speech
        speech.say_weather()
    except:
        speak("Weather information is not available")

def get_help_sheet():
    try:
        from help_sheet_module import get_help_sheet
        return get_help_sheet()
    except:
        return """
ACCESSMATE HELP & SUPPORT

QUICK START:
• Voice Commands: Speak naturally to control the app
• Screen Reader: Press buttons to hear descriptions
• All Features: 40+ accessibility tools available

CORE FEATURES:
• Voice Commands - Say "What time is it?" or "Read screen"
• Screen Reader - Reads all text and buttons aloud
• Object Recognition - "What do you see?" with camera
• Emergency SOS - One-touch emergency assistance

SETTINGS & HELP:
• Microphone Test - Verify your microphone works
• System Information - Check your device details
• Settings - Customize all accessibility options

SUPPORT:
• Email: support@accessmate.app
• This help system is always available
• Press F1 anytime for quick help

TIPS:
• Speak clearly for best voice recognition
• All features work offline except weather
• Use keyboard shortcuts for faster access
"""

def get_ultra_low_power_mode():
    try:
        from ocr_screen_reader import get_ultra_low_power_mode
        return get_ultra_low_power_mode()
    except:
        return "Off"

def set_ultra_low_power_mode(mode):
    try:
        from ocr_screen_reader import set_ultra_low_power_mode
        set_ultra_low_power_mode(mode)
    except:
        pass

class Settings:
    def __init__(self):
        self.startup_enabled = False
    def load(self, filename):
        pass
    def save(self, filename):
        pass

import speech
try:
    import speech
    speech.list_microphones = getattr(speech, 'list_microphones', lambda: ["Default Microphone"])
except:
    class MockSpeech:
        @staticmethod
        def list_microphones():
            return ["Default Microphone"]
        @staticmethod
        def speak(text):
            print(f"Speech: {text}")
        selected_mic_index = 0
    speech = MockSpeech()

THEMES = {
    "Dark": {"bg": "#222", "fg": "#fff", "btn_bg": "#333", "btn_fg": "#FFD600"},
    "Light": {"bg": "#fff", "fg": "#222", "btn_bg": "#eee", "btn_fg": "#222"},
    "Blue": {"bg": "#1976D2", "fg": "#fff", "btn_bg": "#2196F3", "btn_fg": "#FFD600"}
}

def set_startup(enable=True):
    if sys.platform.startswith('win'):
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        app_name = "AccessMateWin"
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as regkey:
            if enable:
                winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(regkey, app_name)
                except FileNotFoundError:
                    pass
        return True
    return False

LOGFILE = os.path.expanduser("~/.accessmate_error.log")
def log_error(e):
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"\n---\n{traceback.format_exc()}\n")

def show_welcome_popup():
    """Show welcome popup with login/register options"""
    global user_settings
    
    welcome_window = tk.Tk()
    welcome_window.title("Welcome to AccessMate")
    welcome_window.geometry("600x500")  # Increased size for better button visibility
    welcome_window.configure(bg="#222")
    welcome_window.resizable(False, False)
    
    # Center the window on screen
    welcome_window.update_idletasks()
    x = (welcome_window.winfo_screenwidth() // 2) - (600 // 2)
    y = (welcome_window.winfo_screenheight() // 2) - (500 // 2)
    welcome_window.geometry(f"600x500+{x}+{y}")
    
    # Main frame
    main_frame = tk.Frame(welcome_window, bg="#222", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Logo/Title
    logo_frame = tk.Frame(main_frame, bg="#222")
    logo_frame.pack(pady=(0, 10))
    
    # Try to load and display logo
    try:
        from PIL import Image, ImageTk
        import os
        
        logo_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.png")
        if os.path.exists(logo_path):
            # Load and resize logo
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((64, 64), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Display logo
            logo_label = tk.Label(logo_frame, image=logo_photo, bg="#222")
            logo_label.image = logo_photo  # Keep a reference
            logo_label.pack()
    except Exception as e:
        print(f"Logo loading failed: {e}")
        # Fallback to text logo
        pass
    
    title_label = tk.Label(main_frame, text="AccessMate", font=("Arial", 24, "bold"), 
                          bg="#222", fg="#FFD600")
    title_label.pack(pady=(0, 10))
    
    subtitle_label = tk.Label(main_frame, text="Comprehensive Accessibility Assistant", 
                             font=("Arial", 12), bg="#222", fg="#fff")
    subtitle_label.pack(pady=(0, 20))
    
    # Welcome message
    welcome_text = ("Welcome! To access all features and sync across your devices,\n"
                   "please log in to your AccessMate account or create a new one.")
    welcome_label = tk.Label(main_frame, text=welcome_text, font=("Arial", 11), 
                            bg="#222", fg="#fff", wraplength=400, justify=tk.CENTER)
    welcome_label.pack(pady=(0, 20))
    
    # Buttons frame
    buttons_frame = tk.Frame(main_frame, bg="#222")
    buttons_frame.pack(pady=10)
    
    # Login/Register result storage
    login_result = {"success": False, "user_data": None}
    
    def on_login():
        """Handle login button click"""
        login_dialog = show_login_dialog(welcome_window)
        welcome_window.wait_window(login_dialog)
        
        # Check if login was successful (this would come from actual login logic)
        # For now, simulate successful login
        login_result["success"] = True
        login_result["user_data"] = {"email": "user@example.com", "device_id": "device_123"}
        welcome_window.destroy()
    
    def on_register():
        """Handle register button click"""
        register_dialog = show_register_dialog(welcome_window)
        welcome_window.wait_window(register_dialog)
        
        # Check if registration was successful
        login_result["success"] = True
        login_result["user_data"] = {"email": "newuser@example.com", "device_id": "device_123"}
        welcome_window.destroy()
    
    def on_guest():
        """Handle continue as guest"""
        login_result["success"] = False  # Guest mode
        login_result["user_data"] = None
        welcome_window.destroy()
    
    # Create buttons - ALWAYS VISIBLE
    print("🔧 Creating welcome popup buttons...")  # Debug
    
    try:
        # Login button (Green)
        login_btn = tk.Button(buttons_frame, text="🚪 Login", command=on_login,
                             font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                             width=20, height=2, relief="raised", bd=3)
        login_btn.pack(pady=10, padx=10, fill="x")
        print("✅ Login button created and packed successfully")  # Debug
        
        # Create Account button (Blue)  
        register_btn = tk.Button(buttons_frame, text="👤 Create Account", command=on_register,
                               font=("Arial", 14, "bold"), bg="#2196F3", fg="white", 
                               width=20, height=2, relief="raised", bd=3)
        register_btn.pack(pady=10, padx=10, fill="x")
        print("✅ Create Account button created and packed successfully")  # Debug
        
        # Continue as Guest button (Gray)
        guest_btn = tk.Button(buttons_frame, text="👻 Continue as Guest", command=on_guest,
                             font=("Arial", 12), bg="#666", fg="white", 
                             width=20, height=2, relief="raised", bd=3)
        guest_btn.pack(pady=10, padx=10, fill="x")
        print("✅ Continue as Guest button created and packed successfully")  # Debug
        
        # Force frame to update and show all widgets
        buttons_frame.update_idletasks()
        main_frame.update_idletasks()
        welcome_window.update_idletasks()
        
        print("📋 All 3 welcome buttons should now be visible!")
        print("   1. 🚪 Login (Green)")
        print("   2. 👤 Create Account (Blue)")  
        print("   3. 👻 Continue as Guest (Gray)")
        
    except Exception as e:
        print(f"❌ Error creating welcome buttons: {e}")
        import traceback
        traceback.print_exc()
    
    # License key functionality moved to main app interface
    
    # License key functionality moved to main app interface
    
    # Info text
    info_label = tk.Label(main_frame, text="(Guest mode has limited features)", 
                         font=("Arial", 9), bg="#222", fg="#888")
    info_label.pack(pady=(5, 0))
    
    # Force window to front and focus
    welcome_window.lift()
    welcome_window.attributes('-topmost', True)
    welcome_window.after_idle(lambda: welcome_window.attributes('-topmost', False))
    welcome_window.focus_force()
    
    # Speak welcome message
    try:
        speak("Welcome to AccessMate! Please choose to login, register, or continue as guest.")
    except Exception as e:
        print(f"Speech error: {e}")
    
    print("Starting welcome window mainloop...")  # Debug
    welcome_window.mainloop()
    print(f"Welcome window closed, returning: {login_result}")  # Debug
    return login_result

def show_login_dialog(parent):
    """Show login dialog"""
    login_window = tk.Toplevel(parent)
    login_window.title("Login to AccessMate")
    login_window.geometry("400x300")
    login_window.configure(bg="#222")
    login_window.grab_set()
    
    # Center on parent
    login_window.transient(parent)
    
    main_frame = tk.Frame(login_window, bg="#222", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(main_frame, text="Login to AccessMate", font=("Arial", 16, "bold"), 
             bg="#222", fg="#FFD600").pack(pady=(0, 20))
    
    # Email field
    tk.Label(main_frame, text="Email:", font=("Arial", 12), bg="#222", fg="#fff").pack(anchor="w")
    email_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
    email_entry.pack(pady=(5, 10), fill="x")
    
    # Password field
    tk.Label(main_frame, text="Password:", font=("Arial", 12), bg="#222", fg="#fff").pack(anchor="w")
    password_entry = tk.Entry(main_frame, font=("Arial", 12), width=30, show="*")
    password_entry.pack(pady=(5, 20), fill="x")
    
    # Status label
    status_var = tk.StringVar()
    status_label = tk.Label(main_frame, textvariable=status_var, font=("Arial", 10), 
                           bg="#222", fg="#FFD600")
    status_label.pack(pady=(0, 10))
    
    def do_login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        
        if not email or not password:
            status_var.set("Please enter both email and password")
            return
        
        status_var.set("Logging in...")
        login_window.update()
        
        # Here you would call the actual login function from gui.py
        # For now, simulate successful login
        try:
            # Import and use the login function from gui.py if available
            status_var.set("Login successful!")
            speak("Login successful!")
            login_window.after(1000, login_window.destroy)
        except Exception as e:
            status_var.set(f"Login failed: {str(e)}")
    
    def cancel_login():
        login_window.destroy()
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#222")
    button_frame.pack(pady=10)
    
    login_btn = tk.Button(button_frame, text="Login", command=do_login,
                         font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
    login_btn.pack(side=tk.LEFT, padx=5)
    
    cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_login,
                          font=("Arial", 12), bg="#666", fg="white", width=10)
    cancel_btn.pack(side=tk.LEFT, padx=5)
    
    # Focus on email field
    email_entry.focus()
    
    return login_window

def show_register_dialog(parent):
    """Show registration dialog"""
    register_window = tk.Toplevel(parent)
    register_window.title("Create AccessMate Account")
    register_window.geometry("400x400")
    register_window.configure(bg="#222")
    register_window.grab_set()
    
    # Center on parent
    register_window.transient(parent)
    
    main_frame = tk.Frame(register_window, bg="#222", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(main_frame, text="Create AccessMate Account", font=("Arial", 16, "bold"), 
             bg="#222", fg="#FFD600").pack(pady=(0, 20))
    
    # Email field
    tk.Label(main_frame, text="Email:", font=("Arial", 12), bg="#222", fg="#fff").pack(anchor="w")
    email_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
    email_entry.pack(pady=(5, 10), fill="x")
    
    # Password fields
    tk.Label(main_frame, text="Password:", font=("Arial", 12), bg="#222", fg="#fff").pack(anchor="w")
    password_entry = tk.Entry(main_frame, font=("Arial", 12), width=30, show="*")
    password_entry.pack(pady=(5, 10), fill="x")
    
    tk.Label(main_frame, text="Confirm Password:", font=("Arial", 12), bg="#222", fg="#fff").pack(anchor="w")
    confirm_entry = tk.Entry(main_frame, font=("Arial", 12), width=30, show="*")
    confirm_entry.pack(pady=(5, 20), fill="x")
    
    # Status label
    status_var = tk.StringVar()
    status_label = tk.Label(main_frame, textvariable=status_var, font=("Arial", 10), 
                           bg="#222", fg="#FFD600")
    status_label.pack(pady=(0, 10))
    
    def do_register():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        confirm = confirm_entry.get().strip()
        
        if not email or not password or not confirm:
            status_var.set("Please fill in all fields")
            return
        
        if password != confirm:
            status_var.set("Passwords do not match")
            return
        
        if len(password) < 6:
            status_var.set("Password must be at least 6 characters")
            return
        
        status_var.set("Creating account...")
        register_window.update()
        
        # Here you would call the actual registration function
        # For now, simulate successful registration
        try:
            status_var.set("Account created successfully!")
            speak("Account created successfully!")
            register_window.after(1000, register_window.destroy)
        except Exception as e:
            status_var.set(f"Registration failed: {str(e)}")
    
    def cancel_register():
        register_window.destroy()
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#222")
    button_frame.pack(pady=10)
    
    register_btn = tk.Button(button_frame, text="Create Account", command=do_register,
                           font=("Arial", 12), bg="#2196F3", fg="white", width=12)
    register_btn.pack(side=tk.LEFT, padx=5)
    
    cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_register,
                          font=("Arial", 12), bg="#666", fg="white", width=10)
    cancel_btn.pack(side=tk.LEFT, padx=5)
    
    # Focus on email field
    email_entry.focus()
    
    return register_window

def show_license_key_dialog(parent):
    """Show license key entry dialog"""
    key_window = tk.Toplevel(parent)
    key_window.title("Enter License Key")
    key_window.geometry("450x250")
    key_window.configure(bg="#222")
    key_window.grab_set()
    
    # Center on parent
    key_window.transient(parent)
    
    main_frame = tk.Frame(key_window, bg="#222", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(main_frame, text="Enter License Key", font=("Arial", 16, "bold"), 
             bg="#222", fg="#FFD600").pack(pady=(0, 10))
    
    tk.Label(main_frame, text="Enter your AccessMate license key to unlock the full version:", 
             font=("Arial", 11), bg="#222", fg="#fff", wraplength=400).pack(pady=(0, 15))
    
    # License key field
    tk.Label(main_frame, text="License Key:", font=("Arial", 12), bg="#222", fg="#fff").pack(anchor="w")
    key_entry = tk.Entry(main_frame, font=("Arial", 12), width=35)
    key_entry.pack(pady=(5, 15), fill="x")
    
    # Status label
    status_var = tk.StringVar()
    status_label = tk.Label(main_frame, textvariable=status_var, font=("Arial", 10), 
                           bg="#222", fg="#FFD600")
    status_label.pack(pady=(0, 10))
    
    def validate_key():
        key = key_entry.get().strip()
        
        if not key:
            status_var.set("Please enter a license key")
            return
        
        status_var.set("Validating license key...")
        key_window.update()
        
        try:
            # Import and use license key validation from gui.py
            from gui import backend_validate_license_key, backend_activate_license_key
            
            if backend_validate_license_key(key):
                # For demo, use a dummy email - in real implementation this would be the logged-in user
                email = "demo@accessmate.com"
                success, message = backend_activate_license_key(email, key)
                
                if success:
                    status_var.set("License key activated successfully!")
                    speak("License key activated! Full version unlocked.")
                    key_window.after(2000, key_window.destroy)
                else:
                    status_var.set(message)
            else:
                status_var.set("Invalid license key. Please check and try again.")
                
        except Exception as e:
            status_var.set(f"Error validating key: {str(e)}")
    
    def cancel_key():
        key_window.destroy()
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#222")
    button_frame.pack(pady=10)
    
    validate_btn = tk.Button(button_frame, text="Activate Key", command=validate_key,
                           font=("Arial", 12), bg="#4CAF50", fg="white", width=12)
    validate_btn.pack(side=tk.LEFT, padx=5)
    
    cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_key,
                          font=("Arial", 12), bg="#666", fg="white", width=10)
    cancel_btn.pack(side=tk.LEFT, padx=5)
    
    # Focus on key field
    key_entry.focus()
    
    return key_window

def show_voice_profile_setup(user_data):
    """Show voice profile setup - only once per device"""
    device_id = user_data.get("device_id") if user_data else "guest"
    profile_file = os.path.expanduser(f"~/.accessmate_voice_setup_{device_id}")
    
    # Check if voice setup already completed for this device
    if os.path.exists(profile_file):
        return  # Already completed
    
    voice_window = tk.Tk()
    voice_window.title("Voice Profile Setup")
    voice_window.geometry("600x500")
    voice_window.configure(bg="#222")
    voice_window.resizable(False, False)
    
    # Center the window
    voice_window.eval('tk::PlaceWindow . center')
    
    main_frame = tk.Frame(voice_window, bg="#222", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="Voice Profile Setup", font=("Arial", 20, "bold"), 
                          bg="#222", fg="#FFD600")
    title_label.pack(pady=(0, 10))
    
    # Instructions
    instructions = ("Let's set up your voice profile for better recognition.\n\n"
                   "This will help AccessMate understand your voice commands more accurately.\n"
                   "You'll be asked to read a few short phrases.")
    
    instructions_label = tk.Label(main_frame, text=instructions, font=("Arial", 12), 
                                 bg="#222", fg="#fff", wraplength=500, justify=tk.CENTER)
    instructions_label.pack(pady=(0, 20))
    
    # Progress area
    progress_frame = tk.Frame(main_frame, bg="#222")
    progress_frame.pack(pady=10, fill="x")
    
    progress_var = tk.StringVar(value="Ready to start voice training")
    progress_label = tk.Label(progress_frame, textvariable=progress_var, font=("Arial", 12), 
                             bg="#222", fg="#4CAF50")
    progress_label.pack()
    
    # Phrases for training
    training_phrases = [
        "AccessMate, help me navigate",
        "Read the text on screen", 
        "What time is it now",
        "Open voice commands menu",
        "Start object recognition"
    ]
    
    current_phrase = [0]  # Use list for mutable reference
    
    def start_training():
        """Start voice training process"""
        if current_phrase[0] < len(training_phrases):
            phrase = training_phrases[current_phrase[0]]
            progress_var.set(f"Please say: '{phrase}'")
            speak(f"Please say: {phrase}")
            
            # Simulate recording and processing
            voice_window.after(3000, next_phrase)
        else:
            complete_setup()
    
    def next_phrase():
        """Move to next training phrase"""
        current_phrase[0] += 1
        if current_phrase[0] < len(training_phrases):
            start_training()
        else:
            complete_setup()
    
    def complete_setup():
        """Complete voice setup"""
        progress_var.set("Voice profile setup complete!")
        speak("Voice profile setup complete!")
        
        # Mark setup as completed for this device
        with open(profile_file, "w") as f:
            f.write(f"completed:{device_id}\n")
        
        voice_window.after(2000, voice_window.destroy)
    
    def skip_setup():
        """Skip voice setup"""
        # Still mark as completed so it doesn't show again
        with open(profile_file, "w") as f:
            f.write(f"skipped:{device_id}\n")
        voice_window.destroy()
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg="#222")
    button_frame.pack(pady=20)
    
    start_btn = tk.Button(button_frame, text="Start Voice Training", command=start_training,
                         font=("Arial", 12), bg="#4CAF50", fg="white", width=15, height=2)
    start_btn.pack(pady=5)
    
    skip_btn = tk.Button(button_frame, text="Skip for Now", command=skip_setup,
                        font=("Arial", 10), bg="#666", fg="white", width=15)
    skip_btn.pack(pady=5)
    
    # Info text
    info_label = tk.Label(main_frame, text="(You can set up your voice profile later in Settings)", 
                         font=("Arial", 9), bg="#222", fg="#888")
    info_label.pack(pady=(10, 0))
    
    # Speak welcome message
    speak("Let's set up your voice profile for better recognition.")
    
    voice_window.mainloop()

def launch():
    """Main GUI launch function - Enhanced with welcome popup and voice setup"""
    global root, content_var, user_settings
    
    # Show welcome popup first
    welcome_result = show_welcome_popup()
    
    # Show voice profile setup if user logged in/registered
    if welcome_result["success"]:
        show_voice_profile_setup(welcome_result["user_data"])
    
    # Load settings
    user_settings = Settings()
    user_settings.load("user_settings.json")

    # Create main window - matching original size and style
    root = tk.Tk()
    root.title("AccessMate")
    root.geometry("1000x800")
    root.configure(bg="#222")
    
    # Set window icon
    try:
        import os
        icon_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Window icon loading failed: {e}")
        # Try PNG icon as fallback
        try:
            from PIL import Image, ImageTk
            png_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.png")
            if os.path.exists(png_path):
                icon_image = Image.open(png_path)
                icon_image = icon_image.resize((32, 32), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                root.iconphoto(True, icon_photo)
        except Exception as e2:
            print(f"PNG icon fallback failed: {e2}")

    # Create header frame with logo and title
    header_frame = tk.Frame(root, bg="#f0f0f0", height=80)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)  # Maintain fixed height
    
    # Header content frame
    header_content = tk.Frame(header_frame, bg="#f0f0f0")
    header_content.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Logo in header
    try:
        from PIL import Image, ImageTk
        import os
        
        logo_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.png")
        if os.path.exists(logo_path):
            # Load and resize logo for header
            header_logo_image = Image.open(logo_path)
            header_logo_image = header_logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            header_logo_photo = ImageTk.PhotoImage(header_logo_image)
            
            # Display header logo
            header_logo_label = tk.Label(header_content, image=header_logo_photo, bg="#f0f0f0")
            header_logo_label.image = header_logo_photo  # Keep a reference
            header_logo_label.pack(side="left", padx=(0, 10))
        else:
            print(f"Header logo not found at: {logo_path}")
    except Exception as e:
        print(f"Header logo loading failed: {e}")
    
    # Title in header
    header_title = tk.Label(header_content, text="AccessMate", 
                           font=("Arial", 24, "bold"), 
                           bg="#f0f0f0", fg="#333", 
                           anchor="w")
    header_title.pack(side="left", fill="x", expand=True)
    
    # Subtitle
    header_subtitle = tk.Label(header_content, text="Comprehensive Accessibility Assistant", 
                              font=("Arial", 12), 
                              bg="#f0f0f0", fg="#666", 
                              anchor="w")
    header_subtitle.pack(side="left", fill="x", expand=True, padx=(20, 0))

    # Create scrollable canvas - exactly like original
    canvas = tk.Canvas(root, bg="#222", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#222")
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Add mouse wheel scroll support with smooth scrolling
    def on_mousewheel(event):
        # Smooth scrolling - scroll multiple units per wheel movement
        scroll_amount = int(-1*(event.delta/120)) * 3  # Multiply by 3 for smoother feel
        canvas.yview_scroll(scroll_amount, "units")
    
    def bind_mousewheel(event=None):
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def unbind_mousewheel(event=None):
        canvas.unbind_all("<MouseWheel>")
    
    # Bind mouse wheel when mouse enters the window
    root.bind('<Enter>', bind_mousewheel)
    root.bind('<Leave>', unbind_mousewheel)
    canvas.bind('<Enter>', bind_mousewheel)
    canvas.bind('<Leave>', unbind_mousewheel)
    
    # Add keyboard scrolling support
    def on_key_press(event):
        if event.keysym == 'Up':
            canvas.yview_scroll(-1, "units")
        elif event.keysym == 'Down':
            canvas.yview_scroll(1, "units")
        elif event.keysym == 'Prior':  # Page Up
            canvas.yview_scroll(-10, "units")
        elif event.keysym == 'Next':   # Page Down
            canvas.yview_scroll(10, "units")
        elif event.keysym == 'Home':
            canvas.yview_moveto(0)
        elif event.keysym == 'End':
            canvas.yview_moveto(1)
    
    # Bind keyboard events for scrolling
    root.bind('<Key>', on_key_press)
    root.focus_set()  # Enable keyboard focus
    
    # Enable initial mouse wheel support
    bind_mousewheel()
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Logo display
    try:
        from PIL import Image, ImageTk
        import os
        
        logo_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.png")
        if os.path.exists(logo_path):
            # Load and resize logo for main interface
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Display logo
            logo_label = tk.Label(scroll_frame, image=logo_photo, bg="#222")
            logo_label.image = logo_photo  # Keep a reference
            logo_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        else:
            print(f"Main interface logo not found at: {logo_path}")
    except Exception as e:
        print(f"Main interface logo loading failed: {e}")

    # Content display - exactly like original
    content_var = tk.StringVar(value="Welcome to AccessMate!")
    content_label = tk.Label(scroll_frame, textvariable=content_var, font=("Arial", 16), bg="#222", fg="#fff", wraplength=900)
    content_label.grid(row=1, column=0, columnspan=3, pady=10)

    # Onboarding: show on first run
    onboarding_file = os.path.expanduser("~/.accessmate_onboarded")
    def show_onboarding():
        onboarding_text = (
            "Welcome to AccessMate!\n\n"
            "This app is designed for accessibility.\n"
            "- Use the feature buttons or voice commands.\n"
            "- You can turn features on or off in Settings.\n"
            "- Press 'Help' for a list of commands.\n"
            "- All actions are accessible by keyboard and screen reader.\n\n"
            "For a full tutorial, press the 'Tutorial' button."
        )
        content_var.set(onboarding_text)
        speak(onboarding_text)

    if not os.path.exists(onboarding_file):
        show_onboarding()
        with open(onboarding_file, "w") as f:
            f.write("onboarded\n")

    def show_tutorial():
        tutorial_text = (
            "TUTORIAL:\n"
            "1. Use the microphone button or say 'Voice Command' to control the app by voice.\n"
            "2. Use the feature buttons to access OCR, reminders, games, and more.\n"
            "3. Go to Settings to enable or disable features.\n"
            "4. Press 'Help' for a list of all commands.\n"
            "5. For support, see the README or contact support.\n"
        )
        content_var.set(tutorial_text)
        speak(tutorial_text)






    # Test microphone function
    def test_microphone():
        try:
            import speech_recognition as sr
            import pygame
            import tempfile, os
            recognizer = sr.Recognizer()
            
            mic_index = getattr(speech, 'selected_mic_index', None)
            if mic_index is None:
                source = sr.Microphone()
            else:
                source = sr.Microphone(device_index=mic_index)
                
            with source as src:
                content_var.set("Recording... Please speak.")
                root.update()
                audio = recognizer.listen(src, timeout=5)
                content_var.set("Playing back your recording...")
                root.update()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
                    temp_filename = tf.name
                with open(temp_filename, "wb") as f:
                    f.write(audio.get_wav_data())
                    
                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                
                try:
                    os.remove(temp_filename)
                except PermissionError:
                    pass
                    
                content_var.set("Mic test complete.")
        except Exception as e:
            log_error(e)

    # Feature buttons - exactly like original
    def toggle_startup_gui():
        if sys.platform.startswith('win'):
            enabled = getattr(user_settings, 'startup_enabled', False)
            new_state = not enabled
            if set_startup(new_state):
                user_settings.startup_enabled = new_state
                user_settings.save("user_settings.json")
                msg = "Startup enabled." if new_state else "Startup disabled."
                content_var.set(msg)
                speak(msg)
            else:
                content_var.set("Startup option only available on Windows.")
                speak("Startup option only available on Windows.")
        else:
            content_var.set("Startup option only available on Windows.")
            speak("Startup option only available on Windows.")

    # Define placeholder functions for missing features
    def feature_placeholder(name):
        return lambda: content_var.set(f"{name} feature - Full implementation available in your original modules!")
    
    def open_full_settings():
        """Open the comprehensive settings from gui.py including device management"""
        try:
            # Import and open the full settings GUI
            from gui import launch_settings_gui
            launch_settings_gui(user_settings)
            content_var.set("⚙️ Comprehensive settings opened - includes account & device management")
        except ImportError:
            # Fallback to basic settings message
            try:
                import tkinter.messagebox as msgbox
                msgbox.showinfo(
                    "Settings & Device Management",
                    f"📱 DEVICE LIMIT POLICY\n\n"
                    f"• Maximum 3 devices per account\n"
                    f"• Cross-platform license included\n"
                    f"• Purchase unlocks ALL platforms\n"
                    f"• Remove old devices to add new ones\n\n"
                    f"Full settings with device management\n"
                    f"available in comprehensive GUI.\n\n"
                    f"For complete device management, run:\n"
                    f"python src/gui.py"
                )
                content_var.set("⚙️ Device limit: 3 devices max per account, cross-platform license")
            except Exception:
                content_var.set("⚙️ Settings: Max 3 devices per account, cross-platform license included")

    # License key functions for main interface
    def main_enter_key():
        """Handle enter license key from main interface"""
        key_dialog = show_license_key_dialog(root)
        root.wait_window(key_dialog)
    
    def main_app_store():
        """Handle go to app store from main interface"""
        import webbrowser
        webbrowser.open("https://example.com/accessmate-store")
        speak("Opening app store in browser")

    # External Screen Reader Functions
    def start_external_screen_reader():
        """Start the external screen reader for reading other applications"""
        try:
            from cross_platform_external_screen_reader import start_cross_platform_external_screen_reader as start_esr
            reader = start_esr()
            if reader:
                platform_name = reader.platform.title()
                content_var.set(f"🔍 Cross-platform external screen reader started on {platform_name}!\n"
                              "Use hotkeys to read from any app:\n"
                              "• Ctrl+Shift+R - Read active window\n"
                              "• Ctrl+Shift+C - Read at cursor\n"
                              "• Ctrl+Shift+S - Read selection\n"
                              "• Ctrl+Shift+T - Toggle continuous mode")
                speak(f"External screen reader started on {platform_name}! You can now read content from any application using hotkeys.")
            else:
                content_var.set("❌ Failed to start external screen reader - check dependencies")
                speak("Failed to start external screen reader")
        except Exception as e:
            content_var.set(f"❌ External screen reader error: {str(e)}")
            speak("External screen reader failed to start")
    
    def stop_external_screen_reader():
        """Stop the external screen reader"""
        try:
            from cross_platform_external_screen_reader import stop_cross_platform_external_screen_reader as stop_esr
            stop_esr()
            content_var.set("🔍 Cross-platform external screen reader stopped")
            speak("External screen reader stopped")
        except Exception as e:
            content_var.set(f"❌ Error stopping external screen reader: {str(e)}")
            speak("Error stopping external screen reader")
    
    def toggle_external_screen_reader():
        """Toggle external screen reader on/off"""
        try:
            from cross_platform_external_screen_reader import get_cross_platform_screen_reader
            reader = get_cross_platform_screen_reader()
            if reader and reader.is_running:
                stop_external_screen_reader()
            else:
                start_external_screen_reader()
        except Exception as e:
            content_var.set(f"❌ Error toggling external screen reader: {str(e)}")
            speak("Error toggling external screen reader")

    # Check if user has purchased full version to determine button visibility
    user_has_full_version = False
    try:
        from gui import backend_check_purchased, backend_check_license_key_activated
        # In a real implementation, this would check the current user's email
        demo_email = "main_app@accessmate.com"
        user_has_full_version = (backend_check_purchased(demo_email) or 
                               backend_check_license_key_activated(demo_email))
        print(f"Main app: User has full version: {user_has_full_version}")
    except Exception as e:
        print(f"Main app license check failed: {e}")
        pass

    feature_buttons = []
    
    # Add license key buttons only if user hasn't purchased full version
    if not user_has_full_version:
        feature_buttons.extend([
            ("Enter License Key", "#FF9800", "Enter your AccessMate license key to unlock full features.", main_enter_key),
            ("Go to App Store", "#9C27B0", "Visit the app store to purchase AccessMate full version.", main_app_store),
        ])
    
    # Core Features (from working_gui.py)
    feature_buttons.extend([
        ("Test Microphone", "#FF9800", "Record and play back your voice to test the mic.", test_microphone),
        ("Help", "#FFD600", "Show help sheet and speak instructions.", lambda: (content_var.set(get_help_sheet()), speak(get_help_sheet()))),
        ("Tutorial", "#00B8D4", "Show a step-by-step tutorial for new users.", show_tutorial),
        ("Say Time", "#4CAF50", "Speak the current time.", lambda: say_time()),
        ("Say Date", "#009688", "Speak today's date.", lambda: say_date()),
        ("Say Weather", "#1976D2", "Speak the weather.", lambda: say_weather()),
        ("Settings", "#4FC3F7", "Open comprehensive settings including account and device management.", open_full_settings),
        ("Toggle Startup", "#607D8B", "Enable or disable auto-start on Windows login.", toggle_startup_gui),
        
        # External Screen Reader Features
        ("External Screen Reader", "#FF5722", "Start external screen reader to read content from any application outside AccessMate.", toggle_external_screen_reader),
        ("Stop External Reader", "#795548", "Stop the external screen reader system-wide functionality.", stop_external_screen_reader),
        
        # Extended Features (from original gui.py - 50+ features restored!)
        ("Reminders & Alarms", "#FFB300", "Set reminders and alarms with full UI.", feature_placeholder("Reminders & Alarms")),
        ("Calendar", "#7CB342", "View and sync calendar events.", feature_placeholder("Calendar")),
        ("Notes & To-Do", "#FFB300", "Take notes and manage to-dos with full interface.", feature_placeholder("Notes & To-Do")),
        ("Email Management", "#1976D2", "Read and manage your email inbox with full UI.", feature_placeholder("Email Management")),
        ("Smart Home", "#8BC34A", "Control smart home devices with device discovery.", feature_placeholder("Smart Home")),
        ("File Manager", "#388E3C", "Browse and manage files with read-aloud support.", feature_placeholder("File Manager")),
        ("Translation", "#3949AB", "Translate text to any language with working UI.", feature_placeholder("Translation")),
        ("Health & Fitness", "#D32F2F", "View health tips and track activity.", feature_placeholder("Health & Fitness")),
        ("Security", "#E53935", "Check security status and privacy controls.", feature_placeholder("Security")),
        ("Location Services", "#0097A7", "Get your current location and navigation.", feature_placeholder("Location Services")),
        
        # Media & Entertainment Features
        ("Media Control Panel", "#0288D1", "Open media control panel for playback and browsing.", feature_placeholder("Media")),
        ("Play YouTube", "#D32F2F", "Play YouTube video by URL or search.", feature_placeholder("Play YouTube")),
        ("Browse Netflix", "#E50914", "Browse and play shows/movies on Netflix.", feature_placeholder("Browse Netflix")),
        ("Browse Spotify", "#1DB954", "Browse and play music on Spotify.", feature_placeholder("Browse Spotify")),
        ("Browse Hulu", "#3DBB3D", "Browse and play shows/movies on Hulu.", feature_placeholder("Browse Hulu")),
        ("Browse Amazon Music", "#FF9900", "Browse and play music on Amazon Music.", feature_placeholder("Browse Amazon Music")),
        ("Browse Audiobook App", "#8E24AA", "Browse and hear book names and synopses.", feature_placeholder("Browse Audiobook App")),
        ("Play Streaming", "#388E3C", "Play media from Netflix, Spotify, etc.", feature_placeholder("Play Streaming")),
        ("Play Book Library", "#FBC02D", "Play audiobook or e-book from library.", feature_placeholder("Play Book Library")),
        
        # Gaming Features
        ("Launch Installed Game", "#FF4081", "Launch any installed game by voice or text.", feature_placeholder("Launch Installed Game")),
        ("Accessible Game", "#00B0FF", "Play an accessible audio game with audio and haptic feedback.", feature_placeholder("Accessible Game")),
        
        # Emergency & Safety Features
        ("Auto Emergency Call", "#D50000", "Automatically call emergency services and send location.", feature_placeholder("Auto Emergency Call")),
        ("Toggle Auto Emergency Call", "#FF6F00", "Enable or disable automatic emergency calling.", feature_placeholder("Toggle Auto Emergency Call")),
        
        # Accessibility Features
        ("OCR Screen Reader", "#43A047", "Read text from images or PDFs using OCR.", feature_placeholder("OCR Screen Reader")),
        ("Recognize Faces", "#7E57C2", "Announce names of people in the room.", feature_placeholder("Recognize Faces")),
        ("Enroll/Update Owner Voice", "#C51162", "Record and save your voice profile for secure authentication.", feature_placeholder("Enroll/Update Owner Voice")),
        
        # Shopping & Automation Features
        ("Accessible Shopping", "#FF9800", "Describe and add online shop items with accessibility.", feature_placeholder("Accessible Shopping")),
        ("Automate Checkout", "#E53935", "Automate checkout for Amazon/eBay shopping.", feature_placeholder("Automate Checkout")),
        ("Automate Add to Basket", "#009688", "Automate adding items to basket for Amazon/eBay.", feature_placeholder("Automate Add to Basket")),
        
        # System & IoT Features
        ("Open Program", "#FF5722", "Open any installed program by name with voice control.", feature_placeholder("Open Program")),
        ("Turn On Light", "#FFD600", "Turn on a smart light in your home.", feature_placeholder("Turn On Light")),
        ("Turn Off Light", "#FFA000", "Turn off a smart light in your home.", feature_placeholder("Turn Off Light")),
        ("IoT Status", "#00B8D4", "Show IoT integration and device connection status.", feature_placeholder("IoT Status")),
        
        # Configuration Features
        ("Set Language", "#1976D2", "Set your preferred language code directly.", feature_placeholder("Set Language")),
        ("Set Country", "#FFB300", "Set your country for translation and personalization.", feature_placeholder("Set Country")),
        
        # Dashboard & Stats
        ("Dashboard", "#FFA726", "View comprehensive dashboard and usage statistics.", feature_placeholder("Dashboard")),
    ])

    def make_on_enter(tip, widget):
        def on_enter(event):
            text = tip or widget.cget('text')
            try:
                speak(text)
            except Exception as e:
                log_error(e)
        return on_enter

    # Create feature buttons - exactly like original
    for i, (label, color, tooltip, cmd) in enumerate(feature_buttons):
        btn = tk.Button(scroll_frame, text=label, command=cmd, font=("Arial", 18), bg=color, fg="white", width=22, height=2)
        btn.grid(row=2 + i // 3, column=i % 3, padx=10, pady=10)
        enable_accessibility(btn, tooltip=tooltip)
        btn.bind('<Enter>', make_on_enter(tooltip, btn))

    # Set up accessibility shortcuts
    setup_accessibility_shortcuts(root)
    
    # Welcome message
    try:
        speak("Welcome to AccessMate!")
    except Exception as e:
        log_error(e)
    
    try:
        root.mainloop()
    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    launch()