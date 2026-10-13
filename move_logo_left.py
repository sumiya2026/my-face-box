import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. පවතින පැරණි දකුණුපස 3D ලෝගෝ HTML කේතය අයින් කිරීම
    c = c.replace('<div class="fb-3d-logo" onclick="location.reload()">f</div>', '')

    # 2. අලුත් 3D ලෝගෝ HTML එක වම්පැත්තේ 'My Face BOX' එකට කලින් බස්සන්න සූදානම් කිරීම
    # margin-left වෙනුවට margin-right දමා වම්පැත්තට ගැලපෙන සේ සැකසීම
    logo_left_html = '<div class="fb-3d-logo" onclick="location.reload()" style="margin-left:0; margin-right:20px;">f</div>'

    # My Face BOX අකුරට වම්පැත්තෙන් ලෝගෝ එක බස්සමු
    if 'style="margin-right:20px;">f</div>' not in c:
        c = c.replace('My Face BOX', logo_left_html + 'My Face BOX')

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] 3D Glass 'f' Logo Successfully Moved to the Top Left!")
else:
    print("[ERROR] index.html not found.")
