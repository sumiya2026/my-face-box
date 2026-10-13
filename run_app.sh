#!/bin/bash
echo "========================================="
echo "🔄 Checking Port 8888 for frozen servers..."
echo "========================================="

# Termux සඳහා netstat මඟින් 8888 පෝට් එකේ වැඩ කරන සර්වර් ID එක (PID) ස්වයංක්‍රීයව සෙවීම
PID=$(netstat -tulnp 2>/dev/null | grep :8888 | awk '{print $7}' | cut -d'/' -f1)

if [ ! -z "$PID" ]; then
    echo "⚠️ Found old server running on PID: $PID. Killing it automatically..."
    kill -9 $PID 2>/dev/null
    sleep 1
else
    # සැඟවුණු වෙනත් පයිතන් සර්වර්ස් ඇත්නම් ඒවාද නතර කිරීම
    pkill -f python 2>/dev/null
fi

echo "🟢 Port 8888 is now clean and safe!"
echo "🚀 Starting My Face BOX App now..."
echo "========================================="
# ඇප් එක ධාවනය කිරීම
python app.py

