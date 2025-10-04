#!/usr/bin/env python3
"""
Create a better Windows .ico file from PNG
"""

from PIL import Image
import os

def create_better_ico():
    # Load the PNG logo
    png_path = os.path.join("src", "accessmate_logo.png")
    if not os.path.exists(png_path):
        print(f"PNG not found: {png_path}")
        return
    
    try:
        # Load original image
        img = Image.open(png_path)
        print(f"Original image size: {img.size}")
        
        # Create different sizes for Windows
        sizes = [(16, 16), (20, 20), (24, 24), (32, 32), (40, 40), (48, 48), (64, 64), (96, 96), (128, 128), (256, 256)]
        
        # Create all sizes
        icons = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icons.append(resized)
            print(f"Created {size[0]}x{size[1]} icon")
        
        # Save as .ico with multiple sizes
        output_path = os.path.join("src", "accessmate_logo_windows.ico")
        icons[0].save(output_path, format='ICO', sizes=[(icon.width, icon.height) for icon in icons])
        
        print(f"✓ Created Windows-compatible .ico file: {output_path}")
        
        # Get file size
        file_size = os.path.getsize(output_path)
        print(f"File size: {file_size} bytes")
        
    except Exception as e:
        print(f"Error creating .ico file: {e}")

if __name__ == "__main__":
    create_better_ico()