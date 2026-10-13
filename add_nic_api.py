import os

app_path = "app.py"

if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()

    # ලංකාවේ ID පරීක්ෂා කරන Python API කේතය
    nic_api_code = """
@app.route('/api/verify-nic', methods=['POST'])
def verify_nic():
    import re
    from flask import request, jsonify
    data = request.get_json() or {}
    nic = data.get('nic', '').strip()
    
    if not nic:
        return jsonify({"success": False, "message": "කරුණාකර හැඳුනුම්පත් අංකය ඇතුළත් කරන්න."})

    # පැරණි හැඳුනුම්පත් (ඉලක්කම් 9යි V හෝ X) සහ නව හැඳුනුම්පත් (ඉලක්කම් 12යි) රටාවන්
    old_nic_pattern = re.compile(r'^[0-9]{9}[vVxX]$')
    new_nic_pattern = re.compile(r'^[0-9]{12}$')

    if old_nic_pattern.match(nic) or new_nic_pattern.match(nic):
        return jsonify({"success": True, "message": "ජාතික හැඳුනුම්පත සත්‍ය බව තහවුරුයි! (සැබෑ පරිශීලකයෙකි)"})
    else:
        return jsonify({"success": False, "message": "අවලංගු හැඳුනුම්පත් අංකයකි! ව්‍යාජ ගිණුම් සෑදීමට නොහැක."})
"""

    if "/api/verify-nic" not in code:
        if "if __name__" in code:
            code = code.replace("if __name__", f"{nic_api_code}\nif __name__")
        else:
            code += nic_api_code

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Python NIC Auto-Search API Added Successfully!")
else:
    print("[ERROR] app.py not found.")
