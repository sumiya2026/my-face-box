const fs = require('fs');
let code = fs.readFileSync('server.js', 'utf8');
const newBackend = `
// --- මෙතැන් සිට අලුත් ලියාපදිංචි කිරීමේ Backend කේතය ---
let usersList = [
    { name: "M.R.A.SUMINDA", phone: "+940767391892", role: "Agent", date: "10/10/2026" }
];
app.post('/api/register', (req, res) => {
    const newUser = {
        name: req.body.name || "Unknown User",
        phone: req.body.phone || "No Phone",
        role: req.body.role || "Shop Owner",
        accountType: req.body.accountType || "Personal Account",
        accountName: req.body.accountName || "",
        publishToList: req.body.publishToList || false,
        date: "10/10/2026"
    };
    usersList.push(newUser);
    res.status(200).json({ success: true, message: "සාර්ථකයි", user: newUser });
});
app.get('/api/users', (req, res) => { res.json(usersList); });
`;
code = code.replace("app.use(express.json());", "app.use(express.json());" + newBackend);
fs.writeFileSync('server.js', code);
console.log('සර්වර් කේතය 100% ක් සාර්ථකව යාවත්කාලීන විය!');
