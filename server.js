const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
// Base64 පින්තූර සේව් කිරීමට ඉඩ ලබාදීම සඳහා limit එක 50mb කරයි
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// 1. MongoDB Atlas සම්බන්ධතාවය
const MONGODB_URI = process.env.MONGODB_URI;

mongoose.connect(MONGODB_URI)
  .then(() => console.log('🍃 MongoDB Atlas Database Connected Successfully!'))
  .catch((err) => console.error('❌ MongoDB Connection Error:', err));

// 2. Database Schema එක සෑදීම
const PostSchema = new mongoose.Schema({
  id: Number,
  name: String,
  avatar: String,
  accountType: String,
  authorSignature: String,
  txt: String,
  media: {
    type: { type: String, default: null },
    src: [String],
    title: { type: String, default: '' }
  },
  likes: { type: Number, default: 0 },
  comments: Array,
  time: { type: String, default: 'Just now' },
  createdAt: { type: Date, default: Date.now }
});

const Post = mongoose.model('Post', PostSchema);

// 3. API Routes (දත්ත ලබාගැනීම සහ සේව් කිරීම)
// සියලුම පෝස්ට් ලබාගැනීමට
app.get('/api/posts', async (req, res) => {
  try {
    const allPosts = await Post.find().sort({ createdAt: -1 });
    res.json(allPosts);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// අලුත් පෝස්ට් එකක් MongoDB එකට සේව් කිරීමට
app.post('/api/posts', async (req, res) => {
  try {
    const newPost = new Post(req.body);
    const savedPost = await newPost.save();
    res.json(savedPost);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Static Front-end Files Serve කිරීම
app.use(express.static(path.join(__dirname, 'public')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`====================================`);
  console.log(`🚀 My Face BOX - Live on Port ${PORT}`);
  console.log(`====================================`);
});
