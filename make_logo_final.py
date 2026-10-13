import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ඔබේ පින්තූරය ඇති නියම නම හෝ ෆෝල්ඩර් එකේ ඇති ඕනෑම පින්තූරයක් සෙවීම
input_path = None
for f in os.listdir('.'):
    if f.lower().endswith(('.png', '.jpg', '.jpeg')) and f != 'new_logo.png':
        input_path = f
        break

# හමු නොවී නම් 'globe.jpg' ලෙස බල කිරීම
if not input_path and os.path.exists('globe.jpg'):
    input_path = 'globe.jpg'

print(f"Target Image Found: {input_path}")
output_path = 'new_logo.png'

if input_path and os.path.exists(input_path):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    
    img = img.crop(((w - side)//2, (h - side)//2, (w + side)//2, (h + side)//2))

    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + img.size, fill=255)
    
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    
    logo_size = 120
    final_img = output.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    gloss = Image.new('RGBA', final_img.size, (255, 255, 255, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.ellipse((logo_size // 4, -logo_size // 2, logo_size * 3 // 4, logo_size // 2), fill=(255, 255, 255, 190))
    gloss = gloss.filter(ImageFilter.GaussianBlur(3))
    final_img = Image.alpha_composite(final_img, gloss)
    
    draw = ImageDraw.Draw(final_img)
    try:
        font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 65)
    except:
        font = ImageFont.load_default()

    text = "f"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (logo_size - tw) // 2 - bbox[0]
    y = (logo_size - th) // 2 - bbox[1]
    
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            draw.text((x+dx, y+dy), text, font=font, fill=(0, 0, 0, 110))
            
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    final_img.save(output_path, format='PNG')
    print("SUCCESS: Logo created successfully!")
else:
    print("ERROR: Please put your globe image into this folder!")
