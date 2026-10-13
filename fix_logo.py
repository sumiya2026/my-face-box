import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

input_path = 'image_2.png'  # <--- මෙහි නම නිවැරදිදැයි පරීක්ෂා කරන්න
output_path = 'new_logo.png'

if os.path.exists(input_path):
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

    # Gloss Effect
    gloss = Image.new('RGBA', final_img.size, (255, 255, 255, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.ellipse((logo_size // 4, -logo_size // 2, logo_size * 3 // 4, logo_size // 2), fill=(255, 255, 255, 180))
    gloss = gloss.filter(ImageFilter.GaussianBlur(3))
    final_img = Image.alpha_composite(final_img, gloss)
    
    # Draw 'f' letter
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
            draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0,100))
    draw.text((x, y), text, font=font, fill=(255,255,255,255))
    
    final_img.save(output_path, format='PNG')
    print("Glass Globe Logo generated successfully!")
else:
    print(f"Error: {input_path} not found! Please check file name.")
