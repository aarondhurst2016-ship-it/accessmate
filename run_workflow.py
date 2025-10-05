#!/usr/bin/env python3
"""
GitHub Actions Workflow Dispatcher
Helps you choose and run workflows individually
"""

def show_workflows():
    """Display available workflows and their characteristics"""
    workflows = {
        "1": {
            "name": "🆓 Free Tier Build - Essential Only",
            "file": "build-free-tier.yml",
            "platforms": "Windows OR Linux (choose)",
            "time": "~10 minutes",
            "cost": "Low (10 minutes)",
            "best_for": "Testing after billing fix"
        },
        "2": {
            "name": "Build Android APK",
            "file": "android-build.yml", 
            "platforms": "Android only",
            "time": "~8 minutes",
            "cost": "Low (8 minutes)",
            "best_for": "Android testing/release"
        },
        "3": {
            "name": "Build All Platforms - Store Ready",
            "file": "build-clean-store.yml",
            "platforms": "Windows, Android, iOS, Linux, macOS",
            "time": "~50 minutes",
            "cost": "High (250 minutes)",
            "best_for": "Full store release"
        },
        "4": {
            "name": "🚀 Build All Platforms - Store Ready (Alt)",
            "file": "build-all-platforms-store.yml",
            "platforms": "All platforms + extras",
            "time": "~60 minutes", 
            "cost": "High (300 minutes)",
            "best_for": "Complete store package"
        },
        "5": {
            "name": "Build ALL Versions - Complete Package",
            "file": "build-complete-all-versions.yml",
            "platforms": "All platforms + GitHub releases",
            "time": "~75 minutes",
            "cost": "Maximum (375 minutes)",
            "best_for": "Full distribution release"
        },
        "0": {
            "name": "🏠 Local Build (No GitHub needed)",
            "file": "build_local.py",
            "platforms": "Current platform only",
            "time": "~5 minutes",
            "cost": "Free (0 minutes)",
            "best_for": "Immediate build, no billing issues"
        }
    }
    
    print("🎯 AccessMate Workflow Selection")
    print("=" * 50)
    print()
    
    for key, workflow in workflows.items():
        print(f"[{key}] {workflow['name']}")
        print(f"    Platforms: {workflow['platforms']}")
        print(f"    Time: {workflow['time']}")
        print(f"    Cost: {workflow['cost']}")
        print(f"    Best for: {workflow['best_for']}")
        print()
    
    return workflows

def get_github_actions_url():
    """Get the GitHub Actions URL for manual execution"""
    return "https://github.com/aarondhurst2016-ship-it/accessmate/actions"

def main():
    """Main workflow selection interface"""
    workflows = show_workflows()
    
    print("💡 How to Run:")
    print("=" * 30)
    print()
    print("🆓 Option 0 (Local - Works Now):")
    print("   python build_local.py")
    print()
    print("🌐 Options 1-5 (GitHub Actions):")
    print("   1. Go to:", get_github_actions_url())
    print("   2. Click on the workflow you want")
    print("   3. Click 'Run workflow'")
    print("   4. Select branch (main)")
    print("   5. Click 'Run workflow' button")
    print()
    print("⚠️  Note: GitHub Actions require billing to be fixed first")
    print("📖 See: GITHUB_BILLING_SOLUTIONS.md for billing help")
    print()
    
    choice = input("Enter choice (0-5) to get specific instructions, or press Enter to exit: ").strip()
    
    if choice == "0":
        print("\n🏠 Running Local Build...")
        import subprocess
        try:
            result = subprocess.run(["python", "build_local.py"], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
        except Exception as e:
            print(f"Error running local build: {e}")
            print("Try running manually: python build_local.py")
    
    elif choice in workflows and choice != "0":
        workflow = workflows[choice]
        print(f"\n🚀 Selected: {workflow['name']}")
        print(f"📁 File: {workflow['file']}")
        print(f"⏱️  Expected time: {workflow['time']}")
        print(f"💰 Cost: {workflow['cost']}")
        print()
        print("🌐 Next steps:")
        print(f"1. Open: {get_github_actions_url()}")
        print(f"2. Find: '{workflow['name']}'")
        print("3. Click 'Run workflow'")
        print("4. Confirm and run")
        print()
        print("⚠️  Make sure billing is fixed first!")
    
    elif choice:
        print("❌ Invalid choice. Please enter 0-5 or press Enter to exit.")

if __name__ == "__main__":
    main()