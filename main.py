import os
import time
import random
import logging
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

# Flask App Setup
app = Flask(__name__)

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instagram Credentials (Railway ENV Variables से लेंगे)
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "_mr.king_op_")
WIFE_USERNAME = os.getenv("WIFE_USERNAME", "ursxlisaaa")

# Messages
WELCOME_MSG = "Welcome! 🎉 How can I assist you today?"
HELP_MSG = "Ask me anything about our services or just say hi! 😊"
ROAST_REPLY = ["Bhai, zyada soch mat!", "Fast soch na! 🔥", "Coding se fast hai meri soch! 😎"]
GOOD_MORNING = "Good morning! ☀️"
GOOD_NIGHT = "Good night! 🌙"

# Function to Start Instagram Web Login
def start_instagram_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.instagram.com/accounts/login/")
        input("👉 Login manually and press Enter here...")
        cookies = page.context.cookies()
        with open("cookies.json", "w") as f:
            f.write(str(cookies))
        browser.close()
    return "✅ Instagram Login Successful!"

# API Route: Start Instagram Web Login
@app.route('/login-instagram', methods=['GET'])
def login_instagram():
    response = start_instagram_login()
    return jsonify({"status": response})

# API Route: Start Bot
@app.route('/start-bot', methods=['GET'])
def start_bot():
    return jsonify({"status": "✅ Bot Started Successfully!"})

# Run Flask App
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)