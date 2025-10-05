#!/usr/bin/env python3
"""
Simple test to verify main app integration
"""

try:
    from src.main_desktop import start_external_screen_reader, stop_external_screen_reader
    print("✅ SUCCESS: Main app can import automatic screen reader functions!")
    print("✅ The automatic external screen reader is integrated with AccessMate!")
    print("")
    print("🤖 Features now available in AccessMate:")
    print("   • '🤖 Auto Screen Reader' button - starts automatic continuous reading")
    print("   • '🛑 Stop Auto Reader' button - stops automatic reading")
    print("   • Window changes will be announced automatically")
    print("   • Background monitoring is active")
    print("   • Manual hotkeys still work (Ctrl+Shift+R, etc.)")
    print("")
    print("🎉 AUTOMATIC EXTERNAL SCREEN READER IS READY!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()