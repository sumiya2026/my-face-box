import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 🎨 පරණ හැම ස්ටයිල් එකක්ම අයින් කරලා, නම විතරක් කොටුවක් නැතුව ඩාර්ක් බ්ලූ කරන නව CSS ස්ටයිල් එක
    final_clean_style = """
    <style>
        /* ඉහළ Header එක පිරිසිදු කිරීම */
        .app-header {
            
            padding: 25px 30px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
        }

        /* ⚽ 3D බෝල හැඩැති 'f' ලෝගෝව */
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
            color: #ffffff !important;
            margin-right: 20px !important;
            vertical-align: middle !important;
            box-shadow: 
                inset 5px 5px 8px rgba(255, 255, 255, 0.5), 
                inset -5px -5px 8px rgba(0, 0, 0, 0.6),
                0 8px 15px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            text-shadow: 2px 3px 5px rgba(0,0,0,0.4) !important;
        }

        /* 💎 කිසිම කොටුවක් නැති, තනිව දිලිසෙන 3D Glass Shine ඩාර්ක් බ්ලූ නම */
        .fb-3d-shiny-title {
            color: #063970 !important; /* ඩාර්ක් බ්ලූ වර්ණය පමණය */
            font-size: 54px !important;
            font-weight: bold !important;
            font-family: 'Segoe UI', Roboto, sans-serif !important;
            display: inline-block !important;
            vertical-align: middle !important;
             /* පසුබිම් නිල් කොටුව මුළුමනින්ම ඉවත් කළා */
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
            margin: 0 !important;
            
            /* 3D සහ වීදුරු වගේ දිලිසෙන Glass Shine Reflection */
            text-shadow: 
                1px 1px 0px #04244c,
                2px 2px 0px #031b3d,
                3px 3px 5px rgba(0, 0, 0, 0.4),
                0px 0px 10px rgba(255, 255, 255, 0.5) !important;
        }
    </style>
    """

    # head එකට නවතම පිරිසිදු ස්ටයිල් එක ඇතුළත් කිරීම
    if "</head>" in c:
        c = c.replace("</head>", final_clean_style + "\n</head>")

    # 📋 මුළු ඉහළ බාර් එකම (Header එකම) පරණ වැරදි කොටු නැතිව අලුතින්ම පිළිවෙළකට ලිවීම
    perfect_header = """<div class="app-header">
        <div class="header-left">
            <button class="menu-toggle-btn" onclick="toggleMenu()" aria-label="Menu"><span></span><span></span><span></span></button>
            <img src="/new_logo.png" alt="Logo" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">
            <h1 class="fb-3d-shiny-title">My Face BOX</h1>
        </div>
        <div class="header-right">
            <select id="langSelect" onchange="changeLanguage(this.value)"><option value="en">English</option><option value="si">සිංහල</option><option value="ta">தமிழ்</option></select>
            <button class="icon-btn">+</button>
            <button class="icon-btn">&#128269;</button>
        </div>
    </div>"""

    # පවතින app-header එක සම්පූර්ණයෙන්ම සොයාගෙන එය අලුත් පිරිසිදු එකෙන් ආදේශ කිරීම
    if '<div class="app-header">' in c:
        start_idx = c.find('<div class="app-header">')
        # මුළු header එකම වැසෙන තැන (body එක ඇතුළත ඊළඟට එන mind-box එකට කලින් කොටස) සොයා ගැනීම
        end_idx = c.find('<div class="mind-box">')
        if end_idx != -1:
            c = c[:start_idx] + perfect_header + "\n" + c[end_idx:]
    elif "<div class='app-header'>" in c:
        start_idx = c.find("<div class='app-header'>")
        end_idx = c.find("<div class='mind-box'>")
        if end_idx == -1:
            end_idx = c.find('<div class="mind-box">')
        if end_idx != -1:
            c = c[:start_idx] + perfect_header + "\n" + c[end_idx:]

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] Blue box removed and title forced to Dark Blue smoothly!")
else:
    print("[ERROR] index.html not found.")
