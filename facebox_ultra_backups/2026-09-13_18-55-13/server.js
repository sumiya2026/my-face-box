const express = require('express');
const app = express();
app.use(express.json());

let posts = [];

app.get('/api/posts', (req, res) => {
    res.json(posts);
});

app.post('/api/posts', (req, res) => {
    const { author, content, image } = req.body;
    const newPost = {
        id: Date.now(),
        author: author || "ස්ුමිය (Sumiya)",
        content: content,
        image: image || null,
        likes: 0,
        comments: []
    };
    posts.unshift(newPost);
    res.json({ success: true, post: newPost });
});

app.post('/api/posts/:id/like', (req, res) => {
    const postId = req.params.id;
    const post = posts.find(p => p.id == postId);
    if (post) {
        post.likes += 1;
        res.json({ success: true, likes: post.likes });
    } else {
        res.status(404).json({ success: false, message: "Post not found" });
    }
});

app.post('/api/posts/:id/comment', (req, res) => {
    const postId = req.params.id;
    const { commentText } = req.body;
    const post = posts.find(p => p.id == postId);
    if (post) {
        post.comments.push(commentText);
        res.json({ success: true, comments: post.comments });
    } else {
        res.status(404).json({ success: false, message: "Post not found" });
    }
});

app.listen(5000, () => {
    console.log('Server running on http://localhost:5000');
});
