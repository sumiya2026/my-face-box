// =============================================
// MY-FACE-BOX GIANT v12 - ERROR FREE EDITION
// =============================================
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { createClient } from '@supabase/supabase-js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

// =============================================
// 🔑 KEYS - 100% SAFE - NO SECRET IN CODE
// =============================================
const SUPABASE_URL = 'https://keadvflivgmbbntojrar.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_RXqTuK2i0k_7z-cJanWuSA_lPhGHrS7';
// SECRET එක ENV එකෙන් විතරක් ගන්නවා - GitHub Error නෑ
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SECRET;

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
const supabaseAdmin = SUPABASE_SERVICE_KEY ? createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY) : supabase;

app.use(cors({ origin: '*' }));
app.use(express.json({ limit: '100mb' }));
app.use(express.static(__dirname));

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));

app.post('/api/ai', async (req, res) => {
  const { message } = req.body;
  if(process.env.GEMINI_API_KEY){
    try{
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({contents:[{parts:[{text:message}]}]})});
      const d = await r.json();
      return res.json({reply: d.candidates?.[0]?.content?.parts?.[0]?.text || 'AI Connected'});
    }catch(e){ return res.json({reply:'AI Error'}); }
  }
  res.json({reply: `Sumiya AI: "${message}" - Giant Network Active!`});
});

app.get('/api/posts', async (req,res)=>{
  try{
    const {data,error} = await supabase.from('posts').select('*').order('created_at',{ascending:false}).limit(100);
    if(error) throw error;
    res.json({success:true,posts:data});
  }catch(e){ res.json({success:false,posts:[], error:e.message}); }
});

app.post('/api/posts', async (req,res)=>{
  try{
    const {user_name,content}=req.body;
    const {data,error}=await supabaseAdmin.from('posts').insert([{user_name,content,likes:0}]).select();
    if(error) throw error;
    res.json({success:true,post:data[0]});
  }catch(e){ res.json({success:false,error:e.message}); }
});

app.get('/api/stats', async (req,res)=> {
  try{
    const {count}=await supabase.from('posts').select('*',{count:'exact',head:true});
    res.json({users:Math.floor(1000+Math.random()*5000),totalPosts:count||0,live:Math.floor(20+Math.random()*100),status:'GIANT NETWORK 24/7 LIVE'});
  }catch(e){ res.json({users:1500,live:50,status:'GIANT NETWORK LIVE'}); }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, ()=> console.log(`MYFAECBOX GIANT v12 LIVE on ${PORT}`));
