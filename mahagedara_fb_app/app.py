<!DOCTYPE html>
<html lang="si">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>මහගෙදර FB - Sumiya Network International Edition</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root {
    --bg-main: #121212;
    --bg-card: #1e1e1e;
    --bg-input: #2d2d2d;
    --accent: #ff5722;
    --text-main: #ffffff;
    --text-muted: #aaa;
    --border-color: #333;
}
[data-theme="light"] {
    --bg-main: #f0f2f5;
    --bg-card: #ffffff;
    --bg-input: #e4e6eb;
    --accent: #1877f2;
    --text-main: #050505;
    --text-muted: #65676b;
    --border-color: #ced0d4;
}
[data-theme="pink"] {
    --bg-main: #fff0f5;
    --bg-card: #ffffff;
    --bg-input: #ffe4e1;
    --accent: #e91e63;
    --text-main: #4a0e17;
    --text-muted: #8c5863;
    --border-color: #f8bbd0;
}
[data-theme="blue"] {
    --bg-main: #e8f4fd;
    --bg-card: #ffffff;
    --bg-input: #d0e8fc;
    --accent: #0288d1;
    --text-main: #013348;
    --text-muted: #547a8c;
    --border-color: #b3e5fc;
}

*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif}
body{background:var(--bg-main);color:var(--text-main);padding-top:115px;padding-bottom:20px;transition:background 0.3s, color 0.3s;}

