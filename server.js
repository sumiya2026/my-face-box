

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












































































const { Pool } = require('pg');

// 🌍 ජාත්‍යන්තර මට්ටමේ සුපිරි Cloud Storage පද්ධතිය සම්බන්ධ කිරීම
const pool = new Pool({
  connectionString: "postgresql://postgres:FY%3Fk%21XyUf9f%25NNQ@db.tqnhcqwgfoandnbyeqvs.supabase.co:6543/postgres?sslmode=require",
});

pool.connect((err, client, release) => {
  if (err) {
    return console.error('❌ Supabase Cloud එකට ලින්ක් වීම අසාර්ථකයි:', err.stack);
  }
  console.log('🚀 MYFAECBOX සාර්ථකව ජාත්‍යන්තර Supabase Cloud Vault එකට ලින්ක් වුණා වස්තු!');
  release();
});
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: "postgresql://postgres:FY%3Fk%21XyUf9f%25NNQ@db.tqnhcqwgfoandnbyeqvs.supabase.co:6543/postgres?sslmode=require",
});

// 🌍 ජාත්‍යන්තර ග්‍රාහකයින්ගේ දත්ත සඳහා Tables සෑදීමේ ස්මාර්ට් ලොජික් එක
const createTables = async () => {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS global_posts (
        id SERIAL PRIMARY KEY,
        username TEXT,
        content TEXT,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS global_stories (
        id SERIAL PRIMARY KEY,
        username TEXT,
        media_url TEXT,
        media_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log("✅ MYFAECBOX Cloud Tables Created Successfully!");
  } catch (err) {
    console.error("❌ Table Creation Error: ", err);
  }
};
createTables();
// 🌍 GLOBAL POST & STORY LOGIC (Supabase Cloud එකෙන් ලෝඩ් කිරීම සහ සේව් කිරීම)

// 1. පෝස්ට් එකක් දාද්දී කෙලින්ම Supabase Cloud එකට සේව් කරන ලොජික් එක
app.post('/api/posts', async (req, res) => {
  const { username, content, image_url } = req.body;
  try {
    const newPost = await pool.query(
      'INSERT INTO global_posts (username, content, image_url) VALUES ($1, $2, $3) RETURNING *',
      [username, content, image_url]
    );
    res.json({ success: true, post: newPost.rows[0] });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: "Cloud Save Error" });
  }
});

// 2. හැමෝම දාන පෝස්ට් සියල්ලම නොමැකී ජාත්‍යන්තරව ලෝඩ් කරගන්නා ලොජික් එක
app.get('/api/posts', async (req, res) => {
  try {
    const allPosts = await pool.query('SELECT * FROM global_posts ORDER BY created_at DESC');
    res.json(allPosts.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Cloud Load Error" });
  }
});

// 3. ස්ටෝරි (Stories) කෙලින්ම Cloud එකට සේව් කරන ලොජික් එක
app.post('/api/stories', async (req, res) => {
  const { username, media_url, media_type } = req.body;
  try {
    const newStory = await pool.query(
      'INSERT INTO global_stories (username, media_url, media_type) VALUES ($1, $2, $3) RETURNING *',
      [username, media_url, media_type]
    );
    res.json({ success: true, story: newStory.rows[0] });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: "Cloud Story Save Error" });
  }
});

// 4. ස්ටෝරි සියල්ලම සජීවීව ලෝඩ් කරගන්නා ලොජික් එක
app.get('/api/stories', async (req, res) => {
  try {
    const allStories = await pool.query('SELECT * FROM global_stories ORDER BY created_at DESC');
    res.json(allStories.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Cloud Story Load Error" });
  }
});
const fs = require('fs');
const path = require('path');

// 📁 පින්තූර මැකෙන්නේ නැති ස්ථිර මතක ෆෝල්ඩරය ස්වයංක්‍රීයව සෑදීමේ එන්ජිම
const uploadDir = '/opt/render/project/src/uploads';
if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir, { recursive: true });
    console.log("✅ ස්ථිර මතක ෆෝල්ඩරය සාර්ථකව සක්‍රීය කළා වස්තු!");
}
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// 📁 Render ස්ථිර මතක තැටිය තුළට ප්‍රධාන ඩේටාබේස් ෆයිල් එක ආරක්ෂිතව ලින්ක් කිරීම
const persistentDbPath = '/opt/render/project/src/uploads/myface_database.db';
const localSourcePath = '/storage/emulated/0/myface_database.db';

// ෆයිල් එක ස්ථිර මතක තැටියේ නැත්නම් මුලින්ම එතැනට කොපි කර ගැනීම
if (!fs.existsSync(persistentDbPath) && fs.existsSync(localSourcePath)) {
    fs.copyFileSync(localSourcePath, persistentDbPath);
    console.log("⚙️ ප්‍රධාන ඩේටාබේස් එක ස්ථිර මතක තැටියට සාර්ථකව පිටපත් කළා වස්තු!");
}

// 🌍 සර්වර් එකේ සියලුම API Routes මේ ප්‍රධාන ෆයිල් එකට සම්බන්ධ කිරීම
const db = new sqlite3.Database(persistentDbPath, (err) => {
    if (err) {
        console.error('❌ Database Connection Error: ', err.message);
    } else {
        console.log('🚀 MYFAECBOX සාර්ථකව ප්‍රධාන myface_database.db එකට ලින්ක් වුණා වස්තු!');
    }
});
