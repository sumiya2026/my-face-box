const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json({limit:'50mb'}));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/manifest.json', (req,res)=>{
  res.json({name:"මහගෙදර FB", short_name:"Mahagedara", start_url:"/", display:"standalone", background_color:"#121212", theme_color:"#ff5722"});
});

try{
  const mongoose = require('mongoose');
  mongoose.connect('mongodb://127.0.0.1:27017/mahagedara').then(()=>console.log('✅ Connected to MongoDB Successfully!')).catch(()=>console.log('⚠️ Mongo Local Mode - LocalStorage Active ✅'));
}catch(e){
  console.log('⚠️ Mongo Local Mode - LocalStorage Active ✅');
}

// FIXED - Express 5 වලට හරියන විදිය
app.use((req,res)=>{
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', ()=>{
  console.log('🚀 Mahagedara Full-Stack Server is running on port '+PORT);
});
