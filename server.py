import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "my_facebox_super_secret_key_1245"

# 🌐 Supabase Cloud Database Connection String
SUPABASE_URL = "postgresql://postgres:FY%3Fk%21XyUf9f%25NNQ@db.tqnhcqwgfoandnybeqvs.supabase.co:6543/postgres?sslmode=require"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    try:
        conn = psycopg2.connect(SUPABASE_URL, connect_timeout=5)
        return conn, "postgres"
    except Exception:
        conn = sqlite3.connect("facebox.db", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn, "sqlite"

def init_db():
    try:
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Users Table
        if db_type == "postgres":
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                profile_pic TEXT DEFAULT 'https://pravatar.cc',
                followers TEXT DEFAULT '[]',
                following TEXT DEFAULT '[]'
            )''')
            
            # 2. Dynamic Content Table (Posts, Stories, Reels, Shop)
            cursor.execute('''CREATE TABLE IF NOT EXISTS content (
                id SERIAL PRIMARY KEY,
                type TEXT NOT NULL,
                username TEXT NOT NULL,
                user_full_name TEXT,
                profile_pic TEXT,
                text_content TEXT,
                media_url TEXT,
                media_type TEXT,
                likes TEXT DEFAULT '[]',
                comments TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
        else:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                profile_pic TEXT DEFAULT 'https://pravatar.cc',
                followers TEXT DEFAULT '[]',
                following TEXT DEFAULT '[]'
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                username TEXT NOT NULL,
                user_full_name TEXT,
                profile_pic TEXT,
                text_content TEXT,
                media_url TEXT,
                media_type TEXT,
                likes TEXT DEFAULT '[]',
                comments TEXT DEFAULT '[]',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )''')
            
        conn.commit()
        conn.close()
        print("Database structure initialized successfully!")
    except Exception as e:
        print("DB Init Error:", str(e))

init_db()

# --- AUTH ROUTES ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username').strip().lower()
    password = generate_password_hash(data.get('password'))
    full_name = data.get('full_name')
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    placeholder = "%s" if db_type == "postgres" else "?"
    
    try:
        cursor.execute(f"INSERT INTO users (username, password, full_name) VALUES ({placeholder}, {placeholder}, {placeholder})", 
                       (username, password, full_name))
        conn.commit()
        return jsonify({"success": True, "message": "ලියාපදිංචිය සාර්ථකයි!"})
    except Exception:
        return jsonify({"success": False, "message": "මෙම පරිශීලක නාමය දැනටමත් භාවිතයේ පවතී!"})
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username').strip().lower()
    password = data.get('password')
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    placeholder = "%s" if db_type == "postgres" else "?"
    
    cursor.execute(f"SELECT password, full_name, profile_pic FROM users WHERE username = {placeholder}", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password_hash(row[0], password):
        session['user'] = username
        session['full_name'] = row[1]
        session['profile_pic'] = row[2]
        return jsonify({"success": True, "user": {"username": username, "full_name": row[1], "profile_pic": row[2]}})
    return jsonify({"success": False, "message": "පරිශීලක නාමය හෝ මුරපදය වැරදියි!"})

@app.route('/api/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- CONTENT ROUTES ---
@app.route('/api/content', methods=['GET'])
def get_content():
    content_type = request.args.get('type')
    conn, db_type = get_db_connection()
    
    cursor = conn.cursor(cursor_factory=RealDictCursor) if db_type == "postgres" else conn.cursor()
    placeholder = "%s" if db_type == "postgres" else "?"
    
    cursor.execute(f"SELECT * FROM content WHERE type = {placeholder} ORDER BY id DESC", (content_type,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        item = dict(r)
        item['likes'] = json.loads(item['likes'])
        item['comments'] = json.loads(item['comments'])
        if db_type == "postgres" and isinstance(item['created_at'], datetime):
            item['created_at'] = item['created_at'].strftime("%Y-%m-%d %H:%M")
        results.append(item)
        
    return jsonify(results)

@app.route('/api/content/create', methods=['POST'])
def create_content():
    if 'user' not in session:
        return jsonify({"success": False, "message": "කරුණාකර පළමුව ලොග් වන්න!"}), 401
        
    c_type = request.form.get('type')
    text = request.form.get('text_content', '')
    media_url = request.form.get('media_url', '')
    media_type = 'none'
    
    file = request.files.get('file')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{datetime.now().timestamp()}_{filename}")
        file.save(filepath)
        media_url = '/' + filepath
        media_type = 'video' if filename.lower().endswith(('.mp4', '.mov', '.avi')) else 'image'
    elif media_url:
        media_type = 'image'

    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    p = "%s" if db_type == "postgres" else "?"
    
    cursor.execute(f"""INSERT INTO content (type, username, user_full_name, profile_pic, text_content, media_url, media_type, likes, comments)
                       VALUES ({p},{p},{p},{p},{p},{p},{p},'[]','[]')""",
                   (c_type, session['user'], session['full_name'], session['profile_pic'], text, media_url, media_type))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/content/like', methods=['POST'])
def like_content():
    if 'user' not in session: return jsonify({"success": False}), 401
    cid = request.json.get('id')
    username = session['user']
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    p = "%s" if db_type == "postgres" else "?"
    
    cursor.execute(f"SELECT likes FROM content WHERE id = {p}", (cid,))
    row = cursor.fetchone()
    if row:
        likes = json.loads(row[0])
        if username in likes: likes.remove(username)
        else: likes.append(username)
        
        cursor.execute(f"UPDATE content SET likes = {p} WHERE id = {p}", (json.dumps(likes), cid))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/content/comment', methods=['POST'])
def comment_content():
    if 'user' not in session: return jsonify({"success": False}), 401
    data = request.json
    cid = data.get('id')
    text = data.get('text')
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    p = "%s" if db_type == "postgres" else "?"
    
    cursor.execute(f"SELECT comments FROM content WHERE id = {p}", (cid,))
    row = cursor.fetchone()
    if row:
        comments = json.loads(row[0])
        comments.append({
            "username": session['user'],
            "full_name": session['full_name'],
            "profile_pic": session['profile_pic'],
            "text": text,
            "time": "දැන්"
        })
        cursor.execute(f"UPDATE content SET comments = {p} WHERE id = {p}", (json.dumps(comments), cid))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/content/delete', methods=['POST'])
def delete_content():
    if 'user' not in session: return jsonify({"success": False}), 401
    cid = request.json.get('id')
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    p = "%s" if db_type == "postgres" else "?"
    
    cursor.execute(f"DELETE FROM content WHERE id = {p} AND username = {p}", (cid, session['user']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/')
def home():
    user_session = json.dumps(session.get('user'))
    user_fullname = json.dumps(session.get('full_name'))
    user_pic = json.dumps(session.get('profile_pic'))
    
    return render_template('index.html', user_session=user_session, user_fullname=user_fullname, user_pic=user_pic)

if __name__ == '__main__':
    app.run(debug=True)
