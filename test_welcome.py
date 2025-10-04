#!/usr/bin/env python3
"""Test script to check if welcome popup shows correctly"""

import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the welcome popup function
try:
    from main_desktop import show_welcome_popup
    
    print("Testing welcome popup...")
    result = show_welcome_popup()
    print(f"Welcome popup result: {result}")
    
except Exception as e:
    print(f"Error testing welcome popup: {e}")
    import traceback
    traceback.print_exc()