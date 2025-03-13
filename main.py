import os
import time
import random
import logging
from datetime import datetime
from instabot import Bot
from flask import Flask, jsonify

# Flask App for API
app = Flask(__name__)

# Logging setup (Better Error Tracking)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Environment Variables
BOT_USERNAME = os.getenv("BOT_USERNAME", "_rip.king_")  
BOT_PASSWORD = os.getenv("BOT_PASSWORD", "LISA#8900@")  
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "_mr.king_op_")
WIFE_USERNAME = os.getenv("WIFE_USERNAME", "ursxlisaaa")

# Messages
WELCOME_MSG = "Welcome to the group! 🎉 How can I assist you today?"
HELP_MSG = "You can ask me anything about our services or just say hi! 😊"
ROAST_REPLY = [
    "Bhai, zyada soch mat!", "Fast soch na! 🔥", "Coding se fast hai meri soch! 😎"
]
GOOD_MORNING = "Good morning, doston! ☀️"
GOOD_NIGHT = "Good night, doston! 🌙"

# Remove old sessions safely
def clear_sessions():
    if os.path.exists("config"):
        import shutil
        shutil.rmtree("config")  # ज़्यादा सुरक्षित तरीका

# Secure Login with Session Management
def login():
    clear_sessions()
    bot = Bot()
    
    try:
        bot.login(username=BOT_USERNAME, password=BOT_PASSWORD, use_cookie=True)
        logging.info("Login Successful!")
        return bot
    except Exception as e:
        logging.error(f"Login Failed: {e}")
        return None

# AI-Powered Reply Handling (More Human-like responses)
def generate_reply(message):
    if "help" in message:
        return HELP_MSG
    if "good morning" in message:
        return GOOD_MORNING
    if "good night" in message:
        return GOOD_NIGHT
    return random.choice(ROAST_REPLY)

# Improved Message Handling
def handle_messages(bot):
    while True:
        try:
            messages = bot.get_messages()
            for msg in messages:
                user = msg.get("user", {}).get("username", "")
                text = msg.get("text", "").lower()

                if not user or not text:
                    continue

                # Respect for Wife
                if WIFE_USERNAME in text and "bad" in text:
                    bot.send_message("Meri bhabhi ke bare me aise mat bol! ⚠️", [msg["user"]["pk"]])

                # Owner Special Message
                elif user == OWNER_USERNAME:
                    bot.send_message(f"Bhai @{OWNER_USERNAME}! Tu aa gaya? 😎 Kya haal hai?", [msg["user"]["pk"]])

                # AI-Based Replies
                else:
                    reply = generate_reply(text)
                    bot.send_message(reply, [msg["user"]["pk"]])

            time.sleep(600)  # 10-Minute Delay for Smooth Operation

        except Exception as e:
            logging.error(f"Error in message handling: {e}")
            time.sleep(30)

@app.route('/start-bot', methods=['GET'])
def start_bot():
    bot = login()
    if bot:
        handle_messages(bot)
        return jsonify({"status": "Bot Started Successfully!"})
    else:
        return jsonify({"status": "Error in Login!"})

# Gunicorn Compatibility (Correct Port Handling)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
