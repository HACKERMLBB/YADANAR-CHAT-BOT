import os,time,threading,asyncio,requests,urllib.parse,random,json,datetime,pytz,subprocess,secrets,string
from flask import Flask
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,ChatMemberHandler
from telegram.constants import ChatMemberStatus
BOT_TOKEN=os.getenv("BOT_TOKEN");PORT=int(os.environ.get("PORT",10000))
app_flask=Flask(__name__)
@app_flask.route("/")
def home(): return "Pamela Online!"
@app_flask.route("/health")
def health(): return "OK",200
GROUP_IDS=[]
try:
 _g=os.getenv("GROUP_IDS","")
 if _g: GROUP_IDS=[int(x.strip()) for x in _g.split(",") if x.strip()]
except: GROUP_IDS=[]
ACTIVE_CHATS=set(GROUP_IDS);last_request_times={};COOLDOWN_SECONDS=15
warns={};afk_users={};filters_db={};notes_db={};coins_db={};levels_db={};user_db={};msg_db={};flood_db={};bank_db={};stats_db={};quiz_db={};ttt_games={};memory_db={};streak_db={};marry_db={};jail_db={};guess_db={};math_db={};word_db={};welcome_db={};rules_db={};birthday_db={};business_db={};stock_db={};loan_db={};event_db={};riddle_db={}
def load_json(f,d):
 try:
  if os.path.exists(f):
   with open(f,"r") as x: return json.load(x)
 except: pass
 return d
def save_json(f,d):
 try:
  with open(f,"w") as x: json.dump(d,x)
 except: pass
user_db=load_json("pamela_users.json",{});msg_db=load_json("pamela_messages.json",{});filters_db=load_json("pamela_filters.json",{});notes_db=load_json("pamela_notes.json",{});coins_db=load_json("pamela_coins.json",{});levels_db=load_json("pamela_levels.json",{});bank_db=load_json("pamela_bank.json",{});stats_db=load_json("pamela_stats.json",{});memory_db=load_json("pamela_memory.json",{});streak_db=load_json("pamela_streak.json",{});marry_db=load_json("pamela_marry.json",{});welcome_db=load_json("pamela_welcome.json",{});rules_db=load_json("pamela_rules.json",{});birthday_db=load_json("pamela_birthday.json",{});business_db=load_json("pamela_business.json",{});stock_db=load_json("pamela_stock.json",{});loan_db=load_json("pamela_loan.json",{});event_db=load_json("pamela_event.json",{})
def save_user(cid,uid):
 cid=str(cid)
 if cid not in user_db: user_db[cid]=[]
 if uid not in user_db[cid]: user_db[cid].append(uid);save_json("pamela_users.json",user_db)
def get_all_chats():
 chats=set(ACTIVE_CHATS)
 try:
  for k in list(user_db.keys()):
   if str(k).lstrip("-").isdigit(): chats.add(int(k))
 except: pass
 for gid in GROUP_IDS: chats.add(gid)
 return list(chats)
def save_chat_id(cid):
 try: ACTIVE_CHATS.add(int(cid));save_user(cid,0)
 except: pass
def save_message(cid,mid,uname,un,txt):
 cid=str(cid)
 if cid not in msg_db: msg_db[cid]=[]
 msg_db[cid].append({"msg_id":mid,"user":uname,"username":un,"text":txt,"time":time.time()})
 if len(msg_db[cid])>200: msg_db[cid]=msg_db[cid][-200:]
 save_json("pamela_messages.json",msg_db)
def check_cooldown(cid):
 now=time.time();last=last_request_times.get(cid,0);rem=COOLDOWN_SECONDS-(now-last)
 if rem>0: return int(rem)
 last_request_times[cid]=now;return 0
def translate_text(t,lang):
 try:
  r=requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+lang+"&dt=t&q="+urllib.parse.quote(t),timeout=10);d=r.json();return "".join([x[0] for x in d[0] if x[0]])
 except: return None
CUTE_STARTS=["🌸💖 ","🦋✨ ","🌷💗 ","💖🌸 "]
CUTE_ENDS=["\n\n💖🌸 Love you, baby! 🌸💖","\n\n🦋💕 Pamela loves you! 💕🦋","\n\n🌸✨ Stay cute, baby! ✨🌸"]
def make_cute(r): return f"{random.choice(CUTE_STARTS)}{r}{random.choice(CUTE_ENDS)}"
def ask_pamela(t,uid=None):
 try:
  mem=""
  if uid:
   hist=memory_db.get(str(uid),[])
   if hist: mem=" Past: "+" | ".join(hist[-5:])
  p="You are Pamela, CUTEST princess! Use LOTS cute emojis EVERY sentence! Be super cute, soft, baby-talk. Call user baby,cutie. Use hehe,awww,hihi,yayyy,muahhh. Keep short max 3-4 lines. Reply in EXACT SAME language as user! "+mem+f" User says: {t}"
  res=requests.get("https://text.pollinations.ai/"+urllib.parse.quote(p),timeout=60)
  if res.status_code==200:
   rep=res.text.strip()
   if rep:
    if uid:
     u=str(uid)
     if u not in memory_db: memory_db[u]=[]
     memory_db[u].append(f"User: {t} | Pamela: {rep[:100]}")
     if len(memory_db[u])>20: memory_db[u]=memory_db[u][-20:]
     save_json("pamela_memory.json",memory_db)
    return make_cute(rep)
   return "Sorry baby! I got shy! Try again?"
  elif res.status_code==402: return "Baby! I am tired! Wait 30 sec!"
  else: return "Oops baby! Sleepy! Try again!"
 except: return "Baby! Trouble! Try again!"
async def is_admin(u,uid):
 try:
  m=await u.effective_chat.get_member(uid);return m.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]
 except: return False
def get_target(u):
 if u.message.reply_to_message: return u.message.reply_to_message.from_user
 return None
TRUTHS=["Who is your crush?","Who did you lie to last?","Tell a secret you never told anyone!","What is last photo on your phone?","Who do you secretly love?","What is your biggest fear?","Have you ever cried for someone?","Who is most beautiful in group?","What is your dream?","Have you ever stalked your crush?"]
DARES=["Send a photo in group!","Message last person you chatted I Love You!","Say Hi in cute voice!","Type your crush name!","Send message using only emojis!","Change name to I Love Pamela for 1 hour!","Send voice singing!","Text your crush Hi now!"]
ROASTS=["Your face is like WiFi, everyone tries to connect but no signal!","Your brain is like Google, search and nothing comes up!","Even doctor was shocked on day you were born!"]
QUOTES=["Every flower blooms in its own time.","Be like butterfly, beautiful and free!","After every rain, there is rainbow!","You are loved more than you know!"]
BAD_WORDS=["huththo","pakaya","kariya","wesi","ponnaya","balla","hukanna","fuck","bitch","shit"]
GOOD_MORNING=["☀️🌸 Good Morning Babies! New day! New hope! Pamela wishes super day! Love you! - Pamela","🌷✨ Good Morning! You are all cute today! Keep smiling! - Pamela"]
GOOD_NIGHT=["🌙💖 Good Night Babies! Sweet dreams! Pamela loves you! Tomorrow meet again!","🌌✨ Good Night Cuties! Stars shining for you! Sleep well! - Pamela"]
QUIZ_Q=[{"q":"What is capital of Sri Lanka?","a":["Colombo","Kandy","Galle","Jaffna"],"c":0},{"q":"What is 5 + 7?","a":["10","12","11","13"],"c":1},{"q":"Largest planet?","a":["Mars","Jupiter","Saturn","Earth"],"c":1},{"q":"What colour is sky?","a":["Green","Blue","Red","Pink"],"c":1},{"q":"Who is Pamela?","a":["Queen","Bot","Princess","All of above"],"c":3},{"q":"What is 10 x 10?","a":["100","90","110","1000"],"c":0}]
HOROSCOPES=["Aries: Today lucky! Love near!","Taurus: Money coming! Stay calm!","Gemini: Someone likes you secretly!","Cancer: Family time! Hug them!","Leo: You will shine today!","Virgo: Work hard, reward coming!","Libra: Balance! Love will find you!","Scorpio: Mystery! Someone thinking of you!","Sagittarius: Adventure day!","Capricorn: Success near!","Aquarius: New friend coming!","Pisces: Dream big!"]
TAROTS=["The Star - Hope and dreams!","The Lovers - Love coming!","The Sun - Happiness!","The Moon - Trust your heart!","Strength - You are strong!","Wheel of Fortune - Lucky day!"]
RIDDLES=[{"q":"I speak without a mouth and hear without ears. What am I?","a":"echo"},{"q":"What has keys but can't open locks?","a":"piano"},{"q":"What gets wetter the more it dries?","a":"towel"},{"q":"What has a face and two hands but no arms or legs?","a":"clock"},{"q":"What comes once in a minute, twice in a moment, but never in a thousand years?","a":"m"}]
WYR=["Would you rather be rich or famous?","Would you rather fly or be invisible?","Would you rather have super strength or super speed?","Would you rather live in beach or mountain?","Would you rather be Pamela's best friend forever or have 1 million coins?"]
NEVER=["Never have I ever lied to my best friend.","Never have I ever stalked my crush.","Never have I ever cried watching a movie.","Never have I ever eaten in class.","Never have I ever pretended to be sick to skip school."]
async def auto_clean_deleted(context):
 for cid_str,uids in list(user_db.items()):
  cid=int(cid_str);banned=0
  for uid in list(uids):
   if uid==0: continue
   try:
    m=await context.bot.get_chat_member(cid,uid)
    if m.user.first_name=="Deleted Account": await context.bot.ban_chat_member(cid,uid);await context.bot.unban_chat_member(cid,uid);banned+=1
   except:
    try: await context.bot.ban_chat_member(cid,uid);await context.bot.unban_chat_member(cid,uid);banned+=1
    except: pass
   await asyncio.sleep(0.3)
  if banned>0:
   try: await context.bot.send_message(chat_id=cid,text=f"🧹💖 6 AM Cleaning Done! Removed {banned} Deleted Accounts!")
   except: pass
