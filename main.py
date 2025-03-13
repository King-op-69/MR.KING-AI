import os
import time
import random
import requests
import logging
from datetime import datetime
from instabot import Bot

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instagram credentials
BOT_USERNAME = "_rip.king_"  # Direct username
BOT_PASSWORD = "LISA#8900@"  # Direct password (Consider using environment variables for security)

# Personal details
OWNER_USERNAME = "_mr.king_op_"
WIFE_USERNAME = "ursxlisaaa"

# Messages
WELCOME_MSG = "Welcome to the group! 🎉 How can I assist you today?"
HELP_MSG = "You can ask me anything about our services or just say hi! 😊"
ROAST_REPLY = [
    "Bhai, zyada soch mat. Seedha pooch le! 😂",
    "Aree, itna slow kyu? Thoda fast soch na! 🔥",
    "Teri soch se fast hai meri coding! 😎"
]
GOOD_MORNING = "Good morning, doston! ☀️ Have a great day!"
GOOD_NIGHT = "Good night, doston! 🌙 Sweet dreams!"

# Remove any previous sessions
def clear_sessions():
    if os.path.exists("config"):
        os.system("rm -rf config")

# Login function without proxy
def login():
    clear_sessions()
    bot = Bot()
    bot.login(username=BOT_USERNAME, password=BOT_PASSWORD, use_cookie=True)
    return bot

# Message handling function
def handle_messages(bot):
    while True:
        try:
            messages = bot.get_messages()
            for message_data in messages:
                if isinstance(message_data, dict):
                    user = message_data.get("user", {}).get("username", "")
                    text = message_data.get("text", "").lower()

                    if not user or not text:
                        continue

                    # Protect your wife
                    if WIFE_USERNAME in text and "bad" in text:
                        bot.send_message("Meri bhabhi ke bare me aise mat bol! ⚠️", [message_data["user"]["pk"]])

                    # Special reply for owner
                    elif user == OWNER_USERNAME:
                        bot.send_message(f"Bhai @_mr.king_op_! Tu aa gaya? 😎 Kya haal hai?", [message_data["user"]["pk"]])

                    # Good morning and good night messages
                    now = datetime.now().time()
                    if now.hour == 7:
                        bot.send_message(GOOD_MORNING, [message_data["user"]["pk"]])
                    elif now.hour == 22:
                        bot.send_message(GOOD_NIGHT, [message_data["user"]["pk"]])

                    # Roast random members
                    else:
                        bot.send_message(random.choice(ROAST_REPLY), [message_data["user"]["pk"]])

            time.sleep(600)  # Check messages every 10 minutes

        except Exception as e:
            logging.error(f"Error in message handling: {e}")
            time.sleep(30)  # Wait before retrying

if __name__ == "__main__":
    bot = login()
    handle_messages(bot)
