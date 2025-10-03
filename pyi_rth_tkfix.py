import os
import sys

# Fix Tcl/Tk library paths for PyInstaller
if hasattr(sys, '_MEIPASS'):
    # We're running in a PyInstaller bundle
    bundle_dir = sys._MEIPASS
    
    # Try multiple possible locations for Tcl/Tk
    tcl_paths = [
        os.path.join(bundle_dir, 'tcl'),
        os.path.join(bundle_dir, 'tcl8.6'),
        os.path.join(bundle_dir, '_tcl_data'),
        os.path.join(bundle_dir, 'lib', 'tcl8.6')
    ]
    
    tk_paths = [
        os.path.join(bundle_dir, 'tk'),
        os.path.join(bundle_dir, 'tk8.6'),
        os.path.join(bundle_dir, '_tk_data'),
        os.path.join(bundle_dir, 'lib', 'tk8.6')
    ]
    
    # Set TCL_LIBRARY
    for tcl_path in tcl_paths:
        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
            break
    
    # Set TK_LIBRARY
    for tk_path in tk_paths:
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path
            break