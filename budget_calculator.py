#!/usr/bin/env python3
"""
GitHub Actions Budget Calculator for AccessMate
Helps estimate monthly costs and set appropriate spending limits
"""

def calculate_costs():
    print("💰 GitHub Actions Budget Calculator")
    print("=" * 50)
    print()
    
    # GitHub Actions pricing
    FREE_MINUTES = 2000  # Per month for private repos
    COST_PER_MINUTE = 0.008  # $0.008 per minute after free tier
    
    # AccessMate workflow costs
    workflows = {
        "🆓 Free Tier Build": 10,
        "Android APK Only": 8, 
        "Full Platform Build": 250,  # 5 platforms × 50 min avg
        "Complete Package": 375      # All platforms + extras
    }
    
    print("📊 AccessMate Workflow Costs:")
    for name, minutes in workflows.items():
        print(f"  • {name}: {minutes} minutes")
    print()
    
    # Get user input
    try:
        print("🤔 How many builds do you plan per month?")
        free_builds = int(input("  Free Tier Builds (10 min each): ") or "0")
        android_builds = int(input("  Android Only Builds (8 min each): ") or "0")  
        full_builds = int(input("  Full Platform Builds (250 min each): ") or "0")
        complete_builds = int(input("  Complete Package Builds (375 min each): ") or "0")
        
        # Calculate total usage
        total_minutes = (
            free_builds * workflows["🆓 Free Tier Build"] +
            android_builds * workflows["Android APK Only"] +
            full_builds * workflows["Full Platform Build"] +
            complete_builds * workflows["Complete Package"]
        )
        
        print(f"\n📈 Monthly Usage Estimate:")
        print(f"  Total minutes: {total_minutes}")
        print(f"  Free tier: {FREE_MINUTES} minutes")
        
        if total_minutes <= FREE_MINUTES:
            print(f"  ✅ Cost: $0 (within free tier)")
            overage = 0
            cost = 0
        else:
            overage = total_minutes - FREE_MINUTES
            cost = overage * COST_PER_MINUTE
            print(f"  ⚠️  Overage: {overage} minutes")
            print(f"  💰 Monthly cost: ${cost:.2f}")
        
        # Recommendations
        print(f"\n💡 Spending Limit Recommendations:")
        
        if cost == 0:
            print("  🎯 Suggested limit: $5-10 (safety buffer)")
            print("  📝 Reason: You're in free tier, but good to have buffer")
        elif cost <= 10:
            print(f"  🎯 Suggested limit: ${max(15, cost * 1.5):.0f}")
            print("  📝 Reason: 50% buffer for unexpected usage")
        elif cost <= 25:
            print(f"  🎯 Suggested limit: ${cost * 1.3:.0f}")
            print("  📝 Reason: 30% buffer for peak usage")
        else:
            print(f"  🎯 Suggested limit: ${cost * 1.2:.0f}")
            print("  📝 Consider making repository public for unlimited free minutes")
        
        print(f"\n🎯 Budget Alerts Setup:")
        suggested_limit = max(10, cost * 1.5) if cost > 0 else 10
        print(f"  50% alert: ${suggested_limit * 0.5:.1f}")
        print(f"  75% alert: ${suggested_limit * 0.75:.1f}")
        print(f"  90% alert: ${suggested_limit * 0.9:.1f}")
        
        # Alternative suggestions
        print(f"\n🔄 Cost Optimization Ideas:")
        if full_builds > 2:
            print("  • Use Free Tier builds for testing")
            print("  • Use Android-only builds for single platform testing")
        if total_minutes > FREE_MINUTES:
            print("  • Consider making repository public (unlimited free minutes)")
            print("  • Use local builds for development: python build_local.py")
        print("  • Only run full builds for releases")
        print("  • Batch multiple changes into single builds")
        
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Invalid input or cancelled")
        return
    
    print(f"\n🚀 Next Steps:")
    print("1. Go to: https://github.com/settings/billing")
    print("2. Set spending limit based on recommendation above")
    print("3. Add payment method")
    print("4. Enable usage alerts at 50%, 75%, 90%")
    print("5. Start with Free Tier builds to test")

def show_quick_estimates():
    """Show quick estimates for common usage patterns"""
    print("\n📋 Quick Cost Estimates:")
    print("=" * 30)
    
    scenarios = [
        ("Light Usage", "2 free tier + 1 full build", 2*10 + 1*250, 270),
        ("Medium Usage", "4 free tier + 2 full builds", 4*10 + 2*250, 540),
        ("Heavy Usage", "2 full + 1 complete build", 2*250 + 1*375, 875),
        ("Testing Only", "8 free tier builds", 8*10, 80),
        ("Android Focus", "4 android + 1 full build", 4*8 + 1*250, 282)
    ]
    
    FREE_MINUTES = 2000
    COST_PER_MINUTE = 0.008
    
    for name, description, minutes, _ in scenarios:
        if minutes <= FREE_MINUTES:
            cost = 0
            status = "FREE"
        else:
            overage = minutes - FREE_MINUTES
            cost = overage * COST_PER_MINUTE
            status = f"${cost:.2f}/month"
        
        print(f"  {name:12} | {description:25} | {minutes:4} min | {status}")

if __name__ == "__main__":
    calculate_costs()
    show_quick_estimates()