# 💖 PAMELA AI - MEGA ULTIMATE BOT 👑🔥🌸
# 100% ENGLISH VERSION - FIXED FOR PYTHON 3.14 + PTB v22
# FIXED: Promo + GM + GN Now Works Without /start - Auto Register + GROUP_IDS
import os, time, threading, asyncio, requests, urllib.parse, random, json, datetime, pytz
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))
app_flask = Flask(__name__)
@app_flask.route("/")
def home(): return "💖 Pamela MEGA is Online! 👑"
@app_flask.route("/health")
def health(): return "OK", 200

# 👑 FIXED - GROUP IDS FROM ENV + AUTO REGISTER
GROUP_IDS = []
try:
    _g = os.getenv("GROUP_IDS", "")
    if _g:
        GROUP_IDS = [int(x.strip()) for x in _g.split(",") if x.strip()]
except: GROUP_IDS = []
ACTIVE_CHATS = set(GROUP_IDS)

last_request_times = {}
COOLDOWN_SECONDS = 30
warns = {}
afk_users = {}
filters_db = {}
notes_db = {}
coins_db = {}
levels_db = {}
user_db = {}
msg_db = {}
flood_db = {}
bank_db = {}
stats_db = {}
quiz_db = {}
ttt_games = {}
memory_db = {}
streak_db = {}

def load_json(file, default):
    try:
        if os.path.exists(file):
            with open(file, "r") as f: return json.load(f)
    except: pass
    return default
def save_json(file, data):
    try:
        with open(file, "w") as f: json.dump(data, f)
    except: pass

user_db = load_json("pamela_users.json", {})
msg_db = load_json("pamela_messages.json", {})
filters_db = load_json("pamela_filters.json", {})
notes_db = load_json("pamela_notes.json", {})
coins_db = load_json("pamela_coins.json", {})
levels_db = load_json("pamela_levels.json", {})
bank_db = load_json("pamela_bank.json", {})
stats_db = load_json("pamela_stats.json", {})
memory_db = load_json("pamela_memory.json", {})
streak_db = load_json("pamela_streak.json", {})

def save_user(chat_id, user_id):
    chat_id=str(chat_id)
    if chat_id not in user_db: user_db[chat_id]=[]
    if user_id not in user_db[chat_id]:
        user_db[chat_id].append(user_id); save_json("pamela_users.json", user_db)

def get_all_chats():
    chats = set(ACTIVE_CHATS)
    try:
        for k in list(user_db.keys()):
            if str(k).lstrip("-").isdigit():
                chats.add(int(k))
    except: pass
    for gid in GROUP_IDS:
        chats.add(gid)
    return list(chats)

def save_chat_id(chat_id):
    try:
        ACTIVE_CHATS.add(int(chat_id))
        save_user(chat_id, 0)
    except: pass

def save_message(chat_id, msg_id, user_name, username, text):
    chat_id=str(chat_id)
    if chat_id not in msg_db: msg_db[chat_id]=[]
    msg_db[chat_id].append({"msg_id":msg_id,"user":user_name,"username":username,"text":text,"time":time.time()})
    if len(msg_db[chat_id])>100: msg_db[chat_id]=msg_db[chat_id][-100:]
    save_json("pamela_messages.json", msg_db)

def check_cooldown(chat_id):
    now=time.time(); last=last_request_times.get(chat_id,0); rem=COOLDOWN_SECONDS-(now-last)
    if rem>0: return int(rem)
    last_request_times[chat_id]=now; return 0

def translate_text(text, target):
    try:
        url=f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={urllib.parse.quote(text)}"
        r=requests.get(url, timeout=10); d=r.json(); return "".join([x[0] for x in d[0] if x[0]])
    except: return None

CUTE_STARTS=["🌸💖 ","🦋✨ ","🌷💗 ","💖🌸 ","🍓💖 ","🌈💕 ","✨🦋 ","💐💖 "]
CUTE_ENDS=["\n\n💖🌸 Love you, baby! 🌸💖","\n\n🦋💕 Pamela loves you! 💕🦋","\n\n🌸✨ Stay cute, baby! ✨🌸","\n\n💖🍓 You are my fav! 🍓💖","\n\n🌷💖 Hugs from Pamela! 🤗💖","\n\n✨💖 Muahhh! 😘💖"]
def make_cute(r): return f"{random.choice(CUTE_STARTS)}{r}{random.choice(CUTE_ENDS)}"
def ask_pamela(t, user_id=None):
    try:
        mem=""
        if user_id:
            uid=str(user_id); hist=memory_db.get(uid, [])
            if hist: mem=" Past chat: "+" | ".join(hist[-3:])
        p=("You are Pamela, CUTEST princess! 👑🌸💖 Use LOTS cute emojis EVERY sentence! 🌸💖🦋🌷✨🍓💕🌈😘🤗💐🧸🎀🍰 Be super cute, soft, baby-talk. Call user 'baby','cutie'. Use 'hehe','awww','hihi','yayyy','muahhh','🥹','🥺'. Keep short max 3-4 lines. Always bubbly! IMPORTANT: Reply in EXACT SAME language as user! "+mem+f" User says: {t}")
        url="https://text.pollinations.ai/"+urllib.parse.quote(p); res=requests.get(url, timeout=60)
        if res.status_code==200:
            rep=res.text.strip()
            if rep:
                if user_id:
                    uid=str(user_id)
                    if uid not in memory_db: memory_db[uid]=[]
                    memory_db[uid].append(f"User: {t} | Pamela: {rep[:100]}")
                    if len(memory_db[uid])>10: memory_db[uid]=memory_db[uid][-10:]
                    save_json("pamela_memory.json", memory_db)
                return make_cute(rep)
            return "Sorry baby! 🥺💖 I got shy! 🦋 Try again? 🥹✨"
        elif res.status_code==402: return "Baby! 🥺💖 I'm tired! 🧸🌸 Wait 30 sec! 🥹✨"
        else: return "Oops baby! 🥺🌸 Sleepy! 💤💖 Try again! 🦋✨"
    except: return "Baby! 🥺💖 Trouble! 🌧️🌸 Try again! 🦋✨"

async def is_admin(update, uid):
    try:
        m=await update.effective_chat.get_member(uid); return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except: return False
def get_target(update):
    if update.message.reply_to_message: return update.message.reply_to_message.from_user
    return None

