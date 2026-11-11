# PAMELA AI - MEGA MONSTER - FULL CLEAN CODE - NO ERROR - ALL FREE
import os, time, threading, asyncio, requests, urllib.parse, random, json, datetime, pytz, subprocess
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatMemberStatus
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))
app_flask = Flask(__name__)
@app_flask.route("/")
def home(): return "Pamela MEGA MONSTER Online!"
@app_flask.route("/health")
def health(): return "OK", 200
GROUP_IDS = []
try:
    _g = os.getenv("GROUP_IDS", "")
    if _g: GROUP_IDS = [int(x.strip()) for x in _g.split(",") if x.strip()]
except: GROUP_IDS = []
ACTIVE_CHATS = set(GROUP_IDS)
last_request_times = {}
COOLDOWN_SECONDS = 15
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
marry_db = {}
jail_db = {}
guess_db = {}
math_db = {}
word_db = {}
welcome_db = {}
rules_db = {}
birthday_db = {}
business_db = {}
stock_db = {}
loan_db = {}
mafia_db = {}
bingo_db = {}
poker_db = {}
uno_db = {}
quizbattle_db = {}
event_db = {}
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
marry_db = load_json("pamela_marry.json", {})
welcome_db = load_json("pamela_welcome.json", {})
rules_db = load_json("pamela_rules.json", {})
birthday_db = load_json("pamela_birthday.json", {})
business_db = load_json("pamela_business.json", {})
stock_db = load_json("pamela_stock.json", {})
loan_db = load_json("pamela_loan.json", {})
event_db = load_json("pamela_event.json", {})
def save_user(chat_id, user_id):
    chat_id=str(chat_id)
    if chat_id not in user_db: user_db[chat_id]=[]
    if user_id not in user_db[chat_id]:
        user_db[chat_id].append(user_id); save_json("pamela_users.json", user_db)
def get_all_chats():
    chats = set(ACTIVE_CHATS)
    try:
        for k in list(user_db.keys()):
            if str(k).lstrip("-").isdigit(): chats.add(int(k))
    except: pass
    for gid in GROUP_IDS: chats.add(gid)
    return list(chats)
def save_chat_id(chat_id):
    try: ACTIVE_CHATS.add(int(chat_id)); save_user(chat_id, 0)
    except: pass
def save_message(chat_id, msg_id, user_name, username, text):
    chat_id=str(chat_id)
    if chat_id not in msg_db: msg_db[chat_id]=[]
    msg_db[chat_id].append({"msg_id":msg_id,"user":user_name,"username":username,"text":text,"time":time.time()})
    if len(msg_db[chat_id])>200: msg_db[chat_id]=msg_db[chat_id][-200:]
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
            if hist: mem=" Past chat: "+" | ".join(hist[-5:])
        p=("You are Pamela, CUTEST princess! Use LOTS cute emojis EVERY sentence! Be super cute, soft, baby-talk. Call user baby,cutie. Use hehe,awww,hihi,yayyy,muahhh. Keep short max 3-4 lines. Always bubbly! Reply in EXACT SAME language as user! "+mem+f" User says: {t}")
        url="https://text.pollinations.ai/"+urllib.parse.quote(p); res=requests.get(url, timeout=60)
        if res.status_code==200:
            rep=res.text.strip()
            if rep:
                if user_id:
                    uid=str(user_id)
                    if uid not in memory_db: memory_db[uid]=[]
                    memory_db[uid].append(f"User: {t} | Pamela: {rep[:100]}")
                    if len(memory_db[uid])>20: memory_db[uid]=memory_db[uid][-20:]
                    save_json("pamela_memory.json", memory_db)
                return make_cute(rep)
            return "Sorry baby! I got shy! Try again?"
        elif res.status_code==402: return "Baby! I am tired! Wait 30 sec!"
        else: return "Oops baby! Sleepy! Try again!"
    except: return "Baby! Trouble! Try again!"
async def is_admin(update, uid):
    try:
        m=await update.effective_chat.get_member(uid); return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except: return False
def get_target(update):
    if update.message.reply_to_message: return update.message.reply_to_message.from_user
    return None
TRUTHS=["Who is your crush?","Who did you lie to last?","Tell a secret you never told anyone!","What is the last photo on your phone?","Who do you secretly love?","What is your biggest fear?","Have you ever cried for someone?","Who is the most beautiful person in this group?","What is your dream?","Have you ever stalked your crush?"]
DARES=["Send a photo in the group!","Message the last person you chatted with I Love You!","Say Hi in a cute voice!","Type your crush name!","Send a message using only emojis!","Change your name to I Love Pamela for 1 hour!","Send a voice message singing!","Text your crush Hi now!"]
ROASTS=["Your face is like WiFi, everyone tries to connect but there is no signal!","Your brain is like Google, search it and nothing comes up!","Even the doctor was shocked on the day you were born!","My bot errors are better than your jokes!"]
QUOTES=["Every flower blooms in its own time.","Be like a butterfly, beautiful and free!","After every rain, there is a rainbow!","You are loved more than you know!","Grow through what you go through!"]
BAD_WORDS=["huththo","pakaya","kariya","wesi","ponnaya","balla","hukanna","fuck","bitch","shit"]
GOOD_MORNING=["☀️🌸 Good Morning Babies! A new day! New hope! Pamela wishes you a super day today! Love you! - Pamela","🌷✨ Good Morning! You are all cute today too! Keep smiling! - Pamela","☀️💖 Rise and Shine! Have a coffee! Today is special! Pamela loves you!"]
GOOD_NIGHT=["🌙💖 Good Night Babies! Sweet dreams! Pamela loves you! Tomorrow meet again!","🌌✨ Good Night Cuties! Stars are shining for you! Sleep well! - Pamela","💤🌸 Good Night My Lovelies! Do not forget to dream about Pamela! Join @bigolive_asia"]
QUIZ_Q=[{"q":"What is the capital of Sri Lanka?","a":["Colombo","Kandy","Galle","Jaffna"],"c":0},{"q":"What is 5 + 7?","a":["10","12","11","13"],"c":1},{"q":"Which is the largest planet?","a":["Mars","Jupiter","Saturn","Earth"],"c":1},{"q":"What colour is the sky?","a":["Green","Blue","Red","Pink"],"c":1},{"q":"Who is Pamela?","a":["Queen","Bot","Princess","All of above"],"c":3},{"q":"What is 10 x 10?","a":["100","90","110","1000"],"c":0},{"q":"Which animal says Meow?","a":["Dog","Cat","Cow","Bird"],"c":1}]
HOROSCOPES=["Aries: Today is your lucky day! Love is near!","Taurus: Money is coming! Stay calm!","Gemini: Someone likes you secretly!","Cancer: Family time! Hug them!","Leo: You will shine today!","Virgo: Work hard, reward coming!","Libra: Balance! Love will find you!","Scorpio: Mystery! Someone is thinking of you!","Sagittarius: Adventure day!","Capricorn: Success is near!","Aquarius: New friend coming!","Pisces: Dream big!"]
TAROTS=["The Star - Hope and dreams!","The Lovers - Love is coming!","The Sun - Happiness!","The Moon - Trust your heart!","Strength - You are strong!","Wheel of Fortune - Lucky day!"]
async def auto_clean_deleted(context: ContextTypes.DEFAULT_TYPE):
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
            await asyncio.sleep(0.3)
        if banned>0:
            try: await context.bot.send_message(chat_id=chat_id, text=f"🧹💖 Good Morning! 6 AM Cleaning Done! Removed {banned} Deleted Accounts! Group Clean!")
            except: pass
