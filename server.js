

const express = require('express');
const { Pool } = require('pg');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));

const PORT = process.env.PORT || 8000;

// 🌐 100% නිවැරදි External PostgreSQL ඩේටාබේස් ලින්ක් එක
const dbUrl = process.env.DATABASE_URL || "postgresql://myfacebox_db_user:3x0sdJNYWKySdDSPfj4VISy1eV0ZtVdp@dpg-dbbopfvavr4c738amvdg-a.ohio-postgres.render.com/myfacebox_db";

const pool = new Pool({
    connectionString: dbUrl,
    ssl: { rejectUnauthorized: false }
});

async function initDb() {
    try {
        await pool.query(`
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                user_name TEXT DEFAULT 'Anonymous',
                profile_pic TEXT,
                time TEXT,
                text TEXT,
                media_url TEXT,
                media_type TEXT,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);
        console.log("✓ PostgreSQL Tables Ready!");
    } catch (err) {
        console.error("❌ DB Error: ", err);
    }
}

app.get('/api/posts', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM posts ORDER BY id DESC');
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/posts', async (req, res) => {
    const { user_name, profile_pic, time, text, media_url, media_type } = req.body;
    try {
        const result = await pool.query(
            `INSERT INTO posts (user_name, profile_pic, time, text, media_url, media_type) 
             VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
            [user_name || 'Anonymous', profile_pic, time || 'දැන්', text, media_url, media_type]
        );
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ✅ 100% නිවැරදි කරන ලද Like API එක (No Escape Backslash)
app.post('/api/posts/:id/like', async (req, res) => {
    try {
        const result = await pool.query('UPDATE posts SET likes = likes + 1 WHERE id = \$1 RETURNING *', [req.params.id]);
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.use(express.static(path.join(__dirname, 'public')));
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, async () => {
    await initDb();
    console.log(`=========================================================`);
    console.log(` 📣 My Face BOX - System Live on Port ${PORT}`);
    console.log(`=========================================================`);
});












































































