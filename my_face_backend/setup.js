const fs = require('fs');
const path = require('path');

// 1. Create database file if not exists
const dbFile = path.join(__dirname, 'database.json');
if (!fs.existsSync(dbFile)) {
    fs.writeFileSync(dbFile, JSON.stringify({ posts: [], messages: [] }, null, 2));
}

// 2. Write the main server code cleanly
const serverCode = `const express = require('express');
const http = require('http');
const path = require('path');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 5000;

app.use(express.json());

const dbFile = path.join(__dirname, 'database.json');
const readDB = () => JSON.parse(fs.readFileSync(dbFile, 'utf8'));
const writeDB = (data) => fs.writeFileSync(dbFile, JSON.stringify(data, null, 2));

app.get('/', (req, res) => {
    res.send(\`
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Face - Mind Chat</title>
        <style>
            body { font-family: sans-serif;  margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; }
            header {  color: #0b2265 !important; width: 100%; padding: 14px 0; text-align: center; font-size: 24px; font-weight: bold; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
            .container { max-width: 500px; width: 95%; margin-top: 15px; box-sizing: border-box; }
            .nav-tabs { display: flex;  width: 100%; justify-content: space-around; padding: 10px 0; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            .tab-btn {  border: none; font-size: 15px; font-weight: bold; color: #0b2265 !important; cursor: pointer; padding: 8px 16px; border-radius: 20px; outline: none; }
            .tab-btn.active {  color: #0b2265 !important; }
            .section { display: none; }
            .section.active { display: block; }
            .post-box {  padding: 15px; border-radius: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px; }
            textarea, input[type="text"] { width: 100%; border: 1px solid #ccd0d5; border-radius: 12px; padding: 12px; font-size: 15px; outline: none; box-sizing: border-box;  }
            textarea { height: 75px; resize: none; }
            .actions-row { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
            .primary-btn {  color: #0b2265 !important; border: none; padding: 10px 24px; border-radius: 20px; font-weight: bold; cursor: pointer; }
            .post-card {  padding: 18px; border-radius: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px; }
            .card-header { display: flex; align-items: center; margin-bottom: 12px; }
            .avatar { width: 40px; height: 40px;  color: #0b2265 !important; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px; }
            .username { font-weight: bold; color: #0b2265 !important; }
            .post-text { color: #0b2265 !important; font-size: 15px; margin-bottom: 12px; word-wrap: break-word; }
            .chat-container {  border-radius: 16px; height: 350px; display: flex; flex-direction: column; overflow: hidden; border: 1px solid #e4e6eb; }
            .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px;  }
            .msg-bubble { max-width: 75%; padding: 10px 14px; border-radius: 16px; font-size: 14px; word-wrap: break-word; }
            .msg-bubble.me {  color: #0b2265 !important; align-self: flex-end; border-bottom-right-radius: 4px; }
            .msg-bubble.other {  color: #0b2265 !important; align-self: flex-start; border-bottom-left-radius: 4px; border: 1px solid #e4e6eb; }
        </style>
    </head>
    <body>
        <header>📘 My Face App</header>
        <div class="container">
            <div class="nav-tabs">
                <button id="btn-feed" class="tab-btn active" onclick="switchTab('feed')">📰 Feed</button>
                <button id="btn-mind" class="tab-btn" onclick="switchTab('mind')">💬 Mind Chat</button>
            </div>
            <div id="feedSection" class="section active">
                <div class="post-box">
                    <textarea id="postContent" placeholder="What's on your mind?"></textarea>
                    <div class="actions-row" style="justify-content: flex-end;">
                        <button class="primary-btn" onclick="createPost()">Post</button>
                    </div>
                </div>
                <div id="newsFeed"></div>
            </div>
            <div id="mindSection" class="section">
                <div class="chat-container">
                    <div class="chat-messages" id="chatBox"></div>
                    <div class="actions-row" style="padding: 10px;  margin: 0; gap: 8px;">
                        <input type="text" id="chatInput" placeholder="Type a message...">
                        <button class="primary-btn" onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>
        </div>
        <script>
            function switchTab(tabName) {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                document.getElementById('btn-' + tabName).classList.add('active');
                if(tabName === 'feed') { document.getElementById('feedSection').classList.add('active'); loadPosts(); }
                if(tabName === 'mind') { document.getElementById('mindSection').classList.add('active'); loadMessages(); }
            }
            async function loadPosts() {
                const res = await fetch('/api/posts'); const data = await res.json();
                const feed = document.getElementById('newsFeed'); feed.innerHTML = '';
                if(!data.posts || data.posts.length === 0) { feed.innerHTML = '<div style="padding:20px;text-align:center;border-radius:16px;">No posts yet!</div>'; return; }
                data.posts.forEach(p => {
                    const div = document.createElement('div'); div.className = 'post-card';
                    div.innerHTML = '<div class="card-header"><div class="avatar">U</div><div class="username">Anonymous User</div></div><div class="post-text">' + p.content + '</div>';
                    feed.appendChild(div);
                });
            }
            async function createPost() {
                const c = document.getElementById('postContent').value.trim(); if(!c) return;
                await fetch('/api/posts/create', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content: c }) });
                document.getElementById('postContent').value = ''; loadPosts();
            }
            async function loadMessages() {
                const res = await fetch('/api/messages'); const data = await res.json();
                const box = document.getElementById('chatBox'); box.innerHTML = '';
                if(!data.messages || data.messages.length === 0) { box.innerHTML = '<div style="text-align:center;color: #0b2265 !important;margin-top:20px;">No messages yet!</div>'; return; }
                data.messages.forEach((m, idx) => {
                    const div = document.createElement('div'); div.className = 'msg-bubble ' + (idx % 2 === 0 ? 'me' : 'other');
                    div.innerText = m.text; box.appendChild(div);
                });
                box.scrollTop = box.scrollHeight;
            }
            async function sendMessage() {
                const t = document.getElementById('chatInput').value.trim(); if(!t) return;
                await fetch('/api/messages/send', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: t }) });
                document.getElementById('chatInput').value = ''; loadMessages();
            }
            loadPosts();
        </script>
    </body>
    </html>
    \`);
});

app.get('/api/posts', (req, res) => res.json({ posts: readDB().posts }));
app.post('/api/posts/create', (req, res) => { const db = readDB(); db.posts.push({ content: req.body.content }); writeDB(db); res.status(201).json({}); });
app.get('/api/messages', (req, res) => res.json({ messages: readDB().messages }));
app.post('/api/messages/send', (req, res) => { const db = readDB(); db.messages.push({ text: req.body.text }); writeDB(db); res.status(201).json({}); });

server.listen(PORT, () => console.log('Mind Chat Server is running on port ' + PORT));`;

fs.writeFileSync(path.join(__dirname, 'server.js'), serverCode);
console.log('Setup script completed successfully! Running server now...');