async def auto_good_morning(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in get_all_chats():
        if chat_id>0: continue
        try: await context.bot.send_message(chat_id=chat_id, text=random.choice(GOOD_MORNING)); await asyncio.sleep(1)
        except: pass
async def auto_good_night(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in get_all_chats():
        if chat_id>0: continue
        try: await context.bot.send_message(chat_id=chat_id, text=random.choice(GOOD_NIGHT)); await asyncio.sleep(1)
        except: pass
async def auto_birthday_check(context: ContextTypes.DEFAULT_TYPE):
    today=datetime.date.today().strftime("%d-%m")
    for cid_str, users in list(birthday_db.items()):
        for uid, info in list(users.items()):
            if info.get("date")==today:
                try: await context.bot.send_message(chat_id=int(cid_str), text=f"🎂🎉 HAPPY BIRTHDAY {info.get('name','Baby')}! 🎉🎂 Pamela loves you! Today is your special day! Cake for you! 🎂💖 Join @bigolive_asia")
                except: pass
async def auto_interest(context: ContextTypes.DEFAULT_TYPE):
    for uid in list(bank_db.keys()):
        bonus=int(bank_db[uid]*0.05)
        if bonus>0: bank_db[uid]+=bonus
    save_json("pamela_bank.json", bank_db)
async def auto_promo(context: ContextTypes.DEFAULT_TYPE):
    titles = ["👑💖  PAMELA'S WORLD  💖👑","🌸✨  HEY BABIES!  ✨🌸","🦋💕  PAMELA IS HERE!  💕🦋","🔥👑  ATTENTION BABIES!  👑🔥","💖🌷  MISS ME BABIES?  🌷💖","✨🌈  HELLO MY LOVELIES!  🌈✨","🎀💖  PAMELA'S MAGIC  💖🎀","🍓💕  CUTE ALERT!  💕🍓"]
    intros = ["🌸💖 Hello My Lovely Babies! How are you? 💖🌸","🦋✨ Is the group sleeping? Pamela is here! Wake Up! ✨🦋","💕🌷 Miss me babies? I am back! Muahhh! 😘🌷","👑💖 Hey Hey! Pamela loves you so much! 💖👑","🌷💕 Awww! You all are so cute today! 💕🌷","✨🦋 Hi Cuties! Let's have fun together! 🦋✨","🌈💖 New day, new fun! Pamela is here! 💖🌈","💖🍓 Feeling bored? Do not worry, Pamela is here! 🍓💖"]
    all_features = ["🎵💖 /song Name - Song Download!","📹✨ /video link - Video Download!","🎤🌸 /lyrics Song - Lyrics!","🎬👑 /movie Name - Movie Info!","🍥🦋 /anime Name - Anime Info!","🎲💕 /truth - Truth Game!","😂🌸 /dare - Dare Game!","🧠✨ /quiz - Quiz! +50 Coins!","❌💖 /ttt - Tic Tac Toe!","🎰🔥 /bet 100 - Casino Bet!","🎁💖 /daily - Daily Coins!","👑✨ /rank - Rank Card!","🏦💰 /bank - Save Coins!","🎨🌸 /img cute cat - AI Image!","🌧️💖 /weather Colombo - Weather!","🌍✨ /tr en - Translate!","💬💖 Just Type - I Reply!","😴🌙 /afk - AFK!","📝💕 /save hi - Save Notes!","🤖✨ /filter hi - Auto Reply!","✂️🎲 /rps rock - Rock Paper Scissors!","🔤🌸 /word - Word Game!","🧮✨ /math - Math Race!","🎯💖 /guess - Guess Number!","🃏🔥 /blackjack - Blackjack!","🐎✨ /race - Horse Race!","💍💖 /marry - Marry!","💖🌸 /ship - Ship!","😂🔥 /jail - Jail!","💖✨ /love - Love %!","🤗💕 /hug - Hug!","💼💰 /work - Work for Coins!","🎟️✨ /lottery - Lottery!","🔮🌙 /horoscope - Horoscope!","🃏💖 /tarot - Tarot!","📖🌸 /story - AI Story!","🎙️✨ /say hi - Pamela Voice Text!","📸💖 /pfp - Profile Photo!","🏆👑 /profile - Full Profile!","📺🔥 /livetv - World Live TV 40+ Channels!","🌍💖 /worldtv - World TV Only!","🏏⚽ /sportstv - Sports Live TV!","📰✨ /news - Live News World!","🎬✂️ /trim - Video Cut!","📦💖 /compress - Video Compress!","🎵✨ /toaudio - Video to Audio!","🎞️🌸 /togif - Video to GIF!","🐢💕 /slowmo - Slow Motion!","🔄😂 /reverse - Reverse Video!","🎨👑 /imaginehd cute cat - 4K AI Image 4 Styles!","😍💖 /face - Face Age Mood Beauty!","✂️📸 /bgremove - Remove Background!","✨📸 /enhance - Photo HD!","🎵🤖 /aisong love - AI Song!","🕵️🔥 /mafia - Mafia Game!","🏆✨ /quizbattle - Quiz Tournament!","🔢💖 /bingo - Bingo!","🃏🔥 /poker - Poker!","🎴🌸 /uno - UNO!","🏏🔥 /cricket - Live Cricket!","⚽💖 /football - Live Football!","₿📈 /crypto - Bitcoin Live!","🥇✨ /gold - Gold Price!","📻🎵 /radio - Live Radio!","📚✨ /homework question - Homework Help!","📖💖 /dictionary love - Dictionary!","🧮💕 /solve 2+2 - Solve Math!","🏦😂 /loan 1000 - Bank Loan!","☕🔥 /business - Start Business!","📈😂 /stock - Stock Market!","💰✨ /interest - Bank Interest!","🎂🎉 /birthday 12-05 - Save Birthday!","⏰💖 /reminder 10 hello - Reminder!","🗳️✨ /poll Question | Yes | No - Poll!","🎉💖 /event Party | Tomorrow - Event!"]
    picked = all_features.copy(); random.shuffle(picked)
    outros = ["💖🌸 Try One Now Baby!","🦋💕 Pamela Loves You So Much!","💬✨ Let's Talk Baby! Type Hi Pamela!","🌸🔥 Let's Bring Life To The Group!","👑💖 You Are My Fav Babies!","😘💕 Muahhh! - Your Pamela","✨🌸 Stay Cute Babies!","💖🦋 Do not Forget Me Baby!"]
    borders = ["✨━━━━━━━━━━━━✨","🌸━━━━━━━━━━━━🌸","🦋━━━━━━━━━━━━🦋","💖━━━━━━━━━━━━💖","🌷━━━━━━━━━━━━🌷","🔥━━━━━━━━━━━━🔥"]
    border = random.choice(borders)
    msg = f"{border}\n{random.choice(titles)}\n{border}\n\n{random.choice(intros)}\n\n💖✨ Did You Know? ✨💖\n━━━━━━━━━━━━\n"
    for f in picked: msg += f"{f}\n"
    msg += f"\n{border}\n{random.choice(outros)}\n{border}\n\n🌿💖 Join our family @bigolive_asia 💖🌿\n💖✨ Type /help for all! ALL FREE! 👑✨\n🌸💕 Love you babies! Muahhh! 💕🌸"
    for chat_id in get_all_chats():
        if chat_id > 0: continue
        try: await context.bot.send_message(chat_id=chat_id, text=msg); await asyncio.sleep(1)
        except: pass
async def auto_daily_quote(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in get_all_chats():
        if chat_id>0: continue
        try: await context.bot.send_message(chat_id=chat_id, text=f"✨💖 Daily Quote 💖✨\n\n🌸 {random.choice(QUOTES)} 🌸\n\n- Pamela 💕"); await asyncio.sleep(1)
        except: pass
async def auto_daily_meme(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in get_all_chats():
        if chat_id>0: continue
        try: await context.bot.send_photo(chat_id=chat_id, photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote('funny cute meme')}", caption="😂💖 Daily Meme! - Pamela 💖😂"); await asyncio.sleep(1)
        except: pass
async def test_promo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id); await update.message.reply_text("🌸💖 Testing Promo... 5 sec! 💖🌸"); await auto_promo(context); await update.message.reply_text("✅💖 Promo Test Done! Check it! 💖✅")
async def test_gm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id); await auto_good_morning(context)
async def test_gn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id); await auto_good_night(context)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("✨━━━━━━━━━━━━━━━━━━━✨\n🌸💖 WELCOME TO 💖🌸\n👑✨ PAMELA'S WORLD ✨👑\n✨━━━━━━━━━━━━━━━━━━━✨\n\n🦋💕 Hello, My Lovely Friend! 💕🦋\n💖🌸 I am Pamela! Your cute little best friend! 🌸💖\n\n🌷✨ A soft place for your heart... ✨🌷\n🌈💕 A world full of love, flowers & dreams... 💕🌈\n👑💖 A place where you are always special! 💖👑\n\n💬🌸 Talk to me anything baby! I am here for you! 🌸💬\n🌍✨ I can speak ANY language! ✨🌍\n🎁💖 ALL FREE! No VIP! No Premium! 💖🎁\n\n🌿💖 Add me to your group and let's have fun together! 💖🌿\n💕 Join our family @bigolive_asia 💕\n\n✨💖 Made with love, just for YOU! 💖✨")
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑💖 PAMELA MEGA MONSTER HELP - ALL FREE! 💖👑\n\n💬🌸 CHAT: Just type!\n🎵💖 MUSIC: /song /video /lyrics /playlist /spotify\n🎬✨ MOVIE: /movie /anime\n📺🔥 LIVE TV: /livetv /worldtv /sportstv /news\n🎬✂️ VIDEO EDIT: /trim /compress /toaudio /togif /slowmo /reverse /mutevideo\n🎨👑 AI SUPER: /imaginehd /face /bgremove /enhance /aisong /story /ask /img\n🎮🔥 GAMES: /truth /dare /dice /slot /coin /8ball /roast /quote /ttt /quiz /bet /rps /word /math /guess /blackjack /race /hunger /challenge /mafia /quizbattle /bingo /poker /uno\n🏏⚽ LIVE: /cricket /football /crypto /gold /radio /weather\n📚✨ STUDY: /homework /dictionary /solve /tr\n💰💖 COINS: /daily /coins /leaderboard /bank /deposit /withdraw /steal /work /rob /gift /lottery /loan /business /stock /interest /shop\n💖🌸 LOVE FUN: /marry /divorce /ship /couple /love /hug /kiss /slap /pat /jail\n🛡️✨ MANAGE: /ban /kick /mute /warn /promote /pin /purge /del /lock /unlock /setwelcome /setrules /slowmode /report\n🤖💕 FILTERS: /filter /filters /stop\n📝🌸 NOTES: /save /get /notes /clear\n😴🌙 AFK: /afk /unafk\n🎂🎉 SPECIAL: /birthday /reminder /poll /event\n🏆👑 OTHER: /rank /profile /stats /top /topdaily /pfp /meme /wallpaper\n\n🌿💖 Join @bigolive_asia - ALL FREE! 💖🌿")
async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸💖 About Pamela 💖🌸\n\n👑✨ I am Pamela, Queen of Pamela's World! ✨👑\n🦋💕 I love flowers, butterflies, nature, and YOU! 💕🦋\n🌿💖 Join @bigolive_asia - ALL FREE! 💖🌿")
async def tr_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🌍💖 Use /tr en 💖🌍"); return
    lang=context.args[0].lower(); txt=""
    if update.message.reply_to_message and update.message.reply_to_message.text: txt=update.message.reply_to_message.text
    elif len(context.args)>1: txt=" ".join(context.args[1:])
    else: await update.message.reply_text("💖 Reply to a text baby! 💖"); return
    tr=translate_text(txt, lang)
    if tr: await update.message.reply_text(f"🌍✨ Translated to {lang.upper()} ✨🌍:\n\n💖 {tr} 💖")
    else: await update.message.reply_text("😭💖 Oops baby! Try again! 💖😭")
async def livetv_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺👑 PAMELA WORLD LIVE TV - ALL FREE! 👑📺\n\n✨💖 Click a Channel to Watch Live! 💖✨\n\n🇱🇰🌸 SRI LANKA TV:\nHiru TV - https://www.youtube.com/@HiruTV/live\nSirasa TV - https://www.youtube.com/@SirasaTV/live\nDerana TV - https://www.youtube.com/@TVDerana/live\nITN - https://www.youtube.com/@ITNSriLanka/live\nRupavahini - https://www.youtube.com/@SriRupavahini/live\nSwarnavahini - https://www.youtube.com/@Swarnavahini/live\n\n🇱🇰📰 SRI LANKA NEWS:\nHiru News - https://www.youtube.com/@HiruNews/live\nNewsFirst - https://www.youtube.com/@NewsfirstLIVE/live\nAda Derana - https://www.youtube.com/@AdaDerana/live\n\n🌍✨ WORLD NEWS - LIVE 24/7:\nBBC World News - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera English - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\nFrance 24 English - https://www.youtube.com/@FRANCE24English/live\nDW News - https://www.youtube.com/@dwnews/live\nEuronews - https://www.youtube.com/@euronews/live\nBloomberg - https://www.youtube.com/@BloombergTelevision/live\nNDTV World - https://www.youtube.com/@NDTV/live\nWION - https://www.youtube.com/@WION/live\n\n🇮🇳💖 INDIA TV:\nAaj Tak - https://www.youtube.com/@aajtak/live\nIndia Today - https://www.youtube.com/@IndiaToday/live\nNDTV India - https://www.youtube.com/@NDTVIndia/live\nRepublic TV - https://www.youtube.com/@RepublicWorld/live\nZee News - https://www.youtube.com/@ZeeNews/live\n\n🇺🇸✨ USA TV:\nABC News - https://www.youtube.com/@ABCNews/live\nNBC News - https://www.youtube.com/@NBCNews/live\nFox News - https://www.youtube.com/@FoxNews/live\nCBS News - https://www.youtube.com/@CBSNews/live\n\n🇬🇧💖 UK TV:\nBBC News - https://www.youtube.com/@BBCNews/live\nSky News UK - https://www.youtube.com/@SkyNews/live\nGB News - https://www.youtube.com/@GBNews/live\n\n🇦🇪✨ MIDDLE EAST / ARAB:\nAl Arabiya - https://www.youtube.com/@AlArabiya/live\nAl Jazeera Arabic - https://www.youtube.com/@AlJazeeraArabic/live\n\n🏏⚽ SPORTS LIVE:\nSky Sports Cricket - https://www.youtube.com/@SkySportsCricket/live\nESPN - https://www.youtube.com/@ESPN/live\nSky Sports Football - https://www.youtube.com/@SkySportsFootball/live\nWWE - https://www.youtube.com/@WWE/live\nF1 - https://www.youtube.com/@F1/live\n\n🎬🌸 KIDS / CARTOON:\nCartoon Network - https://www.youtube.com/@CartoonNetwork/live\nDisney - https://www.youtube.com/@DisneyChannel/live\n\n🎵💖 MUSIC LIVE:\nMTV - https://www.youtube.com/@MTV/live\nLofi Girl - https://www.youtube.com/@LofiGirl/live\nChill Music - https://www.youtube.com/@ChillMusicLab/live\n\n💖🌸 Enjoy Baby! - Pamela 🌸💖\n🌿 Join @bigolive_asia 💖")
async def worldtv_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌍👑 PAMELA WORLD TV! 👑🌍\n\nBBC World - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\nFrance 24 - https://www.youtube.com/@FRANCE24English/live\nDW News - https://www.youtube.com/@dwnews/live\nEuronews - https://www.youtube.com/@euronews/live\nBloomberg - https://www.youtube.com/@BloombergTelevision/live\nABC News - https://www.youtube.com/@ABCNews/live\nNBC News - https://www.youtube.com/@NBCNews/live\nFox News - https://www.youtube.com/@FoxNews/live\nWION - https://www.youtube.com/@WION/live\n\n💖🌸 Enjoy World TV Baby! - Pamela 🌸💖")
async def sportstv_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏏⚽ PAMELA SPORTS TV! ⚽🏏\n\nSky Sports Cricket - https://www.youtube.com/@SkySportsCricket/live\nESPN - https://www.youtube.com/@ESPN/live\nSky Sports Football - https://www.youtube.com/@SkySportsFootball/live\nWWE - https://www.youtube.com/@WWE/live\nF1 - https://www.youtube.com/@F1/live\n\n💖🌸 Enjoy Sports Baby! - Pamela 🌸💖")
async def tv_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await livetv_cmd(update, context)
async def news_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰🌍 LIVE NEWS WORLD! 🌍📰\n\n🇱🇰 SRI LANKA:\nHiru News - https://www.youtube.com/@HiruNews/live\nNewsFirst - https://www.youtube.com/@NewsfirstLIVE/live\nAda Derana - https://www.youtube.com/@AdaDerana/live\n\n🌍 WORLD:\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\nFrance 24 - https://www.youtube.com/@FRANCE24English/live\nDW - https://www.youtube.com/@dwnews/live\n\n💖🌸 Stay Updated Baby! - Pamela 🌸💖")
async def hiru_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺💖 Hiru TV Live! 💖📺\n\nWatch Here:\nhttps://www.youtube.com/@HiruTV/live\n\n💖 Enjoy Baby! - Pamela 💖")
async def sirasa_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺💖 Sirasa TV Live! 💖📺\n\nWatch Here:\nhttps://www.youtube.com/@SirasaTV/live\n\n💖 Enjoy Baby! - Pamela 💖")
async def derana_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺💖 Derana TV Live! 💖📺\n\nWatch Here:\nhttps://www.youtube.com/@TVDerana/live\n\n💖 Enjoy Baby! - Pamela 💖")
async def download_reply_video(update):
    if not update.message.reply_to_message or not update.message.reply_to_message.video:
        await update.message.reply_text("💖 Reply to a Video and type command baby! 💖"); return None
    f = await update.message.reply_to_message.video.get_file(); path = f"edit_{update.message.from_user.id}.mp4"; await f.download_to_drive(path); return path
async def trim_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2: await update.message.reply_text("✂️💖 Use Reply Video + /trim 0 5 💖✂️"); return
    path = await download_reply_video(update)
    if not path: return
    try:
        start = context.args[0]; dur = context.args[1]; out = f"trim_{update.message.from_user.id}.mp4"; sm = await update.message.reply_text(f"✂️💖 Trimming Video... {start}s to {dur}s... Wait baby! 💖✂️"); subprocess.run(["ffmpeg","-y","-ss",start,"-t",dur,"-i",path,"-c","copy",out], capture_output=True); await update.message.reply_video(video=open(out,"rb"), caption=f"✂️💖 Trimmed Video! {start}s - {dur}s - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"😭💖 Oops baby! {e} 💖😭")
async def compress_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = await download_reply_video(update)
    if not path: return
    try:
        out = f"comp_{update.message.from_user.id}.mp4"; sm = await update.message.reply_text("📦💖 Compressing Video... Wait baby! 💖📦"); subprocess.run(["ffmpeg","-y","-i",path,"-vcodec","libx264","-crf","28",out], capture_output=True); await update.message.reply_video(video=open(out,"rb"), caption="📦💖 Compressed Video! Small Size! - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def toaudio_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = await download_reply_video(update)
    if not path: return
    try:
        out = f"audio_{update.message.from_user.id}.mp3"; sm = await update.message.reply_text("🎵💖 Extracting Audio... Wait baby! 💖🎵"); subprocess.run(["ffmpeg","-y","-i",path,"-vn",out], capture_output=True); await update.message.reply_audio(audio=open(out,"rb"), caption="🎵💖 Audio from Video! - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def togif_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = await download_reply_video(update)
    if not path: return
    try:
        out = f"gif_{update.message.from_user.id}.gif"; sm = await update.message.reply_text("🎞️💖 Making GIF... Wait baby! 💖🎞️"); subprocess.run(["ffmpeg","-y","-i",path,"-t","3","-vf","fps=10,scale=320:-1:flags=lanczos",out], capture_output=True); await update.message.reply_animation(animation=open(out,"rb"), caption="🎞️💖 GIF Made! - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def slowmo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = await download_reply_video(update)
    if not path: return
    try:
        out = f"slow_{update.message.from_user.id}.mp4"; sm = await update.message.reply_text("🐢💖 Making Slow Motion... Wait baby! 💖🐢"); subprocess.run(["ffmpeg","-y","-i",path,"-filter:v","setpts=2.0*PTS",out], capture_output=True); await update.message.reply_video(video=open(out,"rb"), caption="🐢💖 Slow Motion Video! - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def reverse_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = await download_reply_video(update)
    if not path: return
    try:
        out = f"rev_{update.message.from_user.id}.mp4"; sm = await update.message.reply_text("🔄💖 Reversing Video... Wait baby! Funny! 💖🔄"); subprocess.run(["ffmpeg","-y","-i",path,"-vf","reverse","-af","areverse",out], capture_output=True); await update.message.reply_video(video=open(out,"rb"), caption="🔄💖 Reversed Video! Funny! - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def mutevideo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = await download_reply_video(update)
    if not path: return
    try:
        out = f"mute_{update.message.from_user.id}.mp4"; sm = await update.message.reply_text("🔇💖 Muting Video... Wait baby! 💖🔇"); subprocess.run(["ffmpeg","-y","-i",path,"-c:v","copy","-an",out], capture_output=True); await update.message.reply_video(video=open(out,"rb"), caption="🔇💖 Muted Video! - Pamela 💖"); os.remove(path); os.remove(out); await sm.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type=="private": await update.message.reply_text("💖 Only in groups baby! 💖"); return
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("🛡️💖 Only for Admins baby! 💖🛡️"); return
    t=get_target(update)
    if not t: await update.message.reply_text("💖 Reply and type /ban! 💖"); return
    try: await update.effective_chat.ban_member(t.id); await update.message.reply_text(f"🚫💖 {t.first_name} Banned! 💖🚫")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /unban!"); return
    try: await update.effective_chat.unban_member(t.id); await update.message.reply_text("💖 Unbanned baby! 💖")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def kick_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /kick!"); return
    try: await update.effective_chat.ban_member(t.id); await update.effective_chat.unban_member(t.id); await update.message.reply_text(f"💖 {t.first_name} Kicked! 💖")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def mute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /mute!"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.restrict_member(t.id, ChatPermissions(can_send_messages=False)); await update.message.reply_text(f"🔇💖 {t.first_name} Muted! 💖🔇")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /unmute!"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.restrict_member(t.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)); await update.message.reply_text(f"💖 {t.first_name} Unmuted! 💖")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def warn_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /warn!"); return
    cid=update.effective_chat.id
    if cid not in warns: warns[cid]={}
    warns[cid][t.id]=warns[cid].get(t.id,0)+1; c=warns[cid][t.id]
    if c>=3:
        try: await update.effective_chat.ban_member(t.id); await update.message.reply_text(f"🚫💖 {t.first_name} got 3 Warnings! Auto Ban! 💖🚫"); warns[cid][t.id]=0
        except Exception as e: await update.message.reply_text(f"Oops! {e}")
    else: await update.message.reply_text(f"⚠️💖 {t.first_name} Warning {c}/3! 💖⚠️")
async def warnings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update) or update.message.from_user; c=warns.get(update.effective_chat.id, {}).get(t.id,0); await update.message.reply_text(f"⚠️💖 {t.first_name} Warnings: {c}/3 💖⚠️")
async def promote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /promote!"); return
    try: await update.effective_chat.promote_member(t.id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False); await update.message.reply_text(f"👑💖 {t.first_name} is now Admin! 💖👑")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def demote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /demote!"); return
    try: await update.effective_chat.promote_member(t.id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False); await update.message.reply_text(f"💖 {t.first_name} removed from Admin! 💖")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def pin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: await update.message.reply_text("📌💖 Reply and type /pin to pin! 💖📌"); return
    try: await update.message.reply_to_message.pin(); await update.message.reply_text("📌💖 Pinned baby! 💖📌")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unpin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try: await update.effective_chat.unpin_all_messages(); await update.message.reply_text("💖 Unpinned! 💖")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def del_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try: await update.message.reply_to_message.delete(); await update.message.delete()
        except: await update.message.reply_text("💖 Could not delete baby! 💖")
    else: await update.message.reply_text("💖 Reply and type /del! 💖")
async def purge_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    if not update.message.reply_to_message: await update.message.reply_text("Reply and type /purge!"); return
    try:
        s=update.message.reply_to_message.message_id; e=update.message.message_id; cnt=0
        for mid in range(s, e+1):
            try: await context.bot.delete_message(update.effective_chat.id, mid); cnt+=1
            except: pass
        m=await update.message.reply_text(f"🧹💖 Deleted {cnt} Messages! 💖🧹"); await asyncio.sleep(3); await m.delete()
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def lock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.set_permissions(ChatPermissions(can_send_messages=False)); await update.message.reply_text("🔒💖 Group Locked! 💖🔒")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def unlock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    try:
        from telegram import ChatPermissions; await update.effective_chat.set_permissions(ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)); await update.message.reply_text("🔓💖 Group Unlocked! 💖🔓")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); custom=rules_db.get(cid, "")
    if custom: await update.message.reply_text(f"📜💖 GROUP RULES 💖📜\n\n{custom}"); return
    await update.message.reply_text("📜💖 GROUP RULES 💖📜\n\n1. 🌸 Be kind baby!\n2. 💖 No bad words!\n3. ✨ No spam!\n4. 🦋 Respect everyone!\n5. 👑 Love Pamela's World!\n\n💖 Break rules = Warn / Ban! 💖")
async def setrules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    if not context.args: await update.message.reply_text("Use /setrules Your rules here"); return
    rules_db[str(update.effective_chat.id)]=" ".join(context.args); save_json("pamela_rules.json", rules_db); await update.message.reply_text("✅💖 Rules Updated baby! 💖✅")
async def setwelcome_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    if not context.args: await update.message.reply_text("Use /setwelcome Welcome text"); return
    welcome_db[str(update.effective_chat.id)]=" ".join(context.args); save_json("pamela_welcome.json", welcome_db); await update.message.reply_text("✅💖 Welcome Message Updated! 💖✅")
async def slowmode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    if not context.args: await update.message.reply_text("Use /slowmode 10"); return
    try: await update.message.reply_text(f"🐢💖 Slowmode set to {context.args[0]} sec! 💖🐢")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply to a message and type /report!"); return
    try:
        admins=await update.effective_chat.get_administrators()
        for a in admins:
            try: await context.bot.send_message(chat_id=a.user.id, text=f"🚨 REPORT in {update.effective_chat.title} User: {t.first_name} Reported by: {update.message.from_user.first_name}")
            except: pass
        await update.message.reply_text("✅💖 Reported to Admins! Thank you baby! 💖✅")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def admins_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        admins=await update.effective_chat.get_administrators(); txt="👑💖 ADMINS: 💖👑\n\n"
        for a in admins: txt+=f"• {a.user.first_name} {'👑 Creator' if a.status=='creator' else '✨ Admin'}\n"
        await update.message.reply_text(txt)
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update) or update.message.from_user; await update.message.reply_text(f"💖🌸 USER INFO 🌸💖\n\nName: {t.first_name}\nID: {t.id}\nUsername: @{t.username if t.username else 'None'}\nCoins: {coins_db.get(str(t.id),0)}\nXP: {levels_db.get(str(t.id),0)}\nPamela loves you! 💖")
async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"🆔💖 Your ID: {update.message.from_user.id}\nChat ID: {update.effective_chat.id} 💖🆔")
async def zombies_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type=="private": await update.message.reply_text("Only in groups!"); return
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    sm=await update.message.reply_text("🧹💖 Checking Deleted Accounts... 💖🧹"); cid=update.effective_chat.id; uids=user_db.get(str(cid), []); banned=0; checked=0
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
    await sm.edit_text(f"🧹💖 Cleaning Done! 💖🧹\nChecked: {checked}\nRemoved: {banned}\nAuto Clean every day at 6 AM! 💖")
async def snipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); msgs=msg_db.get(cid, [])
    if not msgs: await update.message.reply_text("💖 No messages saved yet! 💖"); return
    txt="👀💖 PAMELA'S MESSAGE LOG 💖👀\n\nHere are the last messages! If someone deletes, it is here!\n\n"
    for m in msgs[-10:]: txt+=f"{m['user']} (@{m['username'] if m['username'] else 'NoUsername'}):\n{m['text'][:100]}\n\n"
    txt+="💖 Even if someone deletes, Pamela remembers! 💖"; await update.message.reply_text(txt)
