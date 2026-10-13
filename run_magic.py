import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. ☰ මෙනුව එකතු කිරීම
    if '&#9776;' not in c:
        c = c.replace('My Face BOX', '&#9776; My Face BOX')

    # 2. පහළ ස්ථාවර මෙනු තීරුව (Bottom Nav Bar) එකතු කිරීම
    bottom_nav = '<div style="position:fixed;bottom:0;left:0;width:100%;background:white;display:flex;justify-content:space-around;padding:25px 0;border-top:2px solid #ccc;z-index:99999;font-size:55px;"><button onclick="alert(\'Home\')">🏠</button><button onclick=\"alert(\'Watch\')\">📺</button><button onclick=\"alert(\'Friends\')\">👥</button><button onclick=\"alert(\'Notifications\')\">🔔</button><button onclick=\"alert(\'Menu\')\">⚙️</button></div>'
    if 'position:fixed' not in c:
        c = c.replace('</body>', bottom_nav + '</body>')

    # 3. මුහුණතේ අකුරු සහ layout එක තවත් විශාල කිරීම (2X Responsive Scaling)
    big_styles = '<style>body{font-size:38px !important;padding-bottom:160px !important;}.post-card,.card{font-size:36px !important;padding:40px !important;}.fb-logo{font-size:64px !important;}</style>'
    if 'font-size:38px' not in c:
        c = c.replace('</head>', big_styles + '</head>')

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] Everything injected perfectly in one shot!")
else:
    print("[ERROR] File not found")
