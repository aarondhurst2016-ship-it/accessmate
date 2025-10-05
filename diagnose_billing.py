#!/usr/bin/env python3
"""
GitHub Account Diagnostic Tool
Helps identify why spending limit section is not showing
"""

import webbrowser
import time

def open_multiple_billing_pages():
    """Open different billing pages to check account type"""
    pages = [
        ("Main Billing", "https://github.com/settings/billing"),
        ("Payment Methods", "https://github.com/settings/billing/payment_information"), 
        ("Usage & Billing", "https://github.com/settings/billing/usage")
    ]
    
    print("🔍 Opening GitHub billing pages to diagnose issue...")
    print("Check each page to see what sections are visible:")
    print()
    
    for name, url in pages:
        print(f"Opening: {name}")
        webbrowser.open(url)
        time.sleep(2)

def show_diagnostic_checklist():
    """Show what to look for on billing pages"""
    print("📋 Diagnostic Checklist")
    print("=" * 25)
    print()
    
    print("🎯 On the billing page, look for:")
    print("  □ 'Spending limit' section")
    print("  □ 'Current plan' (Free/Pro/Team)")  
    print("  □ 'Payment information' section")
    print("  □ 'Actions & Packages' usage")
    print("  □ Account type indicator")
    print()
    
    print("❌ Common Issues:")
    print("  • Organization account (not personal)")
    print("  • No payment method added yet")
    print("  • Account verification required")
    print("  • Browser cache issues")
    print()
    
    print("✅ What Should Work:")
    print("  • Personal account with payment method")
    print("  • Should show spending limit controls")
    print("  • Can set limit between $0-unlimited")

def show_quick_fixes():
    """Show quick fixes to try"""
    print("🚀 Quick Fixes to Try:")
    print("=" * 25)
    print()
    
    print("1. **Add Payment Method First:**")
    print("   - Spending limit may only appear after adding card")
    print("   - Go to Payment Information section")
    print("   - Add valid credit/debit card")
    print()
    
    print("2. **Check Account Type:**")
    print("   - Look for 'Personal' vs 'Organization' indicator")
    print("   - Organizations have different billing controls")
    print()
    
    print("3. **Browser Issues:**")
    print("   - Hard refresh: Ctrl+F5")
    print("   - Try different browser")
    print("   - Clear cache and cookies")
    print()
    
    print("4. **Test Workflow Anyway:**")
    print("   - Some public repos work without spending limit")
    print("   - Try running test workflow")

def main():
    """Main diagnostic interface"""
    print("🔧 GitHub Spending Limit Diagnostic Tool")
    print("=" * 45)
    print()
    
    print("Issue: Spending limit section not showing on billing page")
    print("This tool will help identify and fix the problem.")
    print()
    
    choice = input("Choose: (o)pen billing pages, (c)hecklist, (f)ixes, or Enter for all: ").strip().lower()
    
    if choice == 'o':
        open_multiple_billing_pages()
    elif choice == 'c':
        show_diagnostic_checklist()
    elif choice == 'f':
        show_quick_fixes()
    else:
        show_diagnostic_checklist()
        print()
        show_quick_fixes()
        print()
        input("Press Enter to open billing pages...")
        open_multiple_billing_pages()
    
    print()
    print("🧪 After checking billing pages:")
    print("Try running: '🧪 Test Public Repository - Free Actions' workflow")
    print("It might work even without spending limit setup!")

if __name__ == "__main__":
    main()