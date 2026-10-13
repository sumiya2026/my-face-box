from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

posts = []
messages = [
    {"sender": "other", "text": "ආයුබෝවන් සුමිය! අද ඇප් එකේ වැඩ කොහොමද?"},
    {"sender": "me", "text": "නියමයි! වැඩසටහන ඉතා සාර්ථකයි."}
]

@app.route('/')
def home():
    return render_template('facebox.html')

@app.route('/api/feed')
def get_feed():
    return jsonify({"posts": posts})

@app.route('/api/create-post', methods=['POST'])
def create_post():
    data = request.json
    new_post = {
        "id": len(posts) + 1,
        "name": data.get("name", "Sumiya User"),
        "content": data.get("content", ""),
        "image": data.get("image", None),
        "likes": 0,
        "comments": []
    }
    posts.insert(0, new_post)
    return jsonify({"success": True})

@app.route('/api/delete-post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return jsonify({"success": True})

@app.route('/api/edit-post/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    data = request.json
    for p in posts:
        if p["id"] == post_id:
            p["content"] = data.get("content", p["content"])
    return jsonify({"success": True})

@app.route('/api/add-comment', methods=['POST'])
def add_comment():
    data = request.json
    post_id = data.get("postId")
    for p in posts:
        if p["id"] == post_id:
            p.get("comments", []).append({
                "name": data.get("name", "User"),
                "text": data.get("text", "")
            })
    return jsonify({"success": True})

@app.route('/api/messages')
def get_messages():
    return jsonify({"messages": messages})

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json
    messages.append({"sender": "me", "text": data.get("text", "")})
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)

