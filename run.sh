#!/bin/bash
fuser -k 5000/tcp 2>/dev/null
while true
do
    echo "[!] සේවාදායකය ආරක්ෂිතව ආරම්භ කරමින්..."
    node server.js
    echo "✗ සේවාදායකය බිඳ වැටුණි! තත්පර 2කින් ස්වයංක්‍රීයව නැවත ක්‍රියාත්මක වේ..."
    sleep 2
done