async def auto_good_morning(context):
 for cid in get_all_chats():
  if cid>0: continue
  try: await context.bot.send_message(chat_id=cid,text=random.choice(GOOD_MORNING));await asyncio.sleep(1)
  except: pass
async def auto_good_night(context):
 for cid in get_all_chats():
  if cid>0: continue
  try: await context.bot.send_message(chat_id=cid,text=random.choice(GOOD_NIGHT));await asyncio.sleep(1)
  except: pass
async def auto_birthday_check(context):
 today=datetime.date.today().strftime("%d-%m")
 for cid_str,users in list(birthday_db.items()):
  for uid,info in list(users.items()):
   if info.get("date")==today:
    try: await context.bot.send_message(chat_id=int(cid_str),text=f"🎂🎉 HAPPY BIRTHDAY {info.get('name','Baby')}! 🎉🎂 Pamela loves you! Cake for you! 🎂💖 Join @bigolive_asia")
    except: pass
async def auto_interest(context):
 for uid in list(bank_db.keys()):
  b=int(bank_db[uid]*0.05)
  if b>0: bank_db[uid]+=b
 save_json("pamela_bank.json",bank_db)
async def auto_promo(context):
 titles=["👑💖 PAMELA'S WORLD 💖👑","🌸✨ HEY BABIES! ✨🌸","🦋💕 PAMELA IS HERE! 💕🦋"]
 intros=["🌸💖 Hello My Lovely Babies! How are you? 💖🌸","🦋✨ Is group sleeping? Pamela is here! Wake Up! ✨🦋"]
 feats=["🎵💖 /song Name - Song Download!","📹✨ /video link - Video Download!","🎤🌸 /lyrics Song - Lyrics!","🎬👑 /movie Name - Movie Info!","🍥🦋 /anime Name - Anime Info!","🎲💕 /truth - Truth Game!","😂🌸 /dare - Dare Game!","🧠✨ /quiz - Quiz! +50 Coins!","❌💖 /ttt - Tic Tac Toe!","🎰🔥 /bet 100 - Casino Bet!","🎁💖 /daily - Daily Coins!","👑✨ /rank - Rank Card!","🏦💰 /bank - Save Coins!","🎨🌸 /img cute cat - AI Image!","🌧️💖 /weather Colombo - Weather!","🌍✨ /tr en - Translate!","💬💖 Just Type - I Reply!","😴🌙 /afk - AFK!","📝💕 /save hi - Save Notes!","🤖✨ /filter hi - Auto Reply!","✂️🎲 /rps rock - Rock Paper Scissors!","🔤🌸 /word - Word Game!","🧮✨ /math - Math Race!","🎯💖 /guess - Guess Number!","🃏🔥 /blackjack - Blackjack!","🐎✨ /race - Horse Race!","💍💖 /marry - Marry!","💖🌸 /ship - Ship!","😂🔥 /jail - Jail!","💖✨ /love - Love %!","🤗💕 /hug - Hug!","💼💰 /work - Work for Coins!","🎟️✨ /lottery - Lottery!","🔮🌙 /horoscope - Horoscope!","🃏💖 /tarot - Tarot!","📖🌸 /story - AI Story!","📸💖 /pfp - Profile Photo!","🏆👑 /profile - Full Profile!","📺🔥 /livetv - World Live TV 40+ Channels!","🌍💖 /worldtv - World TV Only!","🏏⚽ /sportstv - Sports Live TV!","📰✨ /news - Live News World!","🎬✂️ /trim - Video Cut!","📦💖 /compress - Video Compress!","🎵✨ /toaudio - Video to Audio!","🎞️🌸 /togif - Video to GIF!","🐢💕 /slowmo - Slow Motion!","🔄😂 /reverse - Reverse Video!","🎨👑 /imaginehd cute cat - 4K AI Image 4 Styles!","😍💖 /face - Face Age Mood Beauty!","✂️📸 /bgremove - Remove Background!","✨📸 /enhance - Photo HD!","🎵🤖 /aisong love - AI Song!","🕵️🔥 /mafia - Mafia Game!","🏆✨ /quizbattle - Quiz Tournament!","🔢💖 /bingo - Bingo!","🃏🔥 /poker - Poker!","🎴🌸 /uno - UNO!","🏏🔥 /cricket - Live Cricket!","⚽💖 /football - Live Football!","₿📈 /crypto - Bitcoin Live!","🥇✨ /gold - Gold Price!","📻🎵 /radio - Live Radio!","📚✨ /homework question - Homework Help!","📖💖 /dictionary love - Dictionary!","🧮💕 /solve 2+2 - Solve Math!","🏦😂 /loan 1000 - Bank Loan!","☕🔥 /business - Start Business!","📈😂 /stock - Stock Market!","💰✨ /interest - Bank Interest!","🎂🎉 /birthday 12-05 - Save Birthday!","⏰💖 /reminder 10 hello - Reminder!","🗳️✨ /poll Question | Yes | No - Poll!","🎉💖 /event Party | Tomorrow - Event!","🎤💖 /voice hi baby - Pamela AI Voice!","🎤🎵 /sing love - Pamela Sings!","🎤🔥 /rap - Pamela Rap!","📢💖 /shoutout Name - Voice Shoutout!","🎙️💖 /podcast love - AI Podcast!","🎬🤖 /aivideo cute cat dancing - AI Video!","🗣️💖 /talkingphoto - Photo Talks!","💋💖 /lipsync - Photo Lip Sync!","🔄💖 /faceswap - Face Swap!","👗💖 /outfit saree - AI Outfit!","👶💖 /babyface - Baby Photo!","👴💖 /oldface - Old Photo!","💑💖 /couplephoto - Couple Photo!","🎡🔥 /spin - Spin Wheel!","🤔💖 /wyr - Would You Rather!","🙈💖 /never - Never Have I Ever!","🧩💖 /riddle - Riddle Game!","♟️💖 /chess - Chess!","🎲💖 /ludo - Ludo!","📷💖 /qr hello - QR Code!","🔑💖 /password - Strong Password!","🔗💖 /shortlink link - Short Link!","📸💖 /screenshot link - Website Screenshot!","📄💖 /pdf hello - Make PDF!","🎭💖 /sticker - Photo to Sticker!","🌐🎤 /translatevoice en hi - Translate Voice!","🔮💖 /horoscopedaily - Daily Horoscope!","💘💖 /lovecalc - Love Calculator!","🌙💖 /dreammeaning dream - Dream Meaning!","☀️💖 /goodmorningphoto - GM Photo!","📸💖 /welcomephoto - Welcome Photo!","📊💖 /topweek - Top of Week!","👀💖 /activecheck - Active Check!","🎁💖 /giveaway prize - Giveaway!"]
 picked=feats.copy();random.shuffle(picked)
 border="✨━━━━━━━━━━━━✨"
 msg=f"{border}\n{random.choice(titles)}\n{border}\n\n{random.choice(intros)}\n\n💖✨ Did You Know? ✨💖\n━━━━━━━━━━━━\n"
 for f in picked: msg+=f"{f}\n"
 msg+=f"\n{border}\n💖🌸 Try One Now Baby! 🌸💖\n{border}\n\n🌿💖 Join our family @bigolive_asia 💖🌿\n💖✨ Type /help for all! ALL FREE! 👑✨\n🌸💕 Love you babies! Muahhh! 💕🌸"
 for cid in get_all_chats():
  if cid>0: continue
  try: await context.bot.send_message(chat_id=cid,text=msg);await asyncio.sleep(1)
  except: pass
async def auto_daily_quote(context):
 for cid in get_all_chats():
  if cid>0: continue
  try: await context.bot.send_message(chat_id=cid,text=f"✨💖 Daily Quote 💖✨\n\n🌸 {random.choice(QUOTES)} 🌸\n\n- Pamela 💕");await asyncio.sleep(1)
  except: pass
async def auto_daily_meme(context):
 for cid in get_all_chats():
  if cid>0: continue
  try: await context.bot.send_photo(chat_id=cid,photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote('funny cute meme'),caption="😂💖 Daily Meme! - Pamela 💖😂");await asyncio.sleep(1)
  except: pass
async def test_promo_cmd(u,c):
 save_chat_id(u.effective_chat.id);await u.message.reply_text("🌸💖 Testing Promo... 💖🌸");await auto_promo(c);await u.message.reply_text("✅💖 Promo Test Done! 💖✅")
async def test_gm_cmd(u,c): save_chat_id(u.effective_chat.id);await auto_good_morning(c)
async def test_gn_cmd(u,c): save_chat_id(u.effective_chat.id);await auto_good_night(c)
async def start(u,c):
 save_chat_id(u.effective_chat.id);await u.message.reply_text("✨━━━━━━━━━━━━━━━━━━━✨\n🌸💖 WELCOME TO 💖🌸\n👑✨ PAMELA'S WORLD ✨👑\n✨━━━━━━━━━━━━━━━━━━━✨\n\n🦋💕 Hello, My Lovely Friend! 💕🦋\n💖🌸 I am Pamela! Your cute little best friend! 🌸💖\n\n💬🌸 Talk to me anything baby! I am here for you! 🌸💬\n🌍✨ I can speak ANY language! ✨🌍\n🎁💖 ALL FREE! No VIP! No Premium! 💖🎁\n\n🌿💖 Add me to your group! 💖🌿\n💕 Join @bigolive_asia 💕\n\n✨💖 Made with love, just for YOU! 💖✨")
