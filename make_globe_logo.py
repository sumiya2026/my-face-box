import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

output_path = 'new_logo.png'
logo_size = 120

# නිල් පැහැති මුහුදක් සහ කොළ පැහැති මහද්වීප සහිත ලෝක ගෝලයක් ස්වයංක්‍රීයව නිර්මාණය කිරීම
img = Image.new('RGBA', (logo_size, logo_size), (30, 144, 255, 255))
draw = ImageDraw.Draw(img)

# මහද්වීප හැඩය (Abstract continents) ඇඳීම
draw.ellipse((20, 10, 80, 70), fill=(46, 139, 87, 255))
draw.ellipse((60, 50, 110, 110), fill=(46, 139, 87, 255))
draw.ellipse((10, 60, 50, 100), fill=(46, 139, 87, 255))

# වෘත්තාකාර මාස්ක් එකක් මඟින් පරිපූර්ණ ගෝලයකට කපා ගැනීම
mask = Image.new('L', (logo_size, logo_size), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((0, 0, logo_size, logo_size), fill=255)

output = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
output.paste(img, (0, 0), mask)

# වීදුරු බෝල දිලිසෙන ආචරණය (Glass Gloss Effect)
gloss = Image.new('RGBA', output.size, (255, 255, 255, 0))
g_draw = ImageDraw.Draw(gloss)
g_draw.ellipse((logo_size // 4, -logo_size // 2, logo_size * 3 // 4, logo_size // 2), fill=(255, 255, 255, 200))
gloss = gloss.filter(ImageFilter.GaussianBlur(3))
final_img = Image.alpha_composite(output, gloss)

# මැද සුදු පාටින් 'f' අකුර යෙදීම
text_draw = ImageDraw.Draw(final_img)
try:
    font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 65)
except:
    font = ImageFont.load_default()

text = "f"
bbox = text_draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (logo_size - tw) // 2 - bbox[0]
y = (logo_size - th) // 2 - bbox[1]

for dx in range(-2, 3):
    for dy in range(-2, 3):
        text_draw.text((x+dx, y+dy), text, font=font, fill=(0, 0, 0, 120))
        
text_draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

final_img.save(output_path, format='PNG')
print("SUCCESS: Embedded Globe Logo created successfully!")
