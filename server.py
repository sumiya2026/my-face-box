import os
import sqlite3
import psycopg2
import json
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)
DB_FILE = "facebox.db"

# 🌐 Supabase Cloud Database Connection String
SUPABASE_URL = "postgresql://postgres:FY%3Fk%21XyUf9f%25NNQ@db.byjlowrhvveobhxxfbrj.supabase.co:5432/postgres?sslmode=require"

def get_db_connection():
    try:
        # කෙලින්ම Supabase Cloud Database එකට ස්වයංක්‍රීයව සම්බන්ධ වීම
        conn = psycopg2.connect(SUPABASE_URL, connect_timeout=5)
        return conn
    except Exception as e:
        print(f"Cloud DB බිඳවැටුණි: {e}. Local SQLite භාවිත කරයි.")
        # Cloud එක බිඳවැටුණහොත් Local SQLite එකට ඔටෝ මාරු වීම
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        return conn
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQLite සහ PostgreSQL දෙකටම ගැළපෙන ලෙස Table එක සකස් කිරීම
        # (Reserved keyword එකක් නිසා key වෙනුවට data_key ලෙස වෙනස් කර ඇත)
        cursor.execute('''CREATE TABLE IF NOT EXISTS app_data (
            data_key TEXT PRIMARY KEY,
            value TEXT
        )''')
        conn.commit()
        
        # 1. Posts දත්ත පරීක්ෂාව සහ ඇතුළත් කිරීම
        cursor.execute("SELECT value FROM app_data WHERE data_key = 'posts'")
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
            # PostgreSQL සහ Supabase සඳහා ? වෙනුවට %s භාවිත කර ඇත
            cursor.execute("INSERT INTO app_data (data_key, value) VALUES ('posts', %s)", (json.dumps(initial_posts),))
            conn.commit()

        # 2. Stories දත්ත පරීක්ෂාව සහ ඇතුළත් කිරීම
        cursor.execute("SELECT value FROM app_data WHERE key = 'stories'")
        if not cursor.fetchone():
            initial_stories = [
                {
                    "id": 1,
                    "user_name": "Create story",
                    "user_pic": "https://pravatar.cc",
                    "story_pic": "https://unsplash.com",
                    "is_own": True
                }
            ]
            cursor.execute("INSERT INTO app_data (key, value) VALUES ('stories', ?)", (json.dumps(initial_stories),))

        # 3. Reels දත්ත පරීක්ෂාව සහ ඇතුළත් කිරීම
        cursor.execute("SELECT value FROM app_data WHERE key = 'reels'")
        if not cursor.fetchone():
            initial_reels = [
                {
                    "id": 101,
                    "user": "Sumiya Music",
                    "pic": "https://pravatar.cc",
                    "video": "https://w3schools.com",
                    "caption": "අලුත්ම සින්දු එකතුවක් සමඟින්... 🎵🔥 #Reels",
                    "likes": 1240,
                    "comments": 450,
                    "shares": 89
                }
            ]
            cursor.execute("INSERT INTO app_data (key, value) VALUES ('reels', ?)", (json.dumps(initial_reels),))

        # 4. Shop දත්ත පරීක්ෂාව සහ ඇතුළත් කිරීම
        cursor.execute("SELECT value FROM app_data WHERE key = 'shop_items'")
        if not cursor.fetchone():
            initial_shop = [
                {"id": 201, "title": "Smart Watch Ultra Series 8", "price": "Rs. 6,500/=", "image": "https://picsum.photos", "seller": "Sumiya Store"},
                {"id": 202, "title": "Wireless Bluetooth Earbuds", "price": "Rs. 3,200/=", "image": "https://picsum.photos", "seller": "Tech Hub LK"}
            ]
            cursor.execute("INSERT INTO app_data (key, value) VALUES ('shop_items', ?)", (json.dumps(initial_shop),))

        conn.commit()
        conn.close()
        print("DB Initialized Successfully!")
    except Exception as e:
        print("DB Initialization Error:", str(e))

# ඩේටාබේස් එක ස්වයංක්‍රීයව ක්‍රියාත්මක කිරීම
init_db()

def load_data():
    data = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # නිවැරදි සෙවුම් යතුරු (shop_items) ලූප් කිරීම
        for key in ["posts", "stories", "reels", "shop_items"]:
            cursor.execute('SELECT value FROM app_data WHERE key = ?', (key,))
            row = cursor.fetchone()
            # Frontend එකේ පැරණි කේතයන්ට ගැළපීම සඳහා 'shop_items' යතුර 'shop' ලෙස පරිවර්තනය කිරීම
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
        # Frontend එකෙන් 'shop' කියා එවන විට එය ඩේටාබේස් එකේ 'shop_items' ලෙස සේව් කිරීම
        db_key = "shop_items" if key == "shop" else key
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQLite සහ PostgreSQL දෙකටම ගැළපෙන ආරක්ෂිත INSERT OR REPLACE ක්‍රමවේදය
        try:
            cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?, ?)', (db_key, json.dumps(val_list, ensure_ascii=False)))
        except Exception:
            # PostgreSQL සඳහා UPSERT ක්‍රමවේදය
            cursor.execute('INSERT INTO app_data (key, value) VALUES (?, ?) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value', (db_key, json.dumps(val_list, ensure_ascii=False)))
            
        conn.commit()
        conn.close()
    except Exception as e:
        print("Save Data Error:", str(e))

from flask import Flask, render_template_string, request, jsonify
import sqlite3, os, json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# DB එක හරි Path එකකින් හදනවා
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "myface_database.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_data (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()

    # FIX 1: "posts" වෙනුවට පාවිච්චි කරනවා - මේක තමයි ලොකුම Bug එක
    cursor.execute('SELECT value FROM app_data WHERE key =?', ("posts",))
    if not cursor.fetchone():
        initial_posts = [
            {
                "id": 1,
                "user": "Dasatha Lanka News",
                "pic": "https://i.pravatar.cc/100?img=5",
                "text": "අද නිවාඩු දවසේ 10K වලට follow කරන් යමුද හැමෝම... ❤🎵 #SinhalaClassic",
                "media": None,
                "mediaType": "image",
                "reactions": {"like": 92, "love": 15, "care": 5, "haha": 2, "wow": 1, "sad": 0, "angry": 0},
                "myReaction": None,
                "comments": [{"user": "Nimali", "text": "සුපිරි!"}],
                "shares": 32,
                "time": "6h"
            }
        ]
        cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?,?)', ("posts", json.dumps(initial_posts, ensure_ascii=False)))

    cursor.execute('SELECT value FROM app_data WHERE key =?', ("stories",))
    if not cursor.fetchone():
        cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?,?)', ("stories", "[]"))

    cursor.execute('SELECT value FROM app_data WHERE key =?', ("reels",))
    if not cursor.fetchone():
        initial_reels = [
            {
                "id": 101,
                "user": "Sumiya Music",
                "pic": "https://i.pravatar.cc/100?img=12",
                "video": "https://www.w3schools.com/html/mov_bbb.mp4",
                "caption": "අලුත්ම සින්දු එකතුවක් සමඟින්... 🎵🔥 #Reels",
                "likes": 1240,
                "comments": 45
            }
        ]
        cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?,?)', ("reels", json.dumps(initial_reels, ensure_ascii=False)))

    cursor.execute('SELECT value FROM app_data WHERE key =?', ("shop",))
    if not cursor.fetchone():
        initial_shop = [
            {"id": 201, "title": "Smart Watch Ultra Series 8", "price": "Rs. 6,500/=", "image": "https://picsum.photos/300/300?random=1", "seller": "Sumiya Store"},
            {"id": 202, "title": "Wireless Bluetooth Earbuds", "price": "Rs. 3,200/=", "image": "https://picsum.photos/300/300?random=2", "seller": "Tech Hub LK"}
        ]
        cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?,?)', ("shop", json.dumps(initial_shop, ensure_ascii=False)))

    conn.commit()
    conn.close()
    print("DB Initialized Successfully!")

