const express = require('express');
const path = require('path');
const app = express();
// --- මෙතැන් සිට අලුත් ලියාපදිංචි කිරීමේ Backend කේතය ---
var usersList = [
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

app.get('/api/users', (req, res) => {
    res.json(usersList);
});
// --- අලුත් Backend කේතය අවසානයි ---

app.use(express.json());
// --- මෙතැන් සිට අලුත් ලියාපදිංචි කිරීමේ Backend කේතය ---
var usersList = [
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


// ප්‍රධාන HTML සහ අනෙක් Static ෆයිල්ස් (CSS, JS) ලෝඩ් කිරීමට මඟ සැකසීම
app.use(express.static(__dirname));
app.use(express.static(__dirname));

let posts = [];

// 🌐 1. ප්‍රධාන වෙබ් පිටුව (index.html) බ්‍රවුසර් එකට ලබාදීම
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 🌐 2. භාෂා ගොනුව (translations.json) ලබාදීම
app.get('/translations.json', (req, res) => {
    res.sendFile(path.join(__dirname, 'translations.json'));
});

// 🛡️ 3. ව්‍යාජ ගිණුම් වැළැක්වීමේ ජාතික හැඳුනුම්පත් (NIC) ඔටෝ සර්ච් පද්ධතිය (API)
app.post('/api/verify-nic', (req, res) => {
    const { nic } = req.body;
    if (!nic) {
        return res.json({ success: False, message: "කරුණාකර හැඳුනුම්පත් අංකය ඇතුළත් කරන්න." });
    }

    // ලංකාවේ හැඳුනුම්පත් රටාවන් පරීක්ෂා කිරීම (Regex Algorithm)
    const oldNicRegex = /^[0-9]{9}[vVxX]$/;
    const newNicRegex = /^[0-9]{12}$/;

    if (oldNicRegex.test(nic) || newNicRegex.test(nic)) {
        // අංකය සැබෑ ව්‍යුහයක් නම් ස්වයංක්‍රීයව තහවුරු කරයි
        return res.json({ 
            success: True, 
            message: "ජාතික හැඳුනුම්පත සාර්ථකව තහවුරු කරන ලදී (සැබෑ පරිශීලකයෙකි)." 
        });
    } else {
        return res.json({ 
            success: False, 
            message: "අවලංගු හැඳුනුම්පත් අංකයකි! ව්‍යාජ ගිණුම් සෑදීමට නොහැක." 
        });
    }
});

// පැරණි Posts ලබාගැනීමේ සහ දැමීමේ ක්‍රමවේදයන්
app.get('/api/posts', (req, res) => {
    res.json(posts);
});

app.post('/api/posts', (req, res) => {
    const { author, content, image } = req.body;
    const newPost = {
        id: Date.now(),
        author: author || "සුමියා (Sumiya)",
        content: content,
        image: image || null,
        likes: 0,
        comments: []
    };
    posts.unshift(newPost);
    res.json({ success: true, post: newPost });
});

app.post('/api/posts/:id/like', (req, res) => {
    const postID = req.params.id;
    const post = posts.find(p => p.id == postID);
    if (post) {
        post.likes += 1;
        res.json({ success: true, likes: post.likes });
    } else {
        res.status(404).json({ success: false, message: "Post not found" });
    }
});

app.post('/api/posts/:id/comment', (req, res) => {
    const postID = req.params.id;
    const { commentText } = req.body;
    const post = posts.find(p => p.id == postID);
    if (post) {
        post.comments.push(commentText);
        res.json({ success: true, comments: post.comments });
    } else {
        res.status(404).json({ success: false, message: "Post not found" });
    }
});

app.listen(8000, () => {
    console.log('Server running on http://localhost:8000');
});
