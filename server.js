const express = require('express');
const cors = require('cors');
const { createClient } = require('@supabase/supabase-js');

const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Supabase Configuration
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://your-supabase-project.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_KEY || 'your-supabase-anon-key';
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// OpenAI API Key Configuration
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || 'your-openai-api-key';

// 🤖 1. Sumiya AI Real-Time API Endpoint with Boss Secret Key Authentication
app.post('/api/ai-chat', async (req, res) => {
  try {
    const { message, history } = req.body;
    
    // Check for Boss Secret Key Authentication
    if (message === 'sumiya718264sumiya718264') {
      return res.json({
        reply: "👑 Welcome back, Boss & Master Sumiya! All administrative privileges, cloud pipelines, and system controls are fully unlocked and operational."
      });
    }

    // Call Real OpenAI API
    const openaiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: "You are Sumiya AI assistant for My Face BOX international platform." },
          ...(history || []),
          { role: "user", content: message }
        ]
      })
    });

    const data = await openaiResponse.json();
    if (data.choices && data.choices.length > 0) {
      res.json({ reply: data.choices[0].message.content });
    } else {
      res.json({ reply: "✨ Sumiya AI Hub: System operational. How can I assist you further?" });
    }
  } catch (error) {
    console.error("AI API Error:", error);
    res.status(500).json({ error: "AI connection error", reply: "🤖 AI assistant online (Local Fallback Mode)." });
  }
});

// 🔐 2. Posts & Photo Privacy API (Supabase)
app.post('/api/posts', async (req, res) => {
  try {
    const { author, content, media_url, is_private, user_email } = req.body;
    const { data, error } = await supabase
      .from('posts')
      .insert([{ author, content, media_url, is_private: is_private || false, user_email }]);

    if (error) throw error;
    res.json({ success: true, data });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/posts', async (req, res) => {
  try {
    const { user_email } = req.query;
    const { data, error } = await supabase
      .from('posts')
      .select('*')
      .or(`is_private.eq.false,user_email.eq.${user_email}`)
      .order('created_at', { ascending: false });

    if (error) throw error;
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 🤝 3. Followers & Global Social Network Endpoints
app.post('/api/follow', async (req, res) => {
  try {
    const { follower_email, following_name } = req.body;
    const { data, error } = await supabase
      .from('followers')
      .insert([{ follower_email, following_name }]);

    if (error) throw error;
    res.json({ success: true, message: `Successfully followed ${following_name}` });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/unfollow', async (req, res) => {
  try {
    const { follower_email, following_name } = req.body;
    const { error } = await supabase
      .from('followers')
      .delete()
      .match({ follower_email, following_name });

    if (error) throw error;
    res.json({ success: true, message: `Successfully unfollowed ${following_name}` });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 MY FACE BOX Server running live on port ${PORT}`);
});