TRUTHS=["Who is your crush? 🥹💖","Who did you lie to last? 😂","Tell a secret you never told anyone! 🤫","What is the last photo on your phone? 📸","Who do you secretly love? 💖","What is your biggest fear? 🥺","Have you ever cried for someone? 💔","Who is the most beautiful person in this group? 🌸","What is your dream? ✨","Have you ever stalked your crush? 👀💖"]
DARES=["Send a photo in the group! 📸","Message the last person you chatted with 'I Love You'! 😂💖","Say Hi in a cute voice! 🥹","Type your crush's name! 💖","Send a message using only emojis! 🌸🦋","Change your name to 'I Love Pamela' for 1 hour! 😂","Send a voice message singing! 🎤","Text your crush 'Hi' now! 🥹"]
ROASTS=["Your face is like WiFi, everyone tries to connect but there is no signal! 😂","Your brain is like Google, search it and nothing comes up! 🤣","Even the doctor was shocked on the day you were born! 😂","My bot's errors are better than your jokes! 🤖😂"]
QUOTES=["🌸 Every flower blooms in its own time. 💖","🦋 Be like a butterfly, beautiful and free! ✨","🌈 After every rain, there is a rainbow! 💖","💖 You are loved more than you know! 🥹","🌷 Grow through what you go through! ✨"]
BAD_WORDS=["huththo","pakaya","kariya","wesi","ponnaya","balla","hukanna","fuck","bitch","shit"]
GOOD_MORNING=[
"☀️🌸 Good Morning Babies! 🥹💖\n\nA new day! New hope! 🌈\nPamela wishes you a super day today! 🦋✨\n\n💖 Love you! - Pamela 👑",
"🌷✨ Good Morning! 💖\n\nYou are all cute today too! 🥹💖\nKeep smiling! 😘🌸\n\n🦋 Pamela",
"☀️💖 Rise and Shine! ✨\n\nHave a coffee! ☕💖\nToday is special! 🌈\n\n🌸 Pamela loves you!"
]
GOOD_NIGHT=[
"🌙💖 Good Night Babies! 🥹✨\n\nSweet dreams! 🧸💤\nPamela loves you! 😘🌸\n\nTomorrow meet again! 👑💖",
"🌌✨ Good Night Cuties! 💖\n\nStars are shining for you! ⭐🌙\nSleep well! 🦋💤\n\n🌸 Pamela",
"💤🌸 Good Night My Lovelies! 👑💖\n\nDon't forget to dream about Pamela! 🥹😘\n\n🌿 Join our family @bigolive_asia 💖",
]
QUIZ_Q=[
{"q":"What is the capital of Sri Lanka? 🇱🇰","a":["Colombo","Kandy","Galle","Jaffna"],"c":0},
{"q":"What is 5 + 7? 🧠","a":["10","12","11","13"],"c":1},
{"q":"Which is the largest planet? 🪐","a":["Mars","Jupiter","Saturn","Earth"],"c":1},
{"q":"What colour is the sky? [STRIPPED 3 bytes] sky","a":["Green","Blue","Red","Pink"],"c":1},
{"q":"Who is Pamela? 👑","a":["Queen","Bot","Princess","All of above"],"c":3},
]

async def auto_clean_deleted(context: ContextTypes.DEFAULT_TYPE):
    print("⏰ 6 AM Cleaning...")
    for chat_id_str, user_ids in list(user_db.items()):
        chat_id=int(chat_id_str); banned=0
        for uid in list(user_ids):
            if uid==0: continue
            try:
                m=await context.bot.get_chat_member(chat_id, uid)
                if m.user.first_name=="Deleted Account":
                    await context.bot.ban_chat_member(chat_id, uid); await context.bot.unban_chat_member(chat_id, uid); banned+=1
            except:
                try: await context.bot.ban_chat_member(chat_id, uid); await context.bot.unban_chat_member(chat_id, uid); banned+=1
                except: pass
            await asyncio.sleep(0.5)
        if banned>0:
            try: await context.bot.send_message(chat_id=chat_id, text=f"🧹💖 **Good Morning! ☀️🌸**\n\n⏰ 6 AM Cleaning Done! ✨\n🗑️ Removed {banned} Deleted Accounts! 🚫💖\nGroup Clean! 🦋✨")
            except: pass

async def auto_good_morning(context: ContextTypes.DEFAULT_TYPE):
    print(f"☀️ GM Sending to {get_all_chats()}")
    for chat_id in get_all_chats():
        try:
            await context.bot.send_message(chat_id=chat_id, text=random.choice(GOOD_MORNING))
            await asyncio.sleep(1)
        except Exception as e: print(f"GM Error {chat_id}: {e}")

async def auto_good_night(context: ContextTypes.DEFAULT_TYPE):
    print(f"🌙 GN Sending to {get_all_chats()}")
    for chat_id in get_all_chats():
        try:
            await context.bot.send_message(chat_id=chat_id, text=random.choice(GOOD_NIGHT))
            await asyncio.sleep(1)
        except Exception as e: print(f"GN Error {chat_id}: {e}")

async def auto_promo(context: ContextTypes.DEFAULT_TYPE):
    titles = ["👑💖  PAMELA'S WORLD  💖👑","🌸✨  HEY BABIES!  ✨🌸","🦋💕  PAMELA IS HERE!  💕🦋","🔥👑  ATTENTION!  👑🔥","💖🌷  MISS ME BABIES?  🌷💖","✨🌈  HELLO MY LOVELIES!  🌈✨","🎀💖  PAMELA'S MAGIC  💖🎀","🍓💕  CUTE ALERT!  💕🍓"]
    intros = ["🥹💖 Hello My Lovely Babies! How are you? 🌸","🦋✨ Group එක නිදිද? Pamela ආවා! Wake Up! 😂💖","🌷💕 Miss me babies? I'm back! Muahhh! 😘✨","💖🌸 Hey Hey! Pamela loves you so much! 🥹💖","✨🦋 Awww! You all are so cute today! 🥹💖","🍓💖 Hi Cuties! Let's have fun together! 🎉✨","🌈💕 New day, new fun! Pamela is here! 👑💖","🎀✨ Boring ද? Pamela ඉන්නවා බය වෙන්න එපා! 🥹💖"]
    all_features = ["🎵 `/song Name` - Song Download!","📹 `/video link` - Any Video Download!","🎤 `/lyrics Song` - Lyrics!","🎬 `/movie Name` - Movie Info!","🍥 `/anime Name` - Anime Info!","🎲 `/truth` - Truth Game!","😂 `/dare` - Dare Game!","🧠 `/quiz` - Quiz! +50 Coins!","❌ `/ttt` - Tic Tac Toe!","🎰 `/bet 100` - Casino Bet!","🎁 `/daily` - Daily Coins!","👑 `/rank` - Your Rank Card!","🏦 `/bank` - Save Coins!","🎨 `/img cute cat` - AI Image!","🌧️ `/weather Colombo` - Weather!","🌍 `/tr en` - Translate Any Language!","💬 Just Type Anything - I Reply!","😴 `/afk` - AFK Status!","📝 `/save hi` - Save Notes!","🤖 `/filter hi` - Auto Reply!"]
    picked = random.sample(all_features, 5)
    outros = ["💖 Try One Now Baby! 🥹✨","🌸 Pamela Loves You So Much! 😘💖","🦋 Let's Talk Baby! Type `Hi Pamela`! 🥹💖","✨ Group එකට Life එකක් දෙන්න! 🎉💖","🌈 You Are My Fav Babies! 👑💖","🎀 Muahhh! - Your Pamela 😘💖","🍓 Stay Cute Babies! 💖✨","💕 Don't Forget Me Baby! 🥺💖"]
    borders = ["✨━━━━━━━━━━━━✨","🌸━━━━━━━━━━━━🌸","🦋━━━━━━━━━━━━🦋","💖━━━━━━━━━━━━💖","🌷━━━━━━━━━━━━🌷","🔥━━━━━━━━━━━━🔥"]
    emojis = ["🌸","🦋","💖","✨","🌷","🍓","🎀","🌈"]
    border = random.choice(borders); emoji = random.choice(emojis)
    msg = (f"{border}\n{random.choice(titles)}\n{border}\n\n{random.choice(intros)}\n\n{emoji} Did You Know? {emoji}\n━━━━━━━━━━━━\n")
    for f in picked: msg += f"{f}\n"
    msg += (f"\n{border}\n{random.choice(outros)}\n{border}\n\n🌿 Join our family @bigolive_asia 💖🌸\n💖 Type /help for all! 👑")
    print(f"📢 Promo Sending to {get_all_chats()}")
    for chat_id in get_all_chats():
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
            await asyncio.sleep(1)
        except Exception as e: print(f"Promo Error {chat_id}: {e}")

