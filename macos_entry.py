#!/usr/bin/env python3
"""
macOS Entry Point for AccessMate
Enhanced version that handles macOS-specific initialization and launches the main GUI
"""

import sys
import os
import platform

def setup_macos_environment():
    """Set up macOS-specific environment variables and paths"""
    
    # Add src directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # macOS-specific Tcl/Tk environment setup
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        bundle_dir = sys._MEIPASS
        
        # Set Tcl/Tk library paths for macOS
        tcl_paths = [
            os.path.join(bundle_dir, 'tcl'),
            os.path.join(bundle_dir, 'tcl8.6'),
            '/usr/local/lib/tcl8.6',
            '/opt/homebrew/lib/tcl8.6',
            '/System/Library/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts'
        ]
        
        tk_paths = [
            os.path.join(bundle_dir, 'tk'),
            os.path.join(bundle_dir, 'tk8.6'),
            '/usr/local/lib/tk8.6',
            '/opt/homebrew/lib/tk8.6',
            '/System/Library/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts'
        ]
        
        # Find and set the first existing path
        for tcl_path in tcl_paths:
            if os.path.exists(tcl_path):
                os.environ['TCL_LIBRARY'] = tcl_path
                break
                
        for tk_path in tk_paths:
            if os.path.exists(tk_path):
                os.environ['TK_LIBRARY'] = tk_path
                break
    
    # Set macOS-specific environment variables
    os.environ['LANG'] = os.environ.get('LANG', 'en_US.UTF-8')
    os.environ['LC_ALL'] = os.environ.get('LC_ALL', 'en_US.UTF-8')


class MacOSGUIInstance:
    """Dummy GUI instance for compatibility with gui.launch()"""
    def __init__(self):
        self.platform = "macOS"
        self.version = platform.mac_ver()[0]


def main():
    """Main entry point for macOS"""
    
    print("[macOS] Starting AccessMate for macOS...")
    
    try:
        # Set up macOS environment
        setup_macos_environment()
        
        # Import the main GUI module
        import gui
        
        # Create a GUI instance for compatibility
        gui_instance = MacOSGUIInstance()
        
        # Launch the main application
        print("✅ Launching AccessMate GUI...")
        gui.launch(gui_instance)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required modules are installed:")
        print("  pip3 install -r requirements.txt")
        print("  pip3 install -r requirements-macos.txt")
        return 1
        
    except Exception as e:
        print(f"❌ Error launching AccessMate: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())