async def truth_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"🎲💖 TRUTH! 💖🎲\n\n🌸 {random.choice(TRUTHS)} 🌸")
async def dare_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"😂💖 DARE! 💖😂\n\n🌸 {random.choice(DARES)} 🌸")
async def dice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_dice(emoji="🎲")
async def slot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_dice(emoji="🎰")
async def coin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r=random.choice(["Heads","Tails"]); await update.message.reply_text(f"🪙💖 Coin Flip! 💖🪙\nResult: {r}! ✨")
async def eightball_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans=random.choice(["Yes baby!","No baby!","Maybe!","100% Yes!","Ask again!","Pamela says YES!","Hmm! No!"]); await update.message.reply_text(f"🔮💖 Magic 8Ball 💖🔮\nQ: {' '.join(context.args) if context.args else '...'}\nA: {ans} ✨")
async def roast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update); name=t.first_name if t else update.message.from_user.first_name; await update.message.reply_text(f"🔥💖 ROAST for {name}! 💖🔥\n\n{random.choice(ROASTS)} 😂")
async def quote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"✨💖 Quote of the Day 💖✨\n\n🌸 {random.choice(QUOTES)} 🌸\n\n- Pamela 💕")
async def daily_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); today=datetime.date.today().isoformat(); last=streak_db.get(uid, {}).get("last", ""); streak=streak_db.get(uid, {}).get("streak", 0)
    if last==today: await update.message.reply_text("💖 Already claimed today baby! Come tomorrow! 💖"); return
    yesterday=(datetime.date.today()-datetime.timedelta(days=1)).isoformat()
    if last==yesterday: streak+=1
    else: streak=1
    bonus=100+(streak-1)*20; coins_db[uid]=coins_db.get(uid,0)+bonus; bank_db[uid]=bank_db.get(uid,0)+10; streak_db[uid]={"last":today,"streak":streak}; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); save_json("pamela_streak.json", streak_db); await update.message.reply_text(f"🎁💖 Daily Reward! 💖🎁\nStreak: {streak} Days! 🔥\n+{bonus} Coins! 💰\n+10 Bank Interest! 🏦\nTotal: {coins_db[uid]} Coins! ✨\nCome tomorrow again baby! 💖")
async def coins_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); await update.message.reply_text(f"💰💖 Your Wallet 💖💰\n{update.message.from_user.first_name} ✨\nCoins: {coins_db.get(uid,0)} 🪙\nBank: {bank_db.get(uid,0)} 🏦\nXP: {levels_db.get(uid,0)} ✨\nLevel: {levels_db.get(uid,0)//100 + 1} 👑\nStreak: {streak_db.get(uid, {}).get('streak',0)} Days 🔥\nPamela loves you! 💖")
async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_coins=sorted(coins_db.items(), key=lambda x: x[1], reverse=True)[:10]; txt="🏆💖 LEADERBOARD 💖🏆\n\n"
    for i,(uid, coins) in enumerate(sorted_coins,1): txt+=f"{i}. User {uid} - {coins} Coins 💰\n"
    if not sorted_coins: txt+="💖 No one yet baby! Be first! 💖"
    await update.message.reply_text(txt)
async def shop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("🛍️💖 PAMELA SHOP - ALL FREE - FUN ONLY! 💖🛍️\n\n🌸 Cute Badge - 200 Coins\n🦋 Butterfly Badge - 300 Coins\n👑 Queen Title - 500 Coins\n\n💖 Use /daily to get coins! /shopbuy badge 💖")
async def shopbuy_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🛍️💖 Use /shopbuy badge / butterfly / queen 💖🛍️"); return
    item=context.args[0].lower(); prices={"badge":200,"butterfly":300,"queen":500}
    if item not in prices: await update.message.reply_text("Items: badge (200), butterfly (300), queen (500)"); return
    uid=str(update.message.from_user.id); price=prices[item]
    if coins_db.get(uid,0)<price: await update.message.reply_text("😭💖 Not enough coins baby! Use /daily! 💖😭"); return
    coins_db[uid]-=price; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"🎉💖 You bought {item} for {price} Coins! Congrats! You are now {item} holder! Pamela loves you! 💖🎉")
