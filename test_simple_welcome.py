#!/usr/bin/env python3
"""Simple test to show welcome popup with debug output"""

import tkinter as tk
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def simple_welcome_test():
    """Simple welcome popup to test what buttons are showing"""
    
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
        print("Login button clicked!")
        welcome_window.destroy()
    
    def on_register():
        result["clicked"] = "register"
        print("Register button clicked!")
        welcome_window.destroy()
    
    def on_guest():
        result["clicked"] = "guest"
        print("Guest button clicked!")
        welcome_window.destroy()
    
    # Create buttons
    login_btn = tk.Button(buttons_frame, text="Login", command=on_login,
                         font=("Arial", 12), bg="#4CAF50", fg="white", 
                         width=12, height=2)
    login_btn.pack(pady=5)
    print("Login button created")
    
    register_btn = tk.Button(buttons_frame, text="Create Account", command=on_register,
                           font=("Arial", 12), bg="#2196F3", fg="white", 
                           width=12, height=2)
    register_btn.pack(pady=5)
    print("Register button created")
    
    guest_btn = tk.Button(buttons_frame, text="Continue as Guest", command=on_guest,
                         font=("Arial", 10), bg="#666", fg="white", 
                         width=12, height=1)
    guest_btn.pack(pady=(10, 0))
    print("Guest button created")
    
    print("Starting welcome window...")
    welcome_window.mainloop()
    print(f"Welcome window closed, result: {result}")
    return result

if __name__ == "__main__":
    simple_welcome_test()