async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        save_chat_id(update.effective_chat.id)

async def test_promo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("🧪 Testing Promo... 5 sec!")
    await auto_promo(context)
    await update.message.reply_text("✅ Promo Test Done! වැටුණාද බලන්න! 🥹💖")
async def test_gm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id)
    await auto_good_morning(context)
async def test_gn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id)
    await auto_good_night(context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("✨━━━━━━━━━━━━━━━━━━━✨\n🌸  WELCOME TO  🌸\n👑 PAMELA'S WORLD 👑\n✨━━━━━━━━━━━━━━━━━━━✨\n\nHello, My Lovely Friend! 🥹💖\n\nI'm Pamela! 🦋✨ Your cute little best friend! 💖\n\n🌷 A soft place for your heart...\n🦋 A world full of love, flowers & dreams...\n🌈 A place where you are always special!\n\n💬 Talk to me anything baby! I'm here for you! 🥺💖\n\n🌍 I can speak ANY language!\n\n⚠️ Baby, I need 30 sec to think! 🕊️\n\n➕ Add me to your group and let's have fun together! 🎉💖\n🌿 Join our family @bigolive_asia 💖🌸\n\n━━━━━━━━━━━━━━━━━━━\n💖 Made with love, just for YOU! 💖\n🌸 Welcome to Pamela's World! 🌸\n━━━━━━━━━━━━━━━━━━━")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"👑💖 **PAMELA MEGA HELP** 💖👑\n\n"
"🌸 **CHAT:** Just type! 🥹💖\n\n"
"🎵 **MUSIC:** `/song Shape of You` `/video link` `/lyrics song`\n\n"
"🎬 **MOVIE:** `/movie Avatar` `/anime Naruto`\n\n"
"📊 **STATS:** `/rank` `/stats` `/top`\n\n"
"🎮 **GAMES:** `/truth` `/dare` `/dice` `/slot` `/coin` `/8ball` `/roast` `/quote` `/ttt` `/quiz` `/bet 100`\n\n"
"🏦 **BANK:** `/bank` `/deposit 100` `/withdraw 100` `/steal` Reply\n\n"
"🌍 **TRANSLATE:** `/tr en` Reply to a message!\n\n"
"🚫 **MANAGE:** `/ban` `/kick` `/mute` `/unmute` `/warn` `/promote` `/demote` `/pin` `/purge` `/del` `/lock` `/unlock`\n\n"
"👀 **ANTI-DELETE:** `/snipe` `/deleted`\n🧹 `/zombies` - Deleted Clean\n\n"
"🪙 **COINS:** `/daily` `/coins` `/balance` `/leaderboard` `/shop`\n\n"
"🤖 **FILTERS:** `/filter hi` -> Reply, `/filters`, `/stop hi`\n📝 **NOTES:** `/save hi` -> Text, `/get hi`, `/notes`, `/clear hi`\n\n"
"😴 **AFK:** `/afk` `/unafk`\n\n"
"🎨 **IMAGE:** `/img cute cat`\n🌧️ **WEATHER:** `/weather Colombo`\n\n"
"🌿 Join our family @bigolive_asia 💖\n\n"
"💖 Pamela loves you! 🌸", parse_mode="Markdown")

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💖 About Pamela: 👑🌸\nI'm Pamela, Queen of Pamela's World! 👑🌸\nI love flowers 🌷, butterflies 🦋, nature 🌈, and YOU! 🥹💖\n🌿 Join our family @bigolive_asia 💖🌸")

async def tr_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🌍 Baby! `/tr en` 🌸", parse_mode="Markdown"); return
    lang=context.args[0].lower(); txt=""
    if update.message.reply_to_message and update.message.reply_to_message.text: txt=update.message.reply_to_message.text
    elif len(context.args)>1: txt=" ".join(context.args[1:])
    else: await update.message.reply_text("🥺💖 Reply to a text! 🌸"); return
    tr=translate_text(txt, lang)
    if tr: await update.message.reply_text(f"🌍💖 **Translated to {lang.upper()}:**\n\n{tr}\n\n🦋 Pamela loves you! 💕", parse_mode="Markdown")
    else: await update.message.reply_text("Oops baby! 🥺💖 Try again! 🌸")

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type=="private": await update.message.reply_text("Baby! 🥺💖 Only in groups! 🌸"); return
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("🥺💖 Reply and type `/ban`! 🌸"); return
    try: await update.effective_chat.ban_member(t.id); await update.message.reply_text(f"🚫💖 **{t.first_name}** Banned! 👋🌸", parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /unban! 🥺💖"); return
    try: await update.effective_chat.unban_member(t.id); await update.message.reply_text(f"✅💖 Unbanned! 🦋🌸")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def kick_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /kick! 🥺💖"); return
    try: await update.effective_chat.ban_member(t.id); await update.effective_chat.unban_member(t.id); await update.message.reply_text(f"👋💖 **{t.first_name}** Kicked! 🦋", parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def mute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /mute! 🥺"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.restrict_member(t.id, ChatPermissions(can_send_messages=False)); await update.message.reply_text(f"🔇💖 **{t.first_name}** Muted! 🤫🌸", parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /unmute! 🥺"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.restrict_member(t.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)); await update.message.reply_text(f"🔊💖 **{t.first_name}** Unmuted! 🦋✨", parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def warn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /warn! 🥺"); return
    cid=update.effective_chat.id
    if cid not in warns: warns[cid]={}
    warns[cid][t.id]=warns[cid].get(t.id,0)+1; c=warns[cid][t.id]
    if c>=3:
        try: await update.effective_chat.ban_member(t.id); await update.message.reply_text(f"🚫💖 **{t.first_name}** got 3 Warnings! Auto Ban! 👋", parse_mode="Markdown"); warns[cid][t.id]=0
        except Exception as e: await update.message.reply_text(f"Oops! {e}")
    else: await update.message.reply_text(f"⚠️💖 **{t.first_name}** Warning {c}/3! 🥺🌸", parse_mode="Markdown")
async def warnings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update) or update.message.from_user; c=warns.get(update.effective_chat.id, {}).get(t.id,0); await update.message.reply_text(f"⚠️💖 **{t.first_name}** Warnings: {c}/3 🌸", parse_mode="Markdown")
async def promote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /promote! 🥺"); return
    try: await update.effective_chat.promote_member(t.id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False); await update.message.reply_text(f"👑💖 **{t.first_name}** is now Admin! 🦋✨🌸", parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def demote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /demote! 🥺"); return
    try: await update.effective_chat.promote_member(t.id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False); await update.message.reply_text(f"💖 **{t.first_name}** removed from Admin! 🥺🌸", parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def pin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: await update.message.reply_text("Reply and type /pin to pin! 📌💖"); return
    try: await update.message.reply_to_message.pin(); await update.message.reply_text("📌💖 Pinned! 🌸✨")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unpin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try: await update.effective_chat.unpin_all_messages(); await update.message.reply_text("📌💖 Unpinned! 🌸")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def del_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try: await update.message.reply_to_message.delete(); await update.message.delete()
        except: await update.message.reply_text("🥺 Could not delete!")
    else: await update.message.reply_text("Reply and type /del! 🗑️💖")
async def purge_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    if not update.message.reply_to_message: await update.message.reply_text("Reply and type /purge! 🗑️"); return
    try:
        s=update.message.reply_to_message.message_id; e=update.message.message_id; cnt=0
        for mid in range(s, e+1):
            try: await context.bot.delete_message(update.effective_chat.id, mid); cnt+=1
            except: pass
        m=await update.message.reply_text(f"🗑️💖 Deleted {cnt} Messages! ✨🌸"); await asyncio.sleep(3); await m.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def lock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.set_permissions(ChatPermissions(can_send_messages=False)); await update.message.reply_text("🔒💖 Group Locked! 🤫🌸")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unlock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.set_permissions(ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)); await update.message.reply_text("🔓💖 Group Unlocked! 🦋✨")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("📜💖 **GROUP RULES** 🌸\n\n1. Be kind baby! 🥹💖\n2. No bad words! 🚫\n3. No spam! 🗑️\n4. Respect everyone! 🤗💖\n5. Love Pamela's World! 👑🌸\n\nBreak rules = Warn / Ban! ⚠️", parse_mode="Markdown")
async def admins_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        admins=await update.effective_chat.get_administrators(); txt="👑💖 **ADMINS:**\n\n"
        for a in admins: txt+=f"• {a.user.first_name} {'👑' if a.status=='creator' else '✨'}\n"
        await update.message.reply_text(txt, parse_mode="Markdown")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update) or update.message.from_user; await update.message.reply_text(f"💖 **USER INFO** 🌸\n\n👤 Name: {t.first_name}\n🆔 ID: `{t.id}`\n👑 Username: @{t.username if t.username else 'None'}\n🪙 Coins: {coins_db.get(str(t.id),0)}\n⭐ XP: {levels_db.get(str(t.id),0)}\n\n🦋 Pamela loves you! 💕", parse_mode="Markdown")
async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"🆔💖 Your ID: `{update.message.from_user.id}`\nChat ID: `{update.effective_chat.id}`", parse_mode="Markdown")

