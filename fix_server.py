import os

server_path = "server.js"

if os.path.exists(server_path):
    with open(server_path, "r", encoding="utf-8") as f:
        code = f.read()

    # index.html එක බ්‍රවුසර් එකට පෙන්වන්න අවශ්‍ය ප්‍රධාන කේතය (Route එක) ඇතුළත් කිරීම
    route_code = """
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});
"""

    if "app.get('/'," not in code and "app.get(\"/\"," not in code:
        if "const app = express();" in code:
            code = code.replace("const app = express();", f"const app = express();\n{route_code}")
        elif "const app = express()" in code:
            code = code.replace("const app = express()", f"const app = express()\n{route_code}")
        else:
            code = route_code + "\n" + code

    with open(server_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Server fixed smoothly!")
else:
    print("[ERROR] server.js not found.")
