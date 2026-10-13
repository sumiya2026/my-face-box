import glob
files = glob.glob("templates/*.html") + glob.glob("*.html")
if files:
    fn = files[0]
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    btn_code = "<div style=\"text-align:center; padding:10px;\"><button onclick=\"alert(\x27Camera Ready\x27)\" style=\"background:#FF6B00; color:white; padding:12px 20px; border:none; border-radius:8px; font-size:16px; font-weight:bold; width:100%; cursor:pointer;\">📸 ID ස්කෑන් කැමරාව ක්‍රියාත්මක කරන්න</button></div>\n"
    if "What\x27s on your mind?" in content:
        new_content = content.replace("What\x27s on your mind?", btn_code + "What\x27s on your mind?")
    else:
        new_content = btn_code + content
    with open(fn, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS")

