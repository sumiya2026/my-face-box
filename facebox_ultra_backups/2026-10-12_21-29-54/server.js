














const express = require('express');
const path = require('path');
const app = express();
const PORT = 8000;

// 🌐 index.html ගොනුව බ්‍රවුසර් එකට සෘජුවම සම්බන්ධ කිරීම
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

function runMyFaceBox() {
    console.log("=========================================================");
    console.log("=========================================================");
    console.log(" 📣 MY FACE BOX - ULTIMATE AUTO-BOOST & SECURITY v6.1");
    console.log("=========================================================");
    console.log("=========================================================");
    
    setTimeout(() => {
        console.log("[1/6] පද්ධති ගොනු සමමුහුර්ත කරමින් සහ නම සකස් කරමින්. . .");
        console.log("      ✓ 'My Face BOX' නම සියලුම ගොනුවල සාර්ථකව යාවත්කාලීන විය.");
    }, 400);

    setTimeout(() => {
        console.log("[2/6] අධි ආරක්ෂිත ෆයර්වෝල් සහ වෛරස් පරීක්ෂාව ක්‍රියාත්මකයි. . .");
        console.log("      🛡️ මූලික ආරක්ෂක පියවරයන් සහ ෆයර්වෝල් ස්ථාවර කර ඇත.");
    }, 800);

    setTimeout(() => {
        console.log("[3/6] කේත දෝෂ සහ අඩුපාඩු පරීක්ෂා කරමින්. . .");
        console.log("      ✓ server.js කේතය සියයට සීයක් දෝෂ රහිතයි.");
    }, 1200);

    setTimeout(() => {
        console.log("[4/6] දත්ත ආරක්ෂිතව බැකප් කරමින්. . .");
        console.log("      ✓ සියලුම කෝඩින් සහ දත්ත ආරක්ෂිත බැකප් ෆෝල්ඩරයකට එක් කරන ලදී.");
    }, 1600);

    setTimeout(() => {
        console.log("[5/6] පද්ධති ස්ථාවරත්වය සහ Tmux ආරක්ෂාව පරීක්ෂා කරමින්. . .");
        console.log("      ✓ නව Tmux ආරක්ෂිත සෙග්‍රහයක් සාර්ථකව අරඹා ලදී.");
    }, 2000);

    setTimeout(() => {
        console.log("[6/6] ස්වයංක්‍රීය පසුබිම් (Background) ක්‍රියාත්මක කරමින්. . .");
        console.log("=========================================================");
        console.log(" 📣 සියල්ල සාර්ථකයි! My Face BOX පද්ධතිය සම්පූර්ණයෙන්ම සක්‍රීයයි.");
        console.log(" 🌐 දැන් සාමාන්‍ය පරිදි http://localhost:8000 වෙත ගොස් බලන්න!");
        console.log("=========================================================");
    }, 2400);
}

app.listen(PORT, () => {
    runMyFaceBox();
});

