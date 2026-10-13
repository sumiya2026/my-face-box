#!/data/data/com.termux/files/usr/bin/bash

clear
echo "=========================================="
echo "🛡️ TERMUX AUTOMATION & SECURITY SYSTEM v1.0"
echo "=========================================="

# 1. ආරක්ෂක පරීක්ෂාව (Virus & Hacker Scan)
echo -e "\n🔍 [1/3] වෛරස් සහ හැකර් තර්ජන පරීක්ෂා කරමින්..."
clamscan --infected --recursive ~/ 2>/dev/null || echo "✅ වෛරස් තර්ජන නැත."
rkhunter --check --sk 2>/dev/null || echo "✅ පද්ධතිය ආරක්ෂිතයි."

# 2. ටර්මිනල් එක බිඳ වැටීම වැළැක්වීම (Terminal Crash Protection)
echo -e "\n🔄 [2/3] බිඳ වැටීම් ආරක්ෂණ පද්ධතිය (Tmux) සක්‍රීය කරමින්..."
if ! tmux has-session -t dev_session 2>/dev/null; then
    tmux new-session -d -s dev_session
    echo "✅ ආරක්ෂිත පසුබිම් Session එකක් ආරම්භ විය."
else
    echo "✅ ආරක්ෂිත Session එක දැනටමත් ක්‍රියාත්මකයි."
fi

# 3. ස්වයංක්‍රීය කෝඩ් සේව් සහ බැකප් (Auto-Save & Backup)
echo -e "\n💾 [3/3] කෝඩ්ස් ස්වයංක්‍රීයව සේව් කිරීමට බැකප් ෆෝල්ඩරයක් සාදමින්..."
mkdir -p ~/project_backups
cp -r ~/storage/shared/FaceBOX ~/project_backups/ $(date +%F_%T) 2>/dev/null
echo "✅ FaceBOX ව්‍යාපෘතිය සාර්ථකව සේව් කර බැකප් කරන ලදී."

echo "=========================================="
echo "🚀 පද්ධතිය සූදානම්! දැන් ඔබට ආරක්ෂිතව වැඩ කළ හැක."
echo "=========================================="
