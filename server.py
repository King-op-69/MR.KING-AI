from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

INSTAGRAM_USERNAME = None
INSTAGRAM_PASSWORD = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
    data = request.json
    INSTAGRAM_USERNAME = data.get("username")
    INSTAGRAM_PASSWORD = data.get("password")
    
    if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
        return jsonify({"status": "success", "message": "Logged in!"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials!"})

@app.route('/start-bot', methods=['POST'])
def start_bot():
    if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
        return jsonify({"status": "success", "message": "Bot started!"})
    else:
        return jsonify({"status": "error", "message": "Login first!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