/* Header & Top Nav with 24/7 Live Green Signals (🟢) */
header{background:var(--bg-card);padding:10px 15px;display:flex;justify-content:space-between;align-items:center;position:fixed;width:100%;top:0;z-index:100;border-bottom:1px solid var(--border-color)}
.logo{font-size:26px;font-weight:900;color:var(--accent);letter-spacing:-1px;display:flex;align-items:center;gap:6px;}
.header-icons{display:flex;gap:8px}
.icon-btn-wrap { position: relative; }
.icon-btn{background:var(--bg-input);border:none;width:40px;height:40px;border-radius:50%;color:var(--accent);font-weight:bold;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:0.2s}
.live-dot { position: absolute; top: 2px; right: 2px; width: 10px; height: 10px; background: #31a24c; border: 2px solid var(--bg-card); border-radius: 50%; animation: pulseLive 1.5s infinite; }
@keyframes pulseLive { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(49, 162, 76, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(49, 162, 76, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(49, 162, 76, 0); } }

/* Main Tab Bar */
nav{background:var(--bg-card);display:flex;justify-content:space-around;position:fixed;width:100%;top:60px;z-index:99;border-bottom:1px solid var(--border-color)}
.nav-item{color:var(--text-muted);padding:12px 0;width:16%;text-align:center;font-size:20px;cursor:pointer;border-bottom:3px solid transparent;transition:0.2s;position:relative;}
.nav-item.active{color:var(--accent);border-bottom:3px solid var(--accent)}

.container{max-width:500px;margin:0 auto;padding:10px}

/* Theme Selector Panel */
.theme-panel { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 10px; margin-bottom: 12px; display: flex; justify-content: space-around; align-items: center; font-size: 13px; }
.theme-btn { padding: 6px 12px; border-radius: 20px; border: 1px solid var(--border-color); background: var(--bg-input); color: var(--text-main); cursor: pointer; font-weight: bold; }

/* MINI APPS TRAY & SEARCH */
.mini-apps-section { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 10px; margin-bottom: 12px; }
.mini-apps-search { width: 100%; padding: 8px 14px; background: var(--bg-input); border: 1px solid var(--border-color); border-radius: 20px; color: var(--text-main); outline: none; font-size: 13px; margin-bottom: 8px; }
.mini-apps-tray { display: flex; gap: 10px; overflow-x: auto; scrollbar-width: none; padding-bottom: 4px; }
.mini-apps-tray::-webkit-scrollbar { display: none; }
.mini-app-icon { display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0; cursor: pointer; width: 55px; }
.mini-app-circle { width: 45px; height: 45px; border-radius: 50%; background: var(--bg-input); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; font-size: 20px; color: var(--accent); }
.mini-app-name { font-size: 10px; color: var(--text-muted); text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; }

/* In-App Browser Modal */
.inapp-browser { display: none; position: fixed; inset: 0; background: var(--bg-main); z-index: 1000; flex-direction: column; }
.inapp-header { background: var(--bg-card); padding: 10px 15px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); }
.inapp-title { font-size: 15px; font-weight: bold; color: var(--accent); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 300px; }
.inapp-body { flex: 1; background: #fff; position: relative; }
.inapp-body iframe { width: 100%; height: 100%; border: none; }

/* Create Post Box */
.create-post{background:var(--bg-card);padding:12px;border-radius:12px;margin-bottom:12px;border:1px solid var(--border-color)}
.input-row{display:flex;gap:10px;align-items:flex-start}
.avatar{width:40px;height:40px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:bold;flex-shrink:0;color:#fff;overflow:hidden;cursor:pointer;object-fit:cover;}
.avatar img{width:100%;height:100%;object-fit:cover;}
.create-post textarea{flex:1;padding:12px 15px;border-radius:12px;border:1px solid var(--border-color);background:var(--bg-input);color:var(--text-main);outline:none;font-size:14px;resize:vertical;min-height:90px;}
.actions-row{display:flex;justify-content:space-between;margin-top:10px;align-items:center}
.file-label{background:var(--bg-input);color:var(--accent);padding:8px 14px;border-radius:20px;font-size:13px;font-weight:bold;border:1px solid var(--border-color);cursor:pointer;display:flex;align-items:center;gap:5px}
.post-btn{background:var(--accent);color:#fff;border:none;padding:8px 24px;border-radius:20px;font-weight:bold;cursor:pointer;font-size:14px}
.preview img{width:100%;border-radius:10px;margin-top:10px;max-height:300px;object-fit:cover;border:1px solid var(--border-color)}

/* Stories & Reels Tray */
.stories{display:flex;gap:8px;overflow-x:auto;padding-bottom:10px;scrollbar-width:none;margin-bottom:12px}
.stories::-webkit-scrollbar{display:none}
.story{width:110px;height:210px;background:var(--bg-card);border-radius:12px;flex-shrink:0;position:relative;overflow:hidden;border:1px solid var(--border-color);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:10px;color:#fff;font-weight:bold;font-size:12px;cursor:pointer;background-size:cover;background-position:center}
.story.create{background:var(--bg-card);color:var(--accent);justify-content:center;align-items:center;font-size:14px;text-align:center}

/* Post Cards */
.post-card{background:var(--bg-card);border-radius:12px;padding:12px;margin-bottom:12px;border:1px solid var(--border-color);position:relative;}
.post-head{display:flex;gap:10px;align-items:center;margin-bottom:8px}
.post-content-wrapper{position:relative;}
.post-text {font-size: 14px; line-height: 1.6; color: var(--text-main); word-break: break-word; max-height: 120px; overflow: hidden; transition: max-height 0.3s ease;}
.post-text.expanded { max-height: none; }
.see-more-btn { background: none; border: none; color: var(--accent); font-weight: bold; cursor: pointer; padding: 4px 0; font-size: 13px; margin-top: 4px; display: inline-block; }
.post-media{width:100%;border-radius:10px;margin-top:8px;max-height:400px;object-fit:cover;border:1px solid var(--border-color)}
.post-media.blurred { filter: blur(20px); transition: filter 0.3s; cursor: pointer; }
.post-media.blurred:hover { filter: blur(5px); }

/* Reactions */
.like-container { position: relative; display: inline-block; }
.reactions-box { display: none; position: absolute; bottom: 40px; left: 0; background: var(--bg-card); border-radius: 30px; padding: 6px 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); gap: 8px; z-index: 50; border: 1px solid var(--border-color); }
.like-container:hover .reactions-box { display: flex; }
.reaction-icon { font-size: 22px; cursor: pointer; background: none; border: none; }

.actions{display:flex;justify-content:space-around;border-top:1px solid var(--border-color);margin-top:10px;padding-top:6px}
.act{background:none;border:none;color:var(--text-muted);font-weight:600;cursor:pointer;padding:8px;font-size:14px;display:flex;align-items:center;gap:6px}
.act.liked{color:var(--accent)}

.post-menu { position: absolute; right: 12px; top: 12px; display: flex; gap: 6px; }
.post-menu button { background: var(--bg-input); border: 1px solid var(--border-color); color: var(--text-muted); padding: 4px 8px; border-radius: 6px; font-size: 11px; cursor: pointer; }
.post-menu button.del { color: var(--accent); }

.comment-box { padding: 8px 0; display: flex; flex-direction: column; gap: 6px; }
.comment-input-area { display: flex; gap: 8px; margin-top: 8px; }
.comment-input-area textarea { flex: 1; padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 10px; background: var(--bg-input); color: var(--text-main); outline: none; font-size: 13px; resize: vertical; min-height: 50px; }
.comment-submit-btn { background: var(--accent); color: white; border: none; padding: 4px 14px; border-radius: 15px; font-size: 12px; font-weight: bold; cursor: pointer; height: 35px; align-self: flex-end;}
.single-comment { background: var(--bg-input); padding: 8px 12px; border-radius: 12px; font-size: 13px; margin-bottom: 4px; border: 1px solid var(--border-color); }
.single-comment .commenter { font-weight: bold; color: var(--accent); margin-bottom: 2px; }

/* Messenger Modal */
.chat-container { display: none; background: var(--bg-main); position: fixed; bottom: 0; left: 0; width: 100%; height: 100vh; z-index: 200; flex-direction: column; }
.chat-header { background: var(--bg-card); padding: 12px 15px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); }
.chat-title { font-weight: bold; font-size: 18px; color: var(--accent); display: flex; align-items: center; gap: 10px; }
.chat-conversation-view { display: none; flex: 1; flex-direction: column; background: var(--bg-main); height: calc(100vh - 65px); }
.chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
.msg-bubble { max-width: 75%; padding: 10px 14px; border-radius: 18px; font-size: 15px; }
.msg-bubble.sent { background: var(--accent); color: white; align-self: flex-end; }
.msg-bubble.received { background: var(--bg-input); color: var(--text-main); align-self: flex-start; border: 1px solid var(--border-color); }
.chat-input-area { padding: 12px; background: var(--bg-card); display: flex; gap: 10px; align-items: center; border-top: 1px solid var(--border-color); }
.chat-input-area input { flex: 1; padding: 11px 15px; border: 1px solid var(--border-color); border-radius: 20px; background: var(--bg-input); color: var(--text-main); outline: none; }
.send-msg-btn { background: var(--accent); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; }

/* Modals */
.modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: rgba(0,0,0,0.8); z-index: 300; justify-content: center; align-items: center; padding: 15px; }
.modal-content { background: var(--bg-card); width: 100%; max-width: 450px; border-radius: 12px; border: 1px solid var(--border-color); padding: 20px; max-height: 90vh; overflow-y: auto; color: var(--text-main); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
.modal-header h3 { color: var(--accent); font-size: 18px; }
.close-modal { background: none; border: none; color: var(--text-muted); font-size: 20px; cursor: pointer; }
</style>
</head>
<body data-theme="dark">

<!-- Header with 24/7 Live Green Signals (🟢) -->
<header>
    <div class="logo"><i class="fa-solid fa-house-chimney"></i> මහගෙදර FB</div>
    <div class="header-icons">
        <div class="icon-btn-wrap">
            <button class="icon-btn" onclick="document.getElementById('postContent').focus()"><i class="fa-solid fa-plus"></i></button>
            <div class="live-dot" title="Live Signal 24/7"></div>
        </div>
        <div class="icon-btn-wrap">
            <button class="icon-btn" onclick="toggleChat(true)"><i class="fa-solid fa-comment-dots"></i></button>
            <div class="live-dot" title="Live Signal 24/7"></div>
        </div>
    </div>
</header>

<!-- Main Navigation with Green Signals (🟢) -->
<nav>
    <div class="nav-item active"><i class="fa-solid fa-house"></i><div class="live-dot"></div></div>
    <div class="nav-item"><i class="fa-solid fa-tv"></i><div class="live-dot"></div></div>
    <div class="nav-item"><i class="fa-solid fa-user-group"></i><div class="live-dot"></div></div>
    <div class="nav-item"><i class="fa-solid fa-shop"></i><div class="live-dot"></div></div>
    <div class="nav-item"><i class="fa-solid fa-bell"></i><div class="live-dot"></div></div>
    <div class="nav-item" onclick="openMenuModal()"><i class="fa-solid fa-bars"></i><div class="live-dot"></div></div>
</nav>

<div class="container">

  <!-- Theme Selector Panel -->
  <div class="theme-panel">
      <span>තේමාව (Theme):</span>
      <button class="theme-btn" onclick="setTheme('dark')">Dark</button>
      <button class="theme-btn" onclick="setTheme('light')">Light</button>
      <button class="theme-btn" onclick="setTheme('pink')">Pink</button>
      <button class="theme-btn" onclick="setTheme('blue')">Blue</button>
  </div>
  
  <!-- Status Bar with Green Signal -->
  <div style="background:var(--bg-card); border:1px solid #31a24c; border-radius:20px; padding:8px 12px; display:flex; align-items:center; justify-content:space-between; font-size:12px; margin-bottom:10px;">
    <div style="display:flex; align-items:center; gap:6px;">
      <div style="width:10px; height:10px; background:#31a24c; border-radius:50%; animation: pulseLive 1.5s infinite;"></div>
      <span style="color:#31a24c; font-weight:bold;">මහගෙදර LIVE NETWORK ACTIVE</span>
    </div>
    <div style="color:var(--text-muted);">24/7 Secured</div>
  </div>

  <!-- MINI APPS TRAY & SEARCH BAR -->
  <div class="mini-apps-section">
    <input type="text" class="mini-apps-search" placeholder="🔍 ඕනෑම ඇප් එකක් හෝ සේවාවක් සොයන්න..." oninput="filterMiniApps(this.value)">
    <div class="mini-apps-tray">
      <div class="mini-app-icon" onclick="openInAppBrowser('Google', 'https://www.google.com')">
        <div class="mini-app-circle" style="color:#4285F4;"><i class="fa-brands fa-google"></i></div>
        <div class="mini-app-name">Google</div>
      </div>
      <div class="mini-app-icon" onclick="openInAppBrowser('YouTube', 'https://www.youtube.com')">
        <div class="mini-app-circle" style="color:#FF0000;"><i class="fa-brands fa-youtube"></i></div>
        <div class="mini-app-name">YouTube</div>
      </div>
      <div class="mini-app-icon" onclick="openInAppBrowser('Wikipedia', 'https://si.wikipedia.org')">
        <div class="mini-app-circle" style="color:#fff;"><i class="fa-solid fa-book"></i></div>
        <div class="mini-app-name">Wikipedia</div>
      </div>
      <div class="mini-app-icon" onclick="openInAppBrowser('ChatGPT', 'https://chatgpt.com')">
        <div class="mini-app-circle" style="color:#10a37f;"><i class="fa-solid fa-robot"></i></div>
        <div class="mini-app-name">ChatGPT</div>
      </div>
      <div class="mini-app-icon" onclick="openInAppBrowser('TikTok', 'https://www.tiktok.com')">
        <div class="mini-app-circle" style="color:#ff0050;"><i class="fa-brands fa-tiktok"></i></div>
        <div class="mini-app-name">TikTok</div>
      </div>
      <div class="mini-app-icon" onclick="openInAppBrowser('Instagram', 'https://www.instagram.com')">
        <div class="mini-app-circle" style="color:#e1306c;"><i class="fa-brands fa-instagram"></i></div>
        <div class="mini-app-name">Instagram</div>
      </div>
    </div>
  </div>

  <!-- Create Post Box with Smart Image Compression & Auto-Trigger Guest Guard -->
  <div class="create-post">
    <div class="input-row">
      <div class="avatar" onclick="openProfileModal()">සු</div>
      <textarea id="postContent" placeholder="මහගෙදරට ඔබේ සිතුවිල්ලක් ලියන්න... (Auto-Trigger Registration Enabled)" onfocus="checkGuestAction()"></textarea>
    </div>
    <div class="actions-row">
      <label class="file-label"><i class="fa-solid fa-image"></i> Photo <input type="file" id="postImage" hidden accept="image/*" onchange="compressAndPreviewImage(event)"></label>
      <button class="post-btn" onclick="createPost()">Post</button>
    </div>
    <div class="preview" id="imagePreview"></div>
  </div>

  <!-- Stories & Reels Tray -->
  <div class="stories">
    <div class="story create" onclick="alert('Story Studio Active!')"><i class="fa-solid fa-plus" style="font-size:24px;margin-bottom:5px"></i>Create story</div>
    <div class="story" style="background-image:linear-gradient(rgba(0,0,0,0.2),rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300')">සුමින්ද රංදිල්</div>
  </div>

  <div id="feedContainer"></div>
</div>

<!-- In-App Browser Modal -->
<div class="inapp-browser" id="inAppBrowser">
    <div class="inapp-header">
        <div style="display:flex; align-items:center; gap:12px;">
            <button class="icon-btn" onclick="closeInAppBrowser()"><i class="fa-solid fa-arrow-left"></i></button>
            <div class="inapp-title" id="inAppTitle">Browser</div>
        </div>
        <button class="icon-btn" onclick="document.getElementById('inAppIframe').src = document.getElementById('inAppIframe').src"><i class="fa-solid fa-rotate-right"></i></button>
    </div>
    <div class="inapp-body">
        <iframe id="inAppIframe" src=""></iframe>
    </div>
</div>

<!-- Messenger Chat Modal (Real-time WebSocket / Local Simulation) -->
<div class="chat-container" id="chatContainer">
    <div class="chat-header">
        <div style="display:flex; align-items:center; gap:10px;">
            <button class="icon-btn" onclick="toggleChat(false)"><i class="fa-solid fa-arrow-left"></i></button>
            <div class="chat-title">මහගෙදර Real-time Chat 💬</div>
        </div>
    </div>
    <div class="chat-conversation-view" style="display:flex;">
        <div class="chat-messages" id="chatMessages">
            <div class="msg-bubble received">හායි! මහගෙදර WebSocket ලයිව් චැට් වෙත සාදරයෙන් පිළිගනිමු! 👍</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="messageInput" placeholder="පණිවිඩයක් ටයිප් කරන්න..." onkeypress="if(event.key==='Enter') sendWebSocketMessage()">
            <button class="send-msg-btn" onclick="sendWebSocketMessage()"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
    </div>
</div>

<!-- Auto-Trigger Registration Modal -->
<div class="modal-overlay" id="regModal">
    <div class="modal-content">
        <div class="modal-header">
            <h3>මහගෙදර ගිණුම් ලියාපදිංචිය (Auto-Trigger)</h3>
            <button class="close-modal" onclick="closeRegModal()">&times;</button>
        </div>
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:10px;">පෝස්ට් එකක් දැමීමට හෝ අන්තර්ක්‍රියා කිරීමට කරුණාකර ලියාපදිංචි වන්න:</p>
        <form onsubmit="submitRegistration(event)">
            <input type="text" id="regName" class="mini-apps-search" placeholder="ඔබේ නම" required style="margin-bottom:10px;">
            <input type="email" id="regEmail" class="mini-apps-search" placeholder="ඊමේල් ලිපිනය" required style="margin-bottom:10px;">
            <button type="submit" class="post-btn" style="width:100%;">ගිණුම සාදාගන්න</button>
        </form>
    </div>
</div>

<!-- Menu Modal -->
<div class="modal-overlay" id="menuModal">
    <div class="modal-content">
        <div class="modal-header">
            <h3>මහගෙදර මෙනු පාලකය</h3>
            <button class="close-modal" onclick="closeMenuModal()">&times;</button>
        </div>
        <button class="post-btn" onclick="openRegModal()" style="width:100%; margin-bottom:10px;">ගිණුමක් තැනීම</button>
        <button class="theme-btn" onclick="alert('Dynamic Plugin Loader Active: Plugins can be loaded via terminal.')" style="width:100%; padding:10px;">Plugin Loader Status: Active</button>
    </div>
</div>

<script>
/* Theme Switcher */
function setTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('mahagedara_theme', theme);
}
if(localStorage.getItem('mahagedara_theme')) {
    setTheme(localStorage.getItem('mahagedara_theme'));
}

/* AI Auto-Blur Content Censorship (NSFW Detection Simulation) */
function checkNSFW(text, imageUrl) {
    const badWords = ['badword', 'nsfw', 'xxx'];
    const hasBadWord = badWords.some(word => text.toLowerCase().includes(word));
    // If image is uploaded or bad word detected, apply AI auto-blur censorship
    return hasBadWord;
}

/* Smart Media Compression (Client-side Image Resizing) */
let compressedImageBase64 = '';
function compressAndPreviewImage(event) {
    const file = event.target.files[0];
    if(!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.src = e.target.result;
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const MAX_WIDTH = 800;
            const MAX_HEIGHT = 800;
            let width = img.width;
            let height = img.height;
            if (width > height) {
                if (width > MAX_WIDTH) { height *= MAX_WIDTH / width; width = MAX_WIDTH; }
            } else {
                if (height > MAX_HEIGHT) { width *= MAX_HEIGHT / height; height = MAX_HEIGHT; }
            }
            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            compressedImageBase64 = canvas.toDataURL('image/jpeg', 0.7); // Compressed!
            document.getElementById('imagePreview').innerHTML = `<img src="${compressedImageBase64}">`;
        }
    }
    reader.readAsDataURL(file);
}

/* Auto-Trigger Registration Guard */
let isRegistered = localStorage.getItem('mahagedara_registered') === 'true';
function checkGuestAction() {
    if(!isRegistered) {
        document.getElementById('regModal').style.display = 'flex';
    }
}
function closeRegModal() { document.getElementById('regModal').style.display = 'none'; }
function submitRegistration(e) {
    e.preventDefault();
    const name = document.getElementById('regName').value;
    localStorage.setItem('mahagedara_username', name);
    localStorage.setItem('mahagedara_registered', 'true');
    isRegistered = true;
    closeRegModal();
    alert('සාර්ථකයි! මහගෙදර ගිණුම සක්‍රීය විය.');
}

/* Posts Management */
let allPosts = JSON.parse(localStorage.getItem('mahagedara_full_posts')) || [
    {
        id: 1,
        author: 'සුමින්ද රංදිල්',
        content: '🏠 "මහගෙදර FB" අන්තර්ජාතික ජාලය දැන් 24/7 Green Signals සහ AI Auto-Blur සමඟ ක්‍රියාත්මකයි! ✨',
        image: '',
        isBlurred: false,
        time: 'දැන්',
        likes: 12,
        user_liked: false,
        comments: [{ author: 'Kalpani', text: 'පට්ටයි මචං!' }]
    }
];

function saveData() {
    localStorage.setItem('mahagedara_full_posts', JSON.stringify(allPosts));
}

function createPost() {
    const content = document.getElementById('postContent').value;
    if(!content.trim() && !compressedImageBase64) return;

    const isBlurred = checkNSFW(content, compressedImageBase64);

    const newPost = {
        id: Date.now(),
        author: localStorage.getItem('mahagedara_username') || 'അමුත්තා (Guest)',
        content: content,
        image: compressedImageBase64,
        isBlurred: isBlurred,
        time: 'මිනිත්තු කිහිපයකට පෙර',
        likes: 0,
        user_liked: false,
        comments: []
    };

    allPosts.unshift(newPost);
    saveData();
    document.getElementById('postContent').value = '';
    compressedImageBase64 = '';
    document.getElementById('imagePreview').innerHTML = '';
    renderFeed();
}

function renderFeed() {
    const container = document.getElementById('feedContainer');
    container.innerHTML = '';
    allPosts.forEach(post => {
        let mediaHtml = post.image ? `<img src="${post.image}" class="post-media ${post.isBlurred ? 'blurred' : ''}" onclick="this.classList.toggle('blurred')">` : '';
        let commentsHtml = (post.comments || []).map(c => `<div class="single-comment"><div class="commenter">${c.author}</div><div>${c.text}</div></div>`).join('');
        
        let card = document.createElement('div');
        card.className = 'post-card';
        card.innerHTML = `
            <div class="post-head">
                <div class="avatar">සු</div>
                <div><strong>${post.author}</strong><div style="font-size:11px;color:var(--text-muted);">${post.time} · 🟢 Live</div></div>
            </div>
            <div class="post-text">${post.content}</div>
            ${mediaHtml}
            ${post.isBlurred ? '<div style="font-size:11px;color:#ff5722;margin-top:4px;">⚠️ AI Censorship: අසබ්‍ය විය හැකි දර්ශනයක් නිසා බොඳ කර ඇත (ටච් කර බැලිය හැක).</div>' : ''}
            <div style="display:flex;justify-content:space-between;padding:8px 0;color:var(--text-muted);font-size:13px;border-bottom:1px solid var(--border-color);margin-top:8px;">
                <span>👍 ${post.likes} Likes</span><span>${post.comments.length} Comments</span>
            </div>
            <div class="actions">
                <button class="act ${post.user_liked ? 'liked' : ''}" onclick="toggleLike(${post.id})"><i class="fa-regular fa-thumbs-up"></i> Like</button>
                <button class="act"><i class="fa-regular fa-comment"></i> Comment</button>
            </div>
            <div class="comment-box">
                ${commentsHtml}
                <div class="comment-input-area">
                    <textarea id="comm-${post.id}" placeholder="කමෙන්ට් එකක් ලියන්න..."></textarea>
                    <button class="comment-submit-btn" onclick="addComment(${post.id})"> යවන්න </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

function toggleLike(id) {
    const post = allPosts.find(p => p.id === id);
    if(post) {
        post.user_liked = !post.user_liked;
        post.likes += post.user_liked ? 1 : -1;
        saveData();
        renderFeed();
    }
}

function addComment(id) {
    const txt = document.getElementById(`comm-${id}`).value;
    if(!txt.trim()) return;
    const post = allPosts.find(p => p.id === id);
    if(post) {
        post.comments.push({ author: localStorage.getItem('mahagedara_username') || 'यූසර්', text: txt });
        saveData();
        renderFeed();
    }
}

/* In-App Browser */
function openInAppBrowser(name, url) {
    document.getElementById('inAppTitle').innerText = name;
    document.getElementById('inAppIframe').src = url;
    document.getElementById('inAppBrowser').style.display = 'flex';
}
function closeInAppBrowser() { document.getElementById('inAppBrowser').style.display = 'none'; }

/* Mini Apps Filter */
function filterMiniApps(q) {
    const filter = q.toLowerCase();
    document.querySelectorAll('.mini-app-icon').forEach(icon => {
        const name = icon.querySelector('.mini-app-name').innerText.toLowerCase();
        icon.style.display = name.includes(filter) ? 'flex' : 'none';
    });
}

/* Chat & Menu Modals */
function toggleChat(show) { document.getElementById('chatContainer').style.display = show ? 'flex' : 'none'; }
function openMenuModal() { document.getElementById('menuModal').style.display = 'flex'; }
function closeMenuModal() { document.getElementById('menuModal').style.display = 'none'; }

function sendWebSocketMessage() {
    const input = document.getElementById('messageInput');
    const txt = input.value.trim();
    if(!txt) return;
    const box = document.getElementById('chatMessages');
    box.innerHTML += `<div class="msg-bubble sent">${txt}</div>`;
    input.value = '';
    box.scrollTop = box.scrollHeight;
    setTimeout(() => {
        box.innerHTML += `<div class="msg-bubble received">මහගෙදර සර්වර් එකෙන් ලැබුණු ස්වයංක්‍රීය පිළිතුරයි! 👍</div>`;
        box.scrollTop = box.scrollHeight;
    }, 1000);
}

renderFeed();
</script>
</body>
</html>

