#!/bin/bash
clear
echo "=========================================="
echo "    MY FACE BOX SECURITY SYSTEM STARTING   "
echo "=========================================="
pkill -f http.server 2>/dev/null
pkill -f python 2>/dev/null
export NODE_ENV=production
echo "[+] සර්වර් එක සක්‍රීය වෙමින් පවතී (Localhost:5000)..."
echo "------------------------------------------"
while true; do
    python3 -m http.server 5000 2>/dev/null
    echo "[!!] ටර්මිනල් බිඳ වැටීමක් හඳුනාගන්නා ලදී! ස්වයංක්‍රීයව නැවත ක්‍රියාත්මක වේ..."
    sleep 3
done
