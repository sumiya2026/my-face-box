from flask import Flask, render_template, request, jsonify
import os, json, uuid
from datetime import datetime

app = Flask(__name__)
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Load Pages
if os.path.exists('pages.json'):
    try:
        with open('pages.json','r') as f:
            PAGES=json.load(f)
            if isinstance(PAGES, dict): PAGES=[]
    except: PAGES=[]
else: PAGES=[]

STORIES=[]
FEED=[{"id":"1","user":"My Face Box","text":"Welcome to My Face Box!"}]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-page')
def create_page_page():
    return render_template('create_page.html')

@app.route('/api/feed')
def api_feed():
    return jsonify(FEED)

@app.route('/api/stories')
def api_stories():
    return jsonify(STORIES)

@app.route('/api/page/create', methods=['POST'])
def api_page_create():
    name = request.form.get('name','').strip()
    if not name:
        return jsonify(status='error', msg='Page Name එක දාන්න!')
    img_path=""
    if 'file' in request.files:
        f=request.files['file']
        if f and f.filename:
            fn=f"{uuid.uuid4().hex}_{f.filename}"
            f.save(os.path.join('static/uploads', fn))
            img_path=f"/static/uploads/{fn}"
    page={"id":uuid.uuid4().hex[:8],"name":name,"category":request.form.get('category',''),"bio":request.form.get('bio',''),"image":img_path,"time":datetime.now().strftime("%Y-%m-%d %H:%M")}
    PAGES.append(page)
    with open('pages.json','w') as jf: json.dump(PAGES,jf)
    return jsonify(status='ok', page=page)

@app.route('/api/pages')
def api_pages():
    return jsonify(PAGES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
