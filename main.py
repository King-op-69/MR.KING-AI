import os
import time
import random
import logging
from datetime import datetime
from instabot import Bot

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instagram credentials
BOT_USERNAME = "_rip.king_"  
BOT_PASSWORD = "LISA#8900@"  

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

# Remove old session only once
def clear_sessions():
    if os.path.exists("config"):
        os.system("rm -rf config")

# Login function with session reuse
def login():
    bot = Bot()
    
    # Reuse session if exists
    if os.path.exists("config"):
        logging.info("Session found! Trying to reuse session...")
        bot.load_session(BOT_USERNAME)
        if bot.api.is_logged_in:
            logging.info("Session restored successfully!")
            return bot
        else:
            logging.warning("Session invalid, logging in again...")
            clear_sessions()
    
    try:
        bot.login(username=BOT_USERNAME, password=BOT_PASSWORD)
        logging.info("Login successful!")
        return bot
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return None

# Message handler with rate limiting
def handle_messages(bot):
    fail_count = 0

    while True:
        try:
            messages = bot.get_messages()
            for msg in messages:
                user = msg.get("user", {}).get("username", "")
                text = msg.get("text", "").lower()

                if not user or not text:
                    continue

                # Protect your wife
                if WIFE_USERNAME in text and "bad" in text:
                    bot.send_message("Meri bhabhi ke bare me aise mat bol! ⚠️", [msg["user"]["pk"]])

                # Special reply for owner
                elif user == OWNER_USERNAME:
                    bot.send_message(f"Bhai @_mr.king_op_! Tu aa gaya? 😎 Kya haal hai?", [msg["user"]["pk"]])

                # Good morning and good night messages
                now = datetime.now().time()
                if now.hour == 7:
                    bot.send_message(GOOD_MORNING, [msg["user"]["pk"]])
                elif now.hour == 22:
                    bot.send_message(GOOD_NIGHT, [msg["user"]["pk"]])
                else:
                    bot.send_message(random.choice(ROAST_REPLY), [msg["user"]["pk"]])

                # Random delay between messages to prevent bans
                time.sleep(random.randint(5, 15))

            # Wait longer after batch processing
            time.sleep(600)  

        except Exception as e:
            logging.error(f"Error in message handling: {e}")
            fail_count += 1

            # If too many errors, pause bot
            if fail_count >= 3:
                logging.warning("Too many errors! Pausing bot for 15 minutes to avoid block.")
                time.sleep(900)  # 15 min pause
                fail_count = 0

            time.sleep(30)  # Retry after short delay

if __name__ == "__main__":
    bot = login()
    if bot:
        handle_messages(bot)
