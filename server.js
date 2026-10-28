import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(cors({origin:'*'}));
app.use(express.json({limit:'100mb'}));
app.use(express.static(__dirname));
app.get('/', (req,res)=> res.sendFile(path.join(__dirname,'index.html')));
app.post('/api/ai', async (req,res)=>{
  const {message} = req.body;
  if(process.env.GEMINI_API_KEY){
    try{
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({contents:[{parts:[{text:message}]}]})});
      const d = await r.json();
      const reply = d.candidates?.[0]?.content?.parts?.[0]?.text || 'AI Connected';
      return res.json({reply});
    }catch(e){ return res.json({reply:'AI Error'}); }
  }
  res.json({reply: `Sumiya AI: "${message}" - Giant Network Brain Active!`});
});
app.get('/api/stats', (req,res)=> res.json({users:Math.floor(1000+Math.random()*5000), live:Math.floor(20+Math.random()*100), status:'GIANT NETWORK 24/7 LIVE'}));
const PORT = process.env.PORT || 10000;
app.listen(PORT, ()=> console.log(`MYFAECBOX GIANT v10 LIVE on ${PORT}`));
