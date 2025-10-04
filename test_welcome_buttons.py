#!/usr/bin/env python3
"""Test script to check welcome popup button visibility"""

import tkinter as tk
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_welcome_buttons():
    """Test welcome popup to see exactly what buttons appear"""
    
    welcome_window = tk.Tk()
    welcome_window.title("AccessMate Welcome Test")
    welcome_window.geometry("500x400")
    welcome_window.configure(bg="#222")
    
    # Main frame
    main_frame = tk.Frame(welcome_window, bg="#222", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="AccessMate", font=("Arial", 24, "bold"), 
                          bg="#222", fg="#FFD600")
    title_label.pack(pady=(0, 10))
    
    # Welcome message
    welcome_text = ("Welcome! To access all features and sync across your devices,\n"
                   "please log in to your AccessMate account or create a new one.")
    welcome_label = tk.Label(main_frame, text=welcome_text, font=("Arial", 11), 
                            bg="#222", fg="#fff", wraplength=400, justify=tk.CENTER)
    welcome_label.pack(pady=(0, 20))
    
    # Buttons frame
    buttons_frame = tk.Frame(main_frame, bg="#222")
    buttons_frame.pack(pady=10)
    
    # Result storage
    result = {"clicked": None}
    
    def on_login():
        result["clicked"] = "login"
        print("✅ LOGIN button clicked!")
        welcome_window.destroy()
    
    def on_register():
        result["clicked"] = "register"
        print("✅ CREATE ACCOUNT button clicked!")
        welcome_window.destroy()
    
    def on_guest():
        result["clicked"] = "guest"
        print("✅ CONTINUE AS GUEST button clicked!")
        welcome_window.destroy()
    
    # Create buttons exactly like in main app
    print("🔧 Creating welcome popup buttons...")
    
    # Login button
    login_btn = tk.Button(buttons_frame, text="Login", command=on_login,
                         font=("Arial", 12), bg="#4CAF50", fg="white", 
                         width=15, height=2)
    login_btn.pack(pady=5)
    print("✅ Login button created and packed")
    
    # Create Account button
    register_btn = tk.Button(buttons_frame, text="Create Account", command=on_register,
                           font=("Arial", 12), bg="#2196F3", fg="white", 
                           width=15, height=2)
    register_btn.pack(pady=5)
    print("✅ Create Account button created and packed")
    
    # Continue as Guest button
    guest_btn = tk.Button(buttons_frame, text="Continue as Guest", command=on_guest,
                         font=("Arial", 10), bg="#666", fg="white", 
                         width=15, height=1)
    guest_btn.pack(pady=(10, 0))
    print("✅ Continue as Guest button created and packed")
    
    # Info text
    info_label = tk.Label(main_frame, text="(Guest mode has limited features)", 
                         font=("Arial", 9), bg="#222", fg="#888")
    info_label.pack(pady=(5, 0))
    
    # Force window to front
    welcome_window.lift()
    welcome_window.attributes('-topmost', True)
    welcome_window.after_idle(lambda: welcome_window.attributes('-topmost', False))
    welcome_window.focus_force()
    
    print("🚀 Starting welcome window...")
    print("📋 You should see 3 buttons:")
    print("   1. Login (Green)")
    print("   2. Create Account (Blue)")
    print("   3. Continue as Guest (Gray)")
    
    welcome_window.mainloop()
    print(f"🎯 Result: {result}")
    return result

if __name__ == "__main__":
    test_welcome_buttons()