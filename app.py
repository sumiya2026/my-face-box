from flask import Flask, render_template, request, jsonify, send_from_directory
import os, json

app = Flask(__name__)

@app.route('/translations.json')
def translations():
    try:
        return send_from_directory('.', 'translations.json')
    except:
        return jsonify({"si": "හෙලෝ"})

@app.route('/api/verify-nic', methods=['POST'])
def verify_nic():
    data = request.get_json()
    nic = data.get('nic','') if data else ''
    if not nic:
        return jsonify({"success": False, "message": "NIC දාන්න මචෝ"})
    return jsonify({"success": True, "message": f"{nic} Verified!"})

PAGES = ["home","market","friends","watch","groups","profile","menu"]

@app.route('/')
def home():
    return render_template('index.html', pages=PAGES)

@app.route('/<page_name>')
def pages_route(page_name):
    if page_name in PAGES:
        return render_template('index.html', pages=PAGES, active=page_name)
    return "Not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
