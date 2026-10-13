import os
import sqlite3
import psycopg2
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
DB_FILE = "facebox.db"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB Limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌐 Supabase Cloud Database Connection String
SUPABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres" # ඔබගේ සැබෑ URL එක මෙතැන පවතී

def get_db_connection():
    try:
        conn = psycopg2.connect(SUPABASE_URL, connect_timeout=5)
        return conn
    except Exception:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQLite සහ PostgreSQL දෙකටම ගැළපෙන සේ වගු සෑදීම
        if isinstance(conn, sqlite3.Connection):
            cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                text_content TEXT,
                media_url TEXT,
                media_type TEXT,
                likes INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                timestamp TEXT NOT NULL
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS post_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                comment_text TEXT NOT NULL
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                media_url TEXT NOT NULL,
                expiry_time INTEGER NOT NULL
            )''')
        else:
            cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                text_content TEXT,
                media_url TEXT,
                media_type TEXT,
                likes INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                timestamp TEXT NOT NULL
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS post_comments (
                id SERIAL PRIMARY KEY,
                post_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                comment_text TEXT NOT NULL
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS stories (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                media_url TEXT NOT NULL,
                expiry_time INTEGER NOT NULL
            )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Initialization Error: {e}")
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if isinstance(conn, sqlite3.Connection):
        posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
        import time
        current_time = int(time.time())
        stories = conn.execute('SELECT * FROM stories WHERE expiry_time > ?', (current_time,)).fetchall()
        
        feed_posts = []
        for post in posts:
            comments = conn.execute('SELECT * FROM post_comments WHERE post_id = ? ORDER BY id ASC', (post['id'],)).fetchall()
            feed_posts.append({'data': post, 'comments': comments})
    else:
        cursor.execute('SELECT * FROM posts ORDER BY id DESC')
        posts = cursor.fetchall()
        import time
        current_time = int(time.time())
        cursor.execute('SELECT * FROM stories WHERE expiry_time > ?', (current_time,))
        stories = cursor.fetchall()
        
        feed_posts = []
        for post in posts:
            cursor.execute('SELECT * FROM post_comments WHERE post_id = %s ORDER BY id ASC', (post[0],))
            comments = cursor.fetchall()
            
            # Map tuple to dict style for compatibility
            post_data = {'id': post[0], 'username': post[1], 'text_content': post[2], 'media_url': post[3], 'media_type': post[4], 'likes': post[5], 'shares': post[6], 'timestamp': post[7]}
            comment_data = [{'user_name': c[2], 'comment_text': c[3]} for c in comments]
            feed_posts.append({'data': post_data, 'comments': comment_data})
            
    conn.close()
    
    # Map sqlite rows to dicts if using sqlite
    if isinstance(conn, sqlite3.Connection):
        formatted_posts = []
        for fp in feed_posts:
            p = fp['data']
            formatted_posts.append({
                'data': {'id': p['id'], 'username': p['username'], 'text_content': p['text_content'], 'media_url': p['media_url'], 'media_type': p['media_type'], 'likes': p['likes'], 'shares': p['shares'], 'timestamp': p['timestamp']},
                'comments': [{'user_name': c['user_name'], 'comment_text': c['comment_text']} for c in fp['comments']]
            })
        formatted_stories = [{'username': s['username'], 'media_url': s['media_url']} for s in stories]
        return render_template('index.html', posts=formatted_posts, stories=formatted_stories)
        
    return render_template('index.html', posts=feed_posts, stories=[{'username': s[1], 'media_url': s[2]} for s in stories])

@app.route('/create_post', methods=['POST'])
def create_post():
    username = request.form.get('username', 'Anonymous')
    text_content = request.form.get('text_content', '')
    file = request.files.get('media_file')
    
    media_url = None
    media_type = None
    
    if file and file.filename != '':
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        media_url = '/static/uploads/' + filename
        
        ext = filename.split('.')[-1].lower()
        if ext in ['mp4', 'webm', 'ogg']:
            media_type = 'video'
        elif ext in ['mp3', 'wav']:
            media_type = 'audio'
        else:
            media_type = 'image'

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    if isinstance(conn, sqlite3.Connection):
        conn.execute('INSERT INTO posts (username, text_content, media_url, media_type, timestamp) VALUES (?, ?, ?, ?, ?)',
                     (username, text_content, media_url, media_type, timestamp))
    else:
        cursor.execute('INSERT INTO posts (username, text_content, media_url, media_type, timestamp) VALUES (%s, %s, %s, %s, %s)',
                     (username, text_content, media_url, media_type, timestamp))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))
@app.route('/api/comment_post', methods=['POST'])
def add_post_comment():
    try:
        data = request.json
        post_id = data.get('post_id')
        user_name = data.get('user_name', 'Sumiya. M.R.A')
        comment_text = data.get('comment_text', '')
        
        if not comment_text.strip():
            return jsonify({"status": "error", "message": "හිස් කමෙන්ට් දැමිය නොහැක"})
            
        conn = get_db_connection()
        cursor = conn.cursor()
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("INSERT INTO post_comments (post_id, user_name, comment_text) VALUES (?, ?, ?)",
                           (post_id, user_name, comment_text))
        else:
            cursor.execute("INSERT INTO post_comments (post_id, user_name, comment_text) VALUES (%s, %s, %s)",
                           (post_id, user_name, comment_text))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "კමෙන්ටය සාර්ථකව එක් විය"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    init_db()
    print("MY FACE BOX 24/7 UNLIMITED LIVE SERVICE STARTED...")
    app.run(host='0.0.0.0', port=5000, debug=False)

