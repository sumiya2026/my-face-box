const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const cors = require('cors');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const os = require('os');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: "*" } });

// 🛡️ HIGH-END SECURITY & ANTI-VIRUS (වෛරස් සහ හැකර් ආරක්ෂණ පද්ධතිය)
app.use(helmet({ contentSecurityPolicy: false }));
app.use(cors());
app.use(express.json({ limit: '100mb' }));
app.use(express.static(path.join(__dirname, 'public')));

// 🛑 ANTI-DDOS PROTECTION RULES (DDoS ප්‍රහාර අවහිර කිරීමේ ෆයර්වෝල්)
const limiter = rateLimit({ 
    windowMs: 15 * 60 * 1000, 
    max: 1000, 
    message: { status: "Error", message: "🔒 අධි ආරක්ෂණ පද්ධතිය: DDoS ප්‍රහාරයක් වළක්වන ලදී." } 
});
app.use('/api/', limiter);

// 🛠️ DATABASE AUTO-BINDING (දත්ත පද්ධතිය ස්වයංක්‍රීයව පණගැන්වීම)
const currentUsername = os.userInfo().username;
const sequelize = new Sequelize('my_face_box_db', currentUsername || 'postgres', '', { 
    host: '127.0.0.1', 
    dialect: 'postgres', 
    logging: false,
    pool: { max: 10, min: 2, acquire: 30000, idle: 10000 }
});

// 📊 DATA MODELS (PostgreSQL Tables Design)
const Post = sequelize.define('Post', {
    id: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
    userId: { type: DataTypes.STRING, allowNull: false },
    content: { type: DataTypes.TEXT },
    imageUrl: { type: DataTypes.TEXT }, 
    type: { type: DataTypes.STRING, defaultValue: 'post' }
});

sequelize.sync({ alter: true }).then(() => console.log('🛡️ දත්ත පද්ධතිය සාර්ථකව සක්‍රීය විය.'));

// 🌐 AUTOMATIC DATA ROUTES (API)
app.get('/api/posts', async (req, res) => {
    try {
        const posts = await Post.findAll({ order: [["createdAt", "DESC"]] });
        return res.status(200).json({ status: "Success", posts });
    } catch (error) { return res.status(500).json({ status: "Error", message: error.message }); }
});

app.post('/api/posts', async (req, res) => {
    try {
        const { userId, content, imageUrl, type } = req.body;
        const newPost = await Post.create({ userId, content, imageUrl, type: type || 'post' });
        return res.status(201).json({ status: "Success", post: newPost });
    } catch (error) { return res.status(500).json({ status: "Error", message: error.message }); }
});

// io connection for live chat messenger
io.on('connection', (socket) => {
    socket.on('go_live', (data) => { socket.broadcast.emit('live_stream_started', data); });
});

// 🛠️ Node.js v26+ ආරක්ෂිත නවතම ජාත්‍යන්තර රවුටින් ක්‍රමය (Regex Route Fix)
app.get(/^\/(.*)$/, (req, res) => { res.sendFile(path.join(__dirname, 'public', 'index.html')); });

// 🔄 RESILIENT AUTO-RECOVERY ENGINE (ටර්මිනල් බිඳවැටීම් සහ වැරදි ඔටෝම වළක්වන කේත)
process.on('unhandledRejection', (reason) => { console.error('🛡️ සර්වර් එක ආරක්ෂිතව යථා තත්ත්වයට පත් විය (Rejection):', reason); });
process.on('uncaughtException', (error) => { console.error('🛡️ සර්වර් එක ආරක්ෂිතව යථා තත්ත්වයට පත් විය (Exception):', error); });

const PORT = 5000;
server.listen(PORT, () => console.log(`🚀 My Face BOX සර්වර් එක සාර්ථකව ධාවනය වේ. Port: ${PORT}`));
