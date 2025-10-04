#!/usr/bin/env python3
"""Test script to verify license key button visibility logic"""

import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_license_button_visibility():
    """Test whether license buttons appear based on purchase status"""
    
    try:
        from gui import backend_check_purchased, backend_check_license_key_activated
        
        # Test with demo email (no purchase)
        demo_email = "demo@accessmate.com"
        has_purchase = backend_check_purchased(demo_email)
        has_license = backend_check_license_key_activated(demo_email)
        user_has_full_version = has_purchase or has_license
        
        print(f"Testing user: {demo_email}")
        print(f"Has purchase: {has_purchase}")
        print(f"Has activated license: {has_license}")
        print(f"User has full version: {user_has_full_version}")
        print(f"License buttons should be {'HIDDEN' if user_has_full_version else 'VISIBLE'}")
        
        # Test with a user who might have an activated license
        test_emails = [
            "demo@accessmate.com",
            "main_app@accessmate.com", 
            "mobile_main_app@accessmate.com",
            "test@accessmate.com"
        ]
        
        print("\n--- Testing multiple users ---")
        for email in test_emails:
            has_purchase = backend_check_purchased(email)
            has_license = backend_check_license_key_activated(email)
            user_has_full_version = has_purchase or has_license
            status = "HIDDEN" if user_has_full_version else "VISIBLE"
            print(f"{email}: Buttons {status} (Purchase: {has_purchase}, License: {has_license})")
            
    except Exception as e:
        print(f"Error testing license visibility: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_license_button_visibility()