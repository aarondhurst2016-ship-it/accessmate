#!/usr/bin/env python3
"""
GitHub Actions Usage Calculator
Helps estimate your monthly usage and costs
"""

def calculate_usage():
    print("🔍 GitHub Actions Usage Calculator")
    print("=" * 40)
    
    # Current workflow analysis
    workflows = {
        "build-all-platforms-store.yml": {"jobs": 5, "avg_minutes": 12},
        "build-clean-store.yml": {"jobs": 5, "avg_minutes": 10},
        "build-complete-all-versions.yml": {"jobs": 5, "avg_minutes": 15},
        "android-build.yml": {"jobs": 1, "avg_minutes": 8}
    }
    
    print("📊 Current Workflow Analysis:")
    total_minutes_per_run = 0
    
    for workflow, data in workflows.items():
        minutes = data["jobs"] * data["avg_minutes"]
        total_minutes_per_run += minutes
        print(f"  • {workflow}: {data['jobs']} jobs × {data['avg_minutes']} min = {minutes} minutes")
    
    print(f"\n📈 Total per full run: {total_minutes_per_run} minutes")
    
    # Monthly projections
    print(f"\n📅 Monthly Projections:")
    free_limit = 2000  # Free tier limit
    
    max_runs_free = free_limit // total_minutes_per_run
    print(f"  • Free tier (2,000 min): {max_runs_free} full runs/month")
    print(f"  • Pro tier (3,000 min): {3000 // total_minutes_per_run} full runs/month")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if max_runs_free < 10:
        print("  ⚠️  Consider making repository public (unlimited free minutes)")
        print("  ⚠️  Or upgrade to Pro ($4/month) for more minutes")
    else:
        print("  ✅ Free tier should be sufficient for normal usage")
    
    print(f"\n🎯 Optimization Tips:")
    print("  • Use build-free-tier.yml (saves ~50% minutes)")
    print("  • Build only when src/ files change")
    print("  • Make repository public if possible")
    print("  • Use matrix builds for efficiency")

if __name__ == "__main__":
    calculate_usage()