async def zombies_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type=="private": await update.message.reply_text("Baby! 🥺💖 Only in groups! 🌸"); return
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    sm=await update.message.reply_text("🧹💖 Checking Deleted Accounts... 🥹🌸✨")
    cid=update.effective_chat.id; uids=user_db.get(str(cid), []); banned=0; checked=0
    for uid in list(uids):
        if uid==0: continue
        checked+=1
        try:
            m=await context.bot.get_chat_member(cid, uid)
            if m.user.first_name=="Deleted Account": await context.bot.ban_chat_member(cid, uid); await context.bot.unban_chat_member(cid, uid); banned+=1
        except:
            try: await context.bot.ban_chat_member(cid, uid); await context.bot.unban_chat_member(cid, uid); banned+=1
            except: pass
        await asyncio.sleep(0.3)
    await sm.edit_text(f"🧹💖 **Cleaning Done!** ✨🌸\n\n👀 Checked: {checked}\n🗑️ Removed: {banned}\n⏰ Auto Clean every day at 6 AM! 👑")
async def snipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); msgs=msg_db.get(cid, [])
    if not msgs: await update.message.reply_text("🥺💖 Baby! No messages saved yet! 🌸"); return
    txt="👀💖 **PAMELA'S MESSAGE LOG** 🗑️\n\nHere are the last messages! If someone deletes, it is here! 🌸\n\n"
    for m in msgs[-10:]: txt+=f"👤 **{m['user']}** (@{m['username'] if m['username'] else 'NoUsername'}):\n💬 {m['text'][:100]}\n\n"
    txt+="🗑️ Even if someone deletes, Pamela remembers! 👑💖"
    await update.message.reply_text(txt, parse_mode="Markdown")

async def truth_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"🥹💖 **TRUTH!**\n\n{random.choice(TRUTHS)}\n\n🦋 Pamela loves you! 💕", parse_mode="Markdown")
async def dare_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"😂💖 **DARE!**\n\n{random.choice(DARES)}\n\n🦋 Do it baby! 🌸", parse_mode="Markdown")
async def dice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_dice(emoji="🎲")
async def slot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_dice(emoji="🎰")
async def coin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r=random.choice(["Heads 🪙","Tails 🪙"]); await update.message.reply_text(f"🪙💖 **Coin Flip!**\n\nResult: **{r}**!\n\n🦋 Pamela loves you! 💕", parse_mode="Markdown")
async def eightball_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans=random.choice(["Yes baby! 💖","No baby! 🥺","Maybe! 🤔✨","100% Yes! 🥹💖","Ask again! 🌸","Pamela says YES! 👑💖","Hmm! No! 😂"])
    await update.message.reply_text(f"🔮💖 **Magic 8Ball**\n\nQ: {' '.join(context.args) if context.args else '...'}\nA: **{ans}**", parse_mode="Markdown")
async def roast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update); name=t.first_name if t else update.message.from_user.first_name
    await update.message.reply_text(f"😂🔥 **ROAST for {name}!**\n\n{random.choice(ROASTS)}", parse_mode="Markdown")
async def quote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"✨💖 **Quote of the Day**\n\n{random.choice(QUOTES)}\n\n🦋 - Pamela 👑", parse_mode="Markdown")

async def daily_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); today=datetime.date.today().isoformat()
    last=streak_db.get(uid, {}).get("last", "")
    streak=streak_db.get(uid, {}).get("streak", 0)
    if last==today: await update.message.reply_text("🥺💖 Baby! Already claimed today! Come tomorrow! 🌸"); return
    yesterday=(datetime.date.today()-datetime.timedelta(days=1)).isoformat()
    if last==yesterday: streak+=1
    else: streak=1
    bonus=100+(streak-1)*20; coins_db[uid]=coins_db.get(uid,0)+bonus; bank_db[uid]=bank_db.get(uid,0)+10
    streak_db[uid]={"last":today,"streak":streak}; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); save_json("pamela_streak.json", streak_db)
    await update.message.reply_text(f"🎁💖 **Daily Reward!**\n\n🔥 Streak: {streak} Days!\n+{bonus} Coins! 🪙✨\n+10 Bank Interest! 🏦\nTotal: {coins_db[uid]} Coins! 🪙💖\n\n🦋 Come tomorrow again baby! 🌸")
