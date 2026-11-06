import os
import requests
from datetime import date
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
DAILY_LIMIT = 100
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HI I'M YADANAR💖 you can chat with me.. 💛i'm sweet lovely Myanmar girl")

async def usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    today = str(date.today())
    if user_id not in user_data or user_data[user_id][0] != today:
        await update.message.reply_text(f"You used 0/{DAILY_LIMIT} today")
    else:
        used = user_data[user_id][1]
        await update.message.reply_text(f"You used {used}/{DAILY_LIMIT} today\nRemaining: {DAILY_LIMIT - used}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id
    today = str(date.today())
    if not user_text:
        return

    if user_id not in user_data or user_data[user_id][0] != today:
        user_data[user_id] = [today, 0]

    if user_data[user_id][1] >= DAILY_LIMIT:
        await update.message.reply_text(f"Limit reached ({DAILY_LIMIT}/day). Try tomorrow. Check /usage")
        return

    try:
        response = requests.get(f"https://text.pollinations.ai/{user_text}", timeout=25)
        bot_reply = response.text[:3500]
        user_data[user_id][1] += 1
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("usage", usage))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
