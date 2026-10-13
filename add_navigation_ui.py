import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. ☰ මෙනුව සහ පහළ ස්ථාවර තීරුව (Bottom Nav) සඳහා අවශ්‍ය CSS එකතු කිරීම
    nav_styles = """
    <style>
        /* මුළු තිරයම පහළ Nav බාර් එක නිසා වැසීම වැළැක්වීමට body එකට bottom padding දීම */
        body {
            padding-bottom: 120px !important;
        }

        /* ☰ මෙනු බොත්තමේ හැඩය */
        .menu-btn {
            font-size: 55px;
            color: #FF6B00;
            background: none;
            border: none;
            cursor: pointer;
            margin-right: 15px;
            font-weight: bold;
        }

        /* 📱 පහළ ස්ථාවර මෙනු තීරුව (Fixed Bottom Navigation) */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: white;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px 0;
            border-top: 2px solid #e4e6eb;
            z-index: 99999;
            box-shadow: 0 -4px 10px rgba(0,0,0,0.08);
        }

        .nav-item {
            font-size: 45px;
            color: #65676b;
            cursor: pointer;
            background: none;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }

        .nav-item.active {
            color: #FF6B00;
        }

        /* Notification බෙල් එක උඩ රතු පාට නොටිෆිකේෂන් ගණන පෙන්වන රවුම */
        .badge {
            position: absolute;
            top: -5px;
            right: -10px;
            background: #e41e3f;
            color: white;
            font-size: 22px;
            font-weight: bold;
            border-radius: 50%;
            padding: 2px 10px;
        }
    </style>
    """

    # CSS එක head එකට බැස්සවීම
    if "</head>" in content:
        content = content.replace("</head>", f"{nav_styles}\n</head>")

    # 2. ඉහළ ලෝගෝ එක ළඟින්ම ☰ ඉරි කෑලි තුන එකතු කිරීම
    menu_html = '<button class="menu-btn" onclick="alert(\'මෙනුව සක්‍රීයයි!\')">☰</button>'
    if 'class="fb-logo"' in content and "menu-btn" not in content:
        content = content.replace('<a href="#" class="fb-logo"', f'{menu_html}<a href="#" class="fb-logo"')

    # 3. පහළ ස්ථාවර මෙනු තීරුවේ (Bottom Nav) HTML එක </body> ට පෙර බැස්සවීම
    bottom_nav_html = """
    <!-- 📱 පහළ ස්ථාවර මෙනු තීරුව -->
    <div class="bottom-nav">
        <button class="nav-item active" onclick="alert('Home පිටුව')">🏠</button>
        <button class="nav-item" onclick="alert('දේශීය වීඩියෝ (Watch)')">📺</button>
        <button class="nav-item" onclick="alert('මිතුරන් (Friends)')">👥</button>
        <button class="nav-item" onclick="alert('ප්‍රොෆයිල් එක (Profile)')">👤</button>
        <button class="nav-item" onclick="alert('දැනුම්දීම් (Notifications)')">
            🔔<span class="badge">5</span>
        </button>
        <button class="nav-item" onclick="alert('සැකසුම් මෙනුව')">⚙️</button>
    </div>
    """

    if "bottom-nav" not in content:
        content = content.replace("</body>", f"{bottom_nav_html}\n</body>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Fixed Bottom Navigation and Hamburger Menu added beautifully!")
else:
    print("[ERROR] index.html not found.")
