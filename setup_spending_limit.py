#!/usr/bin/env python3
"""
GitHub Spending Limit Setup Verification
Helps confirm your billing settings are correct for unlimited Actions
"""

import webbrowser
import time

def open_billing_settings():
    """Open GitHub billing settings in browser"""
    print("🔧 Opening GitHub Billing Settings...")
    webbrowser.open("https://github.com/settings/billing/spending_limit")
    time.sleep(2)

def show_setup_steps():
    """Show step-by-step spending limit setup"""
    print("💰 GitHub Spending Limit Setup")
    print("=" * 40)
    print()
    
    print("🎯 Recommended Settings for AccessMate:")
    print("  • Spending Limit: $15.00")
    print("  • Alert at 75%: $11.25") 
    print("  • Alert at 90%: $13.50")
    print("  • Payment Method: Valid credit/debit card")
    print()
    
    print("📋 Step-by-Step Instructions:")
    print("1. Find 'Spending limit' section on billing page")
    print("2. Click 'Update limit' button")
    print("3. Enter: 15.00")
    print("4. Set alerts: 75% and 90%")
    print("5. Add payment method if needed")
    print("6. Click 'Update spending limit'")
    print("7. Wait 5-10 minutes for changes")
    print()
    
    print("✅ Expected Result:")
    print("  • Public repo = $0 actual cost")
    print("  • Spending limit prevents surprises")
    print("  • GitHub Actions work immediately")
    print()

def verify_setup():
    """Help user verify the setup worked"""
    print("🧪 Verification Steps:")
    print("=" * 25)
    print()
    
    print("After setting spending limit:")
    print("1. Wait 5-10 minutes")
    print("2. Go to: https://github.com/aarondhurst2016-ship-it/accessmate/actions")
    print("3. Click: '🧪 Test Public Repository - Free Actions'")
    print("4. Click: 'Run workflow'")
    print("5. Should work without billing errors!")
    print()
    
    print("🚨 If still getting billing errors:")
    print("  • Check payment method is valid")
    print("  • Verify spending limit > $0")
    print("  • Wait up to 24 hours for GitHub sync")
    print("  • Contact GitHub Support if needed")

def main():
    """Main setup assistant"""
    print("🚀 GitHub Actions Spending Limit Setup")
    print("=" * 45)
    print()
    
    print("Your public repository should have unlimited free Actions,")
    print("but GitHub requires a spending limit > $0 due to previous billing issues.")
    print()
    
    choice = input("Press Enter to open billing settings, or 'v' for verification steps: ").strip().lower()
    
    if choice == 'v':
        verify_setup()
    else:
        show_setup_steps()
        input("\nPress Enter to open GitHub billing settings...")
        open_billing_settings()
        print()
        print("✅ Follow the steps above in the browser window.")
        print("🧪 Then test with the verification workflow!")

if __name__ == "__main__":
    main()