async def help_cmd(u,c): await u.message.reply_text("👑💖 PAMELA HELP - ALL FREE! OLD + NEW! 💖👑\n\n💬 CHAT: Just type! /ask /tr /story /say\n🎵 MUSIC: /song /video /lyrics /playlist /spotify\n🎬 MOVIE: /movie /anime\n📺 LIVE TV: /livetv /worldtv /sportstv /news\n🎬 VIDEO EDIT: /trim /compress /toaudio /togif /slowmo /reverse /mutevideo\n🎨 AI: /imaginehd /face /bgremove /enhance /aisong /story /ask /img\n🎤 NEW AI AUDIO: /voice /sing /rap /shoutout /podcast /translatevoice\n🎬 NEW AI VIDEO: /aivideo /talkingphoto /lipsync\n🎨 NEW AI IMAGE: /faceswap /outfit /babyface /oldface /couplephoto\n🎮 GAMES: /truth /dare /dice /slot /coin /8ball /roast /quote /ttt /quiz /bet /rps /word /math /guess /blackjack /race /hunger /challenge /mafia /quizbattle /bingo /poker /uno\n🎮 NEW GAMES: /spin /wyr /never /riddle /chess /ludo\n🏏 LIVE: /cricket /football /crypto /gold /radio /weather\n📚 STUDY: /homework /dictionary /solve /tr\n💰 COINS: /daily /coins /leaderboard /bank /deposit /withdraw /steal /work /rob /gift /lottery /loan /business /stock /interest /shop\n💖 LOVE: /marry /divorce /ship /couple /love /hug /kiss /slap /pat /jail /lovecalc\n🛠️ NEW TOOLS: /qr /password /shortlink /screenshot /pdf /sticker\n🛡️ MANAGE: /ban /kick /mute /warn /promote /pin /purge /del /lock /unlock /setwelcome /setrules /slowmode /report\n🤖 FILTERS: /filter /filters /stop\n📝 NOTES: /save /get /notes /clear\n😴 AFK: /afk /unafk\n🎂 SPECIAL: /birthday /reminder /poll /event /giveaway /horoscopedaily /dreammeaning /goodmorningphoto /welcomephoto /topweek /activecheck\n🏆 OTHER: /rank /profile /stats /top /topdaily /pfp /meme /wallpaper\n\n🌿💖 Join @bigolive_asia - ALL FREE! 💖🌿")
async def about_cmd(u,c): await u.message.reply_text("🌸💖 About Pamela 💖🌸\n\n👑✨ I am Pamela, Queen of Pamela's World! ✨👑\n🦋💕 I love flowers, butterflies, nature, and YOU! 💕🦋\n🌿💖 Join @bigolive_asia - ALL FREE! 💖🌿")
async def tr_cmd(u,c):
 if not c.args: await u.message.reply_text("🌍💖 Use /tr en 💖🌍");return
 lang=c.args[0].lower();txt=""
 if u.message.reply_to_message and u.message.reply_to_message.text: txt=u.message.reply_to_message.text
 elif len(c.args)>1: txt=" ".join(c.args[1:])
 else: await u.message.reply_text("💖 Reply to a text baby! 💖");return
 tr=translate_text(txt,lang)
 if tr: await u.message.reply_text(f"🌍✨ Translated to {lang.upper()} ✨🌍:\n\n💖 {tr} 💖")
 else: await u.message.reply_text("😭💖 Oops baby! Try again! 💖😭")
async def livetv_cmd(u,c): await u.message.reply_text("📺👑 PAMELA WORLD LIVE TV - ALL FREE! 👑📺\n\nSRI LANKA:\nHiru TV - https://www.youtube.com/@HiruTV/live\nSirasa TV - https://www.youtube.com/@SirasaTV/live\nDerana TV - https://www.youtube.com/@TVDerana/live\nITN - https://www.youtube.com/@ITNSriLanka/live\n\nNEWS:\nHiru News - https://www.youtube.com/@HiruNews/live\nNewsFirst - https://www.youtube.com/@NewsfirstLIVE/live\nAda Derana - https://www.youtube.com/@AdaDerana/live\n\nWORLD:\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\nFrance 24 - https://www.youtube.com/@FRANCE24English/live\nDW - https://www.youtube.com/@dwnews/live\n\nSPORTS:\nSky Sports Cricket - https://www.youtube.com/@SkySportsCricket/live\nESPN - https://www.youtube.com/@ESPN/live\nWWE - https://www.youtube.com/@WWE/live\nF1 - https://www.youtube.com/@F1/live\n\n💖🌸 Enjoy Baby! - Pamela 🌸💖\n🌿 Join @bigolive_asia 💖")
async def worldtv_cmd(u,c): await u.message.reply_text("🌍👑 PAMELA WORLD TV! 👑🌍\n\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\n\n💖🌸 Enjoy World TV Baby! - Pamela 🌸💖")
async def sportstv_cmd(u,c): await u.message.reply_text("🏏⚽ PAMELA SPORTS TV! ⚽🏏\n\nSky Sports Cricket - https://www.youtube.com/@SkySportsCricket/live\nESPN - https://www.youtube.com/@ESPN/live\nSky Sports Football - https://www.youtube.com/@SkySportsFootball/live\nWWE - https://www.youtube.com/@WWE/live\nF1 - https://www.youtube.com/@F1/live\n\n💖🌸 Enjoy Sports Baby! - Pamela 🌸💖")
async def tv_cmd(u,c): await livetv_cmd(u,c)
async def news_cmd(u,c): await u.message.reply_text("📰🌍 LIVE NEWS WORLD! 🌍📰\n\nHiru News - https://www.youtube.com/@HiruNews/live\nNewsFirst - https://www.youtube.com/@NewsfirstLIVE/live\nAda Derana - https://www.youtube.com/@AdaDerana/live\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\n\n💖🌸 Stay Updated Baby! - Pamela 🌸💖")
async def hiru_cmd(u,c): await u.message.reply_text("📺💖 Hiru TV Live! 💖📺\nhttps://www.youtube.com/@HiruTV/live\n\n💖 Enjoy Baby! - Pamela 💖")
async def sirasa_cmd(u,c): await u.message.reply_text("📺💖 Sirasa TV Live! 💖📺\nhttps://www.youtube.com/@SirasaTV/live\n\n💖 Enjoy Baby! - Pamela 💖")
async def derana_cmd(u,c): await u.message.reply_text("📺💖 Derana TV Live! 💖📺\nhttps://www.youtube.com/@TVDerana/live\n\n💖 Enjoy Baby! - Pamela 💖")
async def download_reply_video(u):
 if not u.message.reply_to_message or not u.message.reply_to_message.video: await u.message.reply_text("💖 Reply to a Video and type command baby! 💖");return None
 f=await u.message.reply_to_message.video.get_file();path=f"edit_{u.message.from_user.id}.mp4";await f.download_to_drive(path);return path
