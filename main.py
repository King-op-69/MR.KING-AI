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
BOT_PASSWORD = os.getenv("BOT_PASSWORD")  # Secure password from environment variable

# Personal details
OWNER_USERNAME = "_mr.king_op_"  # Corrected owner username
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

# Function to fetch free proxies
def fetch_proxies():
    try:
        response = requests.get('https://www.proxy-list.download/api/v1/get?type=http', timeout=5)
        if response.status_code == 200:
            proxies = response.text.strip().split("\r\n")
            return [proxy for proxy in proxies if proxy]
        else:
            logging.warning("Failed to fetch proxies. Using direct connection.")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Proxy fetch error: {e}")
        return []

# Function to get a random proxy
def get_random_proxy():
    proxies = fetch_proxies()
    if proxies:
        proxy = random.choice(proxies)
        logging.info(f"Using Proxy: {proxy}")
        return proxy
    else:
        logging.warning("No proxies available, using direct connection.")
        return None

# Remove any previous sessions
def clear_sessions():
    if os.path.exists("config"):
        os.system("rm -rf config")

# Login function with proxy support
def login():
    clear_sessions()
    proxy = get_random_proxy()
    
    bot = Bot(proxy=f"http://{proxy}" if proxy else None)
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

            # Auto-switch proxy every 10 minutes without logging out
            time.sleep(600)
            logging.info("Switching Proxy...")
            proxy = get_random_proxy()
            if proxy:
                bot.api.session.proxies.update({"http": f"http://{proxy}", "https": f"http://{proxy}"})

        except Exception as e:
            logging.error(f"Error in message handling: {e}")
            time.sleep(30)  # Wait before retrying

if __name__ == "__main__":
    bot = login()
    handle_messages(bot)
