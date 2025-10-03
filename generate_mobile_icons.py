from PIL import Image
import os

# Source logo
src_logo = r'C:\Users\aaron\Talkback app\src\talkback_logo.png'

# Android icon sizes (in pixels)
android_sizes = [48, 72, 96, 144, 192, 512]
android_folders = [
    'mipmap-mdpi', 'mipmap-hdpi', 'mipmap-xhdpi', 'mipmap-xxhdpi', 'mipmap-xxxhdpi', 'playstore'
]

# iOS icon sizes (in pixels)
ios_sizes = [20, 29, 40, 60, 76, 83, 1024]
ios_scales = [1, 2, 3]

# Output folders
android_res = r'C:\Users\aaron\Talkback app\mobile_icons\android'
ios_res = r'C:\Users\aaron\Talkback app\mobile_icons\ios'
os.makedirs(android_res, exist_ok=True)
os.makedirs(ios_res, exist_ok=True)

img = Image.open(src_logo)

# Android icons
for size, folder in zip(android_sizes, android_folders):
    out_dir = os.path.join(android_res, folder)
    os.makedirs(out_dir, exist_ok=True)
    icon = img.resize((size, size), Image.LANCZOS)
    icon.save(os.path.join(out_dir, 'ic_launcher.png'))

# iOS icons
for size in ios_sizes:
    for scale in ios_scales:
        icon_size = size * scale
        icon = img.resize((icon_size, icon_size), Image.LANCZOS)
        name = f'Icon-{size}x{size}@{scale}x.png'
        icon.save(os.path.join(ios_res, name))

print('Mobile icon PNGs generated in mobile_icons/android and mobile_icons/ios')
