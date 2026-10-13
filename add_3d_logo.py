import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 🎨 දකුණු පැත්තට සෙට් වන, සැබෑ 3D වීදුරු පෙනුම (Embossed 3D Glass Finish) සහිත ලෝගෝවේ CSS කේතය
    logo_3d_css = """
    <style>
        .fb-3d-logo {
            width: 80px;
            height: 80px;
            
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 58px;
            font-weight: bold;
            color: #ffffff;
            margin-left: 20px;
            vertical-align: middle;
            /* 3D සහ වීදුරු පෙනුම ලබාදෙන Shadows */
            box-shadow: 
                inset 4px 4px 6px rgba(255, 255, 255, 0.6), 
                inset -4px -4px 6px rgba(0, 0, 0, 0.5),
                0 10px 20px rgba(0, 0, 0, 0.3),
                0 4px 6px rgba(0, 0, 0, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.2);
            text-shadow: 2px 4px 5px rgba(0, 0, 0, 0.4);
            cursor: pointer;
            transform: perspective(500px) translateZ(10px);
        }
    </style>
    """
    
    logo_3d_html = '<div class="fb-3d-logo" onclick="location.reload()">f</div>'

    # CSS එක head එකට දැමීම
    if "</head>" in c:
        c = c.replace("</head>", logo_3d_css + "\n</head>")

    # උඩ දකුණු පැත්තේ කෙළවරටම (icon-btn වලට පසුව) 3D ලෝගෝව සෙට් කිරීම
    if logo_3d_html not in c:
        # header-right හෝ අන්තිම අයිකන් එකට පස්සේ බස්සමු
        if '&#128269;</button>' in c:
            c = c.replace('&#128269;</button>', '&#128269;</button>' + logo_3d_html)
        elif 'icon-btn' in c:
            # වෙනත් අයිකනයක් ළඟින් සෙට් කිරීමට
            c = c.replace('</div></div>', logo_3d_html + '</div></div>', 1)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] 3D Dark Blue Glass 'f' Logo Installed on Top Right Successfully!")
else:
    print("[ERROR] index.html not found.")
