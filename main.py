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

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instagram Credentials (Login Panel से आएंगे)
INSTAGRAM_USERNAME = None
INSTAGRAM_PASSWORD = None

# Bot Status
bot_running = False

# Messages Templates
WELCOME_MSG = "Welcome to the group! 🎉 How can I assist you today?"
HELP_MSG = "You can ask me anything about our services or just say hi! 😊"
ROAST_REPLY = ["Bhai, zyada soch mat!", "Fast soch na! 🔥", "Coding se fast hai meri soch! 😎"]
GOOD_MORNING = "Good morning, doston! ☀️"
GOOD_NIGHT = "Good night, doston! 🌙"

# Instagram Secure Login via Web Automation
def login_instagram(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Headless=False for manual captcha solving
        page = browser.new_page()
        page.goto("https://www.instagram.com/accounts/login/")
        
        time.sleep(5)  # Wait for page to load
        
        # Enter Username & Password
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        
        time.sleep(10)  # Wait for login process
        browser.close()

# AI-Powered Reply System
def generate_reply(message):
    message = message.lower()
    
    if "help" in message:
        return HELP_MSG
    if "good morning" in message:
        return GOOD_MORNING
    if "good night" in message:
        return GOOD_NIGHT
    
    return random.choice(ROAST_REPLY)

# Message Handling
def handle_messages():
    global bot_running
    bot_running = True
    
    while bot_running:
        try:
            # Messages Handling Logic (To Be Implemented)
            time.sleep(600)  # Check messages every 10 min

        except Exception as e:
            logging.error(f"⚠️ Error in message handling: {e}")
            time.sleep(30)  # Retry after error

# 📌 API Routes
@app.route('/')
def home():
    return "MR.KING AI is Running Successfully!"

@app.route('/login', methods=['POST'])
def login():
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
    data = request.json
    INSTAGRAM_USERNAME = data.get("username")
    INSTAGRAM_PASSWORD = data.get("password")

    if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
        login_instagram(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        return jsonify({"status": "success", "message": "Instagram Logged In!"})
    else:
        return jsonify({"status": "error", "message": "Invalid Credentials!"})

@app.route('/start-bot', methods=['GET'])
def start_bot():
    global bot_running
    if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
        if not bot_running:
            thread = threading.Thread(target=handle_messages)
            thread.start()
            return jsonify({"status": "success", "message": "Bot Started Successfully!"})
        else:
            return jsonify({"status": "error", "message": "Bot is Already Running!"})
    else:
        return jsonify({"status": "error", "message": "Login First!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)