import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 🎨 නමට 3D, ඩාර්ක් බ්ලූ සහ වීදුරු ෆිනිෂ් (3D Glass Finish) ලබා දෙන උසස් CSS මෝස්තරය
    dark_3d_glass_style = """
    <style>
        .app-header h1, .app-title {
            color: #ffffff !important; /* කැපී පෙනෙන තනි සුදු අකුරු */
            font-size: 50px !important;
            font-weight: bold !important;
            letter-spacing: 2px !important;
            
            /* 💙 ලෝගෝ එකේ පාටම ඇති 3D සහ වීදුරු පසුබිම (Glass Container) */
            
            padding: 15px 35px !important;
            border-radius: 20px !important;
            display: inline-block !important;
            
            /* ✨ 3D සහ වීදුරු පෙනුම ලබාදෙන Shadows */
            box-shadow: 
                inset 0 3px 5px rgba(255, 255, 255, 0.4), 
                inset 0 -3px 5px rgba(0, 0, 0, 0.5),
                0 8px 16px rgba(0, 0, 0, 0.2) !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(8px) !important;
            
            /* 📝 අකුරු වලට 3D පෙනුමක් දෙන Shadow එක */
            text-shadow: 2px 4px 6px rgba(0, 0, 0, 0.5) !important;
        }
    </style>
    """
    
    # Style එක head එකට දැමීම
    if "</head>" in c:
        c = c.replace("</head>", dark_3d_glass_style + "\n</head>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] Title Updated with 3D Dark Blue Glass Finish Successfully!")
else:
    print("[ERROR] index.html not found.")