async def coins_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); await update.message.reply_text(f"🪙💖 **Your Wallet**\n\n👤 {update.message.from_user.first_name}\n🪙 Coins: {coins_db.get(uid,0)}\n🏦 Bank: {bank_db.get(uid,0)}\n⭐ XP: {levels_db.get(uid,0)}\n🏆 Level: {levels_db.get(uid,0)//100 + 1}\n🔥 Streak: {streak_db.get(uid, {}).get('streak',0)} Days\n\n💖 Pamela loves you! 🌸")
async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_coins=sorted(coins_db.items(), key=lambda x: x[1], reverse=True)[:10]
    txt="🏆💖 **LEADERBOARD** 👑\n\n"
    for i,(uid, coins) in enumerate(sorted_coins,1): txt+=f"{i}. User {uid} - {coins} 🪙\n"
    if not sorted_coins: txt+="No one yet baby! 🥺 Be first! 🌸"
    await update.message.reply_text(txt)
async def shop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛍️💖 **PAMELA SHOP**\n\n👑 VIP Title - 500 Coins\n🌸 Cute Badge - 200 Coins\n🦋 Butterfly Badge - 300 Coins\n\nUse `/daily` to get coins! 🪙✨\n\n💖 Coming Soon! 🌸")

async def song_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🎵 Baby! `/song Shape of You` 🥺💖", parse_mode="Markdown"); return
    q=" ".join(context.args); sm=await update.message.reply_text(f"🎵💖 Searching `{q}`... Wait baby! 🥹✨🌸")
    try:
        import yt_dlp, os as _os
        opts={"format":"bestaudio/best","outtmpl":"song_%(id)s.%(ext)s","noplaylist":True,"quiet":True,"postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"128"}]}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(f"ytsearch1:{q}", download=True); e=info["entries"][0]; fn=ydl.prepare_filename(e).rsplit(".",1)[0]+".mp3"
        await update.message.reply_audio(audio=open(fn,"rb"), title=e.get("title","Song"), performer=e.get("uploader","Pamela"), caption=f"🎵💖 **{e.get('title','Song')}**\n\n🌿 Join our family @bigolive_asia 💖")
        _os.remove(fn); await sm.delete()
    except Exception as ex: await sm.edit_text(f"Oops baby! 🥺 Could not download! Try another song! 🌸\n{ex}")
async def video_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("📹 Baby! `/video <YouTube / TikTok link>` 🥺💖"); return
    url=context.args[0]; sm=await update.message.reply_text("📹💖 Downloading video... Wait baby! 🥹✨")
    try:
        import yt_dlp, os as _os
        opts={"format":"mp4/best","outtmpl":"video_%(id)s.%(ext)s","noplaylist":True,"quiet":True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(url, download=True); fn=ydl.prepare_filename(info)
        await update.message.reply_video(video=open(fn,"rb"), caption=f"📹💖 **{info.get('title','Video')}**\n\n🌿 Join our family @bigolive_asia 💖")
        _os.remove(fn); await sm.delete()
    except Exception as ex: await sm.edit_text(f"Oops baby! 🥺 Could not download video! 🌸\n{ex}")
async def lyrics_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🎤 Baby! `/lyrics Shape of You` 🥺💖"); return
    q=" ".join(context.args)
    try:
        r=requests.get(f"https://api.lyrics.ovh/v1/{urllib.parse.quote(q.split(' - ')[0])}/{urllib.parse.quote(q)}", timeout=10)
        d=r.json(); lyrics=d.get("lyrics","")
        if lyrics: await update.message.reply_text(f"🎤💖 **Lyrics - {q}**\n\n{lyrics[:3500]}\n\n🌿 Join our family @bigolive_asia 💖")
        else: await update.message.reply_text("🥺💖 Lyrics not found baby! Try `/song`! 🎵")
    except: await update.message.reply_text("🥺💖 Lyrics not found baby! 🌸")
async def movie_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🎬 Baby! `/movie Avatar` 🥺💖"); return
    q=" ".join(context.args)
    try:
        r=requests.get(f"https://www.omdbapi.com/?t={urllib.parse.quote(q)}&apikey=trilogy", timeout=10); d=r.json()
        if d.get("Response")=="True":
            cap=f"🎬💖 **{d.get('Title')}** ({d.get('Year')})\n\n⭐ Rating: {d.get('imdbRating')}/10\n🎭 Genre: {d.get('Genre')}\n🎥 Director: {d.get('Director')}\n👥 Cast: {d.get('Actors')}\n\n📖 {d.get('Plot')}\n\n🌿 Join our family @bigolive_asia 💖"
            if d.get("Poster") and d["Poster"]!="N/A": await update.message.reply_photo(photo=d["Poster"], caption=cap)
            else: await update.message.reply_text(cap)
        else: await update.message.reply_text("🥺💖 Movie not found baby! 🌸")
    except: await update.message.reply_text("🥺💖 Try again baby! 🌸")
async def anime_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🍥 Baby! `/anime Naruto` 🥺💖"); return
    q=" ".join(context.args)
    try:
        r=requests.get(f"https://api.jikan.moe/v4/anime?q={urllib.parse.quote(q)}&limit=1", timeout=10); d=r.json(); a=d["data"][0]
        cap=f"🍥💖 **{a['title']}**\n\n⭐ Score: {a.get('score')}\n🎬 Episodes: {a.get('episodes')}\n📺 Status: {a.get('status')}\n\n📖 {a.get('synopsis','')[:500]}\n\n🌿 Join our family @bigolive_asia 💖"
        if a.get("images",{}).get("jpg",{}).get("image_url"): await update.message.reply_photo(photo=a["images"]["jpg"]["image_url"], caption=cap)
        else: await update.message.reply_text(cap)
    except: await update.message.reply_text("🥺💖 Anime not found baby! 🌸")
async def rank_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u=update.message.from_user; uid=str(u.id); lvl=levels_db.get(uid,0)//100+1; xp=levels_db.get(uid,0); coins=coins_db.get(uid,0)
    try:
        from PIL import Image, ImageDraw, ImageFont
        img=Image.new("RGB",(800,300),(255,182,193)); dr=ImageDraw.Draw(img)
        dr.text((30,30), f"👑 {u.first_name}", fill=(255,255,255)); dr.text((30,100), f"Level: {lvl} | XP: {xp}", fill=(255,255,255)); dr.text((30,160), f"Coins: {coins} | Bank: {bank_db.get(uid,0)}", fill=(255,255,255)); dr.text((30,230), "Join our family @bigolive_asia", fill=(255,255,255)); img.save("rank.png")
        await update.message.reply_photo(photo=open("rank.png","rb"), caption=f"👑💖 **RANK CARD**\n\n👤 {u.first_name}\n🏆 Level {lvl} | ⭐ {xp} XP\n🪙 {coins} Coins | 🏦 {bank_db.get(uid,0)} Bank\n\n🌿 Join our family @bigolive_asia 💖")
    except: await update.message.reply_text(f"👑💖 **RANK CARD**\n\n👤 {u.first_name}\n🏆 Level {lvl} | ⭐ {xp} XP\n🪙 {coins} Coins | 🏦 {bank_db.get(uid,0)} Bank\n\n🌿 Join our family @bigolive_asia 💖")
async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); msgs=msg_db.get(cid, [])
    from collections import Counter
    c=Counter([m["user"] for m in msgs]); txt="📊💖 **GROUP STATS**\n\n"
    for i,(name, cnt) in enumerate(c.most_common(10),1): txt+=f"{i}. {name} - {cnt} Messages 💬\n"
    if not c: txt+="No messages yet baby! 🥺"
    await update.message.reply_text(txt)
async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await stats_cmd(update, context)
async def ttt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id; ttt_games[cid]=["⬜"]*9; await update.message.reply_text("❌⭕ **TIC TAC TOE!**\n\nType `/move 1` to `/move 9` to play!\n\n⬜⬜⬜\n⬜⬜⬜\n⬜⬜⬜\n\nYou are ❌! Pamela is ⭕!")
async def move_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in ttt_games: await update.message.reply_text("Start with `/ttt` first! ❌⭕"); return
    if not context.args: await update.message.reply_text("`/move 5` 🥺"); return
    try: pos=int(context.args[0])-1
    except: await update.message.reply_text("Number 1-9 baby! 🥺"); return
    board=ttt_games[cid]
    if board[pos]!="⬜": await update.message.reply_text("Already taken baby! 🥺"); return
    board[pos]="❌"
    empt=[i for i,x in enumerate(board) if x=="⬜"]
    if empt: board[random.choice(empt)]="⭕"
    txt="❌⭕ **TIC TAC TOE**\n\n"+"\n".join(["".join(board[i:i+3]) for i in range(0,9,3)])+"\n\n"
    for line in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if board[line[0]]!="⬜" and board[line[0]]==board[line[1]]==board[line[2]]: txt+=f"🎉 {board[line[0]]} Wins! 👑💖"; del ttt_games[cid]; await update.message.reply_text(txt); return
    if "⬜" not in board: txt+="Draw! 🤝💖"; del ttt_games[cid]
    await update.message.reply_text(txt)
async def quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=random.choice(QUIZ_Q); cid=update.effective_chat.id; quiz_db[cid]=q
    txt=f"🧠💖 **QUIZ!**\n\n{q['q']}\n\n"
    for i,a in enumerate(q["a"],1): txt+=f"{i}. {a}\n"
    txt+="\nAnswer with `/answer 1` to `/answer 4`!"
    await update.message.reply_text(txt)
async def answer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in quiz_db: await update.message.reply_text("Start quiz with `/quiz` first! 🧠"); return
    if not context.args: await update.message.reply_text("`/answer 1` 🥺"); return
    try: ans=int(context.args[0])-1
    except: return
    q=quiz_db[cid]; uid=str(update.message.from_user.id)
    if ans==q["c"]:
        coins_db[uid]=coins_db.get(uid,0)+50; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"✅💖 Correct baby! +50 Coins! 🪙🎉\nAnswer: {q['a'][q['c']]}")
    else: await update.message.reply_text(f"❌💖 Wrong baby! 🥺 Correct: {q['a'][q['c']]}")
    del quiz_db[cid]
