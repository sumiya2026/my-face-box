#!/bin/bash

echo "🚀 මහගෙදර FB ඇප් එක සූදානම් කරමින් පවතී..."

# 1. Node.js පරීක්ෂා කර ඉන්ස්ටෝල් කිරීම
if ! command -v node &> /dev/null
then
    echo "📦 Node.js ඉන්ස්ටෝල් කරමින්..."
    pkg update && pkg install nodejs -y
fi

# 2. package.json නැත්නම් සදාගැනීම සහ පැකේජ් දැමීම
if [ ! -f "package.json" ]; then
    echo "⚙️ package.json සහ පැකේජ් ඉන්ස්ටෝල් කරමින්..."
    npm init -y
    npm install express mongoose
fi

# 3. අවශ්‍ය ෆෝල්ඩර් සෑදීම
mkdir -p public plugins templates

echo "✅ සියල්ල සූදානම්! සර්වර් එක ආරම්භ වේ..."

# 4. සර්වර් එක රන් කිරීම
node server.js