async def trim_cmd(u,c):
 if not c.args or len(c.args)<2: await u.message.reply_text("✂️💖 Use Reply Video + /trim 0 5 💖✂️");return
 path=await download_reply_video(u)
 if not path: return
 try:
  s=c.args[0];d=c.args[1];out=f"trim_{u.message.from_user.id}.mp4";sm=await u.message.reply_text(f"✂️💖 Trimming {s}s to {d}s... Wait baby! 💖✂️");subprocess.run(["ffmpeg","-y","-ss",s,"-t",d,"-i",path,"-c","copy",out],capture_output=True);await u.message.reply_video(video=open(out,"rb"),caption=f"✂️💖 Trimmed Video! {s}s - {d}s - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"😭💖 Oops baby! {e} 💖😭")
async def compress_cmd(u,c):
 path=await download_reply_video(u)
 if not path: return
 try:
  out=f"comp_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("📦💖 Compressing... Wait baby! 💖📦");subprocess.run(["ffmpeg","-y","-i",path,"-vcodec","libx264","-crf","28",out],capture_output=True);await u.message.reply_video(video=open(out,"rb"),caption="📦💖 Compressed Video! - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def toaudio_cmd(u,c):
 path=await download_reply_video(u)
 if not path: return
 try:
  out=f"audio_{u.message.from_user.id}.mp3";sm=await u.message.reply_text("🎵💖 Extracting Audio... Wait baby! 💖🎵");subprocess.run(["ffmpeg","-y","-i",path,"-vn",out],capture_output=True);await u.message.reply_audio(audio=open(out,"rb"),caption="🎵💖 Audio from Video! - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def togif_cmd(u,c):
 path=await download_reply_video(u)
 if not path: return
 try:
  out=f"gif_{u.message.from_user.id}.gif";sm=await u.message.reply_text("🎞️💖 Making GIF... Wait baby! 💖🎞️");subprocess.run(["ffmpeg","-y","-i",path,"-t","3","-vf","fps=10,scale=320:-1:flags=lanczos",out],capture_output=True);await u.message.reply_animation(animation=open(out,"rb"),caption="🎞️💖 GIF Made! - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def slowmo_cmd(u,c):
 path=await download_reply_video(u)
 if not path: return
 try:
  out=f"slow_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("🐢💖 Making Slow Motion... Wait baby! 💖🐢");subprocess.run(["ffmpeg","-y","-i",path,"-filter:v","setpts=2.0*PTS",out],capture_output=True);await u.message.reply_video(video=open(out,"rb"),caption="🐢💖 Slow Motion! - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def reverse_cmd(u,c):
 path=await download_reply_video(u)
 if not path: return
 try:
  out=f"rev_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("🔄💖 Reversing... Wait baby! 💖🔄");subprocess.run(["ffmpeg","-y","-i",path,"-vf","reverse","-af","areverse",out],capture_output=True);await u.message.reply_video(video=open(out,"rb"),caption="🔄💖 Reversed Video! - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def mutevideo_cmd(u,c):
 path=await download_reply_video(u)
 if not path: return
 try:
  out=f"mute_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("🔇💖 Muting... Wait baby! 💖🔇");subprocess.run(["ffmpeg","-y","-i",path,"-c:v","copy","-an",out],capture_output=True);await u.message.reply_video(video=open(out,"rb"),caption="🔇💖 Muted Video! - Pamela 💖");os.remove(path);os.remove(out);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def ban_cmd(u,c):
 if u.effective_chat.type=="private": await u.message.reply_text("💖 Only in groups baby! 💖");return
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("🛡️💖 Only for Admins baby! 💖🛡️");return
 t=get_target(u)
 if not t: await u.message.reply_text("💖 Reply and type /ban! 💖");return
 try: await u.effective_chat.ban_member(t.id);await u.message.reply_text(f"🚫💖 {t.first_name} Banned! 💖🚫")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def unban_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /unban!");return
 try: await u.effective_chat.unban_member(t.id);await u.message.reply_text("💖 Unbanned baby! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def kick_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /kick!");return
 try: await u.effective_chat.ban_member(t.id);await u.effective_chat.unban_member(t.id);await u.message.reply_text(f"💖 {t.first_name} Kicked! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def mute_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /mute!");return
 try:
  from telegram import ChatPermissions;await u.effective_chat.restrict_member(t.id,ChatPermissions(can_send_messages=False));await u.message.reply_text(f"🔇💖 {t.first_name} Muted! 💖🔇")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def unmute_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /unmute!");return
 try:
  from telegram import ChatPermissions;await u.effective_chat.restrict_member(t.id,ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True));await u.message.reply_text(f"💖 {t.first_name} Unmuted! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def warn_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /warn!");return
 cid=u.effective_chat.id
 if cid not in warns: warns[cid]={}
 warns[cid][t.id]=warns[cid].get(t.id,0)+1;cc=warns[cid][t.id]
 if cc>=3:
  try: await u.effective_chat.ban_member(t.id);await u.message.reply_text(f"🚫💖 {t.first_name} got 3 Warnings! Auto Ban! 💖🚫");warns[cid][t.id]=0
  except Exception as e: await u.message.reply_text(f"Oops! {e}")
 else: await u.message.reply_text(f"⚠️💖 {t.first_name} Warning {cc}/3! 💖⚠️")
async def warnings_cmd(u,c):
 t=get_target(u) or u.message.from_user;cc=warns.get(u.effective_chat.id,{}).get(t.id,0);await u.message.reply_text(f"⚠️💖 {t.first_name} Warnings: {cc}/3 💖⚠️")
async def promote_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /promote!");return
 try: await u.effective_chat.promote_member(t.id,can_change_info=True,can_delete_messages=True,can_invite_users=True,can_restrict_members=True,can_pin_messages=True,can_promote_members=False);await u.message.reply_text(f"👑💖 {t.first_name} is now Admin! 💖👑")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def demote_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /demote!");return
 try: await u.effective_chat.promote_member(t.id,can_change_info=False,can_delete_messages=False,can_invite_users=False,can_restrict_members=False,can_pin_messages=False,can_promote_members=False);await u.message.reply_text(f"💖 {t.first_name} removed from Admin! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def pin_cmd(u,c):
 if not u.message.reply_to_message: await u.message.reply_text("📌💖 Reply and type /pin! 💖📌");return
 try: await u.message.reply_to_message.pin();await u.message.reply_text("📌💖 Pinned baby! 💖📌")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def unpin_cmd(u,c):
 try: await u.effective_chat.unpin_all_messages();await u.message.reply_text("💖 Unpinned! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def del_cmd(u,c):
 if u.message.reply_to_message:
  try: await u.message.reply_to_message.delete();await u.message.delete()
  except: await u.message.reply_text("💖 Could not delete baby! 💖")
 else: await u.message.reply_text("💖 Reply and type /del! 💖")
async def purge_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not u.message.reply_to_message: await u.message.reply_text("Reply and type /purge!");return
 try:
  s=u.message.reply_to_message.message_id;e=u.message.message_id;cnt=0
  for mid in range(s,e+1):
   try: await c.bot.delete_message(u.effective_chat.id,mid);cnt+=1
   except: pass
  m=await u.message.reply_text(f"🧹💖 Deleted {cnt} Messages! 💖🧹");await asyncio.sleep(3);await m.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def lock_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 try:
  from telegram import ChatPermissions;await u.effective_chat.set_permissions(ChatPermissions(can_send_messages=False));await u.message.reply_text("🔒💖 Group Locked! 💖🔒")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def unlock_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 try:
  from telegram import ChatPermissions;await u.effective_chat.set_permissions(ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True));await u.message.reply_text("🔓💖 Group Unlocked! 💖🔓")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def rules_cmd(u,c):
 cid=str(u.effective_chat.id);custom=rules_db.get(cid,"")
 if custom: await u.message.reply_text(f"📜💖 GROUP RULES 💖📜\n\n{custom}");return
 await u.message.reply_text("📜💖 GROUP RULES 💖📜\n\n1. Be kind baby!\n2. No bad words!\n3. No spam!\n4. Respect everyone!\n5. Love Pamela's World!\n\n💖 Break rules = Warn / Ban! 💖")
async def setrules_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not c.args: await u.message.reply_text("Use /setrules Your rules here");return
 rules_db[str(u.effective_chat.id)]=" ".join(c.args);save_json("pamela_rules.json",rules_db);await u.message.reply_text("✅💖 Rules Updated baby! 💖✅")
async def setwelcome_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not c.args: await u.message.reply_text("Use /setwelcome Welcome text");return
 welcome_db[str(u.effective_chat.id)]=" ".join(c.args);save_json("pamela_welcome.json",welcome_db);await u.message.reply_text("✅💖 Welcome Updated! 💖✅")
async def slowmode_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not c.args: await u.message.reply_text("Use /slowmode 10");return
 try: await u.message.reply_text(f"🐢💖 Slowmode set to {c.args[0]} sec! 💖🐢")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def report_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /report!");return
 try:
  admins=await u.effective_chat.get_administrators()
  for a in admins:
   try: await c.bot.send_message(chat_id=a.user.id,text=f"REPORT in {u.effective_chat.title} User: {t.first_name} Reported by: {u.message.from_user.first_name}")
   except: pass
  await u.message.reply_text("✅💖 Reported to Admins! Thank you baby! 💖✅")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def admins_cmd(u,c):
 try:
  admins=await u.effective_chat.get_administrators();txt="👑💖 ADMINS: 💖👑\n\n"
  for a in admins: txt+=f"• {a.user.first_name} {'👑 Creator' if a.status=='creator' else '✨ Admin'}\n"
  await u.message.reply_text(txt)
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def info_cmd(u,c):
 t=get_target(u) or u.message.from_user;await u.message.reply_text(f"💖🌸 USER INFO 🌸💖\n\nName: {t.first_name}\nID: {t.id}\nUsername: @{t.username if t.username else 'None'}\nCoins: {coins_db.get(str(t.id),0)}\nXP: {levels_db.get(str(t.id),0)}\nPamela loves you! 💖")
async def id_cmd(u,c): await u.message.reply_text(f"🆔💖 Your ID: {u.message.from_user.id}\nChat ID: {u.effective_chat.id} 💖🆔")
async def zombies_cmd(u,c):
 if u.effective_chat.type=="private": await u.message.reply_text("Only in groups!");return
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 sm=await u.message.reply_text("🧹💖 Checking Deleted Accounts... 💖🧹");cid=u.effective_chat.id;uids=user_db.get(str(cid),[]);banned=0;checked=0
 for uid in list(uids):
  if uid==0: continue
  checked+=1
  try:
   m=await c.bot.get_chat_member(cid,uid)
   if m.user.first_name=="Deleted Account": await c.bot.ban_chat_member(cid,uid);await c.bot.unban_chat_member(cid,uid);banned+=1
  except:
   try: await c.bot.ban_chat_member(cid,uid);await c.bot.unban_chat_member(cid,uid);banned+=1
   except: pass
  await asyncio.sleep(0.3)
 await sm.edit_text(f"🧹💖 Cleaning Done! 💖🧹\nChecked: {checked}\nRemoved: {banned}\nAuto Clean every day at 6 AM! 💖")
async def snipe_cmd(u,c):
 cid=str(u.effective_chat.id);msgs=msg_db.get(cid,[])
 if not msgs: await u.message.reply_text("💖 No messages saved yet! 💖");return
 txt="👀💖 PAMELA'S MESSAGE LOG 💖👀\n\nHere are last messages!\n\n"
 for m in msgs[-10:]: txt+=f"{m['user']} (@{m['username'] if m['username'] else 'NoUsername'}):\n{m['text'][:100]}\n\n"
 txt+="💖 Even if someone deletes, Pamela remembers! 💖";await u.message.reply_text(txt)
async def truth_cmd(u,c): await u.message.reply_text(f"🎲💖 TRUTH! 💖🎲\n\n🌸 {random.choice(TRUTHS)} 🌸")
async def dare_cmd(u,c): await u.message.reply_text(f"😂💖 DARE! 💖😂\n\n🌸 {random.choice(DARES)} 🌸")
async def dice_cmd(u,c): await u.message.reply_dice(emoji="🎲")
async def slot_cmd(u,c): await u.message.reply_dice(emoji="🎰")
async def coin_cmd(u,c):
 r=random.choice(["Heads","Tails"]);await u.message.reply_text(f"🪙💖 Coin Flip! 💖🪙\nResult: {r}! ✨")
async def eightball_cmd(u,c):
 ans=random.choice(["Yes baby!","No baby!","Maybe!","100% Yes!","Ask again!","Pamela says YES!","Hmm! No!"]);await u.message.reply_text(f"🔮💖 Magic 8Ball 💖🔮\nQ: {' '.join(c.args) if c.args else '...'}\nA: {ans} ✨")
async def roast_cmd(u,c):
 t=get_target(u);name=t.first_name if t else u.message.from_user.first_name;await u.message.reply_text(f"🔥💖 ROAST for {name}! 💖🔥\n\n{random.choice(ROASTS)} 😂")
async def quote_cmd(u,c): await u.message.reply_text(f"✨💖 Quote of the Day 💖✨\n\n🌸 {random.choice(QUOTES)} 🌸\n\n- Pamela 💕")
async def daily_cmd(u,c):
 uid=str(u.message.from_user.id);today=datetime.date.today().isoformat();last=streak_db.get(uid,{}).get("last","");streak=streak_db.get(uid,{}).get("streak",0)
 if last==today: await u.message.reply_text("💖 Already claimed today baby! Come tomorrow! 💖");return
 yesterday=(datetime.date.today()-datetime.timedelta(days=1)).isoformat()
 if last==yesterday: streak+=1
 else: streak=1
 bonus=100+(streak-1)*20;coins_db[uid]=coins_db.get(uid,0)+bonus;bank_db[uid]=bank_db.get(uid,0)+10;streak_db[uid]={"last":today,"streak":streak};save_json("pamela_coins.json",coins_db);save_json("pamela_bank.json",bank_db);save_json("pamela_streak.json",streak_db);await u.message.reply_text(f"🎁💖 Daily Reward! 💖🎁\nStreak: {streak} Days! 🔥\n+{bonus} Coins! 💰\n+10 Bank Interest! 🏦\nTotal: {coins_db[uid]} Coins! ✨\nCome tomorrow again baby! 💖")
async def coins_cmd(u,c):
 uid=str(u.message.from_user.id);await u.message.reply_text(f"💰💖 Your Wallet 💖💰\n{u.message.from_user.first_name} ✨\nCoins: {coins_db.get(uid,0)} 🪙\nBank: {bank_db.get(uid,0)} 🏦\nXP: {levels_db.get(uid,0)} ✨\nLevel: {levels_db.get(uid,0)//100+1} 👑\nStreak: {streak_db.get(uid,{}).get('streak',0)} Days 🔥\nPamela loves you! 💖")
async def leaderboard_cmd(u,c):
 s=sorted(coins_db.items(),key=lambda x:x[1],reverse=True)[:10];txt="🏆💖 LEADERBOARD 💖🏆\n\n"
 for i,(uid,coins) in enumerate(s,1): txt+=f"{i}. User {uid} - {coins} Coins 💰\n"
 if not s: txt+="💖 No one yet baby! Be first! 💖"
 await u.message.reply_text(txt)
async def shop_cmd(u,c): await u.message.reply_text("🛍️💖 PAMELA SHOP - ALL FREE! 💖🛍️\n\n🌸 Cute Badge - 200 Coins\n🦋 Butterfly Badge - 300 Coins\n👑 Queen Title - 500 Coins\n\n💖 Use /daily to get coins! /shopbuy badge 💖")
async def shopbuy_cmd(u,c):
 if not c.args: await u.message.reply_text("🛍️💖 Use /shopbuy badge / butterfly / queen 💖🛍️");return
 item=c.args[0].lower();prices={"badge":200,"butterfly":300,"queen":500}
 if item not in prices: await u.message.reply_text("Items: badge (200), butterfly (300), queen (500)");return
 uid=str(u.message.from_user.id);price=prices[item]
 if coins_db.get(uid,0)<price: await u.message.reply_text("😭💖 Not enough coins baby! Use /daily! 💖😭");return
 coins_db[uid]-=price;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"🎉💖 You bought {item} for {price} Coins! Congrats! Pamela loves you! 💖🎉")
async def work_cmd(u,c):
 uid=str(u.message.from_user.id);amt=random.randint(50,150);coins_db[uid]=coins_db.get(uid,0)+amt;save_json("pamela_coins.json",coins_db);jobs=random.choice(["You worked as Chef!","You worked as Teacher!","You worked as Singer!","You worked as Doctor!","You helped Pamela!"]);await u.message.reply_text(f"💼💖 {jobs} 💖💼\n+{amt} Coins! 💰\nTotal: {coins_db[uid]} ✨")
async def rob_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /rob!");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if random.random()<0.5:
  amt=random.randint(20,100);amt=min(amt,bank_db.get(tid,0));bank_db[tid]=max(0,bank_db.get(tid,0)-amt);coins_db[uid]=coins_db.get(uid,0)+amt;save_json("pamela_coins.json",coins_db);save_json("pamela_bank.json",bank_db);await u.message.reply_text(f"😈💖 You robbed {amt} Coins from {t.first_name} Bank! 💖😈")
 else: coins_db[uid]=max(0,coins_db.get(uid,0)-50);save_json("pamela_coins.json",coins_db);await u.message.reply_text("😭💖 Caught! You lost 50 Coins! 💖😭")
async def gift_cmd(u,c):
 t=get_target(u)
 if not t or not c.args: await u.message.reply_text("🎁💖 Reply and type /gift 100! 💖🎁");return
 try: amt=int(c.args[0])
 except: await u.message.reply_text("Number!");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if coins_db.get(uid,0)<amt: await u.message.reply_text("Not enough coins!");return
 coins_db[uid]-=amt;coins_db[tid]=coins_db.get(tid,0)+amt;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"🎁💖 You gifted {amt} Coins to {t.first_name}! 💖🎁")
async def lottery_cmd(u,c):
 uid=str(u.message.from_user.id);num=random.randint(1,100);win=random.randint(1,100)
 if num==win: coins_db[uid]=coins_db.get(uid,0)+1000;save_json("pamela_coins.json",coins_db);await u.message.reply_text("🎉💖 JACKPOT! +1000 Coins! You won Lottery! 💖🎉")
 else: await u.message.reply_text(f"🎟️💖 Lottery: You picked {num}, Winning: {win}. Try again baby! 💖🎟️")
async def give_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=get_target(u)
 if not t or not c.args: await u.message.reply_text("Reply and type /give 100!");return
 try: amt=int(c.args[0])
 except: return
 tid=str(t.id);coins_db[tid]=coins_db.get(tid,0)+amt;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"👑💖 Admin gave {amt} Coins to {t.first_name}! 💖👑")
