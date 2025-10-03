#!/usr/bin/env python3
"""
Create mobile icons from the main logo for Android and iOS platforms
"""

from PIL import Image
import os

def create_android_icons():
    """Create Android icons in various densities"""
    # Load the main logo
    logo_path = os.path.join("src", "accessmate_logo.png")
    
    if not os.path.exists(logo_path):
        print(f"Logo file not found: {logo_path}")
        return False
    
    try:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")
        
        # Android icon sizes (in pixels)
        android_sizes = {
            "mdpi": 48,      # ~160dpi
            "hdpi": 72,      # ~240dpi  
            "xhdpi": 96,     # ~320dpi
            "xxhdpi": 144,   # ~480dpi
            "xxxhdpi": 192   # ~640dpi
        }
        
        # Create android icons directory
        android_dir = "android_icons"
        os.makedirs(android_dir, exist_ok=True)
        
        for density, size in android_sizes.items():
            # Create directory for this density
            density_dir = os.path.join(android_dir, f"mipmap-{density}")
            os.makedirs(density_dir, exist_ok=True)
            
            # Resize and save
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            icon_path = os.path.join(density_dir, "ic_launcher.png")
            resized.save(icon_path, "PNG")
            print(f"Created Android icon: {icon_path} ({size}x{size})")
        
        # Create a larger icon for Play Store (512x512)
        playstore_dir = os.path.join(android_dir, "playstore")
        os.makedirs(playstore_dir, exist_ok=True)
        playstore = logo.resize((512, 512), Image.Resampling.LANCZOS)
        playstore_path = os.path.join(playstore_dir, "ic_launcher.png")
        playstore.save(playstore_path, "PNG")
        print(f"Created Play Store icon: {playstore_path} (512x512)")
        
        return True
        
    except Exception as e:
        print(f"Error creating Android icons: {e}")
        return False

def create_ios_icons():
    """Create iOS icons in various sizes"""
    logo_path = os.path.join("src", "accessmate_logo.png")
    
    if not os.path.exists(logo_path):
        print(f"Logo file not found: {logo_path}")
        return False
    
    try:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")
        
        # iOS icon sizes (in pixels)
        ios_sizes = {
            "Icon-20x20@1x": 20,
            "Icon-20x20@2x": 40,  
            "Icon-20x20@3x": 60,
            "Icon-29x29@1x": 29,
            "Icon-29x29@2x": 58,
            "Icon-29x29@3x": 87,
            "Icon-40x40@1x": 40,
            "Icon-40x40@2x": 80,
            "Icon-40x40@3x": 120,
            "Icon-60x60@2x": 120,
            "Icon-60x60@3x": 180,
            "Icon-76x76@1x": 76,
            "Icon-76x76@2x": 152,
            "Icon-83.5x83.5@2x": 167,
            "Icon-1024x1024@1x": 1024
        }
        
        # Create iOS icons directory
        ios_dir = "ios_icons"
        os.makedirs(ios_dir, exist_ok=True)
        
        for name, size in ios_sizes.items():
            # Resize and save
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            icon_path = os.path.join(ios_dir, f"{name}.png")
            resized.save(icon_path, "PNG")
            print(f"Created iOS icon: {icon_path} ({size}x{size})")
        
        return True
        
    except Exception as e:
        print(f"Error creating iOS icons: {e}")
        return False

def create_windows_icon():
    """Create Windows ICO file with multiple sizes"""
    logo_path = os.path.join("src", "accessmate_logo.png")
    
    if not os.path.exists(logo_path):
        print(f"Logo file not found: {logo_path}")
        return False
    
    try:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")
        
        # Windows icon sizes
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Create multiple size images
        images = []
        for size in sizes:
            images.append(logo.resize(size, Image.Resampling.LANCZOS))
        
        # Save as ICO with multiple sizes
        ico_path = os.path.join("src", "accessmate_logo_multisize.ico")
        images[0].save(ico_path, format='ICO', sizes=sizes)
        print(f"Created Windows multi-size icon: {ico_path}")
        
        return True
        
    except Exception as e:
        print(f"Error creating Windows icon: {e}")
        return False

def main():
    print("Creating mobile and desktop icons from AccessMate logo...")
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow (PIL) is required. Install with: pip install Pillow")
        return
    
    success = True
    
    print("\n--- Creating Android Icons ---")
    if not create_android_icons():
        success = False
    
    print("\n--- Creating iOS Icons ---")  
    if not create_ios_icons():
        success = False
    
    print("\n--- Creating Windows Icon ---")
    if not create_windows_icon():
        success = False
    
    if success:
        print("\n✅ All icons created successfully!")
        print("\nNext steps:")
        print("1. Copy android icons to your Android project res/mipmap-* directories")
        print("2. Copy iOS icons to your iOS project Images.xcassets/AppIcon.appiconset/")
        print("3. Use accessmate_logo_multisize.ico for Windows builds")
    else:
        print("\n❌ Some icons failed to create. Check errors above.")

if __name__ == "__main__":
    main()