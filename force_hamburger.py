import os

html_path = "index.html"

# ඔයා ලියපු ලස්සන CSS Hamburger එක සහ Layout එක කෙලින්ම ගොනුවට ලිවීම
final_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Face BOX</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;  margin: 0; padding: 0; font-size: 38px; padding-bottom: 180px !important; }
        .menu-toggle-btn {  border: none; cursor: pointer; padding: 5px; display: flex; flex-direction: column; justify-content: space-between; width: 45px; height: 35px; margin-right: 25px; vertical-align: middle; }
        .menu-toggle-btn span { display: block; height: 5px; width: 100%;  border-radius: 2px; }
        .app-header { display: flex; align-items: center; justify-content: space-between; padding: 25px 30px;  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); }
        .header-left { display: flex; align-items: center; }
        .header-right { display: flex; align-items: center; gap: 20px; }
        #langSelect { font-size: 26px; padding: 8px 15px; border-radius: 20px; border: 2px solid #FF6B00; color: #FF6B00; font-weight: bold; }
        .icon-btn {  border: none; width: 80px; height: 80px; border-radius: 50%; font-size: 38px; display: flex; align-items: center; justify-content: center; }
        .mind-box {  padding: 35px; margin-top: 20px; display: flex; gap: 30px; align-items: center; border-bottom: 2px solid #e4e6eb; }
        .user-avatar { width: 110px; height: 110px; border-radius: 50%;  background-size: cover; }
        .mind-input { flex: 1;  border-radius: 60px; padding: 30px 40px; font-size: 36px; border: none; outline: none; }
        .stories-wrapper {  padding: 35px 25px; margin-top: 20px; display: flex; gap: 25px; overflow-x: auto; }
        .story-card { min-width: 260px; height: 440px; border-radius: 25px;  position: relative; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
        .story-avatar { position: absolute; top: 25px; left: 25px; width: 80px; height: 80px; border-radius: 50%; border: 4px solid #FF6B00; z-index: 2; }
        .story-name { position: absolute; bottom: 25px; left: 25px; color: white; font-size: 30px; font-weight: bold; text-shadow: 2px 2px 6px rgba(0,0,0,0.9); z-index: 2; }
        .feed-container { padding: 25px; }
        .post-card {  border-radius: 25px; padding: 40px; margin-bottom: 35px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        .post-header { display: flex; align-items: center; gap: 25px; margin-bottom: 25px; }
        .post-author { font-weight: bold; font-size: 38px; }
        .post-time { color: #65676b; font-size: 28px; }
        .post-content { font-size: 36px; line-height: 1.5; margin-bottom: 25px; }
        .post-image { width: 100%; border-radius: 15px; margin-bottom: 25px; }
        .post-actions { display: flex; justify-content: space-between; border-top: 2px solid #e4e6eb; padding-top: 25px; color: #65676b; font-weight: bold; font-size: 34px; }
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%;  display: flex; justify-content: space-around; align-items: center; padding: 35px 0; border-top: 3px solid #e4e6eb; z-index: 9999; box-shadow: 0 -6px 20px rgba(0,0,0,0.15); }
        .bottom-nav button {  border: none; font-size: 65px; cursor: pointer; }
        .side-drawer { position: fixed; top: 0; left: -100%; width: 80%; height: 100%;  z-index: 100000; box-shadow: 5px 0 15px rgba(0,0,0,0.2); padding: 40px; box-sizing: border-box; transition: 0.3s ease; }
        .side-drawer.open { left: 0; }
        .drawer-close { font-size: 50px;  border: none; cursor: pointer; margin-bottom: 40px; color: #FF6B00; font-weight: bold; }
    </style>
</head>
<body>
    <div class="app-header">
        <div class="header-left">
            <button class="menu-toggle-btn" onclick="toggleMenu()" aria-label="Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <h1 style="color: #FF6B00; font-size: 54px; font-weight: bold; margin: 0;">My Face BOX</h1>
        </div>
        <div class="header-right">
            <select id="langSelect" onchange="changeLanguage(this.value)">
                <option value="en">English</option>
                <option value="si">සිංහල</option>
                <option value="ta">தமிழ்</option>
            </select>
            <button class="icon-btn">+</button>
            <button class="icon-btn">&#128269;</button>
        </div>
    </div>
    <div class="mind-box">
        <div class="user-avatar" style="background-image: url('https://placeholder.com');"></div>
        <input type="text" id="mainMindInput" class="mind-input" placeholder="What is on your mind?">
    </div>
    <div class="stories-wrapper" id="storiesContainer"></div>
    <div class="feed-container" id="feedContainer"></div>
    <div class="bottom-nav">
        <button onclick="location.reload()">&#127968;</button>
        <button onclick="alert('Watch')">&#128250;</button>
        <button onclick="alert('Friends')">&#128101;</button>
        <button onclick="alert('Profile')">&#128100;</button>
        <button onclick="alert('Notifications')">&#128277;</button>
        <button onclick="toggleMenu()">&#9881;</button>
    </div>
    <div id="sideDrawer" class="side-drawer">
        <button class="drawer-close" onclick="toggleMenu()">&#11013; Close</button>
        <h2 style="font-size: 44px; color: #FF6B00;">Menu</h2>
        <ul style="list-style: none; padding: 0; font-size: 36px; line-height: 2.5;">
            <li><a href="#" style="text-decoration: none; color: #050505;">👤 ප්‍රොෆයිල් (Profile)</a></li>
            <li><a href="#" style="text-decoration: none; color: #050505;">⚙️ සැකසුම් (Settings)</a></li>
            <li><a href="#" style="text-decoration: none; color: #e41e3f;">🚪 Log out</a></li>
        </ul>
    </div>
    <script>
    let translations = {};
    fetch('/translations.json?v=' + Date.now()).then(res => res.json()).then(data => { translations = data; const savedLang = localStorage.getItem('selectedLanguage') || 'en'; document.getElementById('langSelect').value = savedLang; changeLanguage(savedLang); });
    function changeLanguage(lang) { localStorage.setItem('selectedLanguage', lang); document.querySelectorAll('[data-i18n]').forEach(element => { const key = element.getAttribute('data-i18n'); if (translations[lang] && translations[lang][key]) { if (element.tagName === 'INPUT') { element.placeholder = translations[lang][key]; } else { element.innerText = translations[lang][key]; } } }); }
    function toggleMenu() { document.getElementById('sideDrawer').classList.toggle('open'); }
    fetch('/api/get-feed?v=' + Date.now()).then(res => res.json()).then(data => {
        const sContainer = document.getElementById('storiesContainer'); sContainer.innerHTML = '';
        data.stories.forEach(s => { sContainer.innerHTML += `<div class="story-card" style="background-image: url('` + (s.bg || 'https://placeholder.com') + `'); background-size: cover;"><img src='` + s.avatar + `' class="story-avatar" onerror="this.src='https://placeholder.com'"><div class="story-name">` + s.user + `</div></div>`; });
        const fContainer = document.getElementById('feedContainer'); fContainer.innerHTML = '';
        data.posts.forEach(p => { fContainer.innerHTML += `<div class="post-card"><div class="post-header"><div class="user-avatar" style="background-image: url('` + p.author_avatar + `'), url('https://placeholder.com'); background-size: cover;"></div><div><div style="font-weight:bold; font-size:38px;">` + p.author + `</div><div class="post-time">` + p.time + `</div></div></div><div class="post-content">` + p.content + `</div>` + (p.image ? `<img src='` + p.image + `' class="post-image" onerror="this.src='https://placeholder.com'">` : '') + `<div class="post-actions"><div>👍 Like (` + p.likes + `)</div><div>💬 Comment</div><div>↪️ Share</div></div></div>`; });
    });
    </script>
</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(final_html)
print("[SUCCESS] Core UI layout updated with Custom CSS Hamburger Menu Overlay completely!")