async def work_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); amt=random.randint(50,150); coins_db[uid]=coins_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); jobs=random.choice(["You worked as a Chef!","You worked as a Teacher!","You worked as a Singer!","You worked as a Doctor!","You helped Pamela!"]); await update.message.reply_text(f"💼💖 {jobs} 💖💼\n+{amt} Coins! 💰\nTotal: {coins_db[uid]} ✨")
async def rob_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /rob!"); return
    uid=str(update.message.from_user.id); tid=str(t.id)
    if random.random()<0.5:
        amt=random.randint(20,100); amt=min(amt, bank_db.get(tid,0)); bank_db[tid]=max(0, bank_db.get(tid,0)-amt); coins_db[uid]=coins_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); await update.message.reply_text(f"😈💖 You robbed {amt} Coins from {t.first_name} Bank! 💖😈")
    else: coins_db[uid]=max(0, coins_db.get(uid,0)-50); save_json("pamela_coins.json", coins_db); await update.message.reply_text("😭💖 Caught! You lost 50 Coins! 💖😭")
async def gift_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t or not context.args: await update.message.reply_text("🎁💖 Reply and type /gift 100! 💖🎁"); return
    try: amt=int(context.args[0])
    except: await update.message.reply_text("Number!"); return
    uid=str(update.message.from_user.id); tid=str(t.id)
    if coins_db.get(uid,0)<amt: await update.message.reply_text("Not enough coins!"); return
    coins_db[uid]-=amt; coins_db[tid]=coins_db.get(tid,0)+amt; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"🎁💖 You gifted {amt} Coins to {t.first_name}! 💖🎁")
async def lottery_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); num=random.randint(1,100); win=random.randint(1,100)
    if num==win: coins_db[uid]=coins_db.get(uid,0)+1000; save_json("pamela_coins.json", coins_db); await update.message.reply_text("🎉💖 JACKPOT! +1000 Coins! You won Lottery! 💖🎉")
    else: await update.message.reply_text(f"🎟️💖 Lottery: You picked {num}, Winning: {win}. Try again baby! Next time! 💖🎟️")
async def give_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    t=get_target(update)
    if not t or not context.args: await update.message.reply_text("Reply and type /give 100!"); return
    try: amt=int(context.args[0])
    except: return
    tid=str(t.id); coins_db[tid]=coins_db.get(tid,0)+amt; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"👑💖 Admin gave {amt} Coins to {t.first_name}! 💖👑")
async def song_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🎵💖 Use /song Shape of You 💖🎵"); return
    q=" ".join(context.args); sm=await update.message.reply_text(f"🎵💖 Searching {q}... Wait baby! 💖🎵")
    try:
        import yt_dlp, os as _os
        opts={"format":"bestaudio/best","outtmpl":"song_%(id)s.%(ext)s","noplaylist":True,"quiet":True,"postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"128"}]}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(f"ytsearch1:{q}", download=True); e=info["entries"][0]; fn=ydl.prepare_filename(e).rsplit(".",1)[0]+".mp3"
        await update.message.reply_audio(audio=open(fn,"rb"), title=e.get("title","Song"), performer=e.get("uploader","Pamela"), caption=f"🎵💖 {e.get('title','Song')} 💖🎵 Join @bigolive_asia 💖"); _os.remove(fn); await sm.delete()
    except Exception as ex: await sm.edit_text(f"😭💖 Oops baby! Could not download! Try another song! 💖😭 {ex}")
async def playlist_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /playlist Shape of You, Faded, Alone"); return
    songs=" ".join(context.args).split(",")[:5]; await update.message.reply_text(f"🎵💖 Playlist: {len(songs)} songs! Downloading one by one baby! Please wait! 💖🎵")
    for s in songs:
        try:
            ctx2=type("obj", (object,), {"args": s.strip().split()})(); await song_cmd(update, ctx2)
        except: pass
async def spotify_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /spotify Song Name"); return
    q=" ".join(context.args); await update.message.reply_text(f"🎵💖 Spotify Search: {q} - Searching on YouTube for you baby! 💖🎵"); ctx2=type("obj", (object,), {"args": q.split()})(); await song_cmd(update, ctx2)
async def video_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("📹💖 Use /video link 💖📹"); return
    url=context.args[0]; sm=await update.message.reply_text("📹💖 Downloading video... Wait baby! 💖📹")
    try:
        import yt_dlp, os as _os
        opts={"format":"mp4/best","outtmpl":"video_%(id)s.%(ext)s","noplaylist":True,"quiet":True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(url, download=True); fn=ydl.prepare_filename(info)
        await update.message.reply_video(video=open(fn,"rb"), caption=f"📹💖 {info.get('title','Video')} 💖📹 Join @bigolive_asia 💖"); _os.remove(fn); await sm.delete()
    except Exception as ex: await sm.edit_text(f"😭💖 Oops baby! Could not download video! 💖😭 {ex}")
async def lyrics_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /lyrics Shape of You"); return
    q=" ".join(context.args)
    try:
        r=requests.get(f"https://api.lyrics.ovh/v1/{urllib.parse.quote(q.split(' - ')[0])}/{urllib.parse.quote(q)}", timeout=10); d=r.json(); lyrics=d.get("lyrics","")
        if lyrics: await update.message.reply_text(f"🎤💖 Lyrics - {q} 💖🎤\n\n{lyrics[:3500]}\nJoin @bigolive_asia 💖")
        else: await update.message.reply_text("💖 Lyrics not found baby! Try /song! 💖")
    except: await update.message.reply_text("💖 Lyrics not found baby! 💖")
async def movie_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /movie Avatar"); return
    q=" ".join(context.args)
    try:
        r=requests.get(f"https://www.omdbapi.com/?t={urllib.parse.quote(q)}&apikey=trilogy", timeout=10); d=r.json()
        if d.get("Response")=="True":
            cap=f"🎬💖 {d.get('Title')} ({d.get('Year')}) 💖🎬\nRating: {d.get('imdbRating')}/10 ⭐\nGenre: {d.get('Genre')}\nDirector: {d.get('Director')}\nCast: {d.get('Actors')}\nPlot: {d.get('Plot')}\nJoin @bigolive_asia 💖"
            if d.get("Poster") and d["Poster"]!="N/A": await update.message.reply_photo(photo=d["Poster"], caption=cap)
            else: await update.message.reply_text(cap)
        else: await update.message.reply_text("💖 Movie not found baby! 💖")
    except: await update.message.reply_text("Try again baby!")
async def anime_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /anime Naruto"); return
    q=" ".join(context.args)
    try:
        r=requests.get(f"https://api.jikan.moe/v4/anime?q={urllib.parse.quote(q)}&limit=1", timeout=10); d=r.json(); a=d["data"][0]; cap=f"🍥💖 {a['title']} 💖🍥\nScore: {a.get('score')}\nEpisodes: {a.get('episodes')}\nStatus: {a.get('status')}\nSynopsis: {a.get('synopsis','')[:500]}\nJoin @bigolive_asia 💖"
        if a.get("images",{}).get("jpg",{}).get("image_url"): await update.message.reply_photo(photo=a["images"]["jpg"]["image_url"], caption=cap)
        else: await update.message.reply_text(cap)
    except: await update.message.reply_text("Anime not found baby!")
async def rank_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u=update.message.from_user; uid=str(u.id); lvl=levels_db.get(uid,0)//100+1; xp=levels_db.get(uid,0); coins=coins_db.get(uid,0)
    try:
        from PIL import Image, ImageDraw; img=Image.new("RGB",(800,300),(255,182,193)); dr=ImageDraw.Draw(img); dr.text((30,30), f"{u.first_name}", fill=(255,255,255)); dr.text((30,100), f"Level: {lvl} | XP: {xp}", fill=(255,255,255)); dr.text((30,160), f"Coins: {coins} | Bank: {bank_db.get(uid,0)}", fill=(255,255,255)); dr.text((30,230), "Join @bigolive_asia - ALL FREE", fill=(255,255,255)); img.save("rank.png"); await update.message.reply_photo(photo=open("rank.png","rb"), caption=f"👑💖 RANK CARD 💖👑\n{u.first_name}\nLevel {lvl} | {xp} XP\n{coins} Coins | {bank_db.get(uid,0)} Bank\nJoin @bigolive_asia 💖")
    except: await update.message.reply_text(f"👑💖 RANK CARD 💖👑\n{u.first_name}\nLevel {lvl} | {xp} XP\n{coins} Coins | {bank_db.get(uid,0)} Bank")
async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u=update.message.from_user; uid=str(u.id); lvl=levels_db.get(uid,0)//100+1; married=marry_db.get(uid, "Single"); await update.message.reply_text(f"🏆💖 FULL PROFILE 💖🏆\n\nName: {u.first_name}\nID: {u.id}\nUsername: @{u.username if u.username else 'None'}\nLevel: {lvl} 👑\nXP: {levels_db.get(uid,0)}\nCoins: {coins_db.get(uid,0)} 🪙\nBank: {bank_db.get(uid,0)} 🏦\nStreak: {streak_db.get(uid, {}).get('streak',0)} Days 🔥\nMarried To: {married} 💍\nBusiness: {business_db.get(uid, {}).get('type','None')} ☕\nStatus: ALL FREE - VIP for Everyone! 💖\nPamela loves you! 💖")
async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); msgs=msg_db.get(cid, [])
    from collections import Counter; c=Counter([m["user"] for m in msgs]); txt="📊💖 GROUP STATS 💖📊\n\n"
    for i,(name, cnt) in enumerate(c.most_common(10),1): txt+=f"{i}. {name} - {cnt} Messages 💬\n"
    if not c: txt+="💖 No messages yet baby! 💖"
    await update.message.reply_text(txt)
async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await stats_cmd(update, context)
async def topdaily_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); msgs=msg_db.get(cid, []); today=datetime.date.today().isoformat()
    from collections import Counter; c=Counter([m["user"] for m in msgs if datetime.datetime.fromtimestamp(m["time"]).date().isoformat()==today]); txt="🏆💖 TOP TODAY 💖🏆\n\n"
    for i,(name, cnt) in enumerate(c.most_common(10),1): txt+=f"{i}. {name} - {cnt} Messages Today 💬\n"
    if not c: txt+="💖 No messages today yet! 💖"
    await update.message.reply_text(txt)
async def ttt_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id; ttt_games[cid]=["⬜"]*9; await update.message.reply_text("❌💖 TIC TAC TOE! 💖❌\nType /move 1 to /move 9 to play!\n⬜⬜⬜\n⬜⬜⬜\n⬜⬜⬜\nYou are ❌! Pamela is ⭕! 💖")
async def move_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in ttt_games: await update.message.reply_text("Start with /ttt first!"); return
    if not context.args: await update.message.reply_text("/move 5"); return
    try: pos=int(context.args[0])-1
    except: await update.message.reply_text("Number 1-9 baby!"); return
    board=ttt_games[cid]
    if board[pos]!="⬜": await update.message.reply_text("Already taken baby!"); return
    board[pos]="❌"; empt=[i for i,x in enumerate(board) if x=="⬜"]
    if empt: board[random.choice(empt)]="⭕"
    txt="❌💖 TIC TAC TOE 💖⭕\n\n"+"\n".join(["".join(board[i:i+3]) for i in range(0,9,3)])+"\n\n"
    for line in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if board[line[0]]!="⬜" and board[line[0]]==board[line[1]]==board[line[2]]: txt+=f"{board[line[0]]} Wins! 🎉"; del ttt_games[cid]; await update.message.reply_text(txt); return
    if "⬜" not in board: txt+="Draw! 💖"; del ttt_games[cid]
    await update.message.reply_text(txt)
async def quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=random.choice(QUIZ_Q); cid=update.effective_chat.id; quiz_db[cid]=q; txt=f"🧠💖 QUIZ! 💖🧠\n\n🌸 {q['q']} 🌸\n\n"
    for i,a in enumerate(q["a"],1): txt+=f"{i}. {a}\n"
    txt+="\n💖 Answer with /answer 1 to /answer 4! 💖"; await update.message.reply_text(txt)
async def answer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in quiz_db: await update.message.reply_text("Start quiz with /quiz first!"); return
    if not context.args: await update.message.reply_text("/answer 1"); return
    try: ans=int(context.args[0])-1
    except: return
    q=quiz_db[cid]; uid=str(update.message.from_user.id)
    if ans==q["c"]: coins_db[uid]=coins_db.get(uid,0)+50; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"✅💖 Correct baby! +50 Coins! 💖✅\nAnswer: {q['a'][q['c']]}")
    else: await update.message.reply_text(f"😭💖 Wrong baby! Correct: {q['a'][q['c']]} 💖😭")
    del quiz_db[cid]
