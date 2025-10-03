#!/usr/bin/env python3
"""
iOS version of AccessMate - Mobile-optimized accessibility assistant
"""

import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    # Import main components
    from gui import launch
    from battery_monitor import BatteryMonitor
    
    print("AccessMate iOS - Starting accessibility assistant...")
    
    # Initialize battery monitoring for mobile
    battery_monitor = BatteryMonitor()
    
    # Launch GUI (mobile-optimized)
    launch(None)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Running in basic mode...")
    
    # Basic iOS app if imports fail
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.title("AccessMate iOS")
    root.geometry("320x480")  # iPhone-like dimensions
    
    tk.Label(root, text="AccessMate", font=("Arial", 20, "bold")).pack(pady=20)
    tk.Label(root, text="Accessibility Assistant", font=("Arial", 14)).pack(pady=10)
    
    def show_info():
        messagebox.showinfo("AccessMate", "Mobile accessibility assistant running on iOS")
    
    tk.Button(root, text="About", command=show_info).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("AccessMate iOS version starting...")
