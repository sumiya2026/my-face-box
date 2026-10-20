const express = require('express');
const Gun = require('gun');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000; 

// public ෆෝල්ඩර් එකේ තියෙන ඔයාගේ HTML/CSS/JS static විදිහට serve කරන්න
app.use(express.static(path.join(__dirname, 'public')));

const server = app.listen(port, () => {
    console.log(`MyFaceBox Master Hub running on port ${port}`);
});

// GunDB එක සර්වර් එකේම radata නමින් දත්ත ස්ථිරව තබා ගන්නා ලෙස ලින්ක් කිරීම
const gun = Gun({ 
    web: server
});

