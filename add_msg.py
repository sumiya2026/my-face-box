import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        c = f.read()

    # ලැන්වේජ් බොත්තම ළඟින්ම මැසෙන්ජර් (💬) අයිකන් එක එකතු කිරීම
    msg_html = '<button onclick="alert(\'Messenger\')" style="background:#e4e6eb; border:none; width:80px; height:80px; border-radius:50%; font-size:38px; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; margin-left:15px; vertical-align:middle;">&#128172;</button>'
    
    if '&#128172;' not in c:
        c = c.replace('</select>', '</select>' + msg_html)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("[SUCCESS] Messenger Icon Injected Successfully!")
else:
    print("[ERROR] index.html not found.")
