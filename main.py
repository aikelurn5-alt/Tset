import telebot
import os
import re
from url import check_url

# Environment variable ကို စစ်ဆေးပါ
API_TOKEN = os.environ.get('API_TOKEN')
if not API_TOKEN:
    print("ERROR: No API_TOKEN environment variable found!")
    # Fallback to hardcoded token (temporary solution)
    API_TOKEN = '7541477009:AAEPEaYn7sT_CCQ_OB5foTOIO8fP8Si4-so'
    print("Using fallback token (not recommended for production)")

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
    print("Bot is starting...")
    print(f"Token: {API_TOKEN[:10]}...")  # Token ရဲ့ first 10 characters ကိုပဲ ပြမယ်
    try:
        bot.infinity_polling()
        print("Bot is running!")
    except Exception as e:
        print(f"Bot error: {e}")
