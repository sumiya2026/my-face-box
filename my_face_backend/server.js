const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });
const PORT = process.env.PORT || 5000;

app.use(helmet({ contentSecurityPolicy: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));

const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100, message: "Too many requests, try again later." });
app.use('/api/', limiter);

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/status', (req, res) => {
  res.status(200).json({ status: "Success", message: "Welcome to My Face BOX API - 100% Protected" });
});

io.on('connection', (socket) => {
  socket.on('disconnect', () => {});
});

server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
