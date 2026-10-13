        return conn
    except Exception:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        return conn

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_data (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        """)
        
        cursor.execute("SELECT value FROM app_data WHERE key = 'posts'")
        if not cursor.fetchone():
            initial_posts = [
                {
                    "id": 1,
                    "user_name": "Sumiya. M.R.A",
                    "profile_pic": "https://pravatar.cc",
                    "time": "මිනිතත්තු කිහිපයකට පෙර",
                    "text": "My Face Box Live Content 🚀",
                    "media_url": "https://unsplash.com",
                    "media_type": "image",
                    "likes": 1,
                    "comments": 0,
                    "shares": 1
                }
            ]
            placeholder = "%s" if hasattr(cursor, 'mogrify') else "?"
            cursor.execute(f"INSERT INTO app_data (key, value) VALUES ('posts', {placeholder})", (json.dumps(initial_posts),))

        cursor.execute("SELECT value FROM app_data WHERE key = 'stories'")
        if not cursor.fetchone():
            initial_stories = []
            placeholder = "%s" if hasattr(cursor, 'mogrify') else "?"
            cursor.execute(f"INSERT INTO app_data (key, value) VALUES ('stories', {placeholder})", (json.dumps(initial_stories),))

        conn.commit()
        cursor.close()
        conn.close()
        print("DB Initialized Successfully!")
    except Exception as e:
        print(f"DB Initialization Error: {e}")

init_db()

def load_data():
    data = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        placeholder = "%s" if hasattr(cursor, 'mogrify') else "?"
        
        for key in ["posts", "stories", "reels", "shop_items"]:
            cursor.execute(f"SELECT value FROM app_data WHERE key = {placeholder}", (key,))
            row = cursor.fetchone()
            dict_key = "shop" if key == "shop_items" else key
            if row:
                try:
                    data[dict_key] = json.loads(row[0])
                except Exception:
                    data[dict_key] = []
            else:
                data[dict_key] = []
        conn.close()
    except Exception:
        for k in ["posts", "stories", "reels", "shop"]:
            data[k] = []
    return data

def save_data_key(key, val_list):
    try:
        db_key = "shop_items" if key == "shop" else key
        conn = get_db_connection()
        cursor = conn.cursor()
        json_val = json.dumps(val_list)
        
        if hasattr(cursor, 'mogrify'):
            cursor.execute("""
                INSERT INTO app_data (key, value) VALUES (%s, %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
            """, (db_key, json_val))
        else:
            cursor.execute("INSERT OR REPLACE INTO app_data (key, value) VALUES (?, ?)", (db_key, json_val))
            
        conn.commit()
        conn.close()
    except Exception as e:
        print("Save Data Error:", str(e))

EOF

python update_flask_backend.py
echo -e "\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=5000, debug=True)" >> update_flask_backend.py
python update_flask_backend.py
cat << 'EOF' >> update_flask_backend.py

@app.route('/')
def home():
    data = load_data()
    return render_template_string(HTML, posts=data.get('posts', []), stories=data.get('stories', []), reels=data.get('reels', []), shop=data.get('shop', []))

EOF

cp /storage/emulated/0/untitled.txt ./untitled_backup.txt
sed -n '/HTML =/,/if __name__/p' untitled_backup.txt | sed '$d' >> update_flask_backend.py
python update_flask_backend.py
rm update_flask_backend.py
rm myface_database.db
nano app.py
tmux ls
tmux attach
cd ~/my_face_box_app
rm app.py
nano app.py
cd ~/my_face_box_app && python app.py
cd ~/my_face_box_app && nano app.py
python app.py
ls
python -m http.server 8000
pkill -9 python
cd ~/my_face_box_app && python app.py
cp app.py.bak app.py
ls -l app.py
python app.py
nano app.py
python app.py
cat << 'EOF' > app.py
from flask import Flask, render_template_string, jsonify, request
import sqlite3
import os
import json

app = Flask(__name__)
DB_FILE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def load_data():
    data = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for key in ["posts", "stories", "reels", "shop_items"]:
            cursor.execute('SELECT value FROM app_data WHERE key = ?', (key,))
            row = cursor.fetchone()
            dict_key = "shop" if key == "shop_items" else key
            if row and row[0]:
                try:
                    data[dict_key] = json.loads(row[0])
                except Exception:
                    data[dict_key] = []
            else:
                data[dict_key] = []
        conn.close()
    except Exception:
        for k in ["posts", "stories", "reels", "shop"]:
            data[k] = []
    return data

def save_data_key(key, val_list):
    try:
        db_key = "shop_items" if key == "shop" else key
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?, ?)', (db_key, json.dumps(val_list)))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Save Data Error:", str(e))

@app.route('/')
def home():
    return "<h1>Face Box Server is Running Successfully!</h1>"

@app.route('/api/posts', methods=['GET'])
def get_posts():
    data = load_data()
    return jsonify({"status": "success", "posts": data.get("posts", [])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF

python app.py
python initapi.py
ls
termux-setup-storage
exit
ps aux | grep python
cd ~/my_face_box_app
python app.py
cd ~/my_face_box_app
python app.py
cd ~/my_face_box_app
rm app.py facebox.db
pkill -f app.py
cat > app.py << 'PYEOF'
import os, sys, time, json, logging, sqlite3
import psycopg2
from psycopg2 import pool
from functools import wraps
from flask import Flask, jsonify, request, render_template_string
print("=== MY FACE BOX ULTIMATE 2076 ===")
SUPABASE_URL = "postgresql://postgres:FY%3Fk%21XyUf9f%25NNQ@db.tqnhcqwgfoandnbyeqvs.supabase.co:6543/postgres?sslmode=require"
LOCAL_DB = "facebox.db"
class ResilientDatabaseManager:
    def __init__(self):
        self.mode = "CLOUD"
        self.pool = None
        try:
            self.pool = pool.SimpleConnectionPool(1, 10, SUPABASE_URL, connect_timeout=3)
            print("Cloud OK")
        except Exception as e:
            print(f"Local Mode: {e}")
            self.mode = "LOCAL"
    def acquire(self):
        if self.mode == "CLOUD" and self.pool:
            try:
                c = self.pool.getconn()
                return c, "CLOUD"
            except: self.mode = "LOCAL"
        return sqlite3.connect(LOCAL_DB, check_same_thread=False), "LOCAL"
    def release(self, c, m):
        if m == "CLOUD": self.pool.putconn(c)
        else: c.close()
db_engine = ResilientDatabaseManager()
def run_query(q, p=(), w=False):
    conn, mode = db_engine.acquire()
    try:
        cur = conn.cursor()
        cur.execute(q, p)
        if w:
            conn.commit()
            return True
        return cur.fetchall()
    except Exception as e:
        if mode == "CLOUD":
            db_engine.mode = "LOCAL"
            return run_query(q, p, w)
        return None
    finally:
        db_engine.release(conn, mode)
run_query("CREATE TABLE IF NOT EXISTS app_data (key TEXT PRIMARY KEY, value TEXT)", w=True)
app = Flask(__name__)
def secure_api(f):
    @wraps(f)
    def decorated(*args, **kwargs): return f(*args, **kwargs)
    return decorated
class PartitionManager:
    @staticmethod
    def get_data(k):
        q = "SELECT value FROM app_data WHERE key = %s" if db_engine.mode == "CLOUD" else "SELECT value FROM app_data WHERE key =?"
        r = run_query(q, (k,))
        if r and r[0]: return json.loads(r[0][0])
        return []
    @staticmethod
    def save_data(k, d):
        q = "INSERT INTO app_data (key,value) VALUES (%s,%s) ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value" if db_engine.mode == "CLOUD" else "INSERT OR REPLACE INTO app_data (key,value) VALUES (?,?)"
        return run_query(q, (k, json.dumps(d)), w=True)
@app.route('/api/posts', methods=['GET'])
def api_get_posts(): return jsonify(PartitionManager.get_data("posts"))
@app.route('/api/add_post', methods=['POST'])
def api_add_post():
    d = request.json; d["id"] = int(time.time()*1000); d["likes"] = 0
    allp = PartitionManager.get_data("posts"); allp.insert(0, d)
    PartitionManager.save_data("posts", allp)
    return jsonify({"status":"success"})
@app.route('/api/delete_post', methods=['POST'])
def api_delete_post():
    pid = request.json.get("id")
    allp = [p for p in PartitionManager.get_data("posts") if p.get("id")!= pid]
    PartitionManager.save_data("posts", allp)
    return jsonify({"status":"success"})
@app.route('/api/like_post', methods=['POST'])
def api_like_post():
    pid = request.json.get("id")
    allp = PartitionManager.get_data("posts")
    for p in allp:
        if p.get("id") == pid: p["likes"] = p.get("likes",0)+1
    PartitionManager.save_data("posts", allp)
    return jsonify({"status":"success"})
@app.route('/api/stories', methods=['GET'])
def api_get_stories(): return jsonify(PartitionManager.get_data("stories"))
@app.route('/')
def index_frontend():
    return render_template_string("""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MY FACE BOX</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
body{margin:0;background:#f0f2f5;font-family:Roboto,Arial}
.navbar{background:#ff6600;color:#fff;padding:12px 15px;display:flex;justify-content:space-between;position:sticky;top:0;z-index:99}
.main{max-width:500px;margin:0 auto;padding:10px;padding-bottom:90px}
.story-bar{display:flex;overflow-x:auto;background:#fff;padding:10px;border-radius:10px;margin-bottom:10px;gap:8px}
.s-card{min-width:95px;height:160px;background:#ddd;border-radius:12px;position:relative;background-size:cover;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:bold;background-color:#ff6600}
.post{background:#fff;border-radius:12px;padding:12px;margin-bottom:12px}
.post img{width:100%;border-radius:8px;margin-top:8px}
.b-nav{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #ddd;display:flex;justify-content:space-around;padding:12px 0}
.btn{background:#ff6600;color:#fff;border:none;padding:9px 16px;border-radius:20px;font-weight:bold}
input{padding:10px 14px;border-radius:20px;border:1px solid #ccc;width:70%}
</style></head><body>
<div class="navbar"><b>MY FACE BOX ULTIMATE</b><span><i class="fas fa-search"></i> <i class="fas fa-bell"></i></span></div>
<div class="main">
<div class="story-bar" id="sBar"><div class="s-card">+ Create Story</div></div>
<div style="background:#fff;padding:12px;border-radius:12px;margin-bottom:10px"><input id="txt" placeholder="What's on your mind, Sumiya?"><button class="btn" onclick="addPost()">Post</button></div>
<div id="feed"></div>
</div>
<div class="b-nav"><div>Home</div><div>Reels</div><div>Shop</div><div>Profile</div></div>
<script>
async function load(){
  let rp=await fetch('/api/posts'); let posts=await rp.json();
  let fd=document.getElementById('feed'); fd.innerHTML='';
  if(posts.length==0){posts=[{id:1,user_name:"My Face Box",time:"now",text:"🔥 ULTIMATE LIVE! Welcome!",media_url:"https://picsum.photos/500/300",likes:12}]}
  posts.forEach(p=>{
    let m=''; if(p.media_url) m=`<img src="${p.media_url}">`;
    fd.innerHTML+=`<div class="post"><b>${p.user_name}</b> - ${p.time}<div style="margin:8px 0">${p.text}</div>${m}<div style="margin-top:8px"><button onclick="likePost(${p.id})">👍 ${p.likes||0}</button> <button onclick="delPost(${p.id})" style="color:red">Delete</button></div></div>`;
  });
}
async function addPost(){let t=document.getElementById('txt').value; if(!t) return; await fetch('/api/add_post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_name:"Sumiya",text:t,media_url:"",time:"just now"})}); document.getElementById('txt').value=''; load();}
async function delPost(id){ await fetch('/api/delete_post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})}); load(); }
async function likePost(id){ await fetch('/api/like_post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})}); load(); }
load(); setInterval(load,4000);
</script></body></html>
    """)
if __name__ == '__main__':
    print("ULTIMATE LIVE ON 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
PYEOF

python app.py
ls
cp app.py.bak app.py
python app.py
pkg install nano -y
nano app.py
python app.py
cd ~/my_face_box_app
rm app.py facebox.db
pkill -f app.py
http://localhost:5000
cd ~/my_face_box_app
rm app.py facebox.db
pkill -f app.py
node server.js
node server.js --clear
node server.js
pkill -f node
ls
node server.js
cp /storage/emulated/0/untitled.txt index.html
node server.js
cp /storage/emulated/0/untitled.txt index.html && node server.js
mv untitled.txt index.html
pwd
ls
cat > index.html
sed -E 's/^[[:space:]]*[0-9]+//' untitled.txt > index.html && ls -lh index.html
termux-setup-storage
cp /storage/emulated/0/untitled.txt ./public/index.html
node server.js
cp /storage/emulated/0/untitled.txt ./templates/index.html
nano index.html
cp index.html ./templates/index.html
node server.js
cp /storage/emulated/0/untitled.txt ./templates/index.html
node server.js
termux-setup-storage
cp /sdcard/untitled.txt ./
mv untitled.txt index.html
cp index.html ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
pkill -f node
npm install -g nodemon
nodemon server.js
pkill -f node
cp /sdcard/untitled.txt ./index.html
cp /sdcard/untitled.txt ./templates/index.html
cat ./templates/index.html | grep "bnav"  # සුදුපාටද කියලා check කරන්න
node server.js
cp /sdcard/untitled.txt ./index.html ✅
cp /sdcard/untitled.txt ./templates/index.html ✅
Server running on http://localhost:8000 ✅
cp /sdcard/untitled.txt ./index.html
cp /sdcard/untitled.txt ./templates/index.html
node server.js
pkill -f node
cp /sdcard/untitled.txt ./index.html
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
pkill -f node
rm -rf ~/.npm ~/.node-gyp
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html 
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
pkill -f node
cat ./templates/index.html
npm install -g nodemon
nodemon server.js
node server.js
cat ./templates/index.html
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
cp /sdcard/untitled.txt ./templates/index.html
node server.js
nano ./templates/index.html
node server.js
nano server.js
node server.js
cat << 'EOF' > update_server.js
const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');
const newBackend = `
// --- මෙතැන් සිට අලුත් ලියාපදිංචි කිරීමේ Backend කේතය ---
let usersList = [
    { name: "M.R.A.SUMINDA", phone: "+940767391892", role: "Agent", date: "10/10/2026" }
];
app.post('/api/register', (req, res) => {
    const newUser = {
        name: req.body.name || "Unknown User",
        phone: req.body.phone || "No Phone",
        role: req.body.role || "Shop Owner",
        accountType: req.body.accountType || "Personal Account",
        accountName: req.body.accountName || "",
        publishToList: req.body.publishToList || false,
        date: "10/10/2026"
    };
    usersList.push(newUser);
    res.status(200).json({ success: true, message: "සාර්ථකයි", user: newUser });
});
app.get('/api/users', (req, res) => { res.json(usersList); });
`;
code = code.replace("app.use(express.json());", "app.use(express.json());" + newBackend);
fs.writeFileSync('server.js', code);
console.log('සර්වර් කේතය 100% ක් සාර්ථකව යාවත්කාලීන විය!');
EOF

node update_server.js
node server.js
sed -i 's/let usersList =/var usersList =/g' server.js
node server.js
python -m http.server 5000
cd /storage/emulated/0/
python -m http.server 5000
ls -la
python -m http.server 5000
python -m http.server 58000
cd /storage/emulated/0/
python -m http.server 58000
cd /storage/emulated/0/
python -m http.server 58000
server.js
node server.js
server.js
rm server.js
const express = require('express');
const app = express();
// 🛠️ පරණ 5000 මතකය සම්පූර්ණයෙන්ම අතුගා දමා 8000 ස්ථාවර කිරීම
const PORT = 8000;
function runMyFaceBox() {     console.log("=========================================================");
}
app.listen(PORT, () => {
});
clear
nano server.js
node server.js
nano server.js
node server.js
cd /storage/emulated/0/
rm -rf ~/.config/google-chrome ~/.mozilla ~/.cache
node server.js
cd ~
node server.js

cd /storage/emulated/0/
python -m http.server 58000
