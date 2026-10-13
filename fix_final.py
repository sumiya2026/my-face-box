import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 🎨 1. නම වටේ තියෙන කොටුව අයින් කර නම ඩාර්ක් බ්ලූ කරන සහ ලෝගෝව ලයිව් කැරකෙන්න සලස්වන CSS කේතය
    # (ටර්මිනල් එක හිරවීම වැළැක්වීමට ! සලකුණ සම්පූර්ණයෙන්ම අයින් කර ඇත)
    animation_css = """
    <style>
        /* ⚽ ලෝගෝව තව චූට්ටක් ලොකු කර සජීවීව කැරකැවීම */
        .fb-3d-ball-logo {
            width: 105px;
            height: 105px;
            
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 72px;
            font-weight: bold;
            color: #ffffff;
            margin-right: 20px;
            vertical-align: middle;
            box-shadow: inset 5px 5px 8px rgba(255, 255, 255, 0.5), inset -5px -5px 8px rgba(0, 0, 0, 0.6), 0 8px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-shadow: 2px 3px 5px rgba(0,0,0,0.4);
            animation: spinBall 6s linear infinite;
        }
        @keyframes spinBall {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        /* 💎 නම වටේ ඇති කොටුව අයින් කර ඩාර්ක් බ්ලූ කිරීම */
        .app-header h1, .fb-3d-shiny-title {
            color: #063970;
            font-size: 54px;
            font-weight: bold;
            
            padding: 0;
            border: none;
            box-shadow: none;
            backdrop-filter: none;
            margin: 0;
            display: inline-block;
            vertical-align: middle;
            text-shadow: 1px 1px 0px #04244c, 2px 2px 0px #031b3d, 3px 3px 5px rgba(0, 0, 0, 0.4);
        }
        
        /* පැරණි නිල් කොටුවේ මෝස්තරය අක්‍රිය කිරීම */
        .app-header {
            
            padding: 25px 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
    </style>
    """

    # පරණ නිල් කොටු පන්තියක් ඇත්නම් එය පිරිසිදු කිරීම
    c = c.replace('', '')
    c = c.replace('', '')
    c = c.replace('color: #ffffff;', 'color: #063970;')
    c = c.replace('color:#ffffff;', 'color:#063970;')

    if "spinBall" not in c:
        c = c.replace("</head>", animation_css + "\n</head>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] Separated Dynamic Rotating Logo and Dark Blue Title Configured Perfectly!")
else:
    print("[ERROR] index.html not found.")