def load_data():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    data = {}
    for key in ["posts", "stories", "reels", "shop"]:
        cursor.execute('SELECT value FROM app_data WHERE key =?', (key,))
        row = cursor.fetchone()
        if row:
            try:
                data[key] = json.loads(row[0])
            except Exception:
                data[key] = []
        else:
            data[key] = []
    conn.close()
    return data

def save_data_key(key, val_list):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO app_data (key, value) VALUES (?,?)', (key, json.dumps(val_list, ensure_ascii=False)))
    conn.commit()
    conn.close()

HTML = """
<!DOCTYPE html>
<html lang="si">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>MY FACE BOX - UNLIMITED SQLITE EDITION</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root{--orange:#ff6a00;--bg:#f0f2f5;--card:#fff;--sub:#65676b;--border:#e4e6eb}
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif}
body{background:var(--bg);padding-top:104px;padding-bottom:62px}
.top-bar{position:fixed;top:0;left:0;width:100%;background:var(--orange);z-index:5000;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.top-main{height:56px;display:flex;justify-content:space-between;align-items:center;padding:0 12px}
.brand{font-size:21px;font-weight:900;color:white;display:flex;gap:10px;align-items:center;cursor:pointer}
.icon-btn{width:36px;height:36px;background:rgba(0,0,0,.15);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;cursor:pointer}
.sub-nav{height:48px;background:var(--orange);display:flex;justify-content:space-around;align-items:center;border-top:1px solid rgba(255,255,255,.2)}
.sub-nav i{font-size:22px;color:rgba(255,255,255,.75);padding:12px 18px;border-bottom:3px solid transparent;cursor:pointer}
.sub-nav i.active{color:white;border-bottom-color:white}
.container{max-width:680px;margin:0 auto}
.card{background:var(--card);border-radius:8px;box-shadow:0 1px 2px rgba(0,0,0,.1);margin-bottom:8px;overflow:hidden}
.card-pad{padding:12px}
.avatar{width:40px;height:40px;border-radius:50%;object-fit:cover}
.post-create{display:flex;gap:10px;align-items:center}
.fake-input{flex:1;background:#f0f2f5;border-radius:20px;padding:11px 14px;color:var(--sub);font-size:14px;cursor:pointer;border:1px solid var(--border)}
.action-row{display:flex;border-top:1px solid var(--border);margin-top:10px}
.action-btn{flex:1;display:flex;justify-content:center;gap:6px;padding:10px 0;color:var(--sub);font-weight:600;font-size:14px;cursor:pointer}
.stories{display:flex;gap:8px;overflow-x:auto;padding:10px}
.story{flex:0 0 112px;height:195px;border-radius:10px;position:relative;overflow:hidden;background:#ddd;border:1px solid #ddd;cursor:pointer}
.story img,.story video{width:100%;height:100%;object-fit:cover}
.story-create{background:white;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:12px;position:relative}
.story-create .story-user-bg {position:absolute;top:0;left:0;width:100%;height:130px;object-fit:cover;}
.story-create .plus-overlay {position:absolute;top:105px;left:50%;transform:translateX(-50%);width:38px;height:38px;background:var(--orange);color:white;border:3px solid white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;z-index:2;}
.story-name{position:absolute;bottom:7px;left:7px;right:7px;color:white;font-size:12px;font-weight:700;text-shadow:0 1px 4px #000;text-align:center;z-index:2;}
.story-create .story-name-bottom {position:absolute;bottom:8px;left:4px;right:4px;color:#000;font-size:11px;font-weight:700;text-align:center;}
.post-head{display:flex;gap:10px;padding:12px;align-items:center;justify-content:space-between}
.post-text{padding:0 12px 10px;font-size:15px;white-space:pre-wrap;word-break:break-word}
.post-media img,.post-media video,.post-media audio{width:100%;max-height:650px;object-fit:contain;display:block;background:#000}
.post-stats { display: flex; justify-content: space-between; padding: 8px 12px; font-size: 13px; color: var(--sub); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); align-items: center; }
.reaction-icons-group { display: flex; align-items: center; gap: 3px; }
.mini-reaction { width: 18px; height: 18px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; color: white; border: 1px solid white; }
.post-actions { display: flex; position: relative; }
.post-actions button { flex: 1; background: none; border: none; padding: 11px 0; font-weight: 600; color: var(--sub); cursor: pointer; display: flex; justify-content: center; gap: 6px; align-items: center; }
.post-actions button.reacted { color: var(--orange); }
.reaction-popup { position: absolute; bottom: 45px; left: 10px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2); border-radius: 30px; padding: 6px 10px; display: none; gap: 10px; z-index: 1000; animation: fadeIn 0.2s ease; }
.reaction-popup span { font-size: 24px; cursor: pointer; transition: transform 0.2s; }
.reaction-popup span:hover { transform: scale(1.3); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.comment-box{padding:8px 12px;display:flex;gap:8px;align-items:center}
.comment-box input{flex:1;background:#f0f2f5;border:1px solid var(--border);border-radius:20px;padding:9px 12px;outline:none;font-size:13px}
.bottom-nav{position:fixed;bottom:0;left:0;width:100%;height:58px;background:white;border-top:1px solid #ddd;display:flex;justify-content:space-around;align-items:center;z-index:5000}
.bottom-nav a{flex:1;display:flex;flex-direction:column;align-items:center;color:#65676b;font-size:10px;text-decoration:none;gap:2px;cursor:pointer}
.bottom-nav a i{font-size:22px}
.bottom-nav a.active{color:var(--orange)}
#menu{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:6000;display:none}
.drawer{width:88%;max-width:360px;height:100%;background:#f0f2f5;overflow-y:auto;padding:12px}
.creator{background:linear-gradient(135deg,#ff6a00,#ff8c33);color:white;padding:16px;border-radius:14px;text-align:center;margin-bottom:12px}
.m-item{background:white;border-radius:12px;padding:14px;display:flex;gap:14px;margin-bottom:8px;font-weight:600;font-size:14px;cursor:pointer}
.m-item i{color:var(--orange);width:20px;font-size:18px;text-align:center}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.65);display:none;justify-content:center;align-items:center;z-index:7000;padding:14px}
.modal-card{background:white;width:100%;max-width:500px;border-radius:16px;padding:18px;max-height:92vh;overflow-y:auto}
.btn{width:100%;background:var(--orange);color:white;border:none;padding:13px;border-radius:10px;font-weight:800;margin-top:10px;cursor:pointer;font-size:15px}
.btn-green{background:#00a400}
.btn-gray{background:#e4e6eb;color:#333}
.input{width:100%;padding:12px;border:1px solid #ccd0d5;border-radius:8px;margin-top:8px;font-size:14px;outline:none}
.profile-header{height:180px;background:linear-gradient(135deg,#ff6a00,#ff8c33);position:relative}
.profile-pic{width:90px;height:90px;border-radius:50%;border:4px solid white;position:absolute;bottom:-40px;left:16px;object-fit:cover;background:white}
.story-viewer{position:fixed;inset:0;background:#000;z-index:9000;display:none;flex-direction:column;justify-content:center;align-items:center}
.story-viewer-content{position:relative;width:100%;max-width:450px;height:85vh;display:flex;flex-direction:column;justify-content:center;align-items:center}
.story-close{position:absolute;top:15px;right:20px;color:white;font-size:28px;cursor:pointer;z-index:9500}
.dropdown-box { position: absolute; top: 60px; right: 12px; width: 300px; background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 8000; display: none; flex-direction: column; overflow: hidden; border: 1px solid var(--border); }
.dropdown-header { background: var(--orange); color: white; padding: 10px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
.dropdown-body { max-height: 250px; overflow-y: auto; padding: 8px; }
.chat-box-modal { position: fixed; bottom: 65px; right: 15px; width: 320px; height: 400px; background: white; border-radius: 12px; box-shadow: 0 5px 25px rgba(0,0,0,0.3); z-index: 8000; display: none; flex-direction: column; overflow: hidden; border: 1px solid var(--border); }
.chat-header { background: var(--orange); color: white; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
.chat-body { flex: 1; padding: 10px; overflow-y: auto; background: #f9f9f9; display: flex; flex-direction: column; gap: 8px; }
.chat-input-row { display: flex; padding: 8px; border-top: 1px solid var(--border); background: white; }
.chat-input-row input { flex: 1; border: 1px solid var(--border); border-radius: 18px; padding: 6px 12px; outline: none; font-size: 13px; }
</style>
</head>
<body>
<div class="top-bar">
  <div class="top-main">
    <div class="brand" onclick="openMenu()"><i class="fa-solid fa-bars"></i> MY FACE BOX</div>
    <div style="display:flex;gap:7px; position:relative;">
      <div class="icon-btn" onclick="toggleSearchModal()"><i class="fa-solid fa-magnifying-glass"></i></div>
      <div class="icon-btn" onclick="toggleNotifModal()"><i class="fa-solid fa-bell"></i></div>
      <div class="icon-btn" onclick="openChatModal()"><i class="fa-brands fa-facebook-messenger"></i></div>
      <div class="dropdown-box" id="searchDropdown">
        <div class="dropdown-header"><span>🔍 Search Posts</span><i class="fa-solid fa-xmark" style="cursor:pointer" onclick="toggleSearchModal()"></i></div>
        <div style="padding:8px;"><input id="searchInput" class="input" placeholder="Search keywords..." oninput="filterPosts(this.value)" style="margin-top:0"></div>
        <div class="dropdown-body" id="searchResultsList" style="font-size:13px;color:var(--sub)">Type to search...</div>
      </div>
      <div class="dropdown-box" id="notifDropdown">
        <div class="dropdown-header"><span>🔔 Notifications</span><i class="fa-solid fa-xmark" style="cursor:pointer" onclick="toggleNotifModal()"></i></div>
        <div class="dropdown-body" style="font-size:13px;">
          <div style="padding:6px;border-bottom:1px solid var(--border)">✨ සුමින්ද රණවීර විසින් අලුත්ම පෝස්ට් එකක් එකතු කරන ලදී.</div>
          <div style="padding:6px;border-bottom:1px solid var(--border)">❤ නව Reaction එකක් ලැබුණි.</div>
          <div style="padding:6px;">💬 නව Comment එකක් එකතු විය.</div>
        </div>
      </div>
    </div>
  </div>
  <div class="sub-nav">
    <i class="fa-solid fa-house active" onclick="nav('home',this)"></i>
    <i class="fa-solid fa-tv" onclick="nav('reels',this)"></i>
    <i class="fa-solid fa-user-group" onclick="nav('friends',this)"></i>
    <i class="fa-solid fa-store" onclick="nav('shop',this)"></i>
    <i class="fa-solid fa-user" onclick="nav('profile',this)"></i>
  </div>
</div>
<div class="container" id="home">
  <div class="card card-pad">
    <div class="post-create">
      <img class="avatar" id="myAvatar" src="https://i.pravatar.cc/100?img=12">
      <div class="fake-input" onclick="openPost()">What's on your mind? (Unlimited SQLite Edition)</div>
    </div>
    <div class="action-row">
      <div class="action-btn" onclick="openPost()"><i class="fa-solid fa-images" style="color:#45bd62"></i> Photos</div>
      <div class="action-btn" onclick="openPost()"><i class="fa-solid fa-video" style="color:#f3425f"></i> Videos</div>
      <div class="action-btn" onclick="openPost()"><i class="fa-solid fa-music" style="color:#10d876"></i> Music</div>
    </div>
  </div>
  <div class="card"><div class="stories" id="stories"></div></div>
  <div id="feed"></div>
</div>
<div class="container" id="other" style="display:none"><div class="card"><div class="card-pad" id="otherText"></div></div></div>
<div class="bottom-nav">
  <a class="active" onclick="nav('home',document.querySelector('.sub-nav i'))"><i class="fa-solid fa-house"></i>Home</a>
  <a onclick="nav('reels',document.querySelectorAll('.sub-nav i')[1])"><i class="fa-solid fa-clapperboard"></i>Reels</a>
  <a onclick="nav('shop',document.querySelectorAll('.sub-nav i')[3])"><i class="fa-solid fa-store"></i>Shop</a>
  <a onclick="toggleNotifModal()"><i class="fa-solid fa-bell"></i>Alerts</a>
  <a onclick="nav('profile',document.querySelectorAll('.sub-nav i')[4])"><i class="fa-solid fa-user"></i>Profile</a>
</div>
<div class="chat-box-modal" id="chatModal">
  <div class="chat-header"><span>💬 Messenger Chat</span><i class="fa-solid fa-xmark" style="cursor:pointer" onclick="closeChatModal()"></i></div>
  <div class="chat-body" id="chatMessages"><div style="background:white;padding:8px 12px;border-radius:12px;font-size:13px;align-self:flex-start;box-shadow:0 1px 2px rgba(0,0,0,0.1)">ආයුබෝවන්! මම ඔබට කෙසේ උදව් කළ යුතුද? 👋</div></div>
  <div class="chat-input-row"><input id="chatInput" placeholder="Type a message..." onkeydown="if(event.key==='Enter') sendChatMessage()"></div>
</div>
<div id="menu" onclick="closeMenu()">
  <div class="drawer" onclick="event.stopPropagation()">
    <div class="m-item" style="background:#fff3e0;border:1px solid var(--orange);" onclick="changeLanguagePrompt();closeMenu()"><i class="fa-solid fa-language"></i><div style="display:flex;flex-direction:column;gap:2px;width:100%;"><span>භාෂාව / Language / மொழி</span><span style="font-size:11px;color:var(--orange);font-weight:normal;">සිංහල | English | Tamil</span></div></div>
    <div class="creator"><h4>👑 නිර්මාතෘ: M.R.A. සුමින්ද රණවීර</h4><p style="font-size:13px;margin-top:4px">📞 0767391892 | 24/7 Unlimited Edition</p></div>
    <div class="m-item" onclick="openReg();closeMenu()"><i class="fa-solid fa-id-card"></i> අංගසම්පූර්ණ ලියාපදිංචිය (Profile)</div>
    <div class="m-item" onclick="closeMenu()"><i class="fa-solid fa-shield-halved"></i> SQLite Database Engine Active ✅</div>
  </div>
</div>
<div class="modal" id="postModal">
  <div class="modal-card">
    <h3 style="color:var(--orange)">Create Post (Unlimited Storage) ♾️️</h3>
    <textarea id="postText" class="input" rows="4" placeholder="What's on your mind?"></textarea>
    <label style="font-size:12px;color:var(--sub);margin-top:8px;display:block;">Select Image, Video or Audio File (Unlimited Size):</label>
    <input type="file" id="postFile" accept="image/*,video/*,audio/*" class="input">
    <div id="mediaPreviewContainer" style="margin-top:10px"></div>
    <button class="btn" onclick="doPost()">Post - Permanent</button>
    <button class="btn btn-gray" onclick="closePost()">Cancel</button>
  </div>
</div>
<div class="modal" id="storyModal">
  <div class="modal-card">
    <h3 style="color:var(--orange)">පැය 24 ස්ටේටස් එකතු කරන්න ♾️</h3>
    <input type="text" id="storyCaption" class="input" placeholder="ස්ටේටස් ශීර්ෂය (Caption)...">
    <input type="file" id="storyFile" accept="image/*,video/*" class="input">
    <video id="storyVideoPreview" style="width:100%;margin-top:10px;border-radius:10px;display:none" controls></video>
    <img id="storyPreview" style="width:100%;margin-top:10px;border-radius:10px;display:none">
    <button class="btn btn-green" onclick="publishStory()">ස්ටේටස් පබ්ලිෂ් කරන්න</button>
    <button class="btn btn-gray" onclick="closeStoryModal()">Cancel</button>
  </div>
</div>
<div class="story-viewer" id="storyViewer"><div class="story-close" onclick="closeStoryViewer()"><i class="fa-solid fa-xmark"></i></div><div class="story-viewer-content" id="storyViewerContent"></div></div>
<div class="modal" id="regModal">
  <div class="modal-card">
    <div style="text-align:center"><img id="regAvatarPreview" src="https://i.pravatar.cc/150" style="width:90px;height:90px;border-radius:50%;border:4px solid #ff6a00;object-fit:cover"><h3 style="color:#ff6a00;margin-top:10px">පැතිකඩ ලියාපදිංචිය ♾</h3></div>
    <input id="regName" class="input" placeholder="Full Name *"><input id="regUsername" class="input" placeholder="Username @*"><textarea id="regBio" class="input" rows="2" placeholder="Bio / Description"></textarea><input type="file" id="regPic" accept="image/*" class="input">
    <button class="btn btn-green" onclick="completeDirectReg()">Save Profile & Enter ♾️</button><button class="btn btn-gray" onclick="closeReg()">Close</button>
  </div>
</div>
<script>
let currentUser = JSON.parse(localStorage.getItem('myface_profile_v4') || 'null') || {name: 'සුමින්ද රණවීර', username: '@sumiya', pic: 'https://i.pravatar.cc/100?img=12', bio: 'World Class Developer & Creator'};
document.getElementById('myAvatar').src = currentUser.pic;
let popupTimer;
let globalPostsCache = [];
async function loadDataAndRender() {
  try {
    let res = await fetch('/api/get_data');
    let data = await res.json();
    globalPostsCache = data.posts || [];
    renderStories(data.stories || []);
    renderFeed(globalPostsCache);
    window.appGlobalData = data;
  } catch(err) { console.error("Data load failed:", err); }
}
setInterval(loadDataAndRender, 3000);
function openMenu() { document.getElementById('menu').style.display = 'block'; }
function closeMenu() { document.getElementById('menu').style.display = 'none'; }
function openPost() { document.getElementById('postModal').style.display = 'flex'; }
function closePost() { document.getElementById('postModal').style.display = 'none'; }
function openReg() { document.getElementById('regModal').style.display = 'flex'; }
function closeReg() { document.getElementById('regModal').style.display = 'none'; }
function openChatModal() { document.getElementById('chatModal').style.display = 'flex'; }
function closeChatModal() { document.getElementById('chatModal').style.display = 'none'; }
function toggleSearchModal() { let box = document.getElementById('searchDropdown'); box.style.display = box.style.display === 'flex'? 'none' : 'flex'; }
function toggleNotifModal() { let box = document.getElementById('notifDropdown'); box.style.display = box.style.display === 'flex'? 'none' : 'flex'; }
function escapeHtml(text) { if (!text) return ''; return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;"); }
function filterPosts(query) {
  let list = document.getElementById('searchResultsList');
  if(!query.trim()) { list.innerHTML = "Type to search..."; return; }
  let filtered = globalPostsCache.filter(p => (p.text && p.text.toLowerCase().includes(query.toLowerCase())) || p.user.toLowerCase().includes(query.toLowerCase()));
  if(filtered.length === 0) { list.innerHTML = "<div style='padding:6px;'>No results found.</div>"; return; }
  list.innerHTML = filtered.map(p => `<div style="padding:6px;border-bottom:1px solid var(--border);cursor:pointer;" onclick="toggleSearchModal()"><b>${escapeHtml(p.user)}:</b> ${escapeHtml(p.text? p.text.substring(0,40) + '...' : '[Media Post]')}</div>`).join('');
}
function sendChatMessage() {
  let input = document.getElementById('chatInput'); let text = input.value.trim(); if(!text) return;
  let chatBody = document.getElementById('chatMessages');
  chatBody.innerHTML += `<div style="background:var(--orange);color:white;padding:8px 12px;border-radius:12px;font-size:13px;align-self:flex-end;max-width:80%">${escapeHtml(text)}</div>`;
  input.value = ''; chatBody.scrollTop = chatBody.scrollHeight;
  setTimeout(() => { chatBody.innerHTML += `<div style="background:white;padding:8px 12px;border-radius:12px;font-size:13px;align-self:flex-start;box-shadow:0 1px 2px rgba(0,0,0,0.1);max-width:80%">තොරතුරු ලැබුණි! ස්තුතියි. 👍</div>`; chatBody.scrollTop = chatBody.scrollHeight; }, 1000);
}
function changeLanguagePrompt() { let lang = prompt("භාෂාව තෝරන්න (Select Language):\\n1. සිංහල\\n2. English\\n3. Tamil", "1"); if(lang) alert("✅ භාෂාව වෙනස් කරන ලදී."); }
async function nav(name, el) {
  document.getElementById('home').style.display = name === 'home'? 'block' : 'none';
  document.getElementById('other').style.display = name!== 'home'? 'block' : 'none';
  let other = document.getElementById('otherText');
  if (name === 'profile') {
    let p = currentUser;
    other.innerHTML = `<div class="profile-header"><img class="profile-pic" src="${p.pic}"></div><div style="margin-top:50px;padding:0 12px"><h2>${escapeHtml(p.name)} ✅</h2><p style="color:#65676b">${escapeHtml(p.username)} • ${escapeHtml(p.bio || '')}</p><div style="display:flex;gap:12px;margin-top:10px"><b>♾ Unlimited Storage & 24/7 Live SQLite Engine</b></div></div>`;
  } else if (name === 'reels') {
    let res = await fetch('/api/get_data'); let data = await res.json();
    let reelsHtml = `<h3 style="margin-bottom:12px">🎬 Reels - Short Videos</h3>`;
    (data.reels || []).forEach(r => { reelsHtml += `<div style="background:black;border-radius:12px;margin-bottom:12px;overflow:hidden;position:relative;"><video src="${r.video}" controls style="width:100%;max-height:450px;display:block;"></video><div style="padding:10px;color:white;display:flex;align-items:center;gap:10px;"><img src="${r.pic}" style="width:35px;height:35px;border-radius:50%;object-fit:cover;"><div><b>${escapeHtml(r.user)}</b><p style="font-size:12px;color:#ccc">${escapeHtml(r.caption)}</p></div></div></div>`; });
    other.innerHTML = reelsHtml;
  } else if (name === 'shop') {
    let res = await fetch('/api/get_data'); let data = await res.json();
    let shopHtml = `<h3 style="margin-bottom:12px">🛍️ Marketplace Shop</h3><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">`;
    (data.shop || []).forEach(item => { shopHtml += `<div style="background:white;border-radius:8px;padding:8px;border:1px solid var(--border);"><img src="${item.image}" style="width:100%;height:140px;object-fit:cover;border-radius:6px;"><h4 style="font-size:14px;margin-top:6px">${escapeHtml(item.title)}</h4><p style="color:var(--orange);font-weight:bold;font-size:13px">${escapeHtml(item.price)}</p><button class="btn" style="padding:6px;font-size:12px;margin-top:6px" onclick="alert('Item ordered successfully!')">Buy Now</button></div>`; });
    shopHtml += `</div>`; other.innerHTML = shopHtml;
  } else { other.innerHTML = `<h3>${name.toUpperCase()} - Unlimited ♾</h3><p>24/7 SQLite Server Engine Active.</p>`; }
  if (el) { document.querySelectorAll('.sub-nav i').forEach(i => i.classList.remove('active')); el.classList.add('active'); }
}
let tempPostMedia = null; let tempPostMediaType = 'image';
document.getElementById('postFile').addEventListener('change', e => {
  let f = e.target.files[0]; if (!f) return;
  let r = new FileReader();
  r.onload = ev => {
    tempPostMedia = ev.target.result; let container = document.getElementById('mediaPreviewContainer');
    if (f.type.includes('video')) { tempPostMediaType = 'video'; container.innerHTML = `<video src="${tempPostMedia}" controls style="width:100%;max-height:250px;border-radius:8px;"></video>`; }
    else if (f.type.includes('audio')) { tempPostMediaType = 'audio'; container.innerHTML = `<audio src="${tempPostMedia}" controls style="width:100%;margin-top:10px;"></audio>`; }
    else { tempPostMediaType = 'image'; container.innerHTML = `<img src="${tempPostMedia}" style="width:100%;max-height:250px;object-fit:contain;border-radius:8px;">`; }
  }; r.readAsDataURL(f);
});
document.getElementById('storyFile').addEventListener('change', e => {
  let f = e.target.files[0]; if (!f) return;
  let r = new FileReader();
  r.onload = ev => {
    let isVideo = f.type.includes('video');
    if (isVideo) { let vp = document.getElementById('storyVideoPreview'); vp.src = ev.target.result; vp.style.display = 'block'; document.getElementById('storyPreview').style.display = 'none'; vp.dataset.data = ev.target.result; vp.dataset.type = 'video'; }
    else { let ip = document.getElementById('storyPreview'); ip.src = ev.target.result; ip.style.display = 'block'; document.getElementById('storyVideoPreview').style.display = 'none'; ip.dataset.data = ev.target.result; ip.dataset.type = 'image'; }
  }; r.readAsDataURL(f);
});
document.getElementById('regPic').addEventListener('change', e => {
  let f = e.target.files[0]; if(!f) return;
  let r = new FileReader(); r.onload = ev => { document.getElementById('regAvatarPreview').src = ev.target.result; localStorage.setItem('myface_regpic', ev.target.result); }; r.readAsDataURL(f);
});
async function doPost() {
  let text = document.getElementById('postText').value.trim();
  if (!text &&!tempPostMedia) { alert('කරුණාකර සටහනක් හෝ මාධ්‍ය/සංගීත ගොනුවක් ඇතුළත් කරන්න!'); return; }
  let np = { id: Date.now(), user: currentUser.name, pic: currentUser.pic, text: text, media: tempPostMedia, mediaType: tempPostMediaType, reactions: {"like": 0, "love": 0, "care": 0, "haha": 0, "wow": 0, "sad": 0, "angry": 0}, myReaction: null, comments: [], shares: 0, time: 'මිනිත්තු කිහිපයකට පෙර' };
  await fetch('/api/add_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(np) });
  closePost(); document.getElementById('postText').value = ''; document.getElementById('postFile').value = ''; document.getElementById('mediaPreviewContainer').innerHTML = ''; tempPostMedia = null; loadDataAndRender();
}
async function deletePost(postId) {
  if(!confirm("මෙම පෝස්ට් එක ඉවත් කිරීමට අවශ්‍ය බව ස්ථිරද?")) return;
  let response = await fetch('/api/delete_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: postId }) });
  let result = await response.json(); if(result.status === 'success') { loadDataAndRender(); }
}
async function publishStory() {
  let caption = document.getElementById('storyCaption').value.trim();
  let ip = document.getElementById('storyPreview'); let vp = document.getElementById('storyVideoPreview');
  let mediaData = null, mediaType = 'image';
  if (ip.style.display!== 'none') { mediaData = ip.dataset.data; mediaType = 'image'; }
  else if (vp.style.display!== 'none') { mediaData = vp.dataset.data; mediaType = 'video'; }
  if (!mediaData) { alert('පින්තූරයක් හෝ වීඩියෝවක් තෝරන්න!'); return; }
  let ns = { id: Date.now(), user: currentUser.name, userPic: currentUser.pic, caption: caption, media: mediaData, mediaType: mediaType, timestamp: Date.now(), likes: 0, comments: [], shares: 0, liked: false };
  await fetch('/api/add_story', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(ns) });
  document.getElementById('storyModal').style.display = 'none'; document.getElementById('storyCaption').value = ''; document.getElementById('storyFile').value = ''; ip.style.display = 'none'; vp.style.display = 'none'; loadDataAndRender(); alert('✅ ස්ටේටස් එක එකතු විය!');
}
function renderStories(stories) {
  let s = document.getElementById('stories');
  let h = `<div class="story story-create" onclick="document.getElementById('storyModal').style.display='flex'"><img class="story-user-bg" src="${currentUser.pic}"><div class="plus-overlay">+</div><div class="story-name-bottom">Create story</div></div>`;
  stories.forEach(st => { let previewMedia = st.mediaType === 'video'? `<video src="${st.media}"></video>` : `<img src="${st.media}">`; h += `<div class="story" onclick="viewStory(${st.id})">${previewMedia}<div class="story-name">${escapeHtml(st.user)}</div></div>`; });
  s.innerHTML = h;
}
async function viewStory(id) {
  let res = await fetch('/api/get_data'); let data = await res.json(); let st = data.stories.find(x => x.id === id); if (!st) return;
  let viewer = document.getElementById('storyViewer'); let content = document.getElementById('storyViewerContent');
  let mediaTag = st.mediaType === 'video'? `<video src="${st.media}" controls autoplay style="width:100%;height:100%;object-fit:contain;"></video>` : `<img src="${st.media}" style="width:100%;height:100%;object-fit:contain;">`;
  content.innerHTML = `<div style="position:absolute;top:10px;left:10px;display:flex;align-items:center;gap:8px;z-index:9500;"><img src="${st.userPic}" style="width:35px;height:35px;border-radius:50%;object-fit:cover;border:2px solid var(--orange)"><span style="color:white;font-weight:bold;">${escapeHtml(st.user)}</span></div><div style="width:100%;height:65vh;display:flex;justify-content:center;align-items:center;background:#111;">${mediaTag}</div>${st.caption? `<div style="color:white;padding:8px;text-align:center;">${escapeHtml(st.caption)}</div>` : ''}`;
  viewer.style.display = 'flex';
}
function closeStoryViewer() { document.getElementById('storyViewer').style.display = 'none'; }
function closeStoryModal() { document.getElementById('storyModal').style.display = 'none'; }
function completeDirectReg() {
  let name = document.getElementById('regName').value.trim(); let username = document.getElementById('regUsername').value.trim();
  if (!name ||!username) { alert('නම සහ Username අවශ්‍යයි!'); return; }
  currentUser = { name: name, username: username, bio: document.getElementById('regBio').value, pic: localStorage.getItem('myface_regpic') || currentUser.pic };
  localStorage.setItem('myface_profile_v4', JSON.stringify(currentUser)); document.getElementById('myAvatar').src = currentUser.pic; closeReg(); alert('✅ සාර්ථකයි!');
}
function showPopup(id) { clearTimeout(popupTimer); document.getElementById('popup-' + id).style.display = 'flex'; }
function hidePopup(id) { popupTimer = setTimeout(() => { document.getElementById('popup-' + id).style.display = 'none'; }, 400); }
async function sendReaction(postId, reactionType) {
  document.getElementById('popup-' + postId).style.display = 'none';
  let response = await fetch('/api/update_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: postId, type: 'reaction', payload: { reaction: reactionType } }) });
  let result = await response.json(); if(result.status === 'success') { updatePostUI(result.post); }
}
function toggleLike(postId) { sendReaction(postId, 'like'); }
async function nativeShare(postId) {
  let shareData = { title: 'My Face Box', text: 'මෙන්න පෝස්ට් එකක්!', url: window.location.href };
  if (navigator.share) {
    try { await navigator.share(shareData); let response = await fetch('/api/update_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: postId, type: 'share' }) }); let result = await response.json(); if(result.status === 'success') updatePostUI(result.post); } catch (err) {}
  } else { let response = await fetch('/api/update_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: postId, type: 'share' }) }); let result = await response.json(); if(result.status === 'success') { updatePostUI(result.post); alert('Share count updated!'); } }
}
async function addComment(postId) {
  let input = document.getElementById('c-input-' + postId); let text = input.value.trim(); if(!text) return;
  let response = await fetch('/api/update_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: postId, type: 'comment', payload: { comment: { user: currentUser.name, text: text } } }) });
  let result = await response.json(); if(result.status === 'success') { input.value = ''; updatePostUI(result.post); }
}
function updatePostUI(post) {
  let totalReactions = Object.values(post.reactions).reduce((a, b) => a + b, 0);
  document.getElementById(`total-reacts-${post.id}`).innerText = totalReactions > 0? totalReactions : '';
  document.getElementById(`share-count-${post.id}`).innerText = post.shares;
  document.getElementById(`comment-count-${post.id}`).innerText = post.comments.length;
  let miniHtml = '';
  if(post.reactions.like > 0) miniHtml += `<span class="mini-reaction" style="background:#1877f2"><i class="fa-solid fa-thumbs-up"></i></span>`;
  if(post.reactions.love > 0) miniHtml += `<span class="mini-reaction" style="background:#e41e3f"><i class="fa-solid fa-heart"></i></span>`;
  if(post.reactions.care > 0) miniHtml += `<span class="mini-reaction" style="background:#f7b928">🥰</span>`;
  if(post.reactions.haha > 0) miniHtml += `<span class="mini-reaction" style="background:#f7b928">😆</span>`;
  document.getElementById(`mini-icons-${post.id}`).innerHTML = miniHtml;
  let btn = document.getElementById(`like-btn-${post.id}`); let text = document.getElementById(`like-text-${post.id}`); let icon = document.getElementById(`like-icon-${post.id}`);
  if(post.myReaction) { btn.classList.add('reacted'); text.innerText = post.myReaction.toUpperCase(); icon.className = "fa-solid fa-thumbs-up"; }
  else { btn.classList.remove('reacted'); text.innerText = "Like"; icon.className = "fa-regular fa-thumbs-up"; }
  let commentContainer = document.getElementById(`comments-list-${post.id}`);
  commentContainer.innerHTML = post.comments.map(c => `<div style="background:#f0f2f5;border-radius:12px;padding:6px 10px;margin:4px 0;font-size:13px"><b>${escapeHtml(c.user)}:</b> ${escapeHtml(c.text)}</div>`).join('');
}
function renderFeed(posts) {
  let feed = document.getElementById('feed');
  if (!feed) return;
  
  feed.innerHTML = posts.map(p => {
    let reactions = p.reactions || {like: 0, love: 0, care: 0, haha: 0};
    let totalReactions = Object.values(reactions).reduce((a, b) => a + b, 0);
    
    let miniHtml = '';
    if(reactions.like > 0) miniHtml += `<span class="mini-reaction" style="background:#1877f2"><i class="fa-solid fa-thumbs-up"></i></span>`;
    if(reactions.love > 0) miniHtml += `<span class="mini-reaction" style="background:#e41e3f"><i class="fa-solid fa-heart"></i></span>`;
    if(reactions.care > 0) miniHtml += `<span class="mini-reaction" style="background:#f7b928">🥰</span>`;
    if(reactions.haha > 0) miniHtml += `<span class="mini-reaction" style="background:#f7b928">😆</span>`;
    
    let mediaContent = '';
    let mediaUrl = p.media_url || p.media;
    let mediaType = p.media_type || p.mediaType;
    
    if (mediaUrl) {
      let downloadBtn = `<br><a href="${mediaUrl}" download="FaceBox_Media_${p.id}" target="_blank" class="download-btn" style="display:inline-flex; align-items: center; gap: 5px; background: rgba(0,0,0,0.05); color: #050505; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: 600; margin-top: 8px; cursor: pointer;"><i class="fa-solid fa-download"></i> Download Media</a>`;
      if (mediaType === 'video') mediaContent = `<video src="${mediaUrl}" controls style="width:100%; border-radius:8px; margin-top:8px;"></video>${downloadBtn}`;
      else if (mediaType === 'audio') mediaContent = `<audio src="${mediaUrl}" controls style="width:100%; padding:5px; margin-top:8px;"></audio>${downloadBtn}`;
      else mediaContent = `<img src="${mediaUrl}" style="width:100%; border-radius:8px; margin-top:8px;">${downloadBtn}`;
    }
    
    let commentsList = Array.isArray(p.comments) ? p.comments : [];
    let userAvatar = (typeof currentUser !== 'undefined' && currentUser.pic) ? currentUser.pic : 'https://pravatar.cc';
    
    return `
      <div class="card" style="background:var(--card); border-radius:8px; padding:12px; margin-bottom:12px; box-shadow:0 1px 2px rgba(0,0,0,0.1); position:relative;">
        <div class="post-head" style="display:flex; justify-content:space-between; align-items:center;">
          <div style="display:flex; gap:10px; align-items:center;">
            <img class="avatar" style="width:40px; height:40px; border-radius:50%;" src="${p.profile_pic || p.pic || 'https://pravatar.cc'}">
            <div>
              <b>${escapeHtml(p.user_name || p.user || 'Anonymous')}</b><br>
              <small>${escapeHtml(p.time || 'Just now')}</small>
            </div>
          </div>
          <i class="fa-solid fa-trash" style="color:#65676b; cursor:pointer; padding:8px;" onclick="deletePost(${p.id})" title="Delete Post"></i>
        </div>
        ${p.text ? `<div class="post-text" style="margin-top:8px; font-size:14px;">${escapeHtml(p.text)}</div>` : ''}
        ${mediaUrl ? `<div class="post-media">${mediaContent}</div>` : ''}

        <div class="post-stats" style="display:flex; justify-content:space-between; margin-top:12px; font-size:13px; color:#65676B; padding-bottom:8px; border-bottom:1px solid #E4E6EB;">
          <div style="display:flex; align-items:center; gap:5px;">
            <div class="reaction-icons-group">${miniHtml}</div>
            <span>${totalReactions > 0 ? totalReactions : '0'} Likes</span>
          </div>
          <div><span>${commentsList.length}</span> Comments • <span>${p.shares || 0}</span> Shares</div>
        </div>
        <div class="post-actions" style="display:flex; justify-content:space-around; padding-top:4px; position:relative; border-top:1px solid #E4E6EB; margin-top:8px;">
          <div class="reaction-popup" id="popup-${p.id}" style="position:absolute; top:-45px; left:10px; background:white; border-radius:24px; padding:4px 8px; box-shadow:0 4px 12px rgba(0,0,0,0.15); gap:12px; z-index:10;">
            <span onclick="sendReaction(${p.id}, 'like')" style="font-size:22px; cursor:pointer;">👍</span>
            <span onclick="sendReaction(${p.id}, 'love')" style="font-size:22px; cursor:pointer;">❤️</span>
            <span onclick="sendReaction(${p.id}, 'care')" style="font-size:22px; cursor:pointer;">🥰</span>
            <span onclick="sendReaction(${p.id}, 'haha')" style="font-size:22px; cursor:pointer;">😆</span>
          </div>
          <button id="like-btn-${p.id}" onclick="toggleLike(${p.id})" style="flex:1; background:none; border:none; padding:8px; color:#65676B; font-weight:600; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; font-size:13px;"><i class="fa-regular fa-thumbs-up"></i> Like</button>
          <button onclick="document.getElementById('c-input-${p.id}').focus()" style="flex:1; background:none; border:none; padding:8px; color:#65676B; font-weight:600; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; font-size:13px;"><i class="fa-regular fa-comment"></i> Comment</button>
          <button onclick="nativeShare(${p.id})" style="flex:1; background:none; border:none; padding:8px; color:#65676B; font-weight:600; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px; font-size:13px;"><i class="fa-solid fa-share"></i> Share</button>
        </div>
        <div class="comment-box" style="display:flex; gap:8px; align-items:center; margin-top:8px; padding-top:8px;">
          <img class="avatar" style="width:32px; height:32px; border-radius:50%;" src="${userAvatar}">
          <input id="c-input-${p.id}" style="flex:1; background:#F0F2F5; border:none; padding:8px 12px; border-radius:18px; font-size:13px; outline:none;" placeholder="Write a comment..." onkeydown="if(event.key==='Enter') addComment(${p.id})">
        </div>
        <div style="padding:0 12px 10px" id="comments-list-${p.id}">
          \${commentsList.map(c => `<div style="background:#f0f2f5; border-radius:12px; padding:6px 10px; margin:4px 0; font-size:13px"><b>${escapeHtml(c.user || 'User')}:</b> ${escapeHtml(c.text || c)}</div>`).join('')}
        </div>
      </div>
    `;
  }).join('');
}

window.onload = function() { loadDataAndRender(); };
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/get_data')
def get_data():
    return jsonify(load_data())

@app.route('/api/add_post', methods=['POST'])
def add_post():
    try:
        p = request.get_json()
        if not p: return jsonify({"status": "error", "message": "Invalid data"}), 400
        data = load_data()
        posts = data.get("posts", [])
        posts.insert(0, p)
        save_data_key("posts", posts)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/delete_post', methods=['POST'])
def delete_post():
    try:
        req = request.get_json()
        post_id = req.get("id")
        data = load_data()
        posts = [p for p in data.get("posts", []) if p["id"]!= post_id]
        save_data_key("posts", posts)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/add_story', methods=['POST'])
def add_story():
    try:
        st = request.get_json()
        if not st: return jsonify({"status": "error", "message": "Invalid data"}), 400
        data = load_data()
        stories = data.get("stories", [])
        stories.insert(0, st)
        save_data_key("stories", stories)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/update_post', methods=['POST'])
def update_post():
    try:
        req_data = request.get_json()
        post_id = req_data.get("id")
        action_type = req_data.get("type")
        payload = req_data.get("payload")
        data = load_data()
        posts = data.get("posts", [])
        post = next((p for p in posts if p["id"] == post_id), None)
        if not post: return jsonify({"status": "error", "message": "Post not found"}), 404
        if "reactions" not in post:
            post["reactions"] = {"like": 0, "love": 0, "care": 0, "haha": 0, "wow": 0, "sad": 0, "angry": 0}
        if action_type == "reaction":
            old_react = post.get("myReaction")
            new_react = payload.get("reaction")
            if old_react and old_react in post["reactions"]:
                post["reactions"][old_react] = max(0, post["reactions"][old_react] - 1)
            if old_react == new_react:
                post["myReaction"] = None
            else:
                post["myReaction"] = new_react
                if new_react in post["reactions"]:
                    post["reactions"][new_react] += 1
        elif action_type == "comment":
            if "comments" not in post: post["comments"] = []
            post["comments"].append(payload.get("comment"))
        elif action_type == "share":
            post["shares"] = post.get("shares", 0) + 1
        save_data_key("posts", posts)
        return jsonify({"status": "success", "post": post})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("MY FACE BOX 24/7 UNLIMITED LIVE SERVER RUNNING...")
    app.run(host='0.0.0.0', port=5000, debug=True)


# =================================================================
# 🎯 1. ඩේටාබේස් එක ඇතුළේ පෝස්ට්, ලයික් සහ කමෙන්ට් වගු (Tables) සෑදීම
# =================================================================
def init_social_tables():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            profile_pic TEXT,
            content TEXT,
            media_url TEXT,
            media_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS post_likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_name TEXT,
            UNIQUE(post_id, user_name)
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS post_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_name TEXT,
            comment_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database Init Error:", str(e))

init_social_tables()

# =================================================================
# 🎯 2. සැබෑ ලෙස පෝස්ට් එකක් අප්ලෝඩ් (Create Post) කරන Route එක
# =================================================================
@app.route('/api/create_post', methods=['POST'])
def create_new_social_post():
    try:
        data = request.json
        user_name = data.get('user_name', 'Sumiya. M.R.A')
        profile_pic = data.get('profile_pic', 'https://pravatar.cc')
        content = data.get('content', '')
        media_url = data.get('media_url', '')
        media_type = data.get('media_type', 'image')

        if not content and not media_url:
            return jsonify({"status": "error", "message": "Post cannot be empty"})

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_posts (user_name, profile_pic, content, media_url, media_type) VALUES (?, ?, ?, ?, ?)",
            (user_name, profile_pic, content, media_url, media_type)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Post uploaded successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# =================================================================
# 🎯 3. ලයික් එකක් දාන සහ අයින් කරන (Toggle Like) Route එක
# =================================================================
@app.route('/api/like_post', methods=['POST'])
def toggle_post_like():
    try:
        data = request.json
        post_id = data.get('post_id')
        user_name = data.get('user_name', 'Sumiya. M.R.A')

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM post_likes WHERE post_id = ? AND user_name = ?", (post_id, user_name))
        row = cursor.fetchone()
        
        if row:
            cursor.execute("DELETE FROM post_likes WHERE post_id = ? AND user_name = ?", (post_id, user_name))
            action = "unliked"
        else:
            cursor.execute("INSERT INTO post_likes (post_id, user_name) VALUES (?, ?)", (post_id, user_name))
            action = "liked"
            
        conn.commit()
        cursor.execute("SELECT COUNT(id) FROM post_likes WHERE post_id = ?", (post_id,))
        like_count = cursor.fetchone()[0]
        
        conn.close()
        return jsonify({"status": "success", "action": action, "likes": like_count})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# =================================================================
# 🎯 4. කමෙන්ට් එකක් සර්වර් එකට අප්ලෝඩ් කරන Route එක
# =================================================================
@app.route('/api/comment_post', methods=['POST'])
def add_post_comment():
    try:
        data = request.json
        post_id = data.get('post_id')
        user_name = data.get('user_name', 'Sumiya. M.R.A')
        comment_text = data.get('comment_text', '')

        if not comment_text.strip():
            return jsonify({"status": "error", "message": "Comment cannot be empty"})

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO post_comments (post_id, user_name, comment_text) VALUES (?, ?, ?)",
            (post_id, user_name, comment_text)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Comment added successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



if __name__ == '__main__':
    init_db()
    print("MY FACE BOX 24/7 UNLIMITED LIVE SERVER RUNNING...")
    app.run(host='0.0.0.0', port=5000, debug=False)

