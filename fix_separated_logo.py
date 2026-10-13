import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 🎨 ලෝගෝව වෙනම 3D බෝලයක් කිරීමට සහ නම වෙනම 3D Glass Shine කිරීමට අවශ්‍ය නව CSS සහ HTML
    separated_style = """
    <style>
        /* 🔵 ඉහළ Header එකේ පසුබිම සහ සැකසුම පිරිසිදු කිරීම */
        .app-header {
            
            box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
        }

        /* ⚽ 1. තනිව පවතින 3D බෝල හැඩැති 'f' ලෝගෝව */
        .fb-3d-ball-logo {
            width: 85px !important;
            height: 85px !important;
            
            border-radius: 50% !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
            font-size: 62px !important;
            font-weight: bold !important;
            color: #ffffff !important; /* තනි සුදු f අකුර */
            margin-right: 20px !important;
            vertical-align: middle !important;
            box-shadow: 
                inset 5px 5px 8px rgba(255, 255, 255, 0.5), 
                inset -5px -5px 8px rgba(0, 0, 0, 0.6),
                0 8px 15px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            text-shadow: 2px 3px 5px rgba(0,0,0,0.4) !important;
        }

        /* 💎 2. පසුබිම් කොටු නැති, තනිව දිලිසෙන 3D Glass Shine නම */
        .fb-3d-shiny-title {
            color: #063970 !important; /* ඩාර්ක් බ්ලූ වර්ණය */
            font-size: 54px !important;
            font-weight: bold !important;
            font-family: 'Segoe UI', Roboto, sans-serif !important;
            display: inline-block !important;
            vertical-align: middle !important;
             /* පසුබිම් කොටුව සම්පූර්ණයෙන්ම ඉවත් කළා */
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
            
            /* 📝 3D සහ වීදුරු වගේ දිලිසෙන (Shine) ස්වභාවය ලබාදෙන Text Shadows */
            text-shadow: 
                1px 1px 0px #04244c,
                2px 2px 0px #031b3d,
                3px 3px 0px #021228,
                3px 3px 5px rgba(0, 0, 0, 0.5),
                0px 0px 10px rgba(255, 255, 255, 0.6) !important; /* Glass Shine Reflection Effect */
        }
    </style>
    """

    # පවතින සියලුම පැරණි වැරදි ටැග් සහ කොටු පිරිසිදු කර නව ව්‍යුහය ඇතුළත් කිරීම
    # head එකට අලුත් ස්ටයිල් එක දැමීම
    if "</head>" in c:
        c = c.replace("</head>", separated_style + "\n</head>")

    # HTML එක ඇතුළේ ලෝගෝව සහ නම වෙන් වෙන්ව පිරිසිදුව ඇතුළත් කිරීම
    new_header_left = """<div class='header-left'>
        <button class='menu-toggle-btn' onclick='toggleMenu()'><span></span><span></span><span></span></button>
        <div class='fb-3d-ball-logo'>f</div>
        <h1 class='fb-3d-shiny-title'>My Face BOX</h1>
    </div>"""

    # පැරණි header-left කොටස සම්පූර්ණයෙන්ම නව එකෙන් ආදේශ කිරීම
    if "<div class='header-left'>" in c:
        start_idx = c.find("<div class='header-left'>")
        # </div> වැසෙන තැන සොයා ගැනීම (පළමු </div> එක header-left එක අවසන් වන තැනයි)
        end_idx = c.find("</div>", start_idx + 25) + 6
        # තවදුරටත් ආරක්ෂිත වීමට මුළු ප්‍රධාන header-left ව්‍යුහයම කෙලින්ම වෙනස් කරමු
        c = c[:start_idx] + new_header_left + c[end_idx:]
    elif '<div class="header-left">' in c:
        start_idx = c.find('<div class="header-left">')
        end_idx = c.find("</div>", start_idx + 25) + 6
        c = c[:start_idx] + new_header_left + c[end_idx:]

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] Separated 3D Ball Logo and 3D Shiny Title Installed Perfectly!")
else:
    print("[ERROR] index.html not found.")
