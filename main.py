import os
import json
import time
import logging
from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright

# Flask App Setup
app = Flask(__name__, template_folder="templates")

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Hardcoded Admin Credentials (Change These!)
ADMIN_ID = "admin"
ADMIN_PASS = "password123"

# Function to Start Instagram Manual Login
def start_instagram_login(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        time.sleep(5)
        cookies = page.context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)
        browser.close()
    return "✅ Instagram Login Successful!"

# API Route: Home Page
@app.route('/')
def home():
    return render_template("index.html")

# API Route: Admin Login
@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    if data['admin_id'] == ADMIN_ID and data['admin_password'] == ADMIN_PASS:
        return jsonify({"status": "✅ Admin Login Successful!"})
    else:
        return jsonify({"status": "❌ Incorrect Admin Credentials!"})

# API Route: Start Instagram Login
@app.route('/login-instagram', methods=['POST'])
def login_instagram():
    data = request.json
    response = start_instagram_login(data['username'], data['password'])
    return jsonify({"status": response})

# API Route: Start Bot
@app.route('/start-bot', methods=['GET'])
def start_bot():
    return jsonify({"status": "✅ Bot Started Successfully!"})

# Run Flask App
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
