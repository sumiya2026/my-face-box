import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ඔබගේ නව ලෝක ගෝල පින්තූරයේ නම මෙහි දමමු (උදාහරණයක් ලෙස පහත නම් වලින් එකක් විය හැක)
possible_names = ['Screenshot_20260914-161703_Google.jpg', 'image_2.png', 'globe.png', 'globe_source.png']
input_path = ''

for name in possible_names:
    if os.path.exists(name):
        input_path = name
        break

# ඔබ මේ මොහොතේ පින්තූරය ඩවුන්ලෝඩ් කර ඇති නිවැරදි නම ඇතුළත් කිරීමට:
if not input_path:
    # ෆෝල්ඩර් එකේ ඇති සියලුම jpg/png පස්සේ පරීක්ෂා කර බැලීම
    for f in os.listdir('.'):
        if f.endswith(('.png', '.jpg', '.jpeg')) and 'Screenshot' in f:
            input_path = f
            break

print(f"Using source image: {input_path}")

output_path = 'new_logo.png'

if input_path and os.path.exists(input_path):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    
    # රූපය මධ්‍යයෙන් වෘත්තාකාරව කපා ගැනීම
    img = img.crop(((w - side)//2, (h - side)//2, (w + side)//2, (h + side)//2))

    # වෘත්තාකාර මාස්ක් එකක් සකස් කිරීම
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + img.size, fill=255)
    
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    
    # ලෝගෝ එකට ගැළපෙන ප්‍රමාණය (120x120 pixels)
    logo_size = 120
    final_img = output.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # වීදුරු බෝල දිලිසෙන ආචරණය (Glass Gloss Effect) එකතු කිරීම
    gloss = Image.new('RGBA', final_img.size, (255, 255, 255, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.ellipse((logo_size // 4, -logo_size // 2, logo_size * 3 // 4, logo_size // 2), fill=(255, 255, 255, 190))
    gloss = gloss.filter(ImageFilter.GaussianBlur(3))
    final_img = Image.alpha_composite(final_img, gloss)
    
    # මැද සුදු පාටින් 'f' අකුර ලිවීම
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
    
    # අකුර පැහැදිලිව පෙනීමට කළු පාටින් සිහින් සෙවනැල්ලක් (shadow) යෙදීම
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            draw.text((x+dx, y+dy), text, font=font, fill=(0, 0, 0, 110))
            
    # ප්‍රධාන සුදු අකුර ඇඳීම
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # අවසාන ලෝගෝව සේව් කිරීම
    final_img.save(output_path, format='PNG')
    print("SUCCESS: Glass Earth Globe Logo with 'f' created successfully!")
else:
    print("ERROR: Source globe image not found! Please check file name.")
