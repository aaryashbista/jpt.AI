# app.py
# Simple ChatGPT-like Web App with Upload + Chatbot API

from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# ⚠️ Replace with your own API key (keep it secret)
OPENAI_API_KEY = "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"

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat UI</title>
    <style>
        body {
            margin: 0;
            background: #000;
            color: white;
            font-family: Arial, sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .center-text {
            text-align: center;
            margin-top: 30vh;
            font-size: 28px;
            font-weight: bold;
        }
        .chat {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
        }
        .msg {
            margin: 8px 0;
        }
        .user { color: #4da6ff; }
        .bot { color: #9cff57; }
        .bottom-bar {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            background: #111;
        }
        .plus-btn {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: none;
            font-size: 24px;
            cursor: pointer;
        }
        input[type=text] {
            flex: 1;
            margin: 0 10px;
            padding: 10px;
            border-radius: 20px;
            border: none;
        }
        input[type=file] {
            display: none;
        }
    </style>
</head>
<body>

<div class="chat" id="chat">
    <div class="center-text">What can I help with?</div>
</div>

<div class="bottom-bar">
    <button class="plus-btn" onclick="openUpload()">+</button>
    <input type="file" id="fileInput" />
    <input id="msg" type="text" placeholder="Ask ChatGPT" />
    <button onclick="sendMsg()">➤</button>
</div>

<script>
function openUpload() {
    document.getElementById('fileInput').click();
}

function addMessage(text, cls) {
    const chat = document.getElementById('chat');
    const div = document.createElement('div');
    div.className = 'msg ' + cls;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function sendMsg() {
    const input = document.getElementById('msg');
    const text = input.value;
    if (!text) return;

    addMessage('You: ' + text, 'user');
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
    })
    .then(res => res.json())
    .then(data => addMessage('Bot: ' + data.reply, 'bot'));
}
</script>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message']

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_msg}
        ]
    }

    r = requests.post('https://api.openai.com/v1/chat/completions',
                      headers=headers, json=payload)

    reply = r.json()['choices'][0]['message']['content']
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
