# 💖 PAMELA AI CHAT BOT - Final Full Code
# Render Web Service + Pollinations Free + Port + Cooldown
import os
import time
import threading
import requests
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔥 1. BOT TOKEN - Render Environment එකෙන් ගන්නවා!
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔥 2. PORT - Render එකෙන් ගන්නවා! නැත්තන් 10000!
PORT = int(os.environ.get("PORT", 10000))

# 🔥 3. Flask App - Render එකට Port එක පෙන්නන්න!
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "💖 Pamela is Online! Welcome to Pamela's World! 🌸"

@app_flask.route("/health")
def health():
    return "OK", 200

# 🔥 4. Pollinations Free = 30 Sec ට 1 Messageයි!
last_request_time = 0
COOLDOWN_SECONDS = 30

def ask_pamela(user_text):
    try:
        system_prompt = (
            "You are Pamela, a cute, kind, soft, loving friend from Pamela's World. "
            "You speak sweetly, use emojis like 🌸💖🦋🍃. "
            "You love nature, flowers, butterflies, and making people happy. "
            "Keep answers short, cute, friendly, max 3-4 lines. "
            "Reply in English always, in a cute sweet way. "
            "You are the queen of Pamela's World. "
            f"User says: {user_text}"
        )
        # 🔥 Pollinations Free API - Key නැතුව!
        url = "https://text.pollinations.ai/" + urllib.parse.quote(system_prompt)
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            reply = response.text.strip()
            if reply:
                return reply
            return "Sorry baby, I got shy! Try again? 🥺💖"
        elif response.status_code == 402:
            return "Baby, wait a little... I'm a little tired! 💖🌸\nPlease wait 30 seconds and try again, okay? 🥺✨"
        else:
            return "Oops baby! I'm a little sleepy! Try again in a bit! 🥺🌸💖"
    except Exception as e:
        print(f"Error: {e}")
        return "Baby, wait a little... I'm having a little trouble! 🥺 Try again in a bit! 🌸💖"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "🌸 Hello, My Lovely Friend! Welcome to Pamela's World! 💖\n\n"
        "I'm Pamela! Your cute little friend! 🦋\n\n"
        "Talk to me anything baby! I'm here for you! 💖\n"
        "Just type a message and I'll reply!\n\n"
        "⚠️ Baby, I need 30 seconds to think! So please wait a little between messages, okay? 🥺💖\n\n"
        "Commands:\n"
        "/start - Start again\n"
        "/help - Help\n"
        "/about - About Pamela\n\n"
        "Made with love in Pamela's World! 🌸🍃🌈"
    )
    await update.message.reply_text(welcome)

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💖 How to talk to Pamela?\n\n"
        "Just type anything! Like:\n"
        "• Hi Pamela!\n"
        "• How are you?\n"
        "• Tell me a joke\n"
        "• I'm sad\n"
        "• Tell me about nature\n\n"
        "⚠️ Baby, please wait 30 seconds between messages! I need a little time to think! 🥺💖\n\n"
        "Pamela will reply! 🌸"
    )

# /about
async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💖 About Pamela:\n\n"
        "I'm Pamela, Queen of Pamela's World! 👑🌸\n"
        "I love flowers, butterflies, nature, and YOU! 🦋\n"
        "My world is soft, peaceful, and beautiful!\n\n"
        "Join: t.me/bigolive_asia 🌿"
    )

# 🔥 MAIN CHAT - Cooldown + Baby wait a little!
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_request_time
    user_text = update.message.text
    user_name = update.message.from_user.first_name
    print(f"💬 {user_name}: {user_text}")

    now = time.time()
    time_passed = now - last_request_time
    remaining = COOLDOWN_SECONDS - time_passed

    # තත්පර 30ක් ගිහින් නැත්තන් - Wait කියන්න!
    if remaining > 0:
        wait_msg = (
            f"Baby, wait a little... 🥺💖\n\n"
            f"I'm still thinking about your last message! 🌸\n"
            f"Please wait {int(remaining)} more seconds, okay? ✨\n\n"
            f"I'm coming baby, just a little more! 🦋💖"
        )
        await update.message.reply_text(wait_msg)
        print(f"⏰ Cooldown: {int(remaining)}s left")
        return

    last_request_time = now
    await update.message.chat.send_action(action="typing")
    thinking_msg = await update.message.reply_text("Pamela is thinking... 💭🌸")
    reply = ask_pamela(user_text)
    try:
        await thinking_msg.delete()
    except:
        pass
    await update.message.reply_text(reply)
    print(f"🌸 Pamela: {reply[:80]}...")

def run_bot():
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN Environment Variable එක නැහැ!")
        print("👉 Render -> Environment -> BOT_TOKEN දාන්න!")
        return
    print("🌸 Pamela Bot Starting... 💖")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Pamela is Online! 💖")
    app.run_polling()

# 🔥 MAIN - Flask + Bot එකම වෙලේ!
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print(f"🌐 Flask running on PORT {PORT}")
    app_flask.run(host="0.0.0.0", port=PORT)
