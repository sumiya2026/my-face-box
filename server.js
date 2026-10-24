const express = require('express');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Static files (HTML, CSS, JS) serve කිරීම
app.use(express.static(path.join(__dirname, 'public')));

// ඕනෑම route එකකින් පැමිණියහොත් ප්‍රධාන පිටුව පෙන්වීම
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`====================================`);
  console.log(`🚀 My Face BOX - System Live on Port ${PORT}`);
  console.log(`====================================`);
});
