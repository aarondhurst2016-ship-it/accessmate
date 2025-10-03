from PIL import Image

# Convert PNG logo to ICO for Windows app icon
img = Image.open(r'C:\Users\aaron\Talkback app\src\accessmate_logo_uploaded.png')
# ICO best practices: 256x256, 128x128, 64x64, 32x32, 16x16
sizes = [(256,256), (128,128), (64,64), (32,32), (16,16)]
img.save(r'C:\Users\aaron\Talkback app\src\accessmate_logo.ico', format='ICO', sizes=sizes)
print('ICO file created: src/accessmate_logo.ico')