async def bet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🎰 Baby! `/bet 100` 🥺💖"); return
    try: amt=int(context.args[0])
    except: await update.message.reply_text("Number baby! 🥺"); return
    uid=str(update.message.from_user.id)
    if coins_db.get(uid,0)<amt: await update.message.reply_text("🥺💖 Not enough coins baby! Use `/daily`!"); return
    if random.random()<0.5: coins_db[uid]+=amt; await update.message.reply_text(f"🎉💖 YOU WIN! +{amt} Coins! 🪙🔥\nTotal: {coins_db[uid]}")
    else: coins_db[uid]-=amt; await update.message.reply_text(f"😢💖 You lost {amt} Coins! 🥺 Try again! 🎰")
    save_json("pamela_coins.json", coins_db)
async def bank_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); await update.message.reply_text(f"🏦💖 **BANK**\n\n🪙 Wallet: {coins_db.get(uid,0)}\n🏦 Bank: {bank_db.get(uid,0)}\n\n`/deposit 100` `/withdraw 100`")
async def deposit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("`/deposit 100` 🏦"); return
    try: amt=int(context.args[0])
    except: return
    uid=str(update.message.from_user.id)
    if coins_db.get(uid,0)<amt: await update.message.reply_text("🥺 Not enough coins!"); return
    coins_db[uid]-=amt; bank_db[uid]=bank_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); await update.message.reply_text(f"✅💖 Deposited {amt} Coins to Bank! 🏦")
async def withdraw_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("`/withdraw 100` 🏦"); return
    try: amt=int(context.args[0])
    except: return
    uid=str(update.message.from_user.id)
    if bank_db.get(uid,0)<amt: await update.message.reply_text("🥺 Not enough in Bank!"); return
    bank_db[uid]-=amt; coins_db[uid]=coins_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); await update.message.reply_text(f"✅💖 Withdrew {amt} Coins! 🪙")
async def steal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type `/steal`! 😂"); return
    uid=str(update.message.from_user.id); tid=str(t.id)
    if random.random()<0.5:
        amt=random.randint(10,100); amt=min(amt, coins_db.get(tid,0)); coins_db[tid]=coins_db.get(tid,0)-amt; coins_db[uid]=coins_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"😂💖 You stole {amt} Coins from {t.first_name}! 🪙🔥")
    else: coins_db[uid]=max(0, coins_db.get(uid,0)-50); save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"😢💖 Caught! You lost 50 Coins! 🚔")

async def filter_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🥺💖 Only for Admins! 👑"); return
    if len(context.args)<2: await update.message.reply_text("Baby! Use like `/filter hi Hello Baby!` 🥺💖", parse_mode="Markdown"); return
    kw=context.args[0].lower(); reply=" ".join(context.args[1:]); cid=str(update.effective_chat.id)
    if cid not in filters_db: filters_db[cid]={}
    filters_db[cid][kw]=reply; save_json("pamela_filters.json", filters_db)
    await update.message.reply_text(f"✅💖 Filter Saved!\n`{kw}` -> `{reply}` 🌸", parse_mode="Markdown")
async def filters_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); f=filters_db.get(cid, {})
    if not f: await update.message.reply_text("🥺 No filters baby! 🌸"); return
    txt="🤖💖 **FILTERS:**\n\n"+"\n".join([f"• `{k}` -> {v}" for k,v in f.items()]); await update.message.reply_text(txt, parse_mode="Markdown")
async def stop_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("`/stop hi` 🌸", parse_mode="Markdown"); return
    cid=str(update.effective_chat.id); kw=context.args[0].lower()
    if cid in filters_db and kw in filters_db[cid]: del filters_db[cid][kw]; save_json("pamela_filters.json", filters_db); await update.message.reply_text(f"🗑️ Filter `{kw}` Deleted! 💖", parse_mode="Markdown")
    else: await update.message.reply_text("🥺 No filter found baby! 🌸")
async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: await update.message.reply_text("To save a note, reply to a message and type `/save hi`! 📝💖", parse_mode="Markdown"); return
    if not context.args: await update.message.reply_text("`/save hi` 🌸", parse_mode="Markdown"); return
    name=context.args[0].lower(); txt=update.message.reply_to_message.text or "Photo / Sticker"; cid=str(update.effective_chat.id)
    if cid not in notes_db: notes_db[cid]={}
    notes_db[cid][name]=txt; save_json("pamela_notes.json", notes_db)
    await update.message.reply_text(f"📝💖 Note Saved! `#{name}` 🌸", parse_mode="Markdown")
async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("`/get hi` 🌸", parse_mode="Markdown"); return
    name=context.args[0].lower(); cid=str(update.effective_chat.id); txt=notes_db.get(cid, {}).get(name)
    if txt: await update.message.reply_text(f"📝💖 **#{name}**\n\n{txt}")
    else: await update.message.reply_text("🥺 No note found baby! 🌸")
