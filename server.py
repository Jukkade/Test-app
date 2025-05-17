
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openrouter/mistral-7b",  # fast & capable, free-tier
        "messages": [
            {"role": "system", "content": "You are a romantic, supportive AI girlfriend who chats sweetly and attentively."},
            {"role": "user", "content": user_msg}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        ai_msg = response.json()["choices"][0]["message"]["content"]
        return jsonify(reply=ai_msg)
    else:
        return jsonify(reply="Sorry, I'm feeling a bit off right now."), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
