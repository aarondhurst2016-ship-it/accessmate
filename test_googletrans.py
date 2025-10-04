#!/usr/bin/env python3
"""
Test script to verify googletrans functionality
"""

def test_googletrans():
    """Test if googletrans can be imported and used"""
    try:
        from googletrans import Translator
        print("✅ Successfully imported googletrans")
        
        translator = Translator()
        print("✅ Successfully created Translator instance")
        
        # Test translation
        result = translator.translate("Hello", src='en', dest='es')
        print(f"✅ Translation test: 'Hello' -> '{result.text}'")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        return False

if __name__ == "__main__":
    print("Testing googletrans functionality...")
    print("=" * 40)
    
    success = test_googletrans()
    
    if success:
        print("\n🎉 All googletrans tests passed!")
    else:
        print("\n💥 googletrans tests failed!")
    
    input("\nPress Enter to exit...")