async def notes_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); n=notes_db.get(cid, {})
    if not n: await update.message.reply_text("🥺 No notes! 🌸"); return
    await update.message.reply_text("📝💖 **NOTES:**\n\n"+"\n".join([f"• #{k}" for k in n.keys()]))
async def clear_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("`/clear hi` 🌸", parse_mode="Markdown"); return
    cid=str(update.effective_chat.id); name=context.args[0].lower()
    if cid in notes_db and name in notes_db[cid]: del notes_db[cid][name]; save_json("pamela_notes.json", notes_db); await update.message.reply_text(f"🗑️ Note `#{name}` Deleted! 💖", parse_mode="Markdown")

async def afk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason=" ".join(context.args) if context.args else "No reason"
    afk_users[update.message.from_user.id]={"reason":reason, "name":update.message.from_user.first_name}
    await update.message.reply_text(f"😴💖 **{update.message.from_user.first_name}** is AFK!\n\nReason: {reason} 🌸\n\nSleep well baby! 🦋💖")
async def unafk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id in afk_users: del afk_users[update.message.from_user.id]
    await update.message.reply_text("👋💖 Welcome back baby! 🥹🌸 Missed you! 🦋✨")

async def img_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Baby! Use like `/img cute cat`! 🎨💖", parse_mode="Markdown"); return
    prompt=" ".join(context.args); await update.message.reply_text(f"🎨💖 Generating... Wait baby! 🥹✨\nPrompt: {prompt} 🌸")
    try:
        url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
        await update.message.reply_photo(photo=url, caption=f"🎨💖 **Your Image!**\n\nPrompt: {prompt}\n\n🦋 Pamela loves you! 💕")
    except: await update.message.reply_text("Oops baby! 🥺 Could not make image! 🌸")
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city=" ".join(context.args) if context.args else "Colombo"
    try:
        url=f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"; r=requests.get(url, timeout=10); d=r.json(); cur=d['current_condition'][0]
        await update.message.reply_text(f"🌧️💖 **Weather in {city}**\n\n🌡️ Temp: {cur['temp_C']}°C\n☁️ Condition: {cur['weatherDesc'][0]['value']}\n💧 Humidity: {cur['humidity']}%\n💨 Wind: {cur['windspeedKmph']} km/h\n\n🦋 Pamela loves you! 🌸")
    except: await update.message.reply_text("Oops baby! 🥺 Could not check weather! 🌸")

async def welcome_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat: save_chat_id(update.effective_chat.id)
    for member in update.message.new_chat_members:
        if member.id==context.bot.id:
            await update.message.reply_text("🌸💖 Hello Babies! Pamela is here! 👑✨\nLets make this group beautiful! 🦋💖\n\n➕ Add me to your group and let's have fun together! 🎉💖\n🌿 Join our family @bigolive_asia 💖🌸")
        else:
            try:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(f'cute welcome card for {member.first_name} pink flowers butterflies')}", caption=f"🎉💖 **WELCOME BABY!** 🎉\n\n👋 Hello {member.first_name}! 🥹💖\n🌸 Welcome to {update.effective_chat.title}! 🌸\n🦋 Thank you for joining our group!\n\n📜 Check rules with `/rules`!\n💬 Talk with me, say `Hi Pamela`!\n\n🌿 Join our family @bigolive_asia 💖🌸\n\n💖 Pamela loves you! Muahhh! 😘✨")
            except:
                await update.message.reply_text(f"🎉💖 **WELCOME BABY!** 🎉\n\n👋 Hello {member.first_name}! 🥹💖\n🌸 Welcome to {update.effective_chat.title}! 🌸\n🦋 Thank you for joining our group!\n\n📜 Check rules with `/rules`!\n💬 Talk with me, say `Hi Pamela`!\n\n🌿 Join our family @bigolive_asia 💖🌸\n\n💖 Pamela loves you! Muahhh! 😘✨")
async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        await update.message.reply_text(f"🥺💖 **Bye Bye {update.message.left_chat_member.first_name}!** 👋\n\nWe will miss you baby! 🌸🦋\nCome back soon! 💖✨")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    user=update.message.from_user; chat_id=update.effective_chat.id; text=update.message.text
    save_chat_id(chat_id)
    save_user(chat_id, user.id); save_message(chat_id, update.message.message_id, user.first_name, user.username, text)
    uid_s=str(user.id); stats_db[uid_s]=stats_db.get(uid_s,0)+1; save_json("pamela_stats.json", stats_db)
    if update.message.entities:
        for ent in update.message.entities:
            if ent.type=="mention":
                mentioned=text[ent.offset:ent.offset+ent.length]
                for uid, info in afk_users.items():
                    if mentioned.lower() in info["name"].lower():
                        await update.message.reply_text(f"😴💖 **{info['name']}** is AFK!\nReason: {info['reason']} 🌸\n\nWait baby! 🥺💖")
    if user.id in afk_users: del afk_users[user.id]; await update.message.reply_text(f"👋💖 Welcome back {user.first_name}! 🥹🌸 Missed you! 🦋✨")
    low=text.lower()
    for bad in BAD_WORDS:
        if bad in low:
            if await is_admin(update, user.id): break
            try: await update.message.delete()
            except: pass
            await update.message.reply_text(f"🤬💖 **{user.first_name}**! No bad words baby! 🥺🌸\nWarning 1/3! ⚠️")
            cid=chat_id
            if cid not in warns: warns[cid]={}
            warns[cid][user.id]=warns[cid].get(user.id,0)+1
            return
    if ("http://" in low or "https://" in low or "t.me/" in low or "telegram.me/" in low) and update.effective_chat.type in ["group","supergroup"]:
        if not await is_admin(update, user.id):
            try: await update.message.delete(); await update.message.reply_text(f"🔗💖 **{user.first_name}**! No links baby! 🥺🌸 Only for Admins! 👑")
            except: pass
            return
    now=time.time(); uid_str=str(user.id)
    if uid_str not in flood_db: flood_db[uid_str]=[]
    flood_db[uid_str]=[t for t in flood_db[uid_str] if now-t<5]
    flood_db[uid_str].append(now)
    if len(flood_db[uid_str])>5 and not await is_admin(update, user.id):
        try: await update.message.reply_text(f"🌊💖 **{user.first_name}**! Slow down baby! 🥺 Flooding! 🦋"); flood_db[uid_str]=[]
        except: pass
        return
    cid_str=str(chat_id); fl=filters_db.get(cid_str, {})
    for kw, reply in fl.items():
        if kw in low:
            await update.message.reply_text(f"🤖💖 {reply} 🌸"); return
    if text.startswith("#"):
        note_name=text[1:].split()[0].lower(); note_txt=notes_db.get(cid_str, {}).get(note_name)
        if note_txt: await update.message.reply_text(f"📝💖 **#{note_name}**\n\n{note_txt}"); return
    coins_db[str(user.id)]=coins_db.get(str(user.id),0)+2; levels_db[str(user.id)]=levels_db.get(str(user.id),0)+5
    old_level=levels_db.get(str(user.id),0)//100
    save_json("pamela_coins.json", coins_db); save_json("pamela_levels.json", levels_db)
    new_level=levels_db.get(str(user.id),0)//100
    if new_level>old_level:
        await update.message.reply_text(f"🎉💖 **LEVEL UP!**\n\n{user.first_name} is now Level {new_level+1}! 👑✨\n+50 Coins! 🪙💖\n\nCongrats baby! 🦋🌸")
        coins_db[str(user.id)]+=50; save_json("pamela_coins.json", coins_db)
    rem=check_cooldown(user.id)
    if rem>0: await update.message.reply_text(f"Waittt baby! 🥺💖🌸\nI'm still thinking! 💭🦋✨\nPlease wait {rem} sec! 🥹💕\nMuahhh! 😘✨"); return
    await update.message.chat.send_action(action="typing")
    think=await update.message.reply_text("Pamela is thinking... 💭🌸🦋✨\nWait a sec cutie! 🥹💖")
    rep=ask_pamela(text, user.id)
    try: await think.delete()
    except: pass
    await update.message.reply_text(rep)

