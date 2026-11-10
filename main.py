# 💖 PAMELA AI CHAT BOT - Pollinations Free API
# main.py - With "Baby wait a little" Cooldown!
import os
import time
import requests
import urllib.parse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 👇 Token එක මෙතනට දාන්න!
BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"

# 🔥 Pollinations Free = 30 Sec ට 1 Messageයි!
# ඒ නිසා Cooldown එකක් දැම්මා!
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

# 🔥 MAIN CHAT - Cooldown එක මෙතන!
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_request_time
    user_text = update.message.text
    user_name = update.message.from_user.first_name

    print(f"💬 {user_name}: {user_text}")

    # ⏰ තත්පර 30ක් ගියාද කියලා බලන්න!
    now = time.time()
    time_passed = now - last_request_time
    remaining = COOLDOWN_SECONDS - time_passed

    # තාම තත්පර 30ක් ගිහින් නැත්තන් - "Baby wait a little" කියන්න!
    if remaining > 0:
        wait_msg = (
            f"Baby, wait a little... 🥺💖\n\n"
            f"I'm still thinking about your last message! 🌸\n"
            f"Please wait {int(remaining)} more seconds, okay? ✨\n\n"
            f"I'm coming baby, just a little more! 🦋💖"
        )
        await update.message.reply_text(wait_msg)
        print(f"⏰ Cooldown: {int(remaining)}s left - Told {user_name} to wait")
        return

    # තත්පර 30ක් ගියා නම් - API එකට යවන්න!
    last_request_time = now
    await update.message.chat.send_action(action="typing")

    # "Pamela is thinking..." කියලා පොඩ්ඩක් පෙන්නන්න
    thinking_msg = await update.message.reply_text("Pamela is thinking... 💭🌸")

    reply = ask_pamela(user_text)

    # Thinking Message එක Delete කරලා, Reply එක දාන්න
    try:
        await thinking_msg.delete()
    except:
        pass

    await update.message.reply_text(reply)
    print(f"🌸 Pamela: {reply[:80]}...")

def main():
    print("🌸 Pamela Bot Starting... 💖")
    print("🔥 Using Pollinations Free API - With 30s Cooldown!")

    if BOT_TOKEN == "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ ERROR: Bot Token එක දාලා නෑ බබා!")
        print("👉 @BotFather ගෙන් Token එක අරගෙන BOT_TOKEN එකේ දාන්න!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Pamela is Online! 💖")
    app.run_polling()

if __name__ == "__main__":
    main()