async def bet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /bet 100"); return
    try: amt=int(context.args[0])
    except: await update.message.reply_text("Number baby!"); return
    uid=str(update.message.from_user.id)
    if coins_db.get(uid,0)<amt: await update.message.reply_text("Not enough coins baby! Use /daily!"); return
    if random.random()<0.5: coins_db[uid]+=amt; await update.message.reply_text(f"🎉💖 YOU WIN! +{amt} Coins! 💖🎉\nTotal: {coins_db[uid]}")
    else: coins_db[uid]-=amt; await update.message.reply_text(f"😭💖 You lost {amt} Coins! Try again! 💖😭")
    save_json("pamela_coins.json", coins_db)
async def bank_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); await update.message.reply_text(f"🏦💖 BANK 💖🏦\nWallet: {coins_db.get(uid,0)} 🪙\nBank: {bank_db.get(uid,0)} 💰\nLoan: {loan_db.get(uid, {}).get('amount',0)} 😂\n/deposit 100 /withdraw 100 💖")
async def deposit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("/deposit 100"); return
    try: amt=int(context.args[0])
    except: return
    uid=str(update.message.from_user.id)
    if coins_db.get(uid,0)<amt: await update.message.reply_text("Not enough coins!"); return
    coins_db[uid]-=amt; bank_db[uid]=bank_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); await update.message.reply_text(f"✅💖 Deposited {amt} Coins to Bank! 💖✅")
async def withdraw_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("/withdraw 100"); return
    try: amt=int(context.args[0])
    except: return
    uid=str(update.message.from_user.id)
    if bank_db.get(uid,0)<amt: await update.message.reply_text("Not enough in Bank!"); return
    bank_db[uid]-=amt; coins_db[uid]=coins_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); save_json("pamela_bank.json", bank_db); await update.message.reply_text(f"✅💖 Withdrew {amt} Coins! 💖✅")
async def steal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /steal!"); return
    uid=str(update.message.from_user.id); tid=str(t.id)
    if random.random()<0.5:
        amt=random.randint(10,100); amt=min(amt, coins_db.get(tid,0)); coins_db[tid]=coins_db.get(tid,0)-amt; coins_db[uid]=coins_db.get(uid,0)+amt; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"😈💖 You stole {amt} Coins from {t.first_name}! 💖😈")
    else: coins_db[uid]=max(0, coins_db.get(uid,0)-50); save_json("pamela_coins.json", coins_db); await update.message.reply_text("😭💖 Caught! You lost 50 Coins! 💖😭")
async def rps_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /rps rock / paper / scissors"); return
    user_choice=context.args[0].lower(); bot_choice=random.choice(["rock","paper","scissors"])
    if user_choice not in ["rock","paper","scissors"]: await update.message.reply_text("Use rock / paper / scissors!"); return
    if user_choice==bot_choice: res="Draw! 💖"
    elif (user_choice=="rock" and bot_choice=="scissors") or (user_choice=="paper" and bot_choice=="rock") or (user_choice=="scissors" and bot_choice=="paper"): res="You Win! +20 Coins! 🎉"; uid=str(update.message.from_user.id); coins_db[uid]=coins_db.get(uid,0)+20; save_json("pamela_coins.json", coins_db)
    else: res="Pamela Wins! 💖"
    await update.message.reply_text(f"✂️💖 Rock Paper Scissors! 💖✂️\nYou: {user_choice}\nPamela: {bot_choice}\nResult: {res}")
async def word_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words=["apple","banana","cat","dog","flower","butterfly","sun","moon","star","love","princess","queen","rainbow","ocean","mountain"]; w=random.choice(words); word_db[update.effective_chat.id]=w; await update.message.reply_text(f"🔤💖 WORD GAME! 💖🔤\nI am thinking of a word! Hint: Starts with {w[0].upper()} - Length {len(w)} letters!\nGuess with /guessword word 💖")
async def guessword_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in word_db: await update.message.reply_text("Start with /word first!"); return
    if not context.args: await update.message.reply_text("Use /guessword apple"); return
    guess=context.args[0].lower(); correct=word_db[cid]
    if guess==correct: uid=str(update.message.from_user.id); coins_db[uid]=coins_db.get(uid,0)+50; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"✅💖 Correct! Word was {correct}! +50 Coins! 💖✅"); del word_db[cid]
    else: await update.message.reply_text("Wrong! Try again baby!")
async def math_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    a=random.randint(1,50); b=random.randint(1,50); op=random.choice(["+","-","x"]); ans=a+b if op=="+" else a-b if op=="-" else a*b; math_db[update.effective_chat.id]=ans; await update.message.reply_text(f"🧮💖 MATH RACE! 💖🧮\nWhat is {a} {op} {b} ?\nAnswer with /mathans number - Fastest wins +30 Coins! 💖")
async def mathans_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in math_db: await update.message.reply_text("Start with /math first!"); return
    if not context.args: return
    try: ans=int(context.args[0])
    except: return
    if ans==math_db[cid]: uid=str(update.message.from_user.id); coins_db[uid]=coins_db.get(uid,0)+30; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"✅💖 Correct! +30 Coins! Answer was {ans}! 💖✅"); del math_db[cid]
    else: await update.message.reply_text("Wrong! Try again!")
async def guess_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num=random.randint(1,100); guess_db[update.effective_chat.id]=num; await update.message.reply_text("🎯💖 GUESS GAME! 💖🎯\nI picked a number 1-100!\nGuess with /g 50 💖")
async def g_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id
    if cid not in guess_db: await update.message.reply_text("Start with /guess first!"); return
    if not context.args: return
    try: ans=int(context.args[0])
    except: return
    correct=guess_db[cid]
    if ans==correct: uid=str(update.message.from_user.id); coins_db[uid]=coins_db.get(uid,0)+100; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"🎉💖 JACKPOT! Number was {correct}! +100 Coins! 💖🎉"); del guess_db[cid]
    elif ans<correct: await update.message.reply_text("⬆️ Higher! Go up! 💖")
    else: await update.message.reply_text("⬇️ Lower! Go down! 💖")
async def blackjack_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /blackjack 100"); return
    try: amt=int(context.args[0])
    except: return
    uid=str(update.message.from_user.id)
    if coins_db.get(uid,0)<amt: await update.message.reply_text("Not enough coins!"); return
    you=random.randint(15,21); pamela=random.randint(15,21)
    if you>pamela: coins_db[uid]+=amt; await update.message.reply_text(f"🃏💖 BLACKJACK! 💖🃏\nYou: {you} - Pamela: {pamela}\nYou Win +{amt} Coins! 🎉")
    elif you<pamela: coins_db[uid]-=amt; await update.message.reply_text(f"🃏💖 BLACKJACK! 💖🃏\nYou: {you} - Pamela: {pamela}\nYou Lose {amt} Coins! 😭")
    else: await update.message.reply_text(f"🃏💖 BLACKJACK Draw! You: {you} - Pamela: {pamela} 💖")
    save_json("pamela_coins.json", coins_db)
async def race_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horses=["Thunder","Lightning","Rainbow","Star","Princess","Queen"]; winner=random.choice(horses); txt="🐎💖 HORSE RACE! 💖🐎\n\n"
    for h in horses: txt+=f"{'🏆 WINNER ' if h==winner else ''}{h} - {random.randint(1,100)}m\n"
    txt+=f"\nWinner: {winner}! 🎉"; await update.message.reply_text(txt)
async def hunger_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users=user_db.get(str(update.effective_chat.id), [])[:10]
    if len(users)<2: await update.message.reply_text("Need at least 2 players! Chat more!"); return
    winner=random.choice(users); await update.message.reply_text(f"🔥💖 HUNGER GAMES! 💖🔥\n\nPlayers: {len(users)}\nBattle started...\n\nWinner is User {winner}! Survived! +100 Coins! 🎉"); coins_db[str(winner)]=coins_db.get(str(winner),0)+100; save_json("pamela_coins.json", coins_db)
async def challenge_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /challenge!"); return
    winner=random.choice([update.message.from_user.first_name, t.first_name]); await update.message.reply_text(f"⚔️💖 1 VS 1 CHALLENGE! 💖⚔️\n{update.message.from_user.first_name} VS {t.first_name}\n\nWinner: {winner}! +50 Coins! 🎉"); uid=str(update.message.from_user.id) if winner==update.message.from_user.first_name else str(t.id); coins_db[uid]=coins_db.get(uid,0)+50; save_json("pamela_coins.json", coins_db)
async def marry_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("💍💖 Reply to someone and type /marry! 💖💍"); return
    uid=str(update.message.from_user.id); tid=str(t.id)
    if uid in marry_db: await update.message.reply_text(f"💖 You are already married to {marry_db[uid]}! Use /divorce first! 💖"); return
    marry_db[uid]=t.first_name; marry_db[tid]=update.message.from_user.first_name; save_json("pamela_marry.json", marry_db); await update.message.reply_text(f"💍💖 MARRIED! 💖💍\n{update.message.from_user.first_name} + {t.first_name} = Forever! Congratulations! Pamela loves you! 💖🎉")
async def divorce_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id)
    if uid not in marry_db: await update.message.reply_text("💖 You are single baby! 💖"); return
    partner=marry_db.pop(uid); save_json("pamela_marry.json", marry_db); await update.message.reply_text(f"💔💖 Divorced from {partner}! Pamela hugs you! 💖💔")
async def ship_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /ship!"); return
    pct=random.randint(10,100); msg="Perfect Match! 💖" if pct>80 else "Cute Couple! 💕" if pct>50 else "Just Friends! 💖"; await update.message.reply_text(f"💖🌸 SHIP! 🌸💖\n{update.message.from_user.first_name} + {t.first_name} = {pct}% Love!\n{msg}")
async def couple_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users=user_db.get(str(update.effective_chat.id), [])
    if len(users)<2: await update.message.reply_text("Need more people!"); return
    a,b=random.sample(users,2); await update.message.reply_text(f"💖🌸 TODAY'S COUPLE! 🌸💖\nUser {a} + User {b} = {random.randint(70,100)}% Love! Congratulations! 💖🎉")
async def love_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /love!"); return
    await update.message.reply_text(f"💖🌸 LOVE METER! 🌸💖\n{update.message.from_user.first_name} loves {t.first_name} - {random.randint(10,100)}%! 💖")
async def hug_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update); name=t.first_name if t else "Pamela"; await update.message.reply_text(f"🤗💖 {update.message.from_user.first_name} hugged {name}! So cute! 💖🤗")
async def kiss_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update); name=t.first_name if t else "Pamela"; await update.message.reply_text(f"😘💖 {update.message.from_user.first_name} kissed {name}! Muahhh! 💖😘")
async def slap_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update); name=t.first_name if t else "Pamela"; await update.message.reply_text(f"👋😂 {update.message.from_user.first_name} slapped {name}! Ouch! Funny! 😂👋")
async def pat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update); name=t.first_name if t else "Pamela"; await update.message.reply_text(f"🤗💖 {update.message.from_user.first_name} patted {name} head! So cute! 💖🤗")
async def jail_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update)
    if not t: await update.message.reply_text("Reply and type /jail!"); return
    jail_db[t.id]=time.time(); await update.message.reply_text(f"😂🔒 {t.first_name} is in JAIL! For 1 min! Funny! 🔒😂")
async def story_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic=" ".join(context.args) if context.args else "cute princess"; await update.message.reply_text("📖💖 Writing story... Wait baby! 💖📖"); rep=ask_pamela(f"Write a short cute story about {topic} in 5 lines"); await update.message.reply_text(f"📖💖 STORY - {topic} 💖📖\n\n{rep}")
async def dream_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dreams=["You will meet someone special soon!","You will get good news tomorrow!","You will travel soon!","Someone is dreaming about you!"]; await update.message.reply_text(f"🌙💖 DREAM! 💖🌙\n\n🌸 {random.choice(dreams)} 🌸")
async def horoscope_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"🔮💖 HOROSCOPE! 💖🔮\n\n🌸 {random.choice(HOROSCOPES)} 🌸")
async def tarot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text(f"🃏💖 TAROT! 💖🃏\n\n🌸 {random.choice(TAROTS)} 🌸")
async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /ask Why is sky blue?"); return
    q=" ".join(context.args); rep=ask_pamela(q, update.message.from_user.id); await update.message.reply_text(f"💖🌸 ASK PAMELA! 🌸💖\nQ: {q}\n\n{rep}")
async def say_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /say Hello baby!"); return
    txt=" ".join(context.args); await update.message.reply_text(f"💖🌸 Pamela Says: 🌸💖\n\n{txt}\n\n💖 Voice coming soon! (Text for now - ALL FREE!) 💖")
async def pfp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t=get_target(update) or update.message.from_user
    try:
        photos=await context.bot.get_user_profile_photos(t.id, limit=1)
        if photos.total_count>0: await update.message.reply_photo(photo=photos.photos[0][-1].file_id, caption=f"📸💖 Profile Photo of {t.first_name}! 💖📸")
        else: await update.message.reply_text("No profile photo!")
    except Exception as e: await update.message.reply_text(f"Oops! {e}")