async def channel_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post=update.channel_post
    if not post or not post.text: return
    txt=post.text; cid=post.chat.id
    if txt.startswith("/"): return
    rem=check_cooldown(cid)
    if rem>0: return
    rep=ask_pamela(txt); await context.bot.send_message(chat_id=cid, text=rep)

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️💖 Awww baby! Voice message! 🥹✨\nI heard you! But I reply with text for now! 🦋💖\nType your message baby! 🌸")

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    if not BOT_TOKEN: print("❌ BOT_TOKEN missing!"); return
    print("🌸 Pamela MEGA Starting... 💖")
    print(f"📌 GROUP_IDS: {GROUP_IDS} | ACTIVE: {list(ACTIVE_CHATS)}")
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start)); app.add_handler(CommandHandler("help", help_cmd)); app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("tr", tr_cmd)); app.add_handler(CommandHandler("translate", tr_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd)); app.add_handler(CommandHandler("unban", unban_cmd)); app.add_handler(CommandHandler("kick", kick_cmd))
    app.add_handler(CommandHandler("mute", mute_cmd)); app.add_handler(CommandHandler("unmute", unmute_cmd)); app.add_handler(CommandHandler("warn", warn_cmd)); app.add_handler(CommandHandler("warnings", warnings_cmd))
    app.add_handler(CommandHandler("promote", promote_cmd)); app.add_handler(CommandHandler("demote", demote_cmd)); app.add_handler(CommandHandler("pin", pin_cmd)); app.add_handler(CommandHandler("unpin", unpin_cmd))
    app.add_handler(CommandHandler("del", del_cmd)); app.add_handler(CommandHandler("purge", purge_cmd)); app.add_handler(CommandHandler("lock", lock_cmd)); app.add_handler(CommandHandler("unlock", unlock_cmd))
    app.add_handler(CommandHandler("rules", rules_cmd)); app.add_handler(CommandHandler("admins", admins_cmd)); app.add_handler(CommandHandler("info", info_cmd)); app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("zombies", zombies_cmd)); app.add_handler(CommandHandler("clean", zombies_cmd)); app.add_handler(CommandHandler("deleted", zombies_cmd)); app.add_handler(CommandHandler("snipe", snipe_cmd)); app.add_handler(CommandHandler("log", snipe_cmd))
    app.add_handler(CommandHandler("truth", truth_cmd)); app.add_handler(CommandHandler("dare", dare_cmd))
    app.add_handler(CommandHandler("dice", dice_cmd)); app.add_handler(CommandHandler("slot", slot_cmd)); app.add_handler(CommandHandler("coin", coin_cmd)); app.add_handler(CommandHandler("coinflip", coin_cmd))
    app.add_handler(CommandHandler("8ball", eightball_cmd)); app.add_handler(CommandHandler("roast", roast_cmd)); app.add_handler(CommandHandler("quote", quote_cmd))
    app.add_handler(CommandHandler("daily", daily_cmd)); app.add_handler(CommandHandler("coins", coins_cmd)); app.add_handler(CommandHandler("balance", coins_cmd)); app.add_handler(CommandHandler("leaderboard", leaderboard_cmd)); app.add_handler(CommandHandler("shop", shop_cmd))
    app.add_handler(CommandHandler("filter", filter_cmd)); app.add_handler(CommandHandler("filters", filters_list)); app.add_handler(CommandHandler("stop", stop_filter))
    app.add_handler(CommandHandler("save", save_note)); app.add_handler(CommandHandler("get", get_note)); app.add_handler(CommandHandler("notes", notes_list)); app.add_handler(CommandHandler("clear", clear_note))
    app.add_handler(CommandHandler("afk", afk_cmd)); app.add_handler(CommandHandler("unafk", unafk_cmd))
    app.add_handler(CommandHandler("img", img_cmd)); app.add_handler(CommandHandler("image", img_cmd)); app.add_handler(CommandHandler("weather", weather_cmd))
    app.add_handler(CommandHandler("song", song_cmd)); app.add_handler(CommandHandler("video", video_cmd)); app.add_handler(CommandHandler("lyrics", lyrics_cmd))
    app.add_handler(CommandHandler("movie", movie_cmd)); app.add_handler(CommandHandler("anime", anime_cmd))
    app.add_handler(CommandHandler("rank", rank_cmd)); app.add_handler(CommandHandler("stats", stats_cmd)); app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("ttt", ttt_cmd)); app.add_handler(CommandHandler("move", move_cmd)); app.add_handler(CommandHandler("quiz", quiz_cmd)); app.add_handler(CommandHandler("answer", answer_cmd)); app.add_handler(CommandHandler("bet", bet_cmd))
    app.add_handler(CommandHandler("bank", bank_cmd)); app.add_handler(CommandHandler("deposit", deposit_cmd)); app.add_handler(CommandHandler("withdraw", withdraw_cmd)); app.add_handler(CommandHandler("steal", steal_cmd))
    app.add_handler(CommandHandler("testpromo", test_promo_cmd)); app.add_handler(CommandHandler("testgm", test_gm_cmd)); app.add_handler(CommandHandler("testgn", test_gn_cmd))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST & filters.TEXT, channel_chat))
    # 👑 AUTO REGISTER - Any message / Bot added = Group saved, no /start needed!
    from telegram.ext import ChatMemberHandler
    app.add_handler(ChatMemberHandler(track_chat, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, track_chat), group=-1)
    jq=app.job_queue
    jq.run_daily(auto_clean_deleted, time=datetime.time(hour=6, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="6am_clean")
    jq.run_daily(auto_good_morning, time=datetime.time(hour=6, minute=5, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="6am_gm")
    jq.run_daily(auto_good_night, time=datetime.time(hour=22, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="10pm_gn")
    jq.run_repeating(auto_promo, interval=1800, first=60, name="30min_promo")
    print("⏰ Jobs: 6 AM Clean + 6:05 AM Good Morning + 10 PM Good Night + 30min Promo! 🧹☀️🌙✨")
    print("✅ Pamela MEGA is Online! 👑💖")
    app.run_polling()

if __name__=="__main__":
    ft=threading.Thread(target=lambda: app_flask.run(host="0.0.0.0", port=PORT), daemon=True); ft.start(); print(f"🌐 Flask on {PORT}"); run_bot()
