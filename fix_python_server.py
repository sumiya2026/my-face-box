import os

app_path = "app.py"

if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()

    # translations.json එක Python සර්වර් එක හරහා බ්‍රවුසර් එකට දීමට අවශ්‍ය කේතය සැකසීම
    translations_route = """
@app.route('/translations.json')
def get_translations():
    import os
    if os.path.exists('translations.json'):
        with open('translations.json', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    return '{"error": "Not Found"}', 404
"""

    if "/translations.json" not in code:
        # if __name__ == '__main__': කොටසට කලින් route එක ඇතුළත් කිරීම
        if "if __name__" in code:
            code = code.replace("if __name__", f"{translations_route}\nif __name__")
        else:
            code += translations_route

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Python Flask server configured for 3 languages smoothly!")
else:
    print("[ERROR] app.py not found.")