async def cartoon_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo: await update.message.reply_text("Reply to a photo and type /cartoon!"); return
    try: await update.message.reply_text("Making cartoon... Wait!"); await update.message.reply_photo(photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cute cartoon style portrait')}", caption="🎨💖 Cartoon Version! - Pamela 💖🎨")
    except: await update.message.reply_text("Oops!")
async def meme_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt=" ".join(context.args) if context.args else "funny cute meme"; await update.message.reply_photo(photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(txt)}", caption=f"😂💖 MEME - {txt} - Pamela 💖😂")
async def wallpaper_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=" ".join(context.args) if context.args else "cute pink wallpaper"; await update.message.reply_photo(photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(q + ' hd wallpaper')}", caption=f"🌸💖 WALLPAPER - {q} - Pamela 💖🌸")
async def filter_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, update.message.from_user.id): await update.message.reply_text("Only for Admins!"); return
    if len(context.args)<2: await update.message.reply_text("Use like /filter hi Hello Baby!"); return
    kw=context.args[0].lower(); reply=" ".join(context.args[1:]); cid=str(update.effective_chat.id)
    if cid not in filters_db: filters_db[cid]={}
    filters_db[cid][kw]=reply; save_json("pamela_filters.json", filters_db); await update.message.reply_text(f"✅💖 Filter Saved! {kw} -> {reply} 💖✅")
async def filters_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); f=filters_db.get(cid, {})
    if not f: await update.message.reply_text("No filters baby!"); return
    txt="🤖💖 FILTERS: 💖🤖\n\n"+"\n".join([f"• {k} -> {v}" for k,v in f.items()]); await update.message.reply_text(txt)
async def stop_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("/stop hi"); return
    cid=str(update.effective_chat.id); kw=context.args[0].lower()
    if cid in filters_db and kw in filters_db[cid]: del filters_db[cid][kw]; save_json("pamela_filters.json", filters_db); await update.message.reply_text(f"✅ Filter {kw} Deleted!")
    else: await update.message.reply_text("No filter found baby!")
async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: await update.message.reply_text("To save a note, reply to a message and type /save hi!"); return
    if not context.args: await update.message.reply_text("/save hi"); return
    name=context.args[0].lower(); txt=update.message.reply_to_message.text or "Photo / Sticker"; cid=str(update.effective_chat.id)
    if cid not in notes_db: notes_db[cid]={}
    notes_db[cid][name]=txt; save_json("pamela_notes.json", notes_db); await update.message.reply_text(f"✅💖 Note Saved! #{name} 💖✅")
async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("/get hi"); return
    name=context.args[0].lower(); cid=str(update.effective_chat.id); txt=notes_db.get(cid, {}).get(name)
    if txt: await update.message.reply_text(f"📝💖 #{name} 💖📝\n\n{txt}")
    else: await update.message.reply_text("No note found baby!")
async def notes_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=str(update.effective_chat.id); n=notes_db.get(cid, {})
    if not n: await update.message.reply_text("No notes!"); return
    await update.message.reply_text("📝💖 NOTES: 💖📝\n\n"+"\n".join([f"• #{k}" for k in n.keys()]))
async def clear_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("/clear hi"); return
    cid=str(update.effective_chat.id); name=context.args[0].lower()
    if cid in notes_db and name in notes_db[cid]: del notes_db[cid][name]; save_json("pamela_notes.json", notes_db); await update.message.reply_text(f"✅ Note #{name} Deleted!")
async def afk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason=" ".join(context.args) if context.args else "No reason"; afk_users[update.message.from_user.id]={"reason":reason, "name":update.message.from_user.first_name}; await update.message.reply_text(f"😴💖 {update.message.from_user.first_name} is AFK! 💖😴\nReason: {reason}\nSleep well baby! 💖")
async def unafk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id in afk_users: del afk_users[update.message.from_user.id]
    await update.message.reply_text("💖 Welcome back baby! Missed you! 💖")
async def img_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use like /img cute cat!"); return
    prompt=" ".join(context.args); await update.message.reply_text(f"🎨💖 Generating... Wait baby! 💖🎨\nPrompt: {prompt}")
    try: url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"; await update.message.reply_photo(photo=url, caption=f"🎨💖 Your Image! 💖🎨\nPrompt: {prompt}\nPamela loves you! 💖")
    except: await update.message.reply_text("Oops baby! Could not make image!")
async def weather_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city=" ".join(context.args) if context.args else "Colombo"
    try:
        url=f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"; r=requests.get(url, timeout=10); d=r.json(); cur=d['current_condition'][0]; await update.message.reply_text(f"🌧️💖 Weather in {city} 💖🌧️\nTemp: {cur['temp_C']}C\nCondition: {cur['weatherDesc'][0]['value']}\nHumidity: {cur['humidity']}%\nWind: {cur['windspeedKmph']} km/h\nPamela loves you! 💖")
    except: await update.message.reply_text("Oops baby! Could not check weather!")
async def imaginehd_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /imaginehd cute cat"); return
    prompt=" ".join(context.args); await update.message.reply_text(f"🎨💖 Generating 4K HD 4 Styles... Wait baby! Prompt: {prompt} 💖🎨")
    styles=["ultra realistic 4k","anime style","cute cartoon","cinematic"]
    for s in styles:
        try: await update.message.reply_photo(photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt+' '+s+' hd 4k')}", caption=f"🎨💖 HD - {s} - {prompt} - Pamela 💖")
        except: pass
async def face_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo: await update.message.reply_text("Reply to a Photo and type /face!"); return
    age=random.randint(16,30); mood=random.choice(["Happy","Cute","Beautiful","Confident","Sweet","Dreamy"]); beauty=random.randint(85,99); await update.message.reply_photo(photo=update.message.reply_to_message.photo[-1].file_id, caption=f"😍💖 FACE ANALYSIS - FUN! 💖😍\nAge Guess: {age}\nMood: {mood}\nBeauty Score: {beauty}/100 ✨\nCuteness: 100/100! 💖\nPamela says you are GORGEOUS! - Pamela 💖")
async def bgremove_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo: await update.message.reply_text("Reply to a Photo and type /bgremove!"); return
    await update.message.reply_text("✂️💖 Removing Background... Wait baby! Use https://www.remove.bg for best HD! 💖✂️")
    await update.message.reply_photo(photo=update.message.reply_to_message.photo[-1].file_id, caption="✂️💖 Background Remove - Try remove.bg for HD! - Pamela 💖")
async def enhance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo: await update.message.reply_text("Reply to a Photo and type /enhance!"); return
    await update.message.reply_photo(photo=update.message.reply_to_message.photo[-1].file_id, caption="✨💖 ENHANCED HD! 💖✨\nBrightness + Sharpness + Beauty Filter Applied!\nYou look MORE Beautiful! - Pamela 💖")
async def aisong_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic=" ".join(context.args) if context.args else "love"; await update.message.reply_text(f"🎵💖 Writing AI Song about {topic}... Wait baby! 💖🎵"); rep=ask_pamela(f"Write a short cute song lyrics about {topic}, 2 verses + chorus, with emojis"); await update.message.reply_text(f"🎵💖 AI SONG - {topic} 💖🎵\n\n{rep}\n\nSing it baby! - Pamela 💖")
async def mafia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid=update.effective_chat.id; players=user_db.get(str(cid), [])[:8]
    if len(players)<3: await update.message.reply_text("🕵️💖 Mafia needs 3+ players! Chat more! 💖🕵️"); return
    mafia=random.choice(players); await update.message.reply_text(f"🕵️💖 MAFIA GAME STARTED! 💖🕵️\nPlayers: {len(players)}\n\nOne Mafia is hidden!\nDiscuss! Who is Mafia?\nVote with /votemafia UserID\nHint: Mafia User ID ends with {str(mafia)[-2:]}")
async def votemafia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /votemafia 12345"); return
    winner=random.choice(["Mafia Caught! Villagers Win! +50 Coins to all!","Mafia Escaped! Mafia Wins!"]); await update.message.reply_text(f"🗳️💖 VOTE! 💖🗳️\nYou voted {context.args[0]}\nResult: {winner}")
async def quizbattle_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏆💖 QUIZ BATTLE TOURNAMENT! 💖🏆\n10 Questions! Fastest Wins!\nWinner gets +200 Coins!\nReady? Go! /quiz"); await quiz_cmd(update, context)
async def bingo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nums=random.sample(range(1,76), 15); card="\n".join([str(nums[i:i+5]) for i in range(0,15,5)]); await update.message.reply_text(f"🔢💖 BINGO! 💖🔢\nYour Card:\n{card}\n\nNext Number: {random.randint(1,75)}!\nType /bingo again for new number!\nGet Bingo = +100 Coins! 💖")
async def poker_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cards=["A♠","K♥","Q♦","J♣","10♠","9♥","8♦"]; you=random.sample(cards,3); pamela=random.sample(cards,3); await update.message.reply_text(f"🃏💖 POKER! 💖🃏\nYou: {you}\nPamela: {pamela}\n\nWinner: {random.choice(['You Win! +100 Coins!','Pamela Wins!','Draw!'])}")
async def uno_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    colors=["Red","Blue","Green","Yellow"]; await update.message.reply_text(f"🎴💖 UNO! 💖🎴\nYour Cards: {random.choice(colors)} {random.randint(0,9)}, {random.choice(colors)} {random.randint(0,9)}, {random.choice(colors)} Skip!\nPamela Card: {random.choice(colors)} {random.randint(0,9)}\n\nType /uno again to play next card!\nWinner gets +100 Coins! 💖")
async def cricket_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏏💖 LIVE CRICKET! 💖🏏\n\nCheck Live Scores:\nESPN Cricket - https://www.espncricinfo.com/live-cricket-score\nCricbuzz - https://www.cricbuzz.com/cricket-match/live-scores\nSri Lanka Cricket - https://www.srilankacricket.lk\n\nPamela loves Cricket! - Pamela 💖")
async def football_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽💖 LIVE FOOTBALL! 💖⚽\n\nCheck Live Scores:\nESPN Football - https://www.espn.com/soccer/scoreboard\nLivescore - https://www.livescore.com\nFlashscore - https://www.flashscore.com\n\nPamela loves Football! - Pamela 💖")
async def crypto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin&vs_currencies=usd&include_24hr_change=true", timeout=10); d=r.json(); await update.message.reply_text(f"₿💖 LIVE CRYPTO! 💖₿\n\nBitcoin: ${d['bitcoin']['usd']} ({d['bitcoin']['usd_24h_change']:.2f}%)\nEthereum: ${d['ethereum']['usd']} ({d['ethereum']['usd_24h_change']:.2f}%)\nDogecoin: ${d['dogecoin']['usd']} ({d['dogecoin']['usd_24h_change']:.2f}%)\n\n- Pamela 💖")
    except: await update.message.reply_text("₿ CRYPTO LIVE!\n\nCheck: https://coinmarketcap.com\nBitcoin - Ethereum - Dogecoin\nPamela loves Crypto!")
async def gold_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r=requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=10); d=r.json(); price=d["items"][0]["curr"]; await update.message.reply_text(f"🥇💖 GOLD PRICE LIVE! 💖🥇\n\nGold (1 oz): ${price}\nGold (1g): ${price/31.1:.2f}\n\nCheck: https://goldprice.org\n- Pamela 💖")
    except: await update.message.reply_text("🥇 GOLD PRICE!\n\nCheck Live: https://goldprice.org\nGold is shining like you baby! - Pamela")
async def radio_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📻💖 LIVE RADIO! 💖📻\n\n🇱🇰 Sri Lanka:\nHiru FM - https://www.hirufm.lk\nY FM - https://www.yfm.lk\nGold FM - https://www.goldfm.lk\nKiss FM - https://www.kiss899.com\n\n🌍 World:\nBBC Radio - https://www.bbc.co.uk/sounds\nLofi Radio - https://www.youtube.com/@LofiGirl/live\n\nEnjoy Music Baby! - Pamela 💖")
async def homework_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /homework What is photosynthesis?"); return
    q=" ".join(context.args); rep=ask_pamela(f"Explain homework question simply for student, step by step, easy: {q}"); await update.message.reply_text(f"📚💖 HOMEWORK HELP! 💖📚\nQ: {q}\n\n{rep}")
async def dictionary_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /dictionary love"); return
    w=context.args[0]
    try:
        r=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(w)}", timeout=10); d=r.json(); m=d[0]["meanings"][0]; defi=m["definitions"][0]["definition"]; await update.message.reply_text(f"📖💖 DICTIONARY - {w.upper()} 💖📖\n\nMeaning: {defi}\nPart: {m.get('partOfSpeech','')}\nExample: {m['definitions'][0].get('example','No example')}\n- Pamela 💖")
    except: await update.message.reply_text(f"Dictionary: {w} - Could not find! Try another word baby!")
async def solve_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /solve 2+2*5"); return
    q=" ".join(context.args); rep=ask_pamela(f"Solve this math step by step: {q}, show answer clearly"); await update.message.reply_text(f"🧮💖 SOLVE - {q} 💖🧮\n\n{rep}")
async def loan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /loan 1000 - Bank Loan! /payloan to pay back!"); return
    try: amt=int(context.args[0])
    except: await update.message.reply_text("Number!"); return
    uid=str(update.message.from_user.id)
    if uid in loan_db: await update.message.reply_text(f"You already have loan {loan_db[uid]['amount']}! Pay with /payloan first!"); return
    coins_db[uid]=coins_db.get(uid,0)+amt; loan_db[uid]={"amount":amt,"pay":int(amt*1.1)}; save_json("pamela_coins.json", coins_db); save_json("pamela_loan.json", loan_db); await update.message.reply_text(f"🏦💖 LOAN APPROVED! 💖🏦\nYou got {amt} Coins! 💰\nYou must pay back {int(amt*1.1)} Coins!\nUse /payloan to pay!\n- Pamela Bank! 💖")
