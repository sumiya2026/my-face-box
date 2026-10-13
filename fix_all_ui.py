import os

html_path = "index.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. පවතින පැරණි භාෂා මෙනු කේතයන් ඉවත් කිරීම (පිරිසිදු කර ගැනීම)
    content = content.replace('position: fixed; right: 15px; top: 15px;', 'position: absolute; left: 320px; top: 25px;')
    content = content.replace('position: absolute; right: 15px; top: 15px;', 'position: absolute; left: 320px; top: 25px;')

    # 2. සම්පූර්ණ HTML එක නවීන 3X විශාල, සැබෑ ෆේස්බුක් පෙනුම ඇති Layout එකකට හැරවීම
    complete_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title data-i18n="title">My Face BOX</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            
            margin: 0;
            padding: 0;
            font-size: 26px;
        }
        
        /* 🔵 ඉහළ තීරුව (Header Layout) */
        .fb-header {
            
            padding: 20px 25px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #e4e6eb;
            position: relative;
        }
        .logo-section {
            display: flex;
            align-items: center;
        }
        .fb-logo {
            font-size: 48px;
            font-weight: bold;
            color: #FF6B00;
            text-decoration: none;
        }
        
        /* 🌐 භාෂා මෙනුව වම්පැත්තේ හිස් තැනට ස්ථානගත කිරීම */
        .language-selector {
            margin-left: 30px;
        }
        #langSelect {
            font-size: 22px;
            padding: 8px 15px;
            border-radius: 20px;
            border: 2px solid #FF6B00;
            
            color: #FF6B00;
            font-weight: bold;
            cursor: pointer;
        }
        
        .header-icons {
            display: flex;
            gap: 15px;
        }
        .icon-btn {
            
            border: none;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }

        /* ✍️ What's on your mind තීරුව */
        .mind-box {
            
            padding: 25px;
            margin-top: 15px;
            display: flex;
            gap: 20px;
            align-items: center;
            border-bottom: 1px solid #e4e6eb;
        }
        .user-avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            
        }
        .mind-input {
            flex: 1;
            
            border-radius: 40px;
            padding: 20px 25px;
            font-size: 26px;
            border: none;
            outline: none;
            cursor: pointer;
        }

        /* 📸 Stories (කතන්දර) බාර් එක */
        .stories-wrapper {
            
            padding: 25px 20px;
            margin-top: 15px;
            display: flex;
            gap: 15px;
            overflow-x: auto;
        }
        .story-card {
            min-width: 160px;
            height: 270px;
            border-radius: 15px;
            
            position: relative;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .story-avatar {
            position: absolute;
            top: 15px;
            left: 15px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 3px solid #FF6B00;
            z-index: 2;
        }
        .story-name {
            position: absolute;
            bottom: 15px;
            left: 15px;
            color: white;
            font-size: 20px;
            font-weight: bold;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
            z-index: 2;
        }

        /* 📰 News Feed පෝස්ට් කාඩ් */
        .feed-container {
            padding: 15px;
        }
        .post-card {
            
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .post-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .post-author {
            font-weight: bold;
            font-size: 26px;
        }
        .post-time {
            color: #65676b;
            font-size: 20px;
        }
        .post-content {
            font-size: 26px;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        .post-image {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        
        /* Like, Comment බട്ടන් */
        .post-actions {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #e4e6eb;
            padding-top: 15px;
            color: #65676b;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <!-- 🔵 Header Section -->
    <div class="fb-header">
        <div class="logo-section">
            <a href="#" class="fb-logo" data-i18n="title">My Face BOX</a>
            <!-- 🌐 භාෂා මෙනුව වම්පැත්තේ හිස් තැනට ආවා -->
            <div class="language-selector">
                <select id="langSelect" onchange="changeLanguage(this.value)">
                    <option value="en">English</option>
                    <option value="si">සිංහල</option>
                    <option value="ta">தமிழ்</option>
                </select>
            </div>
        </div>
        <div class="header-icons">
            <button class="icon-btn">+</button>
            <button class="icon-btn">🔍</button>
        </div>
    </div>

    <!-- ✍️ What's on your mind Section -->
    <div class="mind-box">
        <div class="user-avatar"></div>
        <input type="text" class="mind-input" data-i18n="whatsOnYourMind" placeholder="What's on your mind?">
    </div>

    <!-- 📸 Stories Section -->
    <div class="stories-wrapper" id="storiesContainer">
        <!-- Stories ඔටෝම ලෝඩ් වේ -->
    </div>

    <!-- 📰 News Feed Section -->
    <div class="feed-container" id="feedContainer">
        <!-- Posts ඔටෝම ලෝඩ් වේ -->
    </div>

    <script>
    // 🌐 භාෂා පරිවර්තන පද්ධතිය
    let translations = {};
    fetch('/translations.json')
        .then(res => res.json())
        .then(data => {
            translations = data;
            const savedLang = localStorage.getItem('selectedLanguage') || 'en';
            document.getElementById('langSelect').value = savedLang;
            changeLanguage(savedLang);
        });

    function changeLanguage(lang) {
        localStorage.setItem('selectedLanguage', lang);
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                if (element.tagName === 'INPUT') {
                    element.placeholder = translations[lang][key];
                } else {
                    element.innerText = translations[lang][key];
                }
            }
        });
    }

    // 📰 Backend එකෙන් පෝස්ට් සහ ස්ටෝරි ලෝඩ් කිරීම
    fetch('/api/get-feed')
        .then(res => res.json())
        .then(data => {
            // Stories පිරවීම
            const sContainer = document.getElementById('storiesContainer');
            data.stories.forEach(s => {
                sContainer.innerHTML += `
                    <div class="story-card" style="background-image: url('${s.bg || 'https://placeholder.com'}'); background-size: cover;">
                        <img src="${s.avatar}" class="story-avatar">
                        <div class="story-name">${s.user}</div>
                    </div>
                `;
            });

            // Posts පිරවීම
            const fContainer = document.getElementById('feedContainer');
            data.posts.forEach(p => {
                fContainer.innerHTML += `
                    <div class="post-card">
                        <div class="post-header">
                            <div class="user-avatar" style="background-image: url('${p.author_avatar}'); background-size: cover;"></div>
                            <div>
                                <div class="post-author">${p.author}</div>
                                <div class="post-time">${p.time}</div>
                            </div>
                        </div>
                        <div class="post-content">${p.content}</div>
                        <img src="${p.image}" class="post-image">
                        <div class="post-actions">
                            <div>👍 Like (${p.likes})</div>
                            <div>💬 Comment</div>
                            <div>↪️ Share</div>
                        </div>
                    </div>
                `;
            });
        });
    </script>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(complete_html)
    print("[SUCCESS] Language dropdown moved to the left and UI upscaled successfully!")
else:
    print("[ERROR] index.html not found.")
