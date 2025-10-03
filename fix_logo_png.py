from PIL import Image

# Load the possibly problematic PNG
img = Image.open(r'C:\Users\aaron\Talkback app\src\talkback_logo.png')

# Convert to RGB (removes alpha and color profiles)
img = img.convert('RGB')

# Save as a new, clean PNG (overwrite original)
img.save('src/talkback_logo.png', format='PNG')

print('Logo re-saved as standard PNG.')