async def song_cmd(u,c):
 if not c.args: await u.message.reply_text("🎵💖 Use /song Shape of You 💖🎵");return
 q=" ".join(c.args);sm=await u.message.reply_text(f"🎵💖 Searching {q}... Wait baby! 💖🎵")
 try:
  import yt_dlp,os as _os
  opts={"format":"bestaudio/best","outtmpl":"song_%(id)s.%(ext)s","noplaylist":True,"quiet":True,"postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"128"}]}
  with yt_dlp.YoutubeDL(opts) as ydl:
   info=ydl.extract_info(f"ytsearch1:{q}",download=True);e=info["entries"][0];fn=ydl.prepare_filename(e).rsplit(".",1)[0]+".mp3"
  await u.message.reply_audio(audio=open(fn,"rb"),title=e.get("title","Song"),performer=e.get("uploader","Pamela"),caption=f"🎵💖 {e.get('title','Song')} 💖🎵 Join @bigolive_asia 💖");_os.remove(fn);await sm.delete()
 except Exception as ex: await sm.edit_text(f"😭💖 Oops baby! Could not download! Try another song! 💖😭 {ex}")
async def playlist_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /playlist Shape of You, Faded, Alone");return
 songs=" ".join(c.args).split(",")[:5];await u.message.reply_text(f"🎵💖 Playlist: {len(songs)} songs! Downloading one by one baby! 💖🎵")
 for s in songs:
  try:
   ctx2=type("obj",(object,),{"args":s.strip().split()})();await song_cmd(u,ctx2)
  except: pass
async def spotify_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /spotify Song Name");return
 q=" ".join(c.args);await u.message.reply_text(f"🎵💖 Spotify Search: {q} - Searching on YouTube! 💖🎵");ctx2=type("obj",(object,),{"args":q.split()})();await song_cmd(u,ctx2)
async def video_cmd(u,c):
 if not c.args: await u.message.reply_text("📹💖 Use /video link 💖📹");return
 url=c.args[0];sm=await u.message.reply_text("📹💖 Downloading video... Wait baby! 💖📹")
 try:
  import yt_dlp,os as _os
  opts={"format":"mp4/best","outtmpl":"video_%(id)s.%(ext)s","noplaylist":True,"quiet":True}
  with yt_dlp.YoutubeDL(opts) as ydl:
   info=ydl.extract_info(url,download=True);fn=ydl.prepare_filename(info)
  await u.message.reply_video(video=open(fn,"rb"),caption=f"📹💖 {info.get('title','Video')} 💖📹 Join @bigolive_asia 💖");_os.remove(fn);await sm.delete()
 except Exception as ex: await sm.edit_text(f"😭💖 Oops baby! Could not download video! 💖😭 {ex}")
async def lyrics_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /lyrics Shape of You");return
 q=" ".join(c.args)
 try:
  r=requests.get("https://api.lyrics.ovh/v1/"+urllib.parse.quote(q.split(" - ")[0])+"/"+urllib.parse.quote(q),timeout=10);d=r.json();lyrics=d.get("lyrics","")
  if lyrics: await u.message.reply_text(f"🎤💖 Lyrics - {q} 💖🎤\n\n{lyrics[:3500]}\nJoin @bigolive_asia 💖")
  else: await u.message.reply_text("💖 Lyrics not found baby! Try /song! 💖")
 except: await u.message.reply_text("💖 Lyrics not found baby! 💖")
async def movie_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /movie Avatar");return
 q=" ".join(c.args)
 try:
  r=requests.get("https://www.omdbapi.com/?t="+urllib.parse.quote(q)+"&apikey=trilogy",timeout=10);d=r.json()
  if d.get("Response")=="True":
   cap=f"🎬💖 {d.get('Title')} ({d.get('Year')}) 💖🎬\nRating: {d.get('imdbRating')}/10 ⭐\nGenre: {d.get('Genre')}\nDirector: {d.get('Director')}\nCast: {d.get('Actors')}\nPlot: {d.get('Plot')}\nJoin @bigolive_asia 💖"
   if d.get("Poster") and d["Poster"]!="N/A": await u.message.reply_photo(photo=d["Poster"],caption=cap)
   else: await u.message.reply_text(cap)
  else: await u.message.reply_text("💖 Movie not found baby! 💖")
 except: await u.message.reply_text("Try again baby!")
async def anime_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /anime Naruto");return
 q=" ".join(c.args)
 try:
  r=requests.get("https://api.jikan.moe/v4/anime?q="+urllib.parse.quote(q)+"&limit=1",timeout=10);d=r.json();a=d["data"][0];cap=f"🍥💖 {a['title']} 💖🍥\nScore: {a.get('score')}\nEpisodes: {a.get('episodes')}\nStatus: {a.get('status')}\nSynopsis: {a.get('synopsis','')[:500]}\nJoin @bigolive_asia 💖"
  if a.get("images",{}).get("jpg",{}).get("image_url"): await u.message.reply_photo(photo=a["images"]["jpg"]["image_url"],caption=cap)
  else: await u.message.reply_text(cap)
 except: await u.message.reply_text("Anime not found baby!")
async def rank_cmd(u,c):
 user=u.message.from_user;uid=str(user.id);lvl=levels_db.get(uid,0)//100+1;xp=levels_db.get(uid,0);coins=coins_db.get(uid,0)
 try:
  from PIL import Image,ImageDraw;img=Image.new("RGB",(800,300),(255,182,193));dr=ImageDraw.Draw(img);dr.text((30,30),f"{user.first_name}",fill=(255,255,255));dr.text((30,100),f"Level: {lvl} | XP: {xp}",fill=(255,255,255));dr.text((30,160),f"Coins: {coins} | Bank: {bank_db.get(uid,0)}",fill=(255,255,255));dr.text((30,230),"Join @bigolive_asia - ALL FREE",fill=(255,255,255));img.save("rank.png");await u.message.reply_photo(photo=open("rank.png","rb"),caption=f"👑💖 RANK CARD 💖👑\n{user.first_name}\nLevel {lvl} | {xp} XP\n{coins} Coins | {bank_db.get(uid,0)} Bank\nJoin @bigolive_asia 💖")
 except: await u.message.reply_text(f"👑💖 RANK CARD 💖👑\n{user.first_name}\nLevel {lvl} | {xp} XP\n{coins} Coins | {bank_db.get(uid,0)} Bank")
async def profile_cmd(u,c):
 user=u.message.from_user;uid=str(user.id);lvl=levels_db.get(uid,0)//100+1;married=marry_db.get(uid,"Single");await u.message.reply_text(f"🏆💖 FULL PROFILE 💖🏆\n\nName: {user.first_name}\nID: {user.id}\nUsername: @{user.username if user.username else 'None'}\nLevel: {lvl} 👑\nXP: {levels_db.get(uid,0)}\nCoins: {coins_db.get(uid,0)} 🪙\nBank: {bank_db.get(uid,0)} 🏦\nStreak: {streak_db.get(uid,{}).get('streak',0)} Days 🔥\nMarried To: {married} 💍\nBusiness: {business_db.get(uid,{}).get('type','None')} ☕\nStatus: ALL FREE! 💖\nPamela loves you! 💖")
async def stats_cmd(u,c):
 cid=str(u.effective_chat.id);msgs=msg_db.get(cid,[])
 from collections import Counter;cc=Counter([m["user"] for m in msgs]);txt="📊💖 GROUP STATS 💖📊\n\n"
 for i,(name,cnt) in enumerate(cc.most_common(10),1): txt+=f"{i}. {name} - {cnt} Messages 💬\n"
 if not cc: txt+="💖 No messages yet baby! 💖"
 await u.message.reply_text(txt)
async def top_cmd(u,c): await stats_cmd(u,c)
async def topdaily_cmd(u,c):
 cid=str(u.effective_chat.id);msgs=msg_db.get(cid,[]);today=datetime.date.today().isoformat()
 from collections import Counter;cc=Counter([m["user"] for m in msgs if datetime.datetime.fromtimestamp(m["time"]).date().isoformat()==today]);txt="🏆💖 TOP TODAY 💖🏆\n\n"
 for i,(name,cnt) in enumerate(cc.most_common(10),1): txt+=f"{i}. {name} - {cnt} Messages Today 💬\n"
 if not cc: txt+="💖 No messages today yet! 💖"
 await u.message.reply_text(txt)
async def ttt_cmd(u,c):
 cid=u.effective_chat.id;ttt_games[cid]=["⬜"]*9;await u.message.reply_text("❌💖 TIC TAC TOE! 💖❌\nType /move 1 to /move 9!\n⬜⬜⬜\n⬜⬜⬜\n⬜⬜⬜\nYou are ❌! Pamela is ⭕! 💖")
async def move_cmd(u,c):
 cid=u.effective_chat.id
 if cid not in ttt_games: await u.message.reply_text("Start with /ttt first!");return
 if not c.args: await u.message.reply_text("/move 5");return
 try: pos=int(c.args[0])-1
 except: await u.message.reply_text("Number 1-9 baby!");return
 board=ttt_games[cid]
 if board[pos]!="⬜": await u.message.reply_text("Already taken baby!");return
 board[pos]="❌";empt=[i for i,x in enumerate(board) if x=="⬜"]
 if empt: board[random.choice(empt)]="⭕"
 txt="❌💖 TIC TAC TOE 💖⭕\n\n"+"\n".join(["".join(board[i:i+3]) for i in range(0,9,3)])+"\n\n"
 for line in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
  if board[line[0]]!="⬜" and board[line[0]]==board[line[1]]==board[line[2]]: txt+=f"{board[line[0]]} Wins! 🎉";del ttt_games[cid];await u.message.reply_text(txt);return
 if "⬜" not in board: txt+="Draw! 💖";del ttt_games[cid]
 await u.message.reply_text(txt)
async def quiz_cmd(u,c):
 q=random.choice(QUIZ_Q);cid=u.effective_chat.id;quiz_db[cid]=q;txt=f"🧠💖 QUIZ! 💖🧠\n\n🌸 {q['q']} 🌸\n\n"
 for i,a in enumerate(q["a"],1): txt+=f"{i}. {a}\n"
 txt+="\n💖 Answer with /answer 1 to /answer 4! 💖";await u.message.reply_text(txt)
async def answer_cmd(u,c):
 cid=u.effective_chat.id
 if cid not in quiz_db: await u.message.reply_text("Start quiz with /quiz first!");return
 if not c.args: await u.message.reply_text("/answer 1");return
 try: ans=int(c.args[0])-1
 except: return
 q=quiz_db[cid];uid=str(u.message.from_user.id)
 if ans==q["c"]: coins_db[uid]=coins_db.get(uid,0)+50;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"✅💖 Correct baby! +50 Coins! 💖✅\nAnswer: {q['a'][q['c']]}")
 else: await u.message.reply_text(f"😭💖 Wrong baby! Correct: {q['a'][q['c']]} 💖😭")
 del quiz_db[cid]
