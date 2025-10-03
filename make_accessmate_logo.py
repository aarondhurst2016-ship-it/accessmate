from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple blue/white logo with 'AM' for AccessMate
size = (256, 256)
background = (33, 150, 243)  # Blue
text_color = (255, 255, 255)
text = "AM"

img = Image.new("RGB", size, background)
draw = ImageDraw.Draw(img)


# Try to use a bold font, fallback to default
try:
    font = ImageFont.truetype("arialbd.ttf", 140)
except Exception:
    font = ImageFont.load_default()

# Use getbbox for text size (Pillow 8.0+)
try:
    bbox = font.getbbox(text)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
except Exception:
    w, h = font.getsize(text)

draw.text(((size[0]-w)//2, (size[1]-h)//2), text, fill=text_color, font=font)

# Save PNG
png_path = os.path.join('src', 'accessmate_logo.png')
img.save(png_path)

# Save ICO (multiple sizes)
ico_path = os.path.join('src', 'accessmate_logo.ico')
img.save(ico_path, format='ICO', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])

print(f"AccessMate logo PNG saved to {png_path}")
print(f"AccessMate logo ICO saved to {ico_path}")
