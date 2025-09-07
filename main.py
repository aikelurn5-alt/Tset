import telebot
import os
import re
from url import check_url

API_TOKEN = os.environ.get('API_TOKEN')

if not API_TOKEN:
    raise ValueError("No API_TOKEN environment variable set")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot
I can analyze websites with /url command
""")

@bot.message_handler(commands=['url'])
def send_url(message):
    url = message.text[len('/url '):].strip()
    if not re.match(r'^https?://[^\s]+$', url):
        bot.reply_to(message, "Invalid URL format. Please include http:// or https://")
        return

    bot0 = bot.reply_to(message, "Please wait... ⏳")
    try:
        result = check_url(url)
        bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
    except Exception as e:
        bot.edit_message_text(f"Error: {str(e)}", chat_id=bot0.chat.id, message_id=bot0.message_id)

if __name__ == "__main__":
    print("Bot is working!")
    bot.infinity_polling()