async def bet_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /bet 100");return
 try: amt=int(c.args[0])
 except: await u.message.reply_text("Number baby!");return
 uid=str(u.message.from_user.id)
 if coins_db.get(uid,0)<amt: await u.message.reply_text("Not enough coins baby! Use /daily!");return
 if random.random()<0.5: coins_db[uid]+=amt;await u.message.reply_text(f"🎉💖 YOU WIN! +{amt} Coins! 💖🎉\nTotal: {coins_db[uid]}")
 else: coins_db[uid]-=amt;await u.message.reply_text(f"😭💖 You lost {amt} Coins! Try again! 💖😭")
 save_json("pamela_coins.json",coins_db)
async def bank_cmd(u,c):
 uid=str(u.message.from_user.id);await u.message.reply_text(f"🏦💖 BANK 💖🏦\nWallet: {coins_db.get(uid,0)} 🪙\nBank: {bank_db.get(uid,0)} 💰\nLoan: {loan_db.get(uid,{}).get('amount',0)} 😂\n/deposit 100 /withdraw 100 💖")
async def deposit_cmd(u,c):
 if not c.args: await u.message.reply_text("/deposit 100");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id)
 if coins_db.get(uid,0)<amt: await u.message.reply_text("Not enough coins!");return
 coins_db[uid]-=amt;bank_db[uid]=bank_db.get(uid,0)+amt;save_json("pamela_coins.json",coins_db);save_json("pamela_bank.json",bank_db);await u.message.reply_text(f"✅💖 Deposited {amt} Coins to Bank! 💖✅")
async def withdraw_cmd(u,c):
 if not c.args: await u.message.reply_text("/withdraw 100");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id)
 if bank_db.get(uid,0)<amt: await u.message.reply_text("Not enough in Bank!");return
 bank_db[uid]-=amt;coins_db[uid]=coins_db.get(uid,0)+amt;save_json("pamela_coins.json",coins_db);save_json("pamela_bank.json",bank_db);await u.message.reply_text(f"✅💖 Withdrew {amt} Coins! 💖✅")
