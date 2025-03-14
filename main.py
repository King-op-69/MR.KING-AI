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
WELCOME_MSG = "Welcome to the group! 🎉 How can I assist you today?"
HELP_MSG = "You can ask me anything about our services or just say hi! 😊"
ROAST_REPLY = ["Bhai, zyada soch mat!", "Fast soch na! 🔥", "Coding se fast hai meri soch! 😎"]
GOOD_MORNING = "Good morning, doston! ☀️"
GOOD_NIGHT = "Good night, doston! 🌙"

# सेशन क्लियर करने का फ़ंक्शन
def clear_sessions():
    if os.path.exists("config"):
        os.system("rm -rf config")

# इंस्टाग्राम लॉगिन फंक्शन
def login():
    clear_sessions()
    bot = Bot()
    
    try:
        bot.login(username=BOT_USERNAME, password=BOT_PASSWORD, use_cookie=False)  # Railway के लिए use_cookie=False
        logging.info("✅ Login Successful!")
        return bot
    except Exception as e:
        logging.error(f"❌ Login Failed: {e}")
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

                # वाइफ का सम्मान
                if WIFE_USERNAME in text and "bad" in text:
                    bot.send_message("Meri bhabhi ke bare me aise mat bol! ⚠️", [msg["user"]["pk"]])

                # ओनर को स्पेशल मैसेज
                elif user == OWNER_USERNAME:
                    bot.send_message(f"Bhai @{OWNER_USERNAME}! Tu aa gaya? 😎 Kya haal hai?", [msg["user"]["pk"]])

                # AI रिप्लाई
                else:
                    reply = generate_reply(text)
                    bot.send_message(reply, [msg["user"]["pk"]])

            time.sleep(600)  # 10 मिनट के गैप के साथ रन करेगा

        except Exception as e:
            logging.error(f"⚠️ Error in message handling: {e}")
            time.sleep(30)  # एरर आने पर 30 सेकंड बाद फिर ट्राई करेगा

# 📌 बॉट स्टार्ट करने के लिए API (Thread में रन करेगा)
@app.route('/start-bot', methods=['GET'])
def start_bot():
    bot = login()
    if bot:
        thread = threading.Thread(target=handle_messages, args=(bot,))
        thread.start()
        return jsonify({"status": "✅ Bot Started Successfully!"})
    else:
        return jsonify({"status": "❌ Error in Login!"})

# 📌 Gunicorn के लिए पोर्ट फिक्स
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Railway के लिए dynamic port
    app.run(host='0.0.0.0', port=port, debug=True)