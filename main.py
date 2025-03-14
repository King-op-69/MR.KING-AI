import os
import time
import random
import logging
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from instabot import Bot

# Flask App Setup
app = Flask(__name__)

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# इंस्टाग्राम क्रेडेंशियल्स (Railway ENV Variables से लेंगे)
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")
OWNER_USERNAME = os.getenv("OWNER_USERNAME")
WIFE_USERNAME = os.getenv("WIFE_USERNAME")

# मैसेज टेम्प्लेट्स
WELCOME_MSG = "Welcome to the group! \U0001F389 How can I assist you today?"
HELP_MSG = "You can ask me anything about our services or just say hi! \U0001F60A"
ROAST_REPLY = ["Bhai, zyada soch mat!", "Fast soch na! \U0001F525", "Coding se fast hai meri soch! \U0001F60E"]
GOOD_MORNING = "Good morning, doston! \u2600\ufe0f"
GOOD_NIGHT = "Good night, doston! \U0001F319"

# सेशन क्लियर करने का फ़ंक्शन
def clear_sessions():
    if os.path.exists("config"):
        os.system("rm -rf config")

# इंस्टाग्राम लॉगिन फंक्शन
def login():
    clear_sessions()
    bot = Bot()
    
    try:
        bot.login(username=BOT_USERNAME, password=BOT_PASSWORD, use_cookie=False)
        logging.info("\u2705 Login Successful!")
        return bot
    except Exception as e:
        logging.error(f"\u274C Login Failed: {e}")
        return None

# AI-बेस्ड रिप्लाई फंक्शन
def generate_reply(message):
    message = message.lower()
    
    if "help" in message:
        return HELP_MSG
    if "good morning" in message:
        return GOOD_MORNING
    if "good night" in message:
        return GOOD_NIGHT
    
    return random.choice(ROAST_REPLY)

# मैसेज हैंडलिंग का सिस्टम (Thread में चलाना होगा)
def handle_messages(bot):
    while True:
        try:
            messages = bot.get_messages()
            for msg in messages:
                user = msg.get("user", {}).get("username", "")
                text = msg.get("text", "").lower()

                if not user or not text:
                    continue

                if WIFE_USERNAME in text and "bad" in text:
                    bot.send_message("Meri bhabhi ke bare me aise mat bol! \u26A0\ufe0f", [msg["user"]["pk"]])

                elif user == OWNER_USERNAME:
                    bot.send_message(f"Bhai @{OWNER_USERNAME}! Tu aa gaya? \U0001F60E Kya haal hai?", [msg["user"]["pk"]])

                else:
                    reply = generate_reply(text)
                    bot.send_message(reply, [msg["user"]["pk"]])

            time.sleep(600)

        except Exception as e:
            logging.error(f"⚠️ Error in message handling: {e}")
            time.sleep(30)

# API ROUTES
@app.route('/')
def home():
    return "MR.KING AI is running successfully!"

@app.route('/start-bot', methods=['GET'])
def start_bot():
    bot = login()
    if bot:
        thread = threading.Thread(target=handle_messages, args=(bot,))
        thread.start()
        return jsonify({"status": "✅ Bot Started Successfully!"})
    else:
        return jsonify({"status": "❌ Error in Login!"})

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get("message", "No message received")
    return jsonify({"response": f"AI received: {message}"})

# Gunicorn के लिए पोर्ट फिक्स
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