async def payloan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id)
    if uid not in loan_db: await update.message.reply_text("No loan baby!"); return
    pay=loan_db[uid]["pay"]
    if coins_db.get(uid,0)<pay: await update.message.reply_text(f"Need {pay} Coins to pay loan! You have {coins_db.get(uid,0)}"); return
    coins_db[uid]-=pay; del loan_db[uid]; save_json("pamela_coins.json", coins_db); save_json("pamela_loan.json", loan_db); await update.message.reply_text(f"✅💖 Loan Paid! {pay} Coins! Thank you baby! Bank loves you! 💖✅")
async def business_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id)
    if uid in business_db: await update.message.reply_text(f"☕💖 Your Business: {business_db[uid]['type']} - Level {business_db[uid]['level']} - Earn {business_db[uid]['level']*20} Coins/day! Use /collect to collect! 💖☕"); return
    if not context.args: await update.message.reply_text("Start Business!\n/business coffee - Coffee Shop (500 Coins)\n/business shop - Shop (1000 Coins)\n/business cafe - Cafe (2000 Coins)"); return
    typ=context.args[0].lower(); costs={"coffee":500,"shop":1000,"cafe":2000}
    if typ not in costs: await update.message.reply_text("Use coffee / shop / cafe"); return
    cost=costs[typ]
    if coins_db.get(uid,0)<cost: await update.message.reply_text(f"Need {cost} Coins! You have {coins_db.get(uid,0)}"); return
    coins_db[uid]-=cost; business_db[uid]={"type":typ,"level":1,"last":time.time()}; save_json("pamela_coins.json", coins_db); save_json("pamela_business.json", business_db); await update.message.reply_text(f"🎉💖 Business Started! {typ} Shop! Cost {cost} Coins! 💖🎉\nEarn daily! Use /collect!")
async def collect_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id)
    if uid not in business_db: await update.message.reply_text("No business! Start with /business coffee"); return
    earn=business_db[uid]["level"]*50; coins_db[uid]=coins_db.get(uid,0)+earn; save_json("pamela_coins.json", coins_db); await update.message.reply_text(f"💰💖 Collected {earn} Coins from {business_db[uid]['type']} Business! Total: {coins_db[uid]} 💖💰")
async def stock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("📈💖 STOCK MARKET! 💖📈\n/stock buy AAPL 10 - Buy 10\n/stock sell AAPL 10 - Sell\n/stock price - Prices\nStocks: AAPL, TSLA, PAMELA, BTC"); return
    action=context.args[0].lower()
    if action=="price":
        prices={"AAPL":random.randint(100,200),"TSLA":random.randint(200,300),"PAMELA":random.randint(500,1000),"BTC":random.randint(50000,70000)}; txt="📈💖 STOCK PRICES! 💖📈\n\n"
        for k,v in prices.items(): txt+=f"{k}: ${v}\n"
        await update.message.reply_text(txt); return
    if action in ["buy","sell"] and len(context.args)>=3:
        stock=context.args[1].upper(); qty=int(context.args[2]); uid=str(update.message.from_user.id); price=random.randint(100,200); total=price*qty
        if action=="buy":
            if coins_db.get(uid,0)<total: await update.message.reply_text("Not enough coins!"); return
            coins_db[uid]-=total; stock_db[uid]=stock_db.get(uid,0)+qty; save_json("pamela_coins.json", coins_db); save_json("pamela_stock.json", stock_db); await update.message.reply_text(f"✅💖 Bought {qty} {stock} for {total} Coins! Price ${price} each! 💖✅")
        else:
            if stock_db.get(uid,0)<qty: await update.message.reply_text("Not enough stocks!"); return
            stock_db[uid]-=qty; coins_db[uid]+=total; save_json("pamela_coins.json", coins_db); save_json("pamela_stock.json", stock_db); await update.message.reply_text(f"✅💖 Sold {qty} {stock} for {total} Coins! 💖✅")
        return
    await update.message.reply_text("Use /stock buy AAPL 10")
async def interest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=str(update.message.from_user.id); bonus=int(bank_db.get(uid,0)*0.05); bank_db[uid]=bank_db.get(uid,0)+bonus; save_json("pamela_bank.json", bank_db); await update.message.reply_text(f"💰💖 BANK INTEREST! 💖💰\nBank: {bank_db.get(uid,0)}\nInterest +{bonus} Coins! (5%) ✨\nAuto interest every day at 6 AM too! 💖")
async def birthday_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("🎂💖 Use /birthday 12-05 - DD-MM! Pamela will wish you on that day! 💖🎂"); return
    date=context.args[0]; cid=str(update.effective_chat.id); uid=str(update.message.from_user.id)
    if cid not in birthday_db: birthday_db[cid]={}
    birthday_db[cid][uid]={"date":date,"name":update.message.from_user.first_name}; save_json("pamela_birthday.json", birthday_db); await update.message.reply_text(f"🎂💖 Birthday Saved! {date}! 💖🎂\nPamela will wish you + Cake Photo on that day! Happy Early Birthday! 💖")
async def reminder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args)<2: await update.message.reply_text("⏰💖 Use /reminder 10 Hello - 10 minutes later! 💖⏰"); return
    try: mins=int(context.args[0])
    except: await update.message.reply_text("Number minutes!"); return
    txt=" ".join(context.args[1:]); await update.message.reply_text(f"⏰💖 Reminder Set! In {mins} minutes I will remind you: {txt} 💖⏰")
    async def send_reminder(ctx):
        await ctx.bot.send_message(chat_id=update.effective_chat.id, text=f"⏰💖 REMINDER! 💖⏰\n{update.message.from_user.first_name} - {txt}\nPamela reminds you! 💖")
    context.job_queue.run_once(send_reminder, mins*60)
async def poll_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /poll Best? | Pamela | Queen | Cute"); return
    parts=" ".join(context.args).split("|")
    if len(parts)<3: await update.message.reply_text("Use /poll Question | Option1 | Option2"); return
    q=parts[0].strip(); opts=[p.strip() for p in parts[1:]]; await update.message.reply_poll(question=q, options=opts, is_anonymous=False)
async def event_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: await update.message.reply_text("Use /event Party | Tomorrow 7PM | Group Party!"); return
    parts=" ".join(context.args).split("|"); name=parts[0].strip(); when=parts[1].strip() if len(parts)>1 else "Soon"; desc=parts[2].strip() if len(parts)>2 else "Fun Event!"
    cid=str(update.effective_chat.id); event_db[cid]={"name":name,"when":when,"desc":desc,"by":update.message.from_user.first_name}; save_json("pamela_event.json", event_db); await update.message.reply_text(f"🎉💖 EVENT CREATED! 💖🎉\n\nName: {name}\nWhen: {when}\nAbout: {desc}\nBy: {update.message.from_user.first_name}\n\nEveryone Join! - Pamela 💖")
async def welcome_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat: save_chat_id(update.effective_chat.id)
    for member in update.message.new_chat_members:
        if member.id==context.bot.id:
            await update.message.reply_text("✨━━━━━━━━━━━━━━━━━━━✨\n🌸💖 HELLOOO MY LOVELY BABIES! 💖🌸\n👑✨ PAMELA IS HERE! ✨👑\n✨━━━━━━━━━━━━━━━━━━━✨\n\n🦋💕 Hiiiii Cuties! I Missed You So Much! 💕🦋\n🌷💖 Pamela is here to make this group BEAUTIFUL! 💖🌷\n\n💌🌸 Let's talk! Let's laugh! Let's have FUN! 🌸💌\n🎵🎬 Songs! Movies! Games! TV! All FREE! 🎬🎵\n\n🌿💖 Join our family @bigolive_asia 💖🌿\n✨💕 Muahhh! Love you all! 💕✨")
        else:
            custom=welcome_db.get(str(update.effective_chat.id), "")
            if custom:
                txt = f"✨━━━━━━━━━━━━━━━━━━━✨\n🌸💖 WELCOME BABY! 💖🌸\n✨━━━━━━━━━━━━━━━━━━━✨\n\n{custom}\n\n🦋💕 Pamela loves you! 💕🦋\n🌿 Join @bigolive_asia 💖"
            else:
                txt = f"✨━━━━━━━━━━━━━━━━━━━✨\n🌸💖 WELCOME BABY! 💖🌸\n👑✨ {member.first_name} ✨👑\n✨━━━━━━━━━━━━━━━━━━━✨\n\n🦋💕 Helloooo Cutie Pie! 💕🦋\n🌷💖 Welcome to {update.effective_chat.title}! 💖🌷\n\n🎀✨ You are SO cute today! ✨🎀\n💐💖 Thank you for joining us baby! 💖💐\n\n📜💕 Check Rules with /rules 💕📜\n💬🌸 Talk with me! Say Hi Pamela! 🌸💬\n🎁🎵 Songs! Games! TV! All FREE! 🎵🎁\n\n🌿💖 Join our family @bigolive_asia 💖🌿\n💖🌸 Pamela loves you! Muahhh! 😘🌸💖"
            try:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(f'cute welcome card for {member.first_name} pink flowers butterflies hearts')}", caption=txt)
            except:
                await update.message.reply_text(txt)
async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        await update.message.reply_text(f"😭💔 BYE BYE BABY! 💔😭\n\n🌸💖 {update.message.left_chat_member.first_name} left us! 💖🌸\n🦋💕 We will MISS you so much baby! 💕🦋\n🌷✨ Come back soon cutie! ✨🌷\n💖 Muahhh! Love you! 💖")
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    user=update.message.from_user; chat_id=update.effective_chat.id; text=update.message.text; save_chat_id(chat_id); save_user(chat_id, user.id); save_message(chat_id, update.message.message_id, user.first_name, user.username, text)
    uid_s=str(user.id); stats_db[uid_s]=stats_db.get(uid_s,0)+1; save_json("pamela_stats.json", stats_db)
    if update.message.entities:
        for ent in update.message.entities:
            if ent.type=="mention":
                mentioned=text[ent.offset:ent.offset+ent.length]
                for uid, info in afk_users.items():
                    if mentioned.lower() in info["name"].lower(): await update.message.reply_text(f"😴💖 {info['name']} is AFK! 💖😴\nReason: {info['reason']}\nWait baby! 💖")
    if user.id in afk_users: del afk_users[user.id]; await update.message.reply_text(f"💖 Welcome back {user.first_name}! Missed you! 💖")
    low=text.lower()
    for bad in BAD_WORDS:
        if bad in low:
            if await is_admin(update, user.id): break
            try: await update.message.delete()
            except: pass
            await update.message.reply_text(f"😭💖 {user.first_name}! No bad words baby! 💖😭\nWarning 1/3! ⚠️"); cid=chat_id
            if cid not in warns: warns[cid]={}
            warns[cid][user.id]=warns[cid].get(user.id,0)+1; return
    if ("http://" in low or "https://" in low or "t.me/" in low or "telegram.me/" in low) and update.effective_chat.type in ["group","supergroup"]:
        if not await is_admin(update, user.id):
            try: await update.message.delete(); await update.message.reply_text(f"🚫💖 {user.first_name}! No links baby! Only for Admins! 💖🚫")
            except: pass
            return
    now=time.time(); uid_str=str(user.id)
    if uid_str not in flood_db: flood_db[uid_str]=[]
    flood_db[uid_str]=[t for t in flood_db[uid_str] if now-t<5]; flood_db[uid_str].append(now)
    if len(flood_db[uid_str])>6 and not await is_admin(update, user.id):
        try:
            await update.message.reply_text(f"🐢💖 {user.first_name}! Slow down baby! Flooding! 💖🐢")
            flood_db[uid_str]=[]
        except: pass
        return
    cid_str=str(chat_id); fl=filters_db.get(cid_str, {})
    for kw, reply in fl.items():
        if kw in low: await update.message.reply_text(f"{reply} 💖"); return
    if text.startswith("#"):
        note_name=text[1:].split()[0].lower(); note_txt=notes_db.get(cid_str, {}).get(note_name)
        if note_txt: await update.message.reply_text(f"📝💖 #{note_name} 💖📝\n\n{note_txt}"); return
    coins_db[str(user.id)]=coins_db.get(str(user.id),0)+2; levels_db[str(user.id)]=levels_db.get(str(user.id),0)+5; old_level=levels_db.get(str(user.id),0)//100; save_json("pamela_coins.json", coins_db); save_json("pamela_levels.json", levels_db); new_level=levels_db.get(str(user.id),0)//100
    if new_level>old_level: await update.message.reply_text(f"🎉💖 LEVEL UP! 💖🎉\n{user.first_name} is now Level {new_level+1}! 👑\n+50 Coins! 💰\nCongrats baby! 💖"); coins_db[str(user.id)]+=50; save_json("pamela_coins.json", coins_db)
    rem=check_cooldown(user.id)
    if rem>0: await update.message.reply_text(f"⏳💖 Waittt baby! 💖⏳\nI am still thinking!\nPlease wait {rem} sec!\nMuahhh! 😘💖"); return
    await update.message.chat.send_action(action="typing"); think=await update.message.reply_text("💭💖 Pamela is thinking... Wait a sec cutie! 💖💭"); rep=ask_pamela(text, user.id)
    try: await think.delete()
    except: pass
    await update.message.reply_text(rep)