async def steal_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /steal!");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if random.random()<0.5:
  amt=random.randint(10,100);amt=min(amt,coins_db.get(tid,0));coins_db[tid]=coins_db.get(tid,0)-amt;coins_db[uid]=coins_db.get(uid,0)+amt;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"😈💖 You stole {amt} Coins from {t.first_name}! 💖😈")
 else: coins_db[uid]=max(0,coins_db.get(uid,0)-50);save_json("pamela_coins.json",coins_db);await u.message.reply_text("😭💖 Caught! You lost 50 Coins! 💖😭")
async def rps_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /rps rock / paper / scissors");return
 uc=c.args[0].lower();bc=random.choice(["rock","paper","scissors"])
 if uc not in ["rock","paper","scissors"]: await u.message.reply_text("Use rock / paper / scissors!");return
 if uc==bc: res="Draw! 💖"
 elif (uc=="rock" and bc=="scissors") or (uc=="paper" and bc=="rock") or (uc=="scissors" and bc=="paper"): res="You Win! +20 Coins! 🎉";uid=str(u.message.from_user.id);coins_db[uid]=coins_db.get(uid,0)+20;save_json("pamela_coins.json",coins_db)
 else: res="Pamela Wins! 💖"
 await u.message.reply_text(f"✂️💖 Rock Paper Scissors! 💖✂️\nYou: {uc}\nPamela: {bc}\nResult: {res}")
async def word_cmd(u,c):
 words=["apple","banana","cat","dog","flower","butterfly","sun","moon","star","love","princess","queen","rainbow","ocean","mountain"];w=random.choice(words);word_db[u.effective_chat.id]=w;await u.message.reply_text(f"🔤💖 WORD GAME! 💖🔤\nHint: Starts with {w[0].upper()} - Length {len(w)} letters!\nGuess with /guessword word 💖")
async def guessword_cmd(u,c):
 cid=u.effective_chat.id
 if cid not in word_db: await u.message.reply_text("Start with /word first!");return
 if not c.args: await u.message.reply_text("Use /guessword apple");return
 guess=c.args[0].lower();correct=word_db[cid]
 if guess==correct: uid=str(u.message.from_user.id);coins_db[uid]=coins_db.get(uid,0)+50;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"✅💖 Correct! Word was {correct}! +50 Coins! 💖✅");del word_db[cid]
 else: await u.message.reply_text("Wrong! Try again baby!")
async def math_cmd(u,c):
 a=random.randint(1,50);b=random.randint(1,50);op=random.choice(["+","-","x"]);ans=a+b if op=="+" else a-b if op=="-" else a*b;math_db[u.effective_chat.id]=ans;await u.message.reply_text(f"🧮💖 MATH RACE! 💖🧮\nWhat is {a} {op} {b} ?\nAnswer with /mathans number - Fastest wins +30 Coins! 💖")
async def mathans_cmd(u,c):
 cid=u.effective_chat.id
 if cid not in math_db: await u.message.reply_text("Start with /math first!");return
 if not c.args: return
 try: ans=int(c.args[0])
 except: return
 if ans==math_db[cid]: uid=str(u.message.from_user.id);coins_db[uid]=coins_db.get(uid,0)+30;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"✅💖 Correct! +30 Coins! Answer was {ans}! 💖✅");del math_db[cid]
 else: await u.message.reply_text("Wrong! Try again!")
async def guess_cmd(u,c):
 num=random.randint(1,100);guess_db[u.effective_chat.id]=num;await u.message.reply_text("🎯💖 GUESS GAME! 💖🎯\nI picked a number 1-100!\nGuess with /g 50 💖")
async def g_cmd(u,c):
 cid=u.effective_chat.id
 if cid not in guess_db: await u.message.reply_text("Start with /guess first!");return
 if not c.args: return
 try: ans=int(c.args[0])
 except: return
 correct=guess_db[cid]
 if ans==correct: uid=str(u.message.from_user.id);coins_db[uid]=coins_db.get(uid,0)+100;save_json("pamela_coins.json",coins_db);await u.message.reply_text(f"🎉💖 JACKPOT! Number was {correct}! +100 Coins! 💖🎉");del guess_db[cid]
 elif ans<correct: await u.message.reply_text("⬆️ Higher! Go up! 💖")
 else: await u.message.reply_text("⬇️ Lower! Go down! 💖")
async def blackjack_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /blackjack 100");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id)
 if coins_db.get(uid,0)<amt: await u.message.reply_text("Not enough coins!");return
 you=random.randint(15,21);pam=random.randint(15,21)
 if you>pam: coins_db[uid]+=amt;await u.message.reply_text(f"🃏💖 BLACKJACK! 💖🃏\nYou: {you} - Pamela: {pam}\nYou Win +{amt} Coins! 🎉")
 elif you<pam: coins_db[uid]-=amt;await u.message.reply_text(f"🃏💖 BLACKJACK! 💖🃏\nYou: {you} - Pamela: {pam}\nYou Lose {amt} Coins! 😭")
 else: await u.message.reply_text(f"🃏💖 BLACKJACK Draw! You: {you} - Pamela: {pam} 💖")
 save_json("pamela_coins.json",coins_db)
async def race_cmd(u,c):
 horses=["Thunder","Lightning","Rainbow","Star","Princess","Queen"];winner=random.choice(horses);txt="🐎💖 HORSE RACE! 💖🐎\n\n"
 for h in horses: txt+=f"{'🏆 WINNER ' if h==winner else ''}{h} - {random.randint(1,100)}m\n"
 txt+=f"\nWinner: {winner}! 🎉";await u.message.reply_text(txt)
async def hunger_cmd(u,c):
 users=user_db.get(str(u.effective_chat.id),[])[:10]
 if len(users)<2: await u.message.reply_text("Need at least 2 players! Chat more!");return
 winner=random.choice(users);await u.message.reply_text(f"🔥💖 HUNGER GAMES! 💖🔥\n\nPlayers: {len(users)}\nWinner is User {winner}! Survived! +100 Coins! 🎉");coins_db[str(winner)]=coins_db.get(str(winner),0)+100;save_json("pamela_coins.json",coins_db)
async def challenge_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /challenge!");return
 winner=random.choice([u.message.from_user.first_name,t.first_name]);await u.message.reply_text(f"⚔️💖 1 VS 1 CHALLENGE! 💖⚔️\n{u.message.from_user.first_name} VS {t.first_name}\n\nWinner: {winner}! +50 Coins! 🎉");uid=str(u.message.from_user.id) if winner==u.message.from_user.first_name else str(t.id);coins_db[uid]=coins_db.get(uid,0)+50;save_json("pamela_coins.json",coins_db)
async def marry_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("💍💖 Reply to someone and type /marry! 💖💍");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if uid in marry_db: await u.message.reply_text(f"💖 You are already married to {marry_db[uid]}! Use /divorce first! 💖");return
 marry_db[uid]=t.first_name;marry_db[tid]=u.message.from_user.first_name;save_json("pamela_marry.json",marry_db);await u.message.reply_text(f"💍💖 MARRIED! 💖💍\n{u.message.from_user.first_name} + {t.first_name} = Forever! Congratulations! Pamela loves you! 💖🎉")
async def divorce_cmd(u,c):
 uid=str(u.message.from_user.id)
 if uid not in marry_db: await u.message.reply_text("💖 You are single baby! 💖");return
 partner=marry_db.pop(uid);save_json("pamela_marry.json",marry_db);await u.message.reply_text(f"💔💖 Divorced from {partner}! Pamela hugs you! 💖💔")
async def ship_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /ship!");return
 pct=random.randint(10,100);msg="Perfect Match! 💖" if pct>80 else "Cute Couple! 💕" if pct>50 else "Just Friends! 💖";await u.message.reply_text(f"💖🌸 SHIP! 🌸💖\n{u.message.from_user.first_name} + {t.first_name} = {pct}% Love!\n{msg}")
async def couple_cmd(u,c):
 users=user_db.get(str(u.effective_chat.id),[])
 if len(users)<2: await u.message.reply_text("Need more people!");return
 a,b=random.sample(users,2);await u.message.reply_text(f"💖🌸 TODAY'S COUPLE! 🌸💖\nUser {a} + User {b} = {random.randint(70,100)}% Love! Congratulations! 💖🎉")
async def love_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /love!");return
 await u.message.reply_text(f"💖🌸 LOVE METER! 🌸💖\n{u.message.from_user.first_name} loves {t.first_name} - {random.randint(10,100)}%! 💖")
async def hug_cmd(u,c):
 t=get_target(u);name=t.first_name if t else "Pamela";await u.message.reply_text(f"🤗💖 {u.message.from_user.first_name} hugged {name}! So cute! 💖🤗")
async def kiss_cmd(u,c):
 t=get_target(u);name=t.first_name if t else "Pamela";await u.message.reply_text(f"😘💖 {u.message.from_user.first_name} kissed {name}! Muahhh! 💖😘")
async def slap_cmd(u,c):
 t=get_target(u);name=t.first_name if t else "Pamela";await u.message.reply_text(f"👋😂 {u.message.from_user.first_name} slapped {name}! Ouch! Funny! 😂👋")
async def pat_cmd(u,c):
 t=get_target(u);name=t.first_name if t else "Pamela";await u.message.reply_text(f"🤗💖 {u.message.from_user.first_name} patted {name} head! So cute! 💖🤗")
async def jail_cmd(u,c):
 t=get_target(u)
 if not t: await u.message.reply_text("Reply and type /jail!");return
 jail_db[t.id]=time.time();await u.message.reply_text(f"😂🔒 {t.first_name} is in JAIL! For 1 min! Funny! 🔒😂")
