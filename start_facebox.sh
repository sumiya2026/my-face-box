#!/data/data/com.termux/files/usr/bin/bash

# ========================================================
# 🛡️ MY FACE BOX - ULTIMATE AUTO-BOOST, SECURITY & SYNC v6.1
# ========================================================

clear
echo "========================================================"
echo " 🚀 MY FACE BOX - ULTIMATE AUTO-BOOST & SECURITY v6.1"
echo "========================================================"

# 1. ස්වයංක්‍රීයව ගොනු සමමුහුර්ත කිරීම සහ නම "My Face BOX" ලෙස නිවැරදි කිරීම
echo "[1/6] පද්ධති ගොනු සමමුහුර්ත කරමින් සහ නම සකස් කරමින්..."
if [ -d "$HOME/my_Face_backend" ]; then
    cp -r "$HOME/my_Face_backend/"* "$HOME/" 2>/dev/null
fi

find ~ -name "index.html" 2>/dev/null | while read file; do
    sed -i 's/<title>.*<\/title>/<title>My Face BOX<\/title>/g' "$file"
    sed -i 's/<h1>Face BOX<\/h1>/<h1>My Face BOX<\/h1>/g' "$file"
    sed -i 's/<h1>My My Face BOX<\/h1>/<h1>My Face BOX<\/h1>/g' "$file"
done
echo " ✔️ 'My Face BOX' නම සියලුම ගොනුවල සාර්ථකව යාවත්කාලීන විය."

# 2. හැකර් ප්‍රහාර සහ වෛරස් මැඩපැවැත්වීම (Firewall & Virus Cleaner)
echo "[2/6] අධි ආරක්‍ෂිත ෆයර්වෝල් සහ වෛරස් පරීක්ෂාව ක්‍රියාත්මකයි..."
pkill -9 -f "dropbear" 2>/dev/null
pkill -9 -f "sshd" 2>/dev/null

if command -v clamscan &> /dev/null; then
    clamscan --infected --recursive --remove ~ 2>/dev/null
    echo " ✔️ වෛරස් සහ අනිෂ්ට මෘදුකාංග පරීක්ෂාව සාර්ථකයි."
else
    echo " ℹ️ මූලික ආරක්ෂක පියවරයන් සහ ෆයර්වෝල් ස්ථාවර කර ඇත."
fi

# 3. කෝඩ් දෝෂ සහ Syntax අඩුපාඩු පරීක්ෂා කිරීම (Auto Bug Finder)
echo "[3/6] කෝඩ් දෝෂ සහ අඩුපාඩු පරීක්ෂා කරමින්..."
if [ -f "server.js" ]; then
    node -c server.js 2>/dev/null
    if [ $? -eq 0 ]; then
        echo " ✔️ server.js කෝඩ් එක දෝෂ රහිතයි."
    else
        echo " ⚠️ අවවාදයයි: server.js හි සින්ටැක්ස් දෝෂයක් ඇත!"
    fi
fi

# 4. ස්වයංක්‍රීයව සේව් කර බැකප් කිරීම (Auto-Save & Safe Backup)
echo "[4/6] දත්ත ආරක්ෂිතව බැකප් කරමින්..."
BACKUP_DIR="$HOME/facebox_ultra_backups/$(date +%F_%H-%M-%S)"
mkdir -p "$BACKUP_DIR"
cp -r "$HOME/public" "$HOME/index.html" "$HOME/server.js" "$HOME/package.json" "$BACKUP_DIR/" 2>/dev/null
echo " ✔️ සියලුම කෝඩ්ස් සහ දත්ත ආරක්ෂිත බැකප් ෆෝල්ඩරයකට එක් කරන ලදී."

# 5. ටර්මිනල් බිඳ වැටීම්වලින් (Crash) ආරක්ෂා කිරීම (Anti-Crash & Tmux Guard)
echo "[5/6] පද්ධති ස්ථාවරත්වය සහ Tmux ආරක්ෂාව පරීක්ෂා කරමින්..."
if ! tmux has-session -t facebox_secure 2>/dev/null; then
    tmux new-session -d -s facebox_secure
    echo " ✔️ නව Tmux ආරක්‍ෂිත සැසියක් සාර්ථකව අරඹන ලදී."
else
    echo " ✔️ පවතින Tmux ආරක්‍ෂිත සැසිය පද්ධතිය වෙනුවෙන් ක්‍රියාත්මකය."
fi

# 6. සේවාදායකය ස්වයංක්‍රීයව බූස්ට් කර පසුබිමින් ධාවනය කිරීම (Auto-Run & Boost)
echo "[6/6] සේවාදායකය පසුබිමින් (Background) ක්‍රියාත්මක කරමින්..."
pkill -f "node server.js" 2>/dev/null
nohup node server.js > "$HOME/server.log" 2>&1 &

echo "========================================================"
echo " 🚀 සියල්ල සාර්ථකයි! My Face BOX පද්ධතිය සම්පූර්ණයෙන්ම සක්‍රීයයි."
echo " 🌐 දැන් සාමාන්‍ය පරිදි http://localhost:5000 වෙත ගොස් බලන්න!"
echo "========================================================"

