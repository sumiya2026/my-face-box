import os

server_path = "server.js"

# index.html තියෙන නිවැරදිම තැන සොයා ගැනීම
possible_paths = ["index.html", "public/index.html", "templates/index.html", "static/index.html"]
found_path = ""

for p in possible_paths:
    if os.path.exists(p):
        found_path = p
        break

if found_path:
    print(f"[FOUND] HTML file is located at: {found_path}")
    
    with open(server_path, "r", encoding="utf-8") as f:
        code = f.read()

    # ෆෝල්ඩරය අනුව සර්වර් එකේ කේතය වෙනස් කිරීම
    if "public/" in found_path:
        folder_route = "path.join(__dirname, 'public', 'index.html')"
        static_route = "app.use(express.static(path.join(__dirname, 'public')));"
    elif "templates/" in found_path:
        folder_route = "path.join(__dirname, 'templates', 'index.html')"
        static_route = "app.use(express.static(path.join(__dirname, 'templates')));"
    else:
        folder_route = "path.join(__dirname, 'index.html')"
        static_route = "app.use(express.static(__dirname));"

    # කේතය යාවත්කාලීන කිරීම
    if "res.sendFile(path.join(__dirname, 'index.html'));" in code:
        code = code.replace("res.sendFile(path.join(__dirname, 'index.html'));", f"res.sendFile({folder_route});")
        code = code.replace("app.use(express.static(__dirname));", f"{static_route}\napp.use(express.static(__dirname));")

    with open(server_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Path configuration fixed based on your folder structure!")
else:
    print("[ERROR] Could not find index.html anywhere!")
