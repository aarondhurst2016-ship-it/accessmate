#!/usr/bin/env python3
"""
Test the conditional googletrans import functionality
"""
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_conditional_imports():
    """Test that the conditional imports work correctly"""
    print("Testing conditional googletrans imports...")
    print("=" * 50)
    
    try:
        # Test speech module
        from speech import translate_text, GOOGLETRANS_AVAILABLE
        print(f"✅ speech.py imported successfully")
        print(f"   GOOGLETRANS_AVAILABLE: {GOOGLETRANS_AVAILABLE}")
        
        # Test translation function
        result = translate_text("Hello", "en", "es")
        print(f"   translate_text('Hello', 'en', 'es') -> '{result}'")
        
    except Exception as e:
        print(f"❌ Error importing speech.py: {e}")
        return False
    
    try:
        # Test OCR screen reader module
        from ocr_screen_reader import OCRScreenReader
        print(f"✅ ocr_screen_reader.py imported successfully")
        
        # Create instance (don't actually run it)
        ocr = OCRScreenReader()
        print(f"   OCRScreenReader instance created successfully")
        
    except Exception as e:
        print(f"❌ Error importing ocr_screen_reader.py: {e}")
        return False
    
    print("\n🎉 All conditional import tests passed!")
    print("The application should now run even if googletrans is missing.")
    return True

if __name__ == "__main__":
    print("AccessMate Conditional Import Test")
    print("==================================")
    success = test_conditional_imports()
    
    if success:
        print("\n✅ TEST PASSED - Conditional imports working correctly")
    else:
        print("\n❌ TEST FAILED - Issues with conditional imports")
    
    input("\nPress Enter to exit...")