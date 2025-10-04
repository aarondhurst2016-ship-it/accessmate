#!/usr/bin/env python3
"""Direct test of welcome popup button visibility"""

import tkinter as tk

def direct_welcome_test():
    """Direct test showing exactly what the welcome popup should look like"""
    
    welcome_window = tk.Tk()
    welcome_window.title("AccessMate Welcome - Button Test")
    welcome_window.geometry("600x500")
    welcome_window.configure(bg="#222")
    
    # Center the window
    welcome_window.update_idletasks()
    x = (welcome_window.winfo_screenwidth() // 2) - (600 // 2)
    y = (welcome_window.winfo_screenheight() // 2) - (500 // 2)
    welcome_window.geometry(f"600x500+{x}+{y}")
    
    # Main frame
    main_frame = tk.Frame(welcome_window, bg="#222", padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="AccessMate", font=("Arial", 24, "bold"), 
                          bg="#222", fg="#FFD600")
    title_label.pack(pady=(0, 10))
    
    # Subtitle
    subtitle_label = tk.Label(main_frame, text="Comprehensive Accessibility Assistant", 
                             font=("Arial", 12), bg="#222", fg="#fff")
    subtitle_label.pack(pady=(0, 20))
    
    # Welcome message
    welcome_text = ("Welcome! To access all features and sync across your devices,\n"
                   "please log in to your AccessMate account or create a new one.")
    welcome_label = tk.Label(main_frame, text=welcome_text, font=("Arial", 11), 
                            bg="#222", fg="#fff", wraplength=500, justify=tk.CENTER)
    welcome_label.pack(pady=(0, 30))
    
    # Buttons frame
    buttons_frame = tk.Frame(main_frame, bg="#222")
    buttons_frame.pack(pady=20)
    
    # Status label to show what was clicked
    status_label = tk.Label(main_frame, text="Click any button to test", 
                           font=("Arial", 10), bg="#222", fg="#FFD600")
    status_label.pack(pady=(20, 0))
    
    def on_login():
        status_label.config(text="✅ LOGIN button clicked!", fg="#4CAF50")
        print("LOGIN button clicked!")
    
    def on_register():
        status_label.config(text="✅ CREATE ACCOUNT button clicked!", fg="#2196F3")
        print("CREATE ACCOUNT button clicked!")
    
    def on_guest():
        status_label.config(text="✅ CONTINUE AS GUEST button clicked!", fg="#666")
        print("CONTINUE AS GUEST button clicked!")
    
    # Create highly visible buttons
    print("Creating test buttons...")
    
    # Login button (Green) - Most prominent
    login_btn = tk.Button(buttons_frame, text="🚪 Login", command=on_login,
                         font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", 
                         width=20, height=2, relief="raised", bd=3)
    login_btn.pack(pady=10, padx=10, fill="x")
    print("✅ Login button created")
    
    # Create Account button (Blue) - Equally prominent  
    register_btn = tk.Button(buttons_frame, text="👤 Create Account", command=on_register,
                           font=("Arial", 16, "bold"), bg="#2196F3", fg="white", 
                           width=20, height=2, relief="raised", bd=3)
    register_btn.pack(pady=10, padx=10, fill="x")
    print("✅ Create Account button created")
    
    # Continue as Guest button (Gray) - Secondary option
    guest_btn = tk.Button(buttons_frame, text="👻 Continue as Guest", command=on_guest,
                         font=("Arial", 14), bg="#666", fg="white", 
                         width=20, height=2, relief="raised", bd=3)
    guest_btn.pack(pady=10, padx=10, fill="x")
    print("✅ Continue as Guest button created")
    
    # Info text
    info_label = tk.Label(main_frame, text="(Guest mode has limited features)", 
                         font=("Arial", 9), bg="#222", fg="#888")
    info_label.pack(pady=(10, 0))
    
    print("\n🚀 Welcome popup test starting...")
    print("📋 You should see THREE buttons:")
    print("   1. 🚪 Login (Green)")
    print("   2. 👤 Create Account (Blue)")  
    print("   3. 👻 Continue as Guest (Gray)")
    print("\nClick any button to test functionality!")
    
    welcome_window.mainloop()

if __name__ == "__main__":
    direct_welcome_test()