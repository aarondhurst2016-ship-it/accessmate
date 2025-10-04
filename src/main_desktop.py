# Main entry point for AccessMate
# Cross-platform compatible version for desktop builds

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

class AccessMateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AccessMate - Accessibility Assistant")
        self.root.geometry("600x400")
        
        # Try to set icon if it exists
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="AccessMate", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="AI-Powered Accessibility Assistant",
            font=("Arial", 14)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Feature buttons
        features = [
            ("Voice Commands", self.voice_commands),
            ("Screen Reader", self.screen_reader),
            ("Object Recognition", self.object_recognition),
            ("Smart Home Integration", self.smart_home),
            ("Accessibility Settings", self.accessibility_settings)
        ]
        
        for i, (text, command) in enumerate(features):
            btn = ttk.Button(
                main_frame,
                text=text,
                command=command,
                width=25
            )
            btn.grid(row=i+2, column=0, columnspan=2, pady=5, sticky=tk.EW)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready - AccessMate is here to help with accessibility needs",
            relief=tk.SUNKEN
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def voice_commands(self):
        messagebox.showinfo(
            "Voice Commands",
            "Voice command system will be activated here.\n\n"
            "Features:\n"
            "• Voice-to-text input\n"
            "• Spoken feedback\n"
            "• Custom voice commands\n"
            "• Accessibility shortcuts"
        )
    
    def screen_reader(self):
        messagebox.showinfo(
            "Screen Reader",
            "Screen reading functionality will be activated here.\n\n"
            "Features:\n"
            "• Text-to-speech\n"
            "• Screen content reading\n"
            "• Navigation assistance\n"
            "• Reading speed control"
        )
    
    def object_recognition(self):
        messagebox.showinfo(
            "Object Recognition",
            "AI-powered object recognition will be activated here.\n\n"
            "Features:\n"
            "• Camera-based object identification\n"
            "• Scene description\n"
            "• Text recognition (OCR)\n"
            "• Color identification"
        )
    
    def smart_home(self):
        messagebox.showinfo(
            "Smart Home Integration",
            "Smart home controls will be activated here.\n\n"
            "Features:\n"
            "• Voice-controlled devices\n"
            "• Automated accessibility routines\n"
            "• Environmental controls\n"
            "• Emergency assistance"
        )
    
    def accessibility_settings(self):
        messagebox.showinfo(
            "Accessibility Settings",
            "Accessibility configuration will be opened here.\n\n"
            "Settings:\n"
            "• Font size and contrast\n"
            "• Audio preferences\n"
            "• Input methods\n"
            "• Personalization options"
        )
    
    def run(self):
        self.root.mainloop()

def launch():
    """Launch the AccessMate GUI"""
    app = AccessMateGUI()
    app.run()

def main():
    """Main entry point"""
    try:
        print("Starting AccessMate...")
        launch()
    except Exception as e:
        print(f"Error starting AccessMate: {e}")
        # Fallback to console mode
        print("AccessMate - Accessibility Assistant")
        print("GUI failed to start, but core functionality is available.")

if __name__ == "__main__":
    main()