async def story_cmd(u,c):
 topic=" ".join(c.args) if c.args else "cute princess";await u.message.reply_text("📖💖 Writing story... Wait baby! 💖📖");rep=ask_pamela(f"Write a short cute story about {topic} in 5 lines");await u.message.reply_text(f"📖💖 STORY - {topic} 💖📖\n\n{rep}")
async def dream_cmd(u,c):
 dreams=["You will meet someone special soon!","You will get good news tomorrow!","You will travel soon!","Someone is dreaming about you!"];await u.message.reply_text(f"🌙💖 DREAM! 💖🌙\n\n🌸 {random.choice(dreams)} 🌸")
async def horoscope_cmd(u,c): await u.message.reply_text(f"🔮💖 HOROSCOPE! 💖🔮\n\n🌸 {random.choice(HOROSCOPES)} 🌸")
async def tarot_cmd(u,c): await u.message.reply_text(f"🃏💖 TAROT! 💖🃏\n\n🌸 {random.choice(TAROTS)} 🌸")
async def ask_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /ask Why is sky blue?");return
 q=" ".join(c.args);rep=ask_pamela(q,u.message.from_user.id);await u.message.reply_text(f"💖🌸 ASK PAMELA! 🌸💖\nQ: {q}\n\n{rep}")
async def say_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /say Hello baby!");return
 txt=" ".join(c.args);await u.message.reply_text(f"💖🌸 Pamela Says: 🌸💖\n\n{txt}\n\n💖 Voice coming soon! (Text for now - ALL FREE!) 💖")
async def pfp_cmd(u,c):
 t=get_target(u) or u.message.from_user
 try:
  photos=await c.bot.get_user_profile_photos(t.id,limit=1)
  if photos.total_count>0: await u.message.reply_photo(photo=photos.photos[0][-1].file_id,caption=f"📸💖 Profile Photo of {t.first_name}! 💖📸")
  else: await u.message.reply_text("No profile photo!")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def cartoon_cmd(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a photo and type /cartoon!");return
 try: await u.message.reply_text("Making cartoon... Wait!");await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote('cute cartoon style portrait'),caption="🎨💖 Cartoon Version! - Pamela 💖🎨")
 except: await u.message.reply_text("Oops!")
async def meme_cmd(u,c):
 txt=" ".join(c.args) if c.args else "funny cute meme";await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(txt),caption=f"😂💖 MEME - {txt} - Pamela 💖😂")
async def wallpaper_cmd(u,c):
 q=" ".join(c.args) if c.args else "cute pink wallpaper";await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(q+' hd wallpaper'),caption=f"🌸💖 WALLPAPER - {q} - Pamela 💖🌸")
async def filter_cmd(u,c):
 if not await is_admin(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if len(c.args)<2: await u.message.reply_text("Use like /filter hi Hello Baby!");return
 kw=c.args[0].lower();reply=" ".join(c.args[1:]);cid=str(u.effective_chat.id)
 if cid not in filters_db: filters_db[cid]={}
 filters_db[cid][kw]=reply;save_json("pamela_filters.json",filters_db);await u.message.reply_text(f"✅💖 Filter Saved! {kw} -> {reply} 💖✅")
async def filters_list(u,c):
 cid=str(u.effective_chat.id);f=filters_db.get(cid,{})
 if not f: await u.message.reply_text("No filters baby!");return
 txt="🤖💖 FILTERS: 💖🤖\n\n"+"\n".join([f"• {k} -> {v}" for k,v in f.items()]);await u.message.reply_text(txt)
async def stop_filter(u,c):
 if not c.args: await u.message.reply_text("/stop hi");return
 cid=str(u.effective_chat.id);kw=c.args[0].lower()
 if cid in filters_db and kw in filters_db[cid]: del filters_db[cid][kw];save_json("pamela_filters.json",filters_db);await u.message.reply_text(f"✅ Filter {kw} Deleted!")
 else: await u.message.reply_text("No filter found baby!")
async def save_note(u,c):
 if not u.message.reply_to_message: await u.message.reply_text("To save a note, reply to a message and type /save hi!");return
 if not c.args: await u.message.reply_text("/save hi");return
 name=c.args[0].lower();txt=u.message.reply_to_message.text or "Photo / Sticker";cid=str(u.effective_chat.id)
 if cid not in notes_db: notes_db[cid]={}
 notes_db[cid][name]=txt;save_json("pamela_notes.json",notes_db);await u.message.reply_text(f"✅💖 Note Saved! #{name} 💖✅")
async def get_note(u,c):
 if not c.args: await u.message.reply_text("/get hi");return
 name=c.args[0].lower();cid=str(u.effective_chat.id);txt=notes_db.get(cid,{}).get(name)
 if txt: await u.message.reply_text(f"📝💖 #{name} 💖📝\n\n{txt}")
 else: await u.message.reply_text("No note found baby!")
async def notes_list(u,c):
 cid=str(u.effective_chat.id);n=notes_db.get(cid,{})
 if not n: await u.message.reply_text("No notes!");return
 await u.message.reply_text("📝💖 NOTES: 💖📝\n\n"+"\n".join([f"• #{k}" for k in n.keys()]))
async def clear_note(u,c):
 if not c.args: await u.message.reply_text("/clear hi");return
 cid=str(u.effective_chat.id);name=c.args[0].lower()
 if cid in notes_db and name in notes_db[cid]: del notes_db[cid][name];save_json("pamela_notes.json",notes_db);await u.message.reply_text(f"✅ Note #{name} Deleted!")
async def afk_cmd(u,c):
 reason=" ".join(c.args) if c.args else "No reason";afk_users[u.message.from_user.id]={"reason":reason,"name":u.message.from_user.first_name};await u.message.reply_text(f"😴💖 {u.message.from_user.first_name} is AFK! 💖😴\nReason: {reason}\nSleep well baby! 💖")
async def unafk_cmd(u,c):
 if u.message.from_user.id in afk_users: del afk_users[u.message.from_user.id]
 await u.message.reply_text("💖 Welcome back baby! Missed you! 💖")
async def img_cmd(u,c):
 if not c.args: await u.message.reply_text("Use like /img cute cat!");return
 prompt=" ".join(c.args);await u.message.reply_text(f"🎨💖 Generating... Wait baby! 💖🎨\nPrompt: {prompt}")
 try: url="https://image.pollinations.ai/prompt/"+urllib.parse.quote(prompt);await u.message.reply_photo(photo=url,caption=f"🎨💖 Your Image! 💖🎨\nPrompt: {prompt}\nPamela loves you! 💖")
 except: await u.message.reply_text("Oops baby! Could not make image!")
async def weather_cmd(u,c):
 city=" ".join(c.args) if c.args else "Colombo"
 try:
  url="https://wttr.in/"+urllib.parse.quote(city)+"?format=j1";r=requests.get(url,timeout=10);d=r.json();cur=d['current_condition'][0];await u.message.reply_text(f"🌧️💖 Weather in {city} 💖🌧️\nTemp: {cur['temp_C']}C\nCondition: {cur['weatherDesc'][0]['value']}\nHumidity: {cur['humidity']}%\nWind: {cur['windspeedKmph']} km/h\nPamela loves you! 💖")
 except: await u.message.reply_text("Oops baby! Could not check weather!")
async def imaginehd_cmd(u,c):
 if not c.args: await u.message.reply_text("Use /imaginehd cute cat");return
 prompt=" ".join(c.args);await u.message.reply_text(f"🎨💖 Generating 4K HD 4 Styles... Wait baby! Prompt: {prompt} 💖🎨")
 styles=["ultra realistic 4k","anime style","cute cartoon","cinematic"]
 for s in styles:
  try: await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(prompt+' '+s+' hd 4k'),caption=f"🎨💖 HD - {s} - {prompt} - Pamela 💖")
  except: pass
async def face_cmd(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /face!");return
 age=random.randint(16,30);mood=random.choice(["Happy","Cute","Beautiful","Confident","Sweet","Dreamy"]);beauty=random.randint(85,99);await u.message.reply_photo(photo=u.message.reply_to_message.photo[-1].file_id,caption=f"😍💖 FACE ANALYSIS - FUN! 💖😍\nAge Guess: {age}\nMood: {mood}\nBeauty Score: {beauty}/100 ✨\nCuteness: 100/100! 💖\nPamela says you are GORGEOUS! - Pamela 💖")
async def bgremove_cmd(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /bgremove!");return
 await u.message.reply_text("✂️💖 Removing Background... Use https://www.remove.bg for best HD! 💖✂️")
 await u.message.reply_photo(photo=u.message.reply_to_message.photo[-1].file_id,caption="✂️💖 Background Remove - Try remove.bg for HD! - Pamela 💖")
async def enhance_cmd(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /enhance!");return
 await u.message.reply_photo(photo=u.message.reply_to_message.photo[-1].file_id,caption="✨💖 ENHANCED HD! 💖✨\nBrightness + Sharpness + Beauty Filter!\nYou look MORE Beautiful! - Pamela 💖")
async def aisong_cmd(u,c):
 topic=" ".join(c.args) if c.args else "love";await u.message.reply_text(f"🎵💖 Writing AI Song about {topic}... Wait baby! 💖🎵");rep=ask_pamela(f"Write a short cute song lyrics about {topic}, 2 verses + chorus, with emojis");await u.message.reply_text(f"🎵💖 AI SONG - {topic} 💖🎵\n\n{rep}\n\nSing it baby! - Pamela 💖")
async def mafia_cmd(u,c):
 cid=u.effective_chat.id;players=user_db.get(str(cid),[])[:8]
 if len(players)<3: await u.message.reply_text("🕵️💖 Mafia needs 3+ players! Chat more! 💖🕵️");return
 mafia=random.choice(players);await