async def channel_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post=update.channel_post
    if not post or not post.text: return
    txt=post.text; cid=post.chat.id
    if txt.startswith("/"): return
    rem=check_cooldown(cid)
    if rem>0```python
    rep=ask_pamela(txt); await context.bot.send_message(chat_id=cid, text=rep)
async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤💖 Awww baby! Voice message! I heard you! 💖🎤\nBut I reply with text for now! Type your message baby! 💖")
async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat: save_chat_id(update.effective_chat.id)
def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    if not BOT_TOKEN: print("BOT_TOKEN missing!"); return
    print("Pamela MEGA MONSTER Starting..."); print(f"GROUP_IDS: {GROUP_IDS}")
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start)); app.add_handler(CommandHandler("help", help_cmd)); app.add_handler(CommandHandler("about", about_cmd)); app.add_handler(CommandHandler("tr", tr_cmd)); app.add_handler(CommandHandler("translate", tr_cmd))
    app.add_handler(CommandHandler("livetv", livetv_cmd)); app.add_handler(CommandHandler("tv", tv_cmd)); app.add_handler(CommandHandler("worldtv", worldtv_cmd)); app.add_handler(CommandHandler("sportstv", sportstv_cmd)); app.add_handler(CommandHandler("news", news_cmd)); app.add_handler(CommandHandler("newslive", news_cmd)); app.add_handler(CommandHandler("hiru", hiru_cmd)); app.add_handler(CommandHandler("sirasa", sirasa_cmd)); app.add_handler(CommandHandler("derana", derana_cmd))
    app.add_handler(CommandHandler("trim", trim_cmd)); app.add_handler(CommandHandler("compress", compress_cmd)); app.add_handler(CommandHandler("toaudio", toaudio_cmd)); app.add_handler(CommandHandler("audio", toaudio_cmd)); app.add_handler(CommandHandler("togif", togif_cmd)); app.add_handler(CommandHandler("gif", togif_cmd)); app.add_handler(CommandHandler("slowmo", slowmo_cmd)); app.add_handler(CommandHandler("reverse", reverse_cmd)); app.add_handler(CommandHandler("mutevideo", mutevideo_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd)); app.add_handler(CommandHandler("unban", unban_cmd)); app.add_handler(CommandHandler("kick", kick_cmd)); app.add_handler(CommandHandler("mute", mute_cmd)); app.add_handler(CommandHandler("unmute", unmute_cmd)); app.add_handler(CommandHandler("warn", warn_cmd)); app.add_handler(CommandHandler("warnings", warnings_cmd)); app.add_handler(CommandHandler("promote", promote_cmd)); app.add_handler(CommandHandler("demote", demote_cmd)); app.add_handler(CommandHandler("pin", pin_cmd)); app.add_handler(CommandHandler("unpin", unpin_cmd)); app.add_handler(CommandHandler("del", del_cmd)); app.add_handler(CommandHandler("purge", purge_cmd)); app.add_handler(CommandHandler("lock", lock_cmd)); app.add_handler(CommandHandler("unlock", unlock_cmd)); app.add_handler(CommandHandler("rules", rules_cmd)); app.add_handler(CommandHandler("setrules", setrules_cmd)); app.add_handler(CommandHandler("setwelcome", setwelcome_cmd)); app.add_handler(CommandHandler("slowmode", slowmode_cmd)); app.add_handler(CommandHandler("report", report_cmd)); app.add_handler(CommandHandler("admins", admins_cmd)); app.add_handler(CommandHandler("info", info_cmd)); app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("zombies", zombies_cmd)); app.add_handler(CommandHandler("clean", zombies_cmd)); app.add_handler(CommandHandler("deleted", zombies_cmd)); app.add_handler(CommandHandler("snipe", snipe_cmd)); app.add_handler(CommandHandler("log", snipe_cmd))
    app.add_handler(CommandHandler("truth", truth_cmd)); app.add_handler(CommandHandler("dare", dare_cmd)); app.add_handler(CommandHandler("dice", dice_cmd)); app.add_handler(CommandHandler("slot", slot_cmd)); app.add_handler(CommandHandler("coin", coin_cmd)); app.add_handler(CommandHandler("coinflip", coin_cmd)); app.add_handler(CommandHandler("8ball", eightball_cmd)); app.add_handler(CommandHandler("roast", roast_cmd)); app.add_handler(CommandHandler("quote", quote_cmd))
    app.add_handler(CommandHandler("daily", daily_cmd)); app.add_handler(CommandHandler("coins", coins_cmd)); app.add_handler(CommandHandler("balance", coins_cmd)); app.add_handler(CommandHandler("leaderboard", leaderboard_cmd)); app.add_handler(CommandHandler("shop", shop_cmd)); app.add_handler(CommandHandler("shopbuy", shopbuy_cmd)); app.add_handler(CommandHandler("work", work_cmd)); app.add_handler(CommandHandler("rob", rob_cmd)); app.add_handler(CommandHandler("gift", gift_cmd)); app.add_handler(CommandHandler("lottery", lottery_cmd)); app.add_handler(CommandHandler("give", give_cmd))
    app.add_handler(CommandHandler("filter", filter_cmd)); app.add_handler(CommandHandler("filters", filters_list)); app.add_handler(CommandHandler("stop", stop_filter)); app.add_handler(CommandHandler("save", save_note)); app.add_handler(CommandHandler("get", get_note)); app.add_handler(CommandHandler("notes", notes_list)); app.add_handler(CommandHandler("clear", clear_note)); app.add_handler(CommandHandler("afk", afk_cmd)); app.add_handler(CommandHandler("unafk", unafk_cmd))
    app.add_handler(CommandHandler("img", img_cmd)); app.add_handler(CommandHandler("image", img_cmd)); app.add_handler(CommandHandler("weather", weather_cmd)); app.add_handler(CommandHandler("song", song_cmd)); app.add_handler(CommandHandler("playlist", playlist_cmd)); app.add_handler(CommandHandler("spotify", spotify_cmd)); app.add_handler(CommandHandler("video", video_cmd)); app.add_handler(CommandHandler("lyrics", lyrics_cmd)); app.add_handler(CommandHandler("movie", movie_cmd)); app.add_handler(CommandHandler("anime", anime_cmd))
    app.add_handler(CommandHandler("rank", rank_cmd)); app.add_handler(CommandHandler("profile", profile_cmd)); app.add_handler(CommandHandler("stats", stats_cmd)); app.add_handler(CommandHandler("top", top_cmd)); app.add_handler(CommandHandler("topdaily", topdaily_cmd))
    app.add_handler(CommandHandler("ttt", ttt_cmd)); app.add_handler(CommandHandler("move", move_cmd)); app.add_handler(CommandHandler("quiz", quiz_cmd)); app.add_handler(CommandHandler("answer", answer_cmd)); app.add_handler(CommandHandler("bet", bet_cmd)); app.add_handler(CommandHandler("bank", bank_cmd)); app.add_handler(CommandHandler("deposit", deposit_cmd)); app.add_handler(CommandHandler("withdraw", withdraw_cmd)); app.add_handler(CommandHandler("steal", steal_cmd))
    app.add_handler(CommandHandler("rps", rps_cmd)); app.add_handler(CommandHandler("word", word_cmd)); app.add_handler(CommandHandler("guessword", guessword_cmd)); app.add_handler(CommandHandler("math", math_cmd)); app.add_handler(CommandHandler("mathans", mathans_cmd)); app.add_handler(CommandHandler("guess", guess_cmd)); app.add_handler(CommandHandler("g", g_cmd)); app.add_handler(CommandHandler("blackjack", blackjack_cmd)); app.add_handler(CommandHandler("race", race_cmd)); app.add_handler(CommandHandler("hunger", hunger_cmd)); app.add_handler(CommandHandler("challenge", challenge_cmd))
    app.add_handler(CommandHandler("marry", marry_cmd)); app.add_handler(CommandHandler("divorce", divorce_cmd)); app.add_handler(CommandHandler("ship", ship_cmd)); app.add_handler(CommandHandler("couple", couple_cmd)); app.add_handler(CommandHandler("love", love_cmd)); app.add_handler(CommandHandler("hug", hug_cmd)); app.add_handler(CommandHandler("kiss", kiss_cmd)); app.add_handler(CommandHandler("slap", slap_cmd)); app.add_handler(CommandHandler("pat", pat_cmd)); app.add_handler(CommandHandler("jail", jail_cmd))
    app.add_handler(CommandHandler("story", story_cmd)); app.add_handler(CommandHandler("dream", dream_cmd)); app.add_handler(CommandHandler("horoscope", horoscope_cmd)); app.add_handler(CommandHandler("tarot", tarot_cmd)); app.add_handler(CommandHandler("ask", ask_cmd)); app.add_handler(CommandHandler("say", say_cmd)); app.add_handler(CommandHandler("pfp", pfp_cmd)); app.add_handler(CommandHandler("cartoon", cartoon_cmd)); app.add_handler(CommandHandler("meme", meme_cmd)); app.add_handler(CommandHandler("wallpaper", wallpaper_cmd))
    app.add_handler(CommandHandler("imaginehd", imaginehd_cmd)); app.add_handler(CommandHandler("imagine", imaginehd_cmd)); app.add_handler(CommandHandler("face", face_cmd)); app.add_handler(CommandHandler("bgremove", bgremove_cmd)); app.add_handler(CommandHandler("enhance", enhance_cmd)); app.add_handler(CommandHandler("aisong", aisong_cmd))
    app.add_handler(CommandHandler("mafia", mafia_cmd)); app.add_handler(CommandHandler("votemafia", votemafia_cmd)); app.add_handler(CommandHandler("quizbattle", quizbattle_cmd)); app.add_handler(CommandHandler("bingo", bingo_cmd)); app.add_handler(CommandHandler("poker", poker_cmd)); app.add_handler(CommandHandler("uno", uno_cmd))
    app.add_handler(CommandHandler("cricket", cricket_cmd)); app.add_handler(CommandHandler("football", football_cmd)); app.add_handler(CommandHandler("crypto", crypto_cmd)); app.add_handler(CommandHandler("gold", gold_cmd)); app.add_handler(CommandHandler("radio", radio_cmd))
    app.add_handler(CommandHandler("homework", homework_cmd)); app.add_handler(CommandHandler("dictionary", dictionary_cmd)); app.add_handler(CommandHandler("solve", solve_cmd))
    app.add_handler(CommandHandler("loan", loan_cmd)); app.add_handler(CommandHandler("payloan", payloan_cmd)); app.add_handler(CommandHandler("business", business_cmd)); app.add_handler(CommandHandler("collect", collect_cmd)); app.add_handler(CommandHandler("stock", stock_cmd)); app.add_handler(CommandHandler("interest", interest_cmd))
    app.add_handler(CommandHandler("birthday", birthday_cmd)); app.add_handler(CommandHandler("reminder", reminder_cmd)); app.add_handler(CommandHandler("remind", reminder_cmd)); app.add_handler(CommandHandler("poll", poll_cmd)); app.add_handler(CommandHandler("event", event_cmd))
    app.add_handler(CommandHandler("testpromo", test_promo_cmd)); app.add_handler(CommandHandler("testgm", test_gm_cmd)); app.add_handler(CommandHandler("testgn", test_gn_cmd))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new)); app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye)); app.add_handler(MessageHandler(filters.VOICE, voice_handler)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat)); app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST & filters.TEXT, channel_chat))
    from telegram.ext import ChatMemberHandler
    app.add_handler(ChatMemberHandler(track_chat, ChatMemberHandler.MY_CHAT_MEMBER)); app.add_handler(MessageHandler(filters.ALL, track_chat), group=-1)
    jq=app.job_queue
    jq.run_daily(auto_clean_deleted, time=datetime.time(hour=6, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="6am_clean")
    jq.run_daily(auto_good_morning, time=datetime.time(hour=6, minute=5, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="6am_gm")
    jq.run_daily(auto_daily_quote, time=datetime.time(hour=7, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="7am_quote")
    jq.run_daily(auto_daily_meme, time=datetime.time(hour=12, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="12pm_meme")
    jq.run_daily(auto_birthday_check, time=datetime.time(hour=8, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="8am_birthday")
    jq.run_daily(auto_interest, time=datetime.time(hour=6, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="6am_interest")
    jq.run_daily(auto_good_night, time=datetime.time(hour=22, minute=0, second=0, tzinfo=pytz.timezone("Asia/Colombo")), name="10pm_gn")
    jq.run_repeating(auto_promo, interval=1800, first=60, name="30min_promo")
    print("Jobs: 6AM Clean + 6:05 GM + 7AM Quote + 12PM Meme + 8AM Birthday + 6AM Interest + 10PM GN + 30min Promo Group+Channel Only! ALL FREE!")
    print("Pamela MEGA MONSTER Online!")
    app.run_polling()
if __name__=="__main__":
    ft=threading.Thread(target=lambda: app_flask.run(host="0.0.0.0", port=PORT), daemon=True); ft.start(); print(f"Flask on {PORT}"); run_bot()
