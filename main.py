import os,time,asyncio,requests,urllib.parse,random,json,datetime,subprocess,re,html,xml.etree.ElementTree as ET
from flask import Flask
from telegram import Update,ChatPermissions,InlineKeyboardButton as B,InlineKeyboardMarkup as M
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ChatMemberHandler,CallbackQueryHandler
from telegram.constants import ChatMemberStatus
T=os.getenv("BOT_TOKEN");PORT=int(os.getenv("PORT",10000));F=Flask(__name__)
@F.route("/")
def h(): return "Pamela Online!"
@F.route("/health")
def he(): return "OK",200
GG=[]
try:
 _g=os.getenv("GROUP_IDS","")
 if _g: GG=[int(x.strip()) for x in _g.split(",") if x.strip()]
except: GG=[]
A=set(GG);last={};COOL=15;warns={};afk={};filt={};notes={};coins={};levels={};users={};msgs={};bank={};quiz={};ttt={};mem={};streak={};marry={};guess={};math={};word={};welcome={};rules={};bday={};busi={};stock={};loan={};event={}
def LJ(f,d):
 try:
  if os.path.exists(f):
   with open(f) as x: return json.load(x)
 except: pass
 return d
def SJ(f,d):
 try:
  with open(f,"w") as x: json.dump(d,x)
 except: pass
users=LJ("pamela_users.json",{});msgs=LJ("pamela_messages.json",{});filt=LJ("pamela_filters.json",{});notes=LJ("pamela_notes.json",{});coins=LJ("pamela_coins.json",{});levels=LJ("pamela_levels.json",{});bank=LJ("pamela_bank.json",{});mem=LJ("pamela_memory.json",{});streak=LJ("pamela_streak.json",{});marry=LJ("pamela_marry.json",{});welcome=LJ("pamela_welcome.json",{});rules=LJ("pamela_rules.json",{});bday=LJ("pamela_birthday.json",{});busi=LJ("pamela_business.json",{});stock=LJ("pamela_stock.json",{});loan=LJ("pamela_loan.json",{});event=LJ("pamela_event.json",{})
def SU(cid,uid):
 cid=str(cid)
 if cid not in users: users[cid]=[]
 if uid not in users[cid]: users[cid].append(uid);SJ("pamela_users.json",users)
def AC():
 s=set(A)
 for k in list(users.keys()):
  if str(k).lstrip("-").isdigit(): s.add(int(k))
 for g in GG: s.add(g)
 return list(s)
def SC(cid):
 try: A.add(int(cid));SU(cid,0)
 except: pass
def SM(cid,mid,uname,un,txt):
 cid=str(cid)
 if cid not in msgs: msgs[cid]=[]
 msgs[cid].append({"msg_id":mid,"user":uname,"username":un,"text":txt,"time":time.time()})
 if len(msgs[cid])>200: msgs[cid]=msgs[cid][-200:]
 SJ("pamela_messages.json",msgs)
def CL(cid):
 n=time.time();r=COOL-(n-last.get(cid,0))
 if r>0: return int(r)
 last[cid]=n;return 0
def TR(t,l):
 try:
  r=requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+l+"&dt=t&q="+urllib.parse.quote(t),timeout=10);d=r.json();return "".join([x[0] for x in d[0] if x[0]])
 except: return None
CS=["🌸💖 ","🦋✨ ","🌷💗 ","💖🌸 "];CE=["\n\n💖🌸 Love you, baby! 🌸💖","\n\n🦋💕 Pamela loves you! 💕🦋","\n\n🌸✨ Stay cute, baby! ✨🌸"]
def CU(r): return f"{random.choice(CS)}{r}{random.choice(CE)}"
def ASK(t,uid=None):
 try:
  m=""
  if uid:
   h=mem.get(str(uid),[])
   if h: m=" Past: "+" | ".join(h[-5:])
  p="You are Pamela, CUTEST princess! Use LOTS cute emojis EVERY sentence! Be super cute, soft, baby-talk. Call user baby,cutie. Use hehe,awww,hihi,yayyy,muahhh. Keep short max 3-4 lines. Reply in EXACT SAME language as user! "+m+f" User says: {t}"
  res=requests.get("https://text.pollinations.ai/"+urllib.parse.quote(p),timeout=60)
  if res.status_code==200:
   rep=res.text.strip()
   if rep:
    if uid:
     u=str(uid)
     if u not in mem: mem[u]=[]
     mem[u].append(f"User: {t} | Pamela: {rep[:100]}")
     if len(mem[u])>20: mem[u]=mem[u][-20:]
     SJ("pamela_memory.json",mem)
    return CU(rep)
   return "Sorry baby! I got shy! Try again?"
  elif res.status_code==402: return "Baby! I am tired! Wait 30 sec!"
  else: return "Oops baby! Sleepy! Try again!"
 except: return "Baby! Trouble! Try again!"
async def ADM(u,uid):
 try:
  m=await u.effective_chat.get_member(uid);return m.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]
 except: return False
def TG(u):
 if u.message.reply_to_message: return u.message.reply_to_message.from_user
 return None
TRUTHS=["Who is your crush?","Who did you lie to last?","Tell a secret you never told anyone!","What is last photo on your phone?","Who do you secretly love?","What is your biggest fear?","Have you ever cried for someone?","Who is most beautiful in group?","What is your dream?","Have you ever stalked your crush?"]
DARES=["Send a photo in group!","Message last person you chatted I Love You!","Say Hi in cute voice!","Type your crush name!","Send message using only emojis!","Change name to I Love Pamela for 1 hour!","Send voice singing!","Text your crush Hi now!"]
ROASTS=["Your face is like WiFi, everyone tries to connect but no signal!","Your brain is like Google, search and nothing comes up!","Even doctor was shocked on day you were born!"]
QUOTES=["Every flower blooms in its own time.","Be like butterfly, beautiful and free!","After every rain, there is rainbow!","You are loved more than you know!"]
BAD=["huththo","pakaya","kariya","wesi","ponnaya","balla","hukanna","fuck","bitch","shit"]
GM=["☀️🌸 Good Morning Babies! New day! New hope! Pamela wishes super day! Love you! - Pamela","🌷✨ Good Morning! You are all cute today! Keep smiling! - Pamela"]
GN=["🌙💖 Good Night Babies! Sweet dreams! Pamela loves you! Tomorrow meet again!","🌌✨ Good Night Cuties! Stars shining for you! Sleep well! - Pamela"]
QQ=[{"q":"What is capital of Sri Lanka?","a":["Colombo","Kandy","Galle","Jaffna"],"c":0},{"q":"What is 5 + 7?","a":["10","12","11","13"],"c":1},{"q":"Largest planet?","a":["Mars","Jupiter","Saturn","Earth"],"c":1},{"q":"What colour is sky?","a":["Green","Blue","Red","Pink"],"c":1},{"q":"Who is Pamela?","a":["Queen","Bot","Princess","All of above"],"c":3},{"q":"What is 10 x 10?","a":["100","90","110","1000"],"c":0}]
HORO=["Aries: Today lucky! Love near!","Taurus: Money coming! Stay calm!","Gemini: Someone likes you secretly!","Cancer: Family time! Hug them!","Leo: You will shine today!","Virgo: Work hard, reward coming!","Libra: Balance! Love will find you!","Scorpio: Mystery! Someone thinking of you!","Sagittarius: Adventure day!","Capricorn: Success near!","Aquarius: New friend coming!","Pisces: Dream big!"]
TAROT=["The Star - Hope and dreams!","The Lovers - Love coming!","The Sun - Happiness!","The Moon - Trust your heart!","Strength - You are strong!","Wheel of Fortune - Lucky day!"]
RIDD=[{"q":"I speak without a mouth and hear without ears. What am I?","a":"echo"},{"q":"What has keys but can't open locks?","a":"piano"},{"q":"What gets wetter the more it dries?","a":"towel"},{"q":"What has a face and two hands but no arms or legs?","a":"clock"},{"q":"What comes once in a minute, twice in a moment, but never in a thousand years?","a":"m"}]
WYR=["Would you rather be rich or famous?","Would you rather fly or be invisible?","Would you rather have super strength or super speed?","Would you rather live in beach or mountain?","Would you rather be Pamela's best friend forever or have 1 million coins?"]
NEVER=["Never have I ever lied to my best friend.","Never have I ever stalked my crush.","Never have I ever cried watching a movie.","Never have I ever eaten in class.","Never have I ever pretended to be sick to skip school."]
YC="https://www.youtube.com/channel/UCR4MDIWLNe4p_J-RP0dnS5g";YID="UCR4MDIWLNe4p_J-RP0dnS5g";YW="https://pamelacullen.onrender.com/";YWT=f"\n\n🌐 Join Our Website:\n👇 Click Here Baby! 👇\n{YW}\n💖 Pamela's World - Stay Cute, Stay Loved! 🌸";YL={"id":None};YV={"videos":[],"time":0,"latest":None,"latest_time":0};YCS=300
def YCV(t): return (time.time()-t)<YCS
def YCT(r):
 r=(r or "Pamela Video").strip()
 if len(r)>80: r=r[:77]+"..."
 return html.escape(r)
def YTH(v): return f"https://i.ytimg.com/vi/{v}/hqdefault.jpg" if v else ""
def YTL(v): return [f"https://i.ytimg.com/vi/{v}/hqdefault.jpg"] if v else []
def YFR():
 try:
  r=requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={YID}",timeout=10,headers={"User-Agent":"Mozilla/5.0"})
  if r.status_code==200 and r.content and b"<entry" in r.content: return r.content
 except: pass
 return None
def YFI(c=10):
 for b in ["https://yewtu.be","https://inv.us.projectsegfau.lt"]:
  try:
   r=requests.get(f"{b}/api/v1/channels/{YID}/videos",timeout=10,headers={"User-Agent":"Mozilla/5.0"})
   if r.status_code==200:
    d=r.json();v=[]
    for it in d[:c]:
     vid=it.get("videoId")
     if not vid: continue
     v.append({"title":it.get("title","Pamela Video"),"link":f"https://www.youtube.com/watch?v={vid}","id":vid,"thumb":f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"})
    if v: return v
  except: continue
 return []
def YFS(c=10):
 try:
  r=requests.get(f"https://www.youtube.com/channel/{YID}/videos",timeout=15,headers={"User-Agent":"Mozilla/5.0"})
  if r.status_code!=200: return []
  ids=re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"',r.text);tls=re.findall(r'"title":{"simpleText":"([^"]+)"}',r.text);s=set();u=[]
  for vid in ids:
   if vid not in s: s.add(vid);u.append(vid)
   if len(u)>=c: break
  v=[]
  for i,vid in enumerate(u[:c]):
   t=tls[i] if i<len(tls) else "Pamela Video";t=t.replace("\\u0026","&").replace("\\u0027","'").replace("\\u0022",'"');v.append({"title":t,"link":f"https://www.youtube.com/watch?v={vid}","id":vid,"thumb":f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"})
  return v
 except: return []
def YGL():
 if YV["latest"] and YCV(YV["latest_time"]): return YV["latest"]
 try:
  ct=YFR()
  if ct:
   rt=ET.fromstring(ct);ns={'atom':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'};e=rt.find('atom:entry',ns)
   if e is not None:
    res={"title":e.find('atom:title',ns).text,"link":e.find('atom:link',ns).attrib['href'],"id":e.find('yt:videoId',ns).text,"thumb":YTH(e.find('yt:videoId',ns).text)};YV["latest"]=res;YV["latest_time"]=time.time();return res
 except: pass
 v=YFI(1)
 if v: YV["latest"]=v[0];YV["latest_time"]=time.time();return v[0]
 v=YFS(1)
 if v: YV["latest"]=v[0];YV["latest_time"]=time.time();return v[0]
 return None
def YGV(c=10):
 if YV["videos"] and YCV(YV["time"]) and len(YV["videos"])>=c: return YV["videos"][:c]
 vs=[]
 try:
  ct=YFR()
  if ct:
   rt=ET.fromstring(ct);ns={'atom':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'}
   for e in rt.findall('atom:entry',ns)[:c]:
    vs.append({"title":e.find('atom:title',ns).text,"link":e.find('atom:link',ns).attrib['href'],"id":e.find('yt:videoId',ns).text,"thumb":YTH(e.find('yt:videoId',ns).text)})
   if vs: YV["videos"]=vs;YV["time"]=time.time();return vs
 except: pass
 v=YFI(c)
 if v: YV["videos"]=v;YV["time"]=time.time();return v
 v=YFS(c)
 if v: YV["videos"]=v;YV["time"]=time.time();return v
 return []
async def YSP(bot,cid,th,cap,rm=None,vid=None):
 ths=YTL(vid) if vid else [th] if th else []
 for t in ths:
  try: return await bot.send_photo(chat_id=cid,photo=t,caption=cap,parse_mode="HTML",reply_markup=rm)
  except: continue
 return await bot.send_message(chat_id=cid,text=cap,parse_mode="HTML",disable_web_page_preview=False,reply_markup=rm)
async def YSS(mo,vd,rm=None):
 txt=f"🎬 <b>{YCT(vd['title'])}</b>\n\n👇 <b>Watch Now Baby! 👇</b>\n{vd['link']}"+YWT
 for th in YTL(vd.get("id")):
  try: await mo.reply_photo(photo=th,caption=txt,parse_mode="HTML",reply_markup=rm);return
  except: continue
 await mo.reply_text(txt,parse_mode="HTML",disable_web_page_preview=False,reply_markup=rm)
async def YSV(mo,cb=False):
 vs=YGV(10)
 if not vs:
  lo=YGL()
  if lo: vs=[lo]
 if not vs:
  await mo.reply_text(f"😢 <b>Videos loading Baby... Try again!</b> 🥺\n\n🎬 <b>Watch All My Videos Here Baby! 👇</b>\n{YC}\n\n🔗 <b>Channel:</b> {YC}"+YWT,parse_mode="HTML",disable_web_page_preview=False);return
 await mo.reply_text("🎬 <b>Latest 10 Videos:</b> 🎬"+YWT,parse_mode="HTML",disable_web_page_preview=True)
 for i,v in enumerate(vs,1):
  cap=f"🎬 <b>{i}. {YCT(v['title'])}</b>\n\n👇 <b>Watch Now Baby! 👇</b>\n{v['link']}"+YWT;ok=False
  for th in YTL(v.get("id")):
   try: await mo.reply_photo(photo=th,caption=cap,parse_mode="HTML");ok=True;break
   except: continue
  if not ok: await mo.reply_text(cap,parse_mode="HTML",disable_web_page_preview=False)
def YMK(): return M([[B("🌐 Join Our Website",url=YW)],[B("🎬 Latest Video",callback_data="yt_latest")],[B("🎥 All Videos",callback_data="yt_videos"),B("❤️ Subscribe",url=YC)],[B("🎮 Games",callback_data="yt_game"),B("📜 Rules",callback_data="yt_rules")],[B("💬 Chat With Pamela",callback_data="yt_chat")]])
def YBK(): return M([[B("🌐 Join Our Website",url=YW)],[B("🔙 Back to Menu",callback_data="yt_menu")]])
async def YST(u,c):
 vd=YGL();t1=("🌸✨・゜✧ <b>Welcome to My World</b> ✧゜・✨🌸\n━━━━━━━━━━━━━━━━━━━\n\n💖 <b>Hi Baby! I'm Pamela 🥰</b>\n🌹 <b>Your Cutest Live Streamer from Colombia 🇨🇴</b>\n🎂 <b>20 Years Old | Sweet, Cute &amp; Full of Love 💕</b>\n🔴 <b>I Go LIVE Every Day! Come Talk With Me!</b>\n💬 <b>Let's Laugh, Chat &amp; Be Best Friends Forever! 🫶</b>\n\n━━━━━━━━━━━━━━━━━━━"+YWT);await u.message.reply_text(t1,parse_mode="HTML",disable_web_page_preview=True)
 if vd: await YSS(u.message,vd)
 else: await u.message.reply_text(f"🎬 <b>Latest Video:</b>\n👇 <b>Watch My Videos Here Baby! 👇</b>\n{YC}"+YWT,parse_mode="HTML",disable_web_page_preview=False)
 t3=("━━━━━━━━━━━━━━━━━━━\n💌 <i>\"You made my day by coming here! I love you so much!\" 💖</i>\n\n👇 <b>My Videos Are Here Baby! 👇</b>\n\n💬 <b>You Can Chat With Me Anytime!</b>\nJust tag me in the group and talk to me! 🥰\n\n🌸 Love You All! 🌸💖"+YWT);await u.message.reply_text(t3,parse_mode="HTML",disable_web_page_preview=True,reply_markup=YMK())
async def YLT(u,c):
 vd=YGL()
 if vd:
  txt=f"🎬 <b>Latest Video:</b>\n<b>{YCT(vd['title'])}</b>\n\n👇 <b>Watch Now:</b>\n{vd['link']}"+YWT
  try: await u.message.reply_photo(photo=vd["thumb"],caption=txt,parse_mode="HTML",reply_markup=YBK());return
  except: pass
  await u.message.reply_text(txt,parse_mode="HTML",disable_web_page_preview=False,reply_markup=YBK())
 else: await u.message.reply_text(f"😢 Sorry, Video loading Baby! 🥺\n\n🎬 <b>Watch Here:</b>\n{YC}"+YWT,parse_mode="HTML",disable_web_page_preview=False)
async def YVD(u,c): await YSV(u.message)
async def YSU(u,c): await u.message.reply_text(f"❤️ <b>Pamela Cullen Channel</b>\n\n🔗 {YC}\n\nPlease Subscribe &amp; Support Me! 🥰💖"+YWT,parse_mode="HTML",disable_web_page_preview=True,reply_markup=YBK())
async def YBH(u,c):
 q=u.callback_query;await q.answer();d=q.data
 if d=="yt_latest":
  vd=YGL()
  if vd:
   txt=f"🎬 <b>Latest Video:</b>\n<b>{YCT(vd['title'])}</b>\n\n👇 <b>Watch Now:</b>\n{vd['link']}"+YWT
   try: await q.message.reply_photo(photo=vd["thumb"],caption=txt,parse_mode="HTML",reply_markup=YBK());return
   except: pass
   await q.message.reply_text(txt,parse_mode="HTML",disable_web_page_preview=False,reply_markup=YBK())
  else: await q.message.reply_text(f"😢 No video found! Try again Baby!\n\n🎬 <b>Watch Here:</b>\n{YC}"+YWT,parse_mode="HTML",disable_web_page_preview=False)
 elif d=="yt_videos": await YSV(q.message,True);await q.message.reply_text("👆 <b>Above are the Latest 10 Videos Baby!</b> 🥰"+YWT,parse_mode="HTML",reply_markup=YBK())
 elif d=="yt_game": await q.message.reply_text("🎮 <b>Pamela Game Zone!</b>\n\n🎲 /dice\n✂️ /rps rock\n🔢 /guess\n❤️ /love A B\n💬 /quote"+YWT,parse_mode="HTML",reply_markup=YBK())
 elif d=="yt_rules": await q.message.reply_text("📜 <b>Group Rules - Pamela's House:</b>\n\n1. Be Kind 💖\n2. No Spam 🚫\n3. No Bad Words 🙏\n4. Love Pamela & Subscribe! ❤️\n5. Have Fun!"+YWT,parse_mode="HTML",reply_markup=YBK())
 elif d=="yt_chat": await q.message.reply_text("Hiii my love! 🥰💖 How are you? I missed you so much! Tell me, what game do you like? 🎮"+YWT,reply_markup=YBK())
 elif d=="yt_menu":
  vd=YGL();txt="🌸 <b>Pamela Menu</b> 🌸\n\n"
  if vd: txt+=f"🎬 <b>Latest:</b> {YCT(vd['title'])}\n{vd['link']}\n\n"
  else: txt+=f"🎬 <b>Channel:</b> {YC}\n\n"
  txt+="👇 Choose one baby! 👇"+YWT;await q.message.reply_text(txt,parse_mode="HTML",disable_web_page_preview=False,reply_markup=YMK())
async def YCN(ctx):
 ch=[x.strip() for x in os.getenv("CHANNEL_IDS","").split(",") if x.strip()] or [str(x) for x in GG]
 if not ch: return
 vd=YGL()
 if not vd: return
 if YL["id"] is None: YL["id"]=vd["id"];return
 if vd["id"]!=YL["id"]:
  YL["id"]=vd["id"];t1=("🌸✨・゜✧・゜✧・゜✧・゜✧🌸\n🔥 <b>NEW VIDEO IS OUT BABY! 🔥</b>\n🌸✨・゜✧・゜✧・゜✧・゜✧🌸\n━━━━━━━━━━━━━━━━━━━\n\n💖 <b>Hi Baby! I'm Pamela 🥰</b>\n🌹 <b>Your Cutest Live Streamer from Colombia 🇨🇴</b>\n🎂 <b>20 Years Old | Sweet, Cute &amp; Full of Love 💕</b>\n🔴 <b>I Go LIVE Every Day! Come Talk With Me!</b>\n💬 <b>Let's Laugh, Chat &amp; Be Best Friends Forever! 🫶</b>"+YWT);cap=f"🎬 <b>My Latest Video Just Dropped! 🔥</b>\n📌 {YCT(vd['title'])}\n\n👇 <b>Watch Now Baby! 👇</b>\n{vd['link']}"+YWT;t3="━━━━━━━━━━━━━━━━━━━\n💌 <i>Go watch it now baby! Like &amp; Comment!</i>\n💖 <i>I love you so much! You are my everything! 🥰❤️</i>"+YWT
  for CH in ch:
   try:
    try: await ctx.bot.unpin_all_chat_messages(chat_id=int(CH))
    except: pass
    await ctx.bot.send_message(chat_id=int(CH),text=t1,parse_mode="HTML",disable_web_page_preview=True);msg=await YSP(ctx.bot,int(CH),vd["thumb"],cap,vid_id=vd["id"]);await ctx.bot.send_message(chat_id=int(CH),text=t3,parse_mode="HTML",disable_web_page_preview=True)
    try: await ctx.bot.pin_chat_message(chat_id=int(CH),message_id=msg.message_id,disable_notification=True)
    except: pass
   except Exception as e: print(e)
async def YPR(ctx):
 ch=[x.strip() for x in os.getenv("CHANNEL_IDS","").split(",") if x.strip()] or [str(x) for x in GG]
 if not ch: return
 vd=YGL()
 if not vd: return
 pr=[("🌸✨ <b>Hey My Lovelies! ✨🌸</b>\n\n" f"🎬 <b>Have You Watched My Latest Video Yet?</b>\n📌 {YCT(vd['title'])}\n\n" "💖 <b>Go Watch It Now, My Love!</b>\nIt would mean the world to me! 🥰\n\n👍 <b>Don't Forget To:</b>\n❤️ <b>LIKE</b>\n💬 <b>COMMENT</b>\n🔔 <b>SUBSCRIBE</b>\n\n" f"👇 <b>Watch Here Baby! 👇</b>\n{vd['link']}\n\n" "💌 <i>I love you all so much! Thank you for supporting me! 🥰❤️</i>"+YWT),("🔥 <b>Hey Baby! Are You There? 🔥</b>\n\n" f"🎬 <b>My New Video Is Waiting For You!</b>\n📌 {YCT(vd['title'])}\n\n" "🥰 <b>Please Go Watch It Now!</b>\nYour love makes my day so special! ✨\n\n" f"👇 <b>Click Here To Watch:</b>\n{vd['link']}\n\n" "❤️ <b>LIKE + COMMENT + SUBSCRIBE</b>\n💖 <i>Every like is a kiss from you to me! 😘</i>"+YWT),("💖 <b>Hello My Beautiful Family! 💖</b>\n\n🌹 <b>I Made Something Special Just For You!</b>\n" f"🎬 {YCT(vd['title'])}\n\n" "✨ <b>Go Watch, Enjoy &amp; Show Me Some Love!</b>\n\n" f"🎥 <b>Watch Now:</b>\n{vd['link']}\n\n" "🫶 <b>Please:</b>\n👍 LIKE\n💬 COMMENT\n🔔 SUBSCRIBE\n\n🌸 <i>Love you forever! - Your Pamela 🥰</i>"+YWT)];txt=random.choice(pr)
 for CH in ch:
  try: await YSP(ctx.bot,int(CH),vd["thumb"],txt,vid_id=vd["id"])
  except: pass
async def START(u,c): SC(u.effective_chat.id);await u.message.reply_text("✨━━━━━━━━━━━━━━━━━━━✨\n🌸💖 WELCOME TO 💖🌸\n👑✨ PAMELA'S WORLD ✨👑\n✨━━━━━━━━━━━━━━━━━━━✨\n\n🦋💕 Hello, My Lovely Friend! 💕🦋\n💖🌸 I am Pamela! Your cute little best friend! 🌸💖\n\n💬🌸 Talk to me anything baby! I am here for you! 🌸💬\n🌍✨ I can speak ANY language! ✨🌍\n🎁💖 ALL FREE! No VIP! No Premium! 💖🎁\n\n🌿💖 Add me to your group! 💖🌿\n💕 Join @bigolive_asia 💕\n\n✨💖 Made with love, just for YOU! 💖✨")
async def HELP(u,c): await u.message.reply_text("👑💖 PAMELA HELP - ALL FREE! 💖👑\n\n💬 CHAT: Just type! /ask /tr /story /say\n🎵 MUSIC: /song /video /lyrics /playlist /spotify\n🎬 MOVIE: /movie /anime\n📺 LIVE TV: /livetv /worldtv /sportstv /news /ytvideos /ytlatest /ytstart /ytsubs\n🎬 VIDEO EDIT: /trim /compress /toaudio /togif /slowmo /reverse /mutevideo\n🎨 AI: /imaginehd /face /bgremove /enhance /aisong /img\n🎤 AUDIO: /voice /sing /rap /shoutout /podcast /translatevoice\n🎬 AI VIDEO: /aivideo /talkingphoto /lipsync\n🎨 AI IMAGE: /faceswap /outfit /babyface /oldface /couplephoto\n🎮 GAMES: /truth /dare /dice /slot /coin /8ball /roast /quote /ttt /quiz /bet /rps /word /math /guess /blackjack /race /hunger /challenge /mafia /quizbattle /bingo /poker /uno /spin /wyr /never /riddle /chess /ludo\n🏏 LIVE: /cricket /football /crypto /gold /radio /weather\n📚 STUDY: /homework /dictionary /solve /tr\n💰 COINS: /daily /coins /leaderboard /bank /deposit /withdraw /steal /work /rob /gift /lottery /loan /business /stock /interest /shop\n💖 LOVE: /marry /divorce /ship /couple /love /hug /kiss /slap /pat /jail /lovecalc\n🛠️ TOOLS: /qr /password /shortlink /screenshot /pdf /sticker\n🛡️ MANAGE: /ban /kick /mute /warn /promote /pin /purge /del /lock /unlock /setwelcome /setrules /slowmode /report\n🤖 FILTERS: /filter /filters /stop\n📝 NOTES: /save /get /notes /clear\n😴 AFK: /afk /unafk\n🎂 SPECIAL: /birthday /reminder /poll /event /giveaway /horoscopedaily /dreammeaning /goodmorningphoto /welcomephoto /topweek /activecheck\n🏆 OTHER: /rank /profile /stats /top /topdaily /pfp /meme /wallpaper\n\n🌿💖 Join @bigolive_asia - ALL FREE! 💖🌿")
async def ABOUT(u,c): await u.message.reply_text("🌸💖 About Pamela 💖🌸\n\n👑✨ I am Pamela, Queen of Pamela's World! ✨👑\n🦋💕 I love flowers, butterflies, nature, and YOU! 💕🦋\n🌿💖 Join @bigolive_asia - ALL FREE! 💖🌿")
async def TRC(u,c):
 if not c.args: await u.message.reply_text("🌍💖 Use /tr en 💖🌍");return
 lang=c.args[0].lower();txt=""
 if u.message.reply_to_message and u.message.reply_to_message.text: txt=u.message.reply_to_message.text
 elif len(c.args)>1: txt=" ".join(c.args[1:])
 else: await u.message.reply_text("💖 Reply to a text baby! 💖");return
 tr=TR(txt,lang);await u.message.reply_text(f"🌍✨ Translated to {lang.upper()} ✨🌍:\n\n💖 {tr} 💖" if tr else "😭💖 Oops baby! Try again! 💖😭")
async def LIVETV(u,c): await u.message.reply_text("📺👑 PAMELA WORLD LIVE TV - ALL FREE! 👑📺\n\nSRI LANKA:\nHiru TV - https://www.youtube.com/@HiruTV/live\nSirasa TV - https://www.youtube.com/@SirasaTV/live\nDerana TV - https://www.youtube.com/@TVDerana/live\nITN - https://www.youtube.com/@ITNSriLanka/live\n\nNEWS:\nHiru News - https://www.youtube.com/@HiruNews/live\nNewsFirst - https://www.youtube.com/@NewsfirstLIVE/live\nAda Derana - https://www.youtube.com/@AdaDerana/live\n\nWORLD:\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\nFrance 24 - https://www.youtube.com/@FRANCE24English/live\nDW - https://www.youtube.com/@dwnews/live\n\nSPORTS:\nSky Sports Cricket - https://www.youtube.com/@SkySportsCricket/live\nESPN - https://www.youtube.com/@ESPN/live\nWWE - https://www.youtube.com/@WWE/live\nF1 - https://www.youtube.com/@F1/live\n\n💖🌸 Enjoy Baby! - Pamela 🌸💖\n🌿 Join @bigolive_asia 💖")
async def WORLDTV(u,c): await u.message.reply_text("🌍👑 PAMELA WORLD TV! 👑🌍\n\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\nAl Jazeera - https://www.youtube.com/@AlJazeeraEnglish/live\nSky News - https://www.youtube.com/@SkyNews/live\n\n💖🌸 Enjoy World TV Baby! - Pamela 🌸💖")
async def SPORTTV(u,c): await u.message.reply_text("🏏⚽ PAMELA SPORTS TV! ⚽🏏\n\nSky Sports Cricket - https://www.youtube.com/@SkySportsCricket/live\nESPN - https://www.youtube.com/@ESPN/live\nSky Sports Football - https://www.youtube.com/@SkySportsFootball/live\nWWE - https://www.youtube.com/@WWE/live\nF1 - https://www.youtube.com/@F1/live\n\n💖🌸 Enjoy Sports Baby! - Pamela 🌸💖")
async def NEWSC(u,c): await u.message.reply_text("📰🌍 LIVE NEWS WORLD! 🌍📰\n\nHiru News - https://www.youtube.com/@HiruNews/live\nNewsFirst - https://www.youtube.com/@NewsfirstLIVE/live\nAda Derana - https://www.youtube.com/@AdaDerana/live\nBBC - https://www.youtube.com/@BBCNews/live\nCNN - https://www.youtube.com/@CNN/live\n\n💖🌸 Stay Updated Baby! - Pamela 🌸💖")
async def DLVID(u):
 if not u.message.reply_to_message or not u.message.reply_to_message.video: await u.message.reply_text("💖 Reply to a Video and type command baby! 💖");return None
 f=await u.message.reply_to_message.video.get_file();p=f"edit_{u.message.from_user.id}.mp4";await f.download_to_drive(p);return p
async def TRIM(u,c):
 if not c.args or len(c.args)<2: await u.message.reply_text("✂️💖 Use Reply Video + /trim 0 5 💖✂️");return
 p=await DLVID(u)
 if not p: return
 try:
  s=c.args[0];d=c.args[1];o=f"trim_{u.message.from_user.id}.mp4";sm=await u.message.reply_text(f"✂️💖 Trimming {s}s to {d}s... Wait baby! 💖✂️");subprocess.run(["ffmpeg","-y","-ss",s,"-t",d,"-i",p,"-c","copy",o],capture_output=True);await u.message.reply_video(video=open(o,"rb"),caption=f"✂️💖 Trimmed Video! {s}s - {d}s - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"😭💖 Oops baby! {e} 💖😭")
async def COMP(u,c):
 p=await DLVID(u)
 if not p: return
 try:
  o=f"comp_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("📦💖 Compressing... Wait baby! 💖📦");subprocess.run(["ffmpeg","-y","-i",p,"-vcodec","libx264","-crf","28",o],capture_output=True);await u.message.reply_video(video=open(o,"rb"),caption="📦💖 Compressed Video! - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def TOAUD(u,c):
 p=await DLVID(u)
 if not p: return
 try:
  o=f"audio_{u.message.from_user.id}.mp3";sm=await u.message.reply_text("🎵💖 Extracting Audio... Wait baby! 💖🎵");subprocess.run(["ffmpeg","-y","-i",p,"-vn",o],capture_output=True);await u.message.reply_audio(audio=open(o,"rb"),caption="🎵💖 Audio from Video! - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def TOGIF(u,c):
 p=await DLVID(u)
 if not p: return
 try:
  o=f"gif_{u.message.from_user.id}.gif";sm=await u.message.reply_text("🎞️💖 Making GIF... Wait baby! 💖🎞️");subprocess.run(["ffmpeg","-y","-i",p,"-t","3","-vf","fps=10,scale=320:-1:flags=lanczos",o],capture_output=True);await u.message.reply_animation(animation=open(o,"rb"),caption="🎞️💖 GIF Made! - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def SLOWMO(u,c):
 p=await DLVID(u)
 if not p: return
 try:
  o=f"slow_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("🐢💖 Making Slow Motion... Wait baby! 💖🐢");subprocess.run(["ffmpeg","-y","-i",p,"-filter:v","setpts=2.0*PTS",o],capture_output=True);await u.message.reply_video(video=open(o,"rb"),caption="🐢💖 Slow Motion! - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def REV(u,c):
 p=await DLVID(u)
 if not p: return
 try:
  o=f"rev_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("🔄💖 Reversing... Wait baby! 💖🔄");subprocess.run(["ffmpeg","-y","-i",p,"-vf","reverse","-af","areverse",o],capture_output=True);await u.message.reply_video(video=open(o,"rb"),caption="🔄💖 Reversed Video! - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def MUTEVID(u,c):
 p=await DLVID(u)
 if not p: return
 try:
  o=f"mute_{u.message.from_user.id}.mp4";sm=await u.message.reply_text("🔇💖 Muting... Wait baby! 💖🔇");subprocess.run(["ffmpeg","-y","-i",p,"-c:v","copy","-an",o],capture_output=True);await u.message.reply_video(video=open(o,"rb"),caption="🔇💖 Muted Video! - Pamela 💖");os.remove(p);os.remove(o);await sm.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def BAN(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("🛡️💖 Only for Admins baby! 💖🛡️");return
 t=TG(u)
 if not t: await u.message.reply_text("💖 Reply and type /ban! 💖");return
 try: await u.effective_chat.ban_member(t.id);await u.message.reply_text(f"🚫💖 {t.first_name} Banned! 💖🚫")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def UNBAN(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /unban!");return
 try: await u.effective_chat.unban_member(t.id);await u.message.reply_text("💖 Unbanned baby! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def KICK(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /kick!");return
 try: await u.effective_chat.ban_member(t.id);await u.effective_chat.unban_member(t.id);await u.message.reply_text(f"💖 {t.first_name} Kicked! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def MUTE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /mute!");return
 try: await u.effective_chat.restrict_member(t.id,ChatPermissions(can_send_messages=False));await u.message.reply_text(f"🔇💖 {t.first_name} Muted! 💖🔇")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def UNMUTE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /unmute!");return
 try: await u.effective_chat.restrict_member(t.id,ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True));await u.message.reply_text(f"💖 {t.first_name} Unmuted! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def WARN(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /warn!");return
 cid=u.effective_chat.id
 if cid not in warns: warns[cid]={}
 warns[cid][t.id]=warns[cid].get(t.id,0)+1;cc=warns[cid][t.id]
 if cc>=3:
  try: await u.effective_chat.ban_member(t.id);await u.message.reply_text(f"🚫💖 {t.first_name} got 3 Warnings! Auto Ban! 💖🚫");warns[cid][t.id]=0
  except Exception as e: await u.message.reply_text(f"Oops! {e}")
 else: await u.message.reply_text(f"⚠️💖 {t.first_name} Warning {cc}/3! 💖⚠️")
async def PROMOTE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /promote!");return
 try: await u.effective_chat.promote_member(t.id,can_change_info=True,can_delete_messages=True,can_invite_users=True,can_restrict_members=True,can_pin_messages=True,can_promote_members=False);await u.message.reply_text(f"👑💖 {t.first_name} is now Admin! 💖👑")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def PIN(u,c):
 if not u.message.reply_to_message: await u.message.reply_text("📌💖 Reply and type /pin! 💖📌");return
 try: await u.message.reply_to_message.pin();await u.message.reply_text("📌💖 Pinned baby! 💖📌")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def DEL(u,c):
 if u.message.reply_to_message:
  try: await u.message.reply_to_message.delete();await u.message.delete()
  except: await u.message.reply_text("💖 Could not delete baby! 💖")
 else: await u.message.reply_text("💖 Reply and type /del! 💖")
async def PURGE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not u.message.reply_to_message: await u.message.reply_text("Reply and type /purge!");return
 try:
  s=u.message.reply_to_message.message_id;e=u.message.message_id;cnt=0
  for mid in range(s,e+1):
   try: await c.bot.delete_message(u.effective_chat.id,mid);cnt+=1
   except: pass
  m=await u.message.reply_text(f"🧹💖 Deleted {cnt} Messages! 💖🧹");await asyncio.sleep(3);await m.delete()
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def RULES(u,c):
 cid=str(u.effective_chat.id);cu=rules.get(cid,"");await u.message.reply_text(f"📜💖 GROUP RULES 💖📜\n\n{cu}" if cu else "📜💖 GROUP RULES 💖📜\n\n1. Be kind baby!\n2. No bad words!\n3. No spam!\n4. Respect everyone!\n5. Love Pamela's World!\n\n💖 Break rules = Warn / Ban! 💖")
async def SETRULES(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not c.args: await u.message.reply_text("Use /setrules Your rules here");return
 rules[str(u.effective_chat.id)]=" ".join(c.args);SJ("pamela_rules.json",rules);await u.message.reply_text("✅💖 Rules Updated baby! 💖✅")
async def SETWELCOME(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not c.args: await u.message.reply_text("Use /setwelcome Welcome text");return
 welcome[str(u.effective_chat.id)]=" ".join(c.args);SJ("pamela_welcome.json",welcome);await u.message.reply_text("✅💖 Welcome Updated! 💖✅")
async def TRUTH(u,c): await u.message.reply_text(f"🎲💖 TRUTH! 💖🎲\n\n🌸 {random.choice(TRUTHS)} 🌸")
async def DARE(u,c): await u.message.reply_text(f"😂💖 DARE! 💖😂\n\n🌸 {random.choice(DARES)} 🌸")
async def DICE(u,c): await u.message.reply_dice(emoji="🎲")
async def SLOT(u,c): await u.message.reply_dice(emoji="🎰")
async def COIN(u,c): await u.message.reply_text(f"🪙💖 Coin Flip! 💖🪙\nResult: {random.choice(['Heads','Tails'])}! ✨")
async def EIGHT(u,c): await u.message.reply_text(f"🔮💖 Magic 8Ball 💖🔮\nQ: {' '.join(c.args) if c.args else '...'}\nA: {random.choice(['Yes baby!','No baby!','Maybe!','100% Yes!','Ask again!','Pamela says YES!','Hmm! No!'])} ✨")
async def ROAST(u,c):
 t=TG(u);n=t.first_name if t else u.message.from_user.first_name;await u.message.reply_text(f"🔥💖 ROAST for {n}! 💖🔥\n\n{random.choice(ROASTS)} 😂")
async def QUOTE(u,c): await u.message.reply_text(f"✨💖 Quote of the Day 💖✨\n\n🌸 {random.choice(QUOTES)} 🌸\n\n- Pamela 💕")
async def DAILY(u,c):
 uid=str(u.message.from_user.id);today=datetime.date.today().isoformat();ld=streak.get(uid,{}).get("last","");st=streak.get(uid,{}).get("streak",0)
 if ld==today: await u.message.reply_text("💖 Already claimed today baby! Come tomorrow! 💖");return
 yest=(datetime.date.today()-datetime.timedelta(days=1)).isoformat();st=st+1 if ld==yest else 1;bonus=100+(st-1)*20;coins[uid]=coins.get(uid,0)+bonus;bank[uid]=bank.get(uid,0)+10;streak[uid]={"last":today,"streak":st};SJ("pamela_coins.json",coins);SJ("pamela_bank.json",bank);SJ("pamela_streak.json",streak);await u.message.reply_text(f"🎁💖 Daily Reward! 💖🎁\nStreak: {st} Days! 🔥\n+{bonus} Coins! 💰\n+10 Bank Interest! 🏦\nTotal: {coins[uid]} Coins! ✨\nCome tomorrow again baby! 💖")
async def COINS(u,c):
 uid=str(u.message.from_user.id);await u.message.reply_text(f"💰💖 Your Wallet 💖💰\n{u.message.from_user.first_name} ✨\nCoins: {coins.get(uid,0)} 🪙\nBank: {bank.get(uid,0)} 🏦\nXP: {levels.get(uid,0)} ✨\nLevel: {levels.get(uid,0)//100+1} 👑\nStreak: {streak.get(uid,{}).get('streak',0)} Days 🔥\nPamela loves you! 💖")
async def LEADER(u,c):
 s=sorted(coins.items(),key=lambda x:x[1],reverse=True)[:10];txt="🏆💖 LEADERBOARD 💖🏆\n\n"
 for i,(uid,co) in enumerate(s,1): txt+=f"{i}. User {uid} - {co} Coins 💰\n"
 await u.message.reply_text(txt if s else "💖 No one yet baby! Be first! 💖")
async def WORK(u,c):
 uid=str(u.message.from_user.id);amt=random.randint(50,150);coins[uid]=coins.get(uid,0)+amt;SJ("pamela_coins.json",coins);await u.message.reply_text(f"💼💖 {random.choice(['You worked as Chef!','You worked as Teacher!','You worked as Singer!','You worked as Doctor!','You helped Pamela!'])} 💖💼\n+{amt} Coins! 💰\nTotal: {coins[uid]} ✨")
async def BET(u,c):
 if not c.args: await u.message.reply_text("Use /bet 100");return
 try: amt=int(c.args[0])
 except: await u.message.reply_text("Number baby!");return
 uid=str(u.message.from_user.id)
 if coins.get(uid,0)<amt: await u.message.reply_text("Not enough coins baby! Use /daily!");return
 if random.random()<0.5: coins[uid]+=amt;await u.message.reply_text(f"🎉💖 YOU WIN! +{amt} Coins! 💖🎉\nTotal: {coins[uid]}")
 else: coins[uid]-=amt;await u.message.reply_text(f"😭💖 You lost {amt} Coins! Try again! 💖😭")
 SJ("pamela_coins.json",coins)
async def BANKC(u,c):
 uid=str(u.message.from_user.id);await u.message.reply_text(f"🏦💖 BANK 💖🏦\nWallet: {coins.get(uid,0)} 🪙\nBank: {bank.get(uid,0)} 💰\nLoan: {loan.get(uid,{}).get('amount',0)} 😂\n/deposit 100 /withdraw 100 💖")
async def DEP(u,c):
 if not c.args: await u.message.reply_text("/deposit 100");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id)
 if coins.get(uid,0)<amt: await u.message.reply_text("Not enough coins!");return
 coins[uid]-=amt;bank[uid]=bank.get(uid,0)+amt;SJ("pamela_coins.json",coins);SJ("pamela_bank.json",bank);await u.message.reply_text(f"✅💖 Deposited {amt} Coins to Bank! 💖✅")
async def WITH(u,c):
 if not c.args: await u.message.reply_text("/withdraw 100");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id)
 if bank.get(uid,0)<amt: await u.message.reply_text("Not enough in Bank!");return
 bank[uid]-=amt;coins[uid]=coins.get(uid,0)+amt;SJ("pamela_coins.json",coins);SJ("pamela_bank.json",bank);await u.message.reply_text(f"✅💖 Withdrew {amt} Coins! 💖✅")
async def SONG(u,c):
 if not c.args: await u.message.reply_text("🎵💖 Use /song Shape of You 💖🎵");return
 q=" ".join(c.args);sm=await u.message.reply_text(f"🎵💖 Searching {q}... Wait baby! 💖🎵")
 try:
  import yt_dlp,os as _os;opts={"format":"bestaudio/best","outtmpl":"song_%(id)s.%(ext)s","noplaylist":True,"quiet":True,"postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"128"}]}
  with yt_dlp.YoutubeDL(opts) as ydl:
   info=ydl.extract_info(f"ytsearch1:{q}",download=True);e=info["entries"][0];fn=ydl.prepare_filename(e).rsplit(".",1)[0]+".mp3"
  await u.message.reply_audio(audio=open(fn,"rb"),title=e.get("title","Song"),performer=e.get("uploader","Pamela"),caption=f"🎵💖 {e.get('title','Song')} 💖🎵 Join @bigolive_asia 💖");_os.remove(fn);await sm.delete()
 except Exception as ex: await sm.edit_text(f"😭💖 Oops baby! Could not download! Try another song! 💖😭 {ex}")
async def VIDEO(u,c):
 if not c.args: await u.message.reply_text("📹💖 Use /video link 💖📹");return
 url=c.args[0];sm=await u.message.reply_text("📹💖 Downloading video... Wait baby! 💖📹")
 try:
  import yt_dlp,os as _os;opts={"format":"mp4/best","outtmpl":"video_%(id)s.%(ext)s","noplaylist":True,"quiet":True}
  with yt_dlp.YoutubeDL(opts) as ydl:
   info=ydl.extract_info(url,download=True);fn=ydl.prepare_filename(info)
  await u.message.reply_video(video=open(fn,"rb"),caption=f"📹💖 {info.get('title','Video')} 💖📹 Join @bigolive_asia 💖");_os.remove(fn);await sm.delete()
 except Exception as ex: await sm.edit_text(f"😭💖 Oops baby! Could not download video! 💖😭 {ex}")
async def LYRICS(u,c):
 if not c.args: await u.message.reply_text("Use /lyrics Shape of You");return
 q=" ".join(c.args)
 try:
  r=requests.get("https://api.lyrics.ovh/v1/"+urllib.parse.quote(q.split(" - ")[0])+"/"+urllib.parse.quote(q),timeout=10);d=r.json();ly=d.get("lyrics","");await u.message.reply_text(f"🎤💖 Lyrics - {q} 💖🎤\n\n{ly[:3500]}\nJoin @bigolive_asia 💖" if ly else "💖 Lyrics not found baby! Try /song! 💖")
 except: await u.message.reply_text("💖 Lyrics not found baby! 💖")
async def MOVIE(u,c):
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
async def ANIME(u,c):
 if not c.args: await u.message.reply_text("Use /anime Naruto");return
 q=" ".join(c.args)
 try:
  r=requests.get("https://api.jikan.moe/v4/anime?q="+urllib.parse.quote(q)+"&limit=1",timeout=10);d=r.json();a=d["data"][0];cap=f"🍥💖 {a['title']} 💖🍥\nScore: {a.get('score')}\nEpisodes: {a.get('episodes')}\nStatus: {a.get('status')}\nSynopsis: {a.get('synopsis','')[:500]}\nJoin @bigolive_asia 💖"
  if a.get("images",{}).get("jpg",{}).get("image_url"): await u.message.reply_photo(photo=a["images"]["jpg"]["image_url"],caption=cap)
  else: await u.message.reply_text(cap)
 except: await u.message.reply_text("Anime not found baby!")
async def RANK(u,c):
 user=u.message.from_user;uid=str(user.id);lvl=levels.get(uid,0)//100+1;xp=levels.get(uid,0);co=coins.get(uid,0)
 try:
  from PIL import Image,ImageDraw;img=Image.new("RGB",(800,300),(255,182,193));dr=ImageDraw.Draw(img);dr.text((30,30),f"{user.first_name}",fill=(255,255,255));dr.text((30,100),f"Level: {lvl} | XP: {xp}",fill=(255,255,255));dr.text((30,160),f"Coins: {co} | Bank: {bank.get(uid,0)}",fill=(255,255,255));dr.text((30,230),"Join @bigolive_asia - ALL FREE",fill=(255,255,255));img.save("rank.png");await u.message.reply_photo(photo=open("rank.png","rb"),caption=f"👑💖 RANK CARD 💖👑\n{user.first_name}\nLevel {lvl} | {xp} XP\n{co} Coins | {bank.get(uid,0)} Bank\nJoin @bigolive_asia 💖")
 except: await u.message.reply_text(f"👑💖 RANK CARD 💖👑\n{user.first_name}\nLevel {lvl} | {xp} XP\n{co} Coins | {bank.get(uid,0)} Bank")
async def PROFILE(u,c):
 user=u.message.from_user;uid=str(user.id);lvl=levels.get(uid,0)//100+1;await u.message.reply_text(f"🏆💖 FULL PROFILE 💖🏆\n\nName: {user.first_name}\nID: {user.id}\nUsername: @{user.username if user.username else 'None'}\nLevel: {lvl} 👑\nXP: {levels.get(uid,0)}\nCoins: {coins.get(uid,0)} 🪙\nBank: {bank.get(uid,0)} 🏦\nStreak: {streak.get(uid,{}).get('streak',0)} Days 🔥\nMarried To: {marry.get(uid,'Single')} 💍\nBusiness: {busi.get(uid,{}).get('type','None')} ☕\nStatus: ALL FREE! 💖\nPamela loves you! 💖")
async def TTT(u,c):
 cid=u.effective_chat.id;ttt[cid]=["⬜"]*9;await u.message.reply_text("❌💖 TIC TAC TOE! 💖❌\nType /move 1 to /move 9!\n⬜⬜⬜\n⬜⬜⬜\n⬜⬜⬜\nYou are ❌! Pamela is ⭕! 💖")
async def MOVE(u,c):
 cid=u.effective_chat.id
 if cid not in ttt: await u.message.reply_text("Start with /ttt first!");return
 if not c.args: await u.message.reply_text("/move 5");return
 try: pos=int(c.args[0])-1
 except: await u.message.reply_text("Number 1-9 baby!");return
 b=ttt[cid]
 if b[pos]!="⬜": await u.message.reply_text("Already taken baby!");return
 b[pos]="❌";e=[i for i,x in enumerate(b) if x=="⬜"]
 if e: b[random.choice(e)]="⭕"
 txt="❌💖 TIC TAC TOE 💖⭕\n\n"+"\n".join(["".join(b[i:i+3]) for i in range(0,9,3)])+"\n\n"
 for line in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
  if b[line[0]]!="⬜" and b[line[0]]==b[line[1]]==b[line[2]]: txt+=f"{b[line[0]]} Wins! 🎉";del ttt[cid];await u.message.reply_text(txt);return
 if "⬜" not in b: txt+="Draw! 💖";del ttt[cid]
 await u.message.reply_text(txt)
async def QUIZ(u,c):
 q=random.choice(QQ);cid=u.effective_chat.id;quiz[cid]=q;txt=f"🧠💖 QUIZ! 💖🧠\n\n🌸 {q['q']} 🌸\n\n"
 for i,a in enumerate(q["a"],1): txt+=f"{i}. {a}\n"
 await u.message.reply_text(txt+"\n💖 Answer with /answer 1 to /answer 4! 💖")
async def ANSWER(u,c):
 cid=u.effective_chat.id
 if cid not in quiz: await u.message.reply_text("Start quiz with /quiz first!");return
 if not c.args: await u.message.reply_text("/answer 1");return
 try: ans=int(c.args[0])-1
 except: return
 q=quiz[cid];uid=str(u.message.from_user.id)
 if ans==q["c"]: coins[uid]=coins.get(uid,0)+50;SJ("pamela_coins.json",coins);await u.message.reply_text(f"✅💖 Correct baby! +50 Coins! 💖✅\nAnswer: {q['a'][q['c']]}")
 else: await u.message.reply_text(f"😭💖 Wrong baby! Correct: {q['a'][q['c']]} 💖😭")
 del quiz[cid]
async def RPS(u,c):
 if not c.args: await u.message.reply_text("Use /rps rock / paper / scissors");return
 uc=c.args[0].lower();bc=random.choice(["rock","paper","scissors"])
 if uc not in ["rock","paper","scissors"]: await u.message.reply_text("Use rock / paper / scissors!");return
 if uc==bc: res="Draw! 💖"
 elif (uc=="rock" and bc=="scissors") or (uc=="paper" and bc=="rock") or (uc=="scissors" and bc=="paper"): res="You Win! +20 Coins! 🎉";uid=str(u.message.from_user.id);coins[uid]=coins.get(uid,0)+20;SJ("pamela_coins.json",coins)
 else: res="Pamela Wins! 💖"
 await u.message.reply_text(f"✂️💖 Rock Paper Scissors! 💖✂️\nYou: {uc}\nPamela: {bc}\nResult: {res}")
async def WORD(u,c):
 w=random.choice(["apple","banana","cat","dog","flower","butterfly","sun","moon","star","love","princess","queen","rainbow","ocean","mountain"]);word[u.effective_chat.id]=w;await u.message.reply_text(f"🔤💖 WORD GAME! 💖🔤\nHint: Starts with {w[0].upper()} - Length {len(w)} letters!\nGuess with /guessword word 💖")
async def GUESSWORD(u,c):
 cid=u.effective_chat.id
 if cid not in word: await u.message.reply_text("Start with /word first!");return
 if not c.args: await u.message.reply_text("Use /guessword apple");return
 g=c.args[0].lower();cor=word[cid]
 if g==cor: uid=str(u.message.from_user.id);coins[uid]=coins.get(uid,0)+50;SJ("pamela_coins.json",coins);await u.message.reply_text(f"✅💖 Correct! Word was {cor}! +50 Coins! 💖✅");del word[cid]
 else: await u.message.reply_text("Wrong! Try again baby!")
async def MATH(u,c):
 a=random.randint(1,50);b=random.randint(1,50);op=random.choice(["+","-","x"]);ans=a+b if op=="+" else a-b if op=="-" else a*b;math[u.effective_chat.id]=ans;await u.message.reply_text(f"🧮💖 MATH RACE! 💖🧮\nWhat is {a} {op} {b} ?\nAnswer with /mathans number - Fastest wins +30 Coins! 💖")
async def MATHANS(u,c):
 cid=u.effective_chat.id
 if cid not in math: await u.message.reply_text("Start with /math first!");return
 if not c.args: return
 try: ans=int(c.args[0])
 except: return
 if ans==math[cid]: uid=str(u.message.from_user.id);coins[uid]=coins.get(uid,0)+30;SJ("pamela_coins.json",coins);await u.message.reply_text(f"✅💖 Correct! +30 Coins! Answer was {ans}! 💖✅");del math[cid]
 else: await u.message.reply_text("Wrong! Try again!")
async def GUESS(u,c):
 num=random.randint(1,100);guess[u.effective_chat.id]=num;await u.message.reply_text("🎯💖 GUESS GAME! 💖🎯\nI picked a number 1-100!\nGuess with /g 50 💖")
async def GCMD(u,c):
 cid=u.effective_chat.id
 if cid not in guess: await u.message.reply_text("Start with /guess first!");return
 if not c.args: return
 try: ans=int(c.args[0])
 except: return
 cor=guess[cid]
 if ans==cor: uid=str(u.message.from_user.id);coins[uid]=coins.get(uid,0)+100;SJ("pamela_coins.json",coins);await u.message.reply_text(f"🎉💖 JACKPOT! Number was {cor}! +100 Coins! 💖🎉");del guess[cid]
 elif ans<cor: await u.message.reply_text("⬆️ Higher! Go up! 💖")
 else: await u.message.reply_text("⬇️ Lower! Go down! 💖")
async def MARRY(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("💍💖 Reply to someone and type /marry! 💖💍");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if uid in marry: await u.message.reply_text(f"💖 You are already married to {marry[uid]}! Use /divorce first! 💖");return
 marry[uid]=t.first_name;marry[tid]=u.message.from_user.first_name;SJ("pamela_marry.json",marry);await u.message.reply_text(f"💍💖 MARRIED! 💖💍\n{u.message.from_user.first_name} + {t.first_name} = Forever! Congratulations! Pamela loves you! 💖🎉")
async def DIVORCE(u,c):
 uid=str(u.message.from_user.id)
 if uid not in marry: await u.message.reply_text("💖 You are single baby! 💖");return
 p=marry.pop(uid);SJ("pamela_marry.json",marry);await u.message.reply_text(f"💔💖 Divorced from {p}! Pamela hugs you! 💖💔")
async def SHIP(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /ship!");return
 pct=random.randint(10,100);msg="Perfect Match! 💖" if pct>80 else "Cute Couple! 💕" if pct>50 else "Just Friends! 💖";await u.message.reply_text(f"💖🌸 SHIP! 🌸💖\n{u.message.from_user.first_name} + {t.first_name} = {pct}% Love!\n{msg}")
async def LOVE(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /love!");return
 await u.message.reply_text(f"💖🌸 LOVE METER! 🌸💖\n{u.message.from_user.first_name} loves {t.first_name} - {random.randint(10,100)}%! 💖")
async def LOVEACT(u,c,txt):
 t=TG(u);n=t.first_name if t else "Pamela";await u.message.reply_text(txt.format(u=u.message.from_user.first_name,n=n))
async def HUG(u,c): await LOVEACT(u,c,"🤗💖 {u} hugged {n}! So cute! 💖🤗")
async def KISS(u,c): await LOVEACT(u,c,"😘💖 {u} kissed {n}! Muahhh! 💖😘")
async def SLAP(u,c): await LOVEACT(u,c,"👋😂 {u} slapped {n}! Ouch! Funny! 😂👋")
async def PAT(u,c): await LOVEACT(u,c,"🤗💖 {u} patted {n} head! So cute! 💖🤗")
async def JAIL(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /jail!");return
 await u.message.reply_text(f"😂🔒 {t.first_name} is in JAIL! For 1 min! Funny! 🔒😂")
async def STORY(u,c):
 topic=" ".join(c.args) if c.args else "cute princess";await u.message.reply_text("📖💖 Writing story... Wait baby! 💖📖");rep=ASK(f"Write a short cute story about {topic} in 5 lines");await u.message.reply_text(f"📖💖 STORY - {topic} 💖📖\n\n{rep}")
async def HORO(u,c): await u.message.reply_text(f"🔮💖 HOROSCOPE! 💖🔮\n\n🌸 {random.choice(HORO)} 🌸")
async def TAROTC(u,c): await u.message.reply_text(f"🃏💖 TAROT! 💖🃏\n\n🌸 {random.choice(TAROT)} 🌸")
async def ASKC(u,c):
 if not c.args: await u.message.reply_text("Use /ask Why is sky blue?");return
 q=" ".join(c.args);rep=ASK(q,u.message.from_user.id);await u.message.reply_text(f"💖🌸 ASK PAMELA! 🌸💖\nQ: {q}\n\n{rep}")
async def SAY(u,c):
 if not c.args: await u.message.reply_text("Use /say Hello baby!");return
 txt=" ".join(c.args);await u.message.reply_text(f"💖🌸 Pamela Says: 🌸💖\n\n{txt}\n\n💖 Voice coming soon! (Text for now - ALL FREE!) 💖")
async def PFP(u,c):
 t=TG(u) or u.message.from_user
 try:
  ph=await c.bot.get_user_profile_photos(t.id,limit=1)
  if ph.total_count>0: await u.message.reply_photo(photo=ph.photos[0][-1].file_id,caption=f"📸💖 Profile Photo of {t.first_name}! 💖📸")
  else: await u.message.reply_text("No profile photo!")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def IMG(u,c):
 if not c.args: await u.message.reply_text("Use like /img cute cat!");return
 pr=" ".join(c.args);await u.message.reply_text(f"🎨💖 Generating... Wait baby! 💖🎨\nPrompt: {pr}")
 try: await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(pr),caption=f"🎨💖 Your Image! 💖🎨\nPrompt: {pr}\nPamela loves you! 💖")
 except: await u.message.reply_text("Oops baby! Could not make image!")
async def WEATHER(u,c):
 city=" ".join(c.args) if c.args else "Colombo"
 try:
  r=requests.get("https://wttr.in/"+urllib.parse.quote(city)+"?format=j1",timeout=10);d=r.json();cur=d['current_condition'][0];await u.message.reply_text(f"🌧️💖 Weather in {city} 💖🌧️\nTemp: {cur['temp_C']}C\nCondition: {cur['weatherDesc'][0]['value']}\nHumidity: {cur['humidity']}%\nWind: {cur['windspeedKmph']} km/h\nPamela loves you! 💖")
 except: await u.message.reply_text("Oops baby! Could not check weather!")
async def IMAGINEHD(u,c):
 if not c.args: await u.message.reply_text("Use /imaginehd cute cat");return
 pr=" ".join(c.args);await u.message.reply_text(f"🎨💖 Generating 4K HD 4 Styles... Wait baby! Prompt: {pr} 💖🎨")
 for s in ["ultra realistic 4k","anime style","cute cartoon","cinematic"]:
  try: await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(pr+' '+s+' hd 4k'),caption=f"🎨💖 HD - {s} - {pr} - Pamela 💖")
  except: pass
async def FACE(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /face!");return
 await u.message.reply_photo(photo=u.message.reply_to_message.photo[-1].file_id,caption=f"😍💖 FACE ANALYSIS - FUN! 💖😍\nAge Guess: {random.randint(16,30)}\nMood: {random.choice(['Happy','Cute','Beautiful','Confident','Sweet','Dreamy'])}\nBeauty Score: {random.randint(85,99)}/100 ✨\nCuteness: 100/100! 💖\nPamela says you are GORGEOUS! - Pamela 💖")
async def MEME(u,c):
 txt=" ".join(c.args) if c.args else "funny cute meme";await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(txt),caption=f"😂💖 MEME - {txt} - Pamela 💖😂")
async def WALL(u,c):
 q=" ".join(c.args) if c.args else "cute pink wallpaper";await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote(q+' hd wallpaper'),caption=f"🌸💖 WALLPAPER - {q} - Pamela 💖🌸")
async def FILTC(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if len(c.args)<2: await u.message.reply_text("Use like /filter hi Hello Baby!");return
 kw=c.args[0].lower();reply=" ".join(c.args[1:]);cid=str(u.effective_chat.id)
 if cid not in filt: filt[cid]={}
 filt[cid][kw]=reply;SJ("pamela_filters.json",filt);await u.message.reply_text(f"✅💖 Filter Saved! {kw} -> {reply} 💖✅")
async def FILTL(u,c):
 cid=str(u.effective_chat.id);f=filt.get(cid,{});await u.message.reply_text("🤖💖 FILTERS: 💖🤖\n\n"+"\n".join([f"• {k} -> {v}" for k,v in f.items()]) if f else "No filters baby!")
async def STOPF(u,c):
 if not c.args: await u.message.reply_text("/stop hi");return
 cid=str(u.effective_chat.id);kw=c.args[0].lower()
 if cid in filt and kw in filt[cid]: del filt[cid][kw];SJ("pamela_filters.json",filt);await u.message.reply_text(f"✅ Filter {kw} Deleted!")
 else: await u.message.reply_text("No filter found baby!")
async def SAVEN(u,c):
 if not u.message.reply_to_message: await u.message.reply_text("To save a note, reply to a message and type /save hi!");return
 if not c.args: await u.message.reply_text("/save hi");return
 name=c.args[0].lower();txt=u.message.reply_to_message.text or "Photo / Sticker";cid=str(u.effective_chat.id)
 if cid not in notes: notes[cid]={}
 notes[cid][name]=txt;SJ("pamela_notes.json",notes);await u.message.reply_text(f"✅💖 Note Saved! #{name} 💖✅")
async def GETN(u,c):
 if not c.args: await u.message.reply_text("/get hi");return
 name=c.args[0].lower();cid=str(u.effective_chat.id);txt=notes.get(cid,{}).get(name);await u.message.reply_text(f"📝💖 #{name} 💖📝\n\n{txt}" if txt else "No note found baby!")
async def NOTESL(u,c):
 cid=str(u.effective_chat.id);n=notes.get(cid,{});await u.message.reply_text("📝💖 NOTES: 💖📝\n\n"+"\n".join([f"• #{k}" for k in n.keys()]) if n else "No notes!")
async def AFK(u,c):
 reason=" ".join(c.args) if c.args else "No reason";afk[u.message.from_user.id]={"reason":reason,"name":u.message.from_user.first_name};await u.message.reply_text(f"😴💖 {u.message.from_user.first_name} is AFK! 💖😴\nReason: {reason}\nSleep well baby! 💖")
async def UNAFK(u,c):
 if u.message.from_user.id in afk: del afk[u.message.from_user.id]
 await u.message.reply_text("💖 Welcome back baby! Missed you! 💖")
async def CRICKET(u,c):
 try:
  r=requests.get("https://www.cricbuzz.com/api/cricket/matches/list?matchState=live",timeout=10,headers={"User-Agent":"Mozilla/5.0"});d=r.json();ms=d.get("typeMatches",[]);txt="🏏🔥 LIVE CRICKET! 🔥🏏\n\n"
  for tm in ms:
   for sm in tm.get("seriesMatches",[]):
    for m in sm.get("seriesAdWrapper",{}).get("matches",[])[:3]: txt+=f"{m.get('matchInfo',{}).get('team1',{}).get('teamName','?')} vs {m.get('matchInfo',{}).get('team2',{}).get('teamName','?')} - {m.get('matchInfo',{}).get('status','Live')} 🏏\n"
  await u.message.reply_text(txt+"💖 Join @bigolive_asia 💖" if len(txt)>30 else "🏏 No Live Match Now Baby! Check Later! 💖")
 except: await u.message.reply_text("🏏 Live Cricket: Check https://www.cricbuzz.com/cricket-match/live-scores 💖")
async def FOOTBALL(u,c): await u.message.reply_text("⚽💖 LIVE FOOTBALL! 💖⚽\n\nCheck Live Scores:\nhttps://www.flashscore.com/football/\nhttps://www.livescore.com/\n\n💖 Enjoy Baby! - Pamela 💖")
async def CRYPTO(u,c):
 try:
  r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true",timeout=10);d=r.json();await u.message.reply_text(f"₿📈 CRYPTO LIVE! 📈₿\n\nBitcoin: ${d['bitcoin']['usd']:,.0f} ({d['bitcoin'].get('usd_24h_change',0):.2f}%)\nEthereum: ${d['ethereum']['usd']:,.0f} ({d['ethereum'].get('usd_24h_change',0):.2f}%)\n\n💖 Pamela Loves Crypto! 💖")
 except: await u.message.reply_text("₿ Crypto: Bitcoin ~ $95,000 - Check CoinGecko! 💖")
async def GOLD(u,c): await u.message.reply_text("🥇✨ GOLD PRICE! ✨🥇\n\nGold: ~ $2,600 / oz\nSri Lanka 22K: ~ Rs. 38,500 / Sovereign\n\n💖 Check https://www.goldprice.org 💖")
async def RADIO(u,c): await u.message.reply_text("📻🎵 LIVE RADIO! 🎵📻\n\nHiru FM - https://www.hirufm.lk\nY FM - https://www.yfm.lk\nKiss 899 - https://www.kiss899.com\nGold FM - https://www.goldfm.lk\n\n💖 Enjoy Music Baby! - Pamela 💖")
async def HOMEWORK(u,c):
 if not c.args: await u.message.reply_text("Use /homework What is 5+5?");return
 q=" ".join(c.args);rep=ASK(f"Explain homework simply: {q}");await u.message.reply_text(f"📚✨ HOMEWORK HELP! ✨📚\nQ: {q}\n\n{rep}")
async def DICT(u,c):
 if not c.args: await u.message.reply_text("Use /dictionary love");return
 w=c.args[0]
 try:
  r=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(w)}",timeout=10);d=r.json();m=d[0]["meanings"][0]["definitions"][0]["definition"];await u.message.reply_text(f"📖💖 DICTIONARY - {w} 💖📖\n\n{w}: {m}\n\n💖 Pamela Loves Words! 💖")
 except: await u.message.reply_text("Word not found baby!")
async def SOLVE(u,c):
 if not c.args: await u.message.reply_text("Use /solve 2+2");return
 ex=" ".join(c.args)
 try:
  res=eval(ex.replace("x","*").replace("÷","/"),{"__builtins__":{}});await u.message.reply_text(f"🧮💕 SOLVED! 💕🧮\n{ex} = {res} ✨\nPamela is smart! 💖")
 except: await u.message.reply_text("Could not solve baby!")
async def LOAN(u,c):
 if not c.args: await u.message.reply_text("Use /loan 1000");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id);loan[uid]={"amount":amt};bank[uid]=bank.get(uid,0)+amt;SJ("pamela_loan.json",loan);SJ("pamela_bank.json",bank);await u.message.reply_text(f"🏦😂 LOAN APPROVED! 😂🏦\nYou got {amt} Coins! Return in 7 days with 10% interest! 💖")
async def BUSINESS(u,c):
 uid=str(u.message.from_user.id)
 if uid in busi: await u.message.reply_text(f"☕🔥 You already have {busi[uid].get('type')} business! 💖");return
 typ=random.choice(["Coffee Shop","Flower Shop","Bakery","Boutique"]);busi[uid]={"type":typ};SJ("pamela_business.json",busi);await u.message.reply_text(f"☕🔥 BUSINESS STARTED! 🔥☕\nYour Business: {typ}!\nCome daily to earn! Use /business again to collect! 💖")
async def STOCKM(u,c):
 uid=str(u.message.from_user.id);amt=random.randint(-50,100);coins[uid]=coins.get(uid,0)+amt;SJ("pamela_coins.json",coins);await u.message.reply_text(f"📈😂 STOCK MARKET! 😂📈\nYou {'gained' if amt>=0 else 'lost'} {abs(amt)} Coins!\nTotal: {coins[uid]} 💖")
async def BDAY(u,c):
 if not c.args: await u.message.reply_text("Use /birthday 12-05");return
 bday.setdefault(str(u.effective_chat.id),{})[str(u.message.from_user.id)]={"date":c.args[0],"name":u.message.from_user.first_name};SJ("pamela_birthday.json",bday);await u.message.reply_text(f"🎂🎉 Birthday Saved! {c.args[0]}! Pamela will wish you! 💖🎉")
async def REMIND(u,c):
 if len(c.args)<2: await u.message.reply_text("Use /reminder 10 hello");return
 try: sec=int(c.args[0])
 except: await u.message.reply_text("Number of seconds!");return
 txt=" ".join(c.args[1:]);await u.message.reply_text(f"⏰💖 Reminder set for {sec} sec! 💖⏰");await asyncio.sleep(sec);await u.message.reply_text(f"⏰💖 REMINDER! 💖⏰\n{txt}\nPamela reminds you! 💖")
async def POLL(u,c):
 if not c.args: await u.message.reply_text("Use /poll Q | Yes | No");return
 parts=" ".join(c.args).split("|");q=parts[0].strip();opts=[p.strip() for p in parts[1:]] or ["Yes","No"];await u.message.reply_poll(question=q[:300],options=opts[:10],allows_multiple_answers=False)
async def EVENT(u,c):
 if not c.args: await u.message.reply_text("Use /event Party | Tomorrow");return
 parts=" ".join(c.args).split("|");await u.message.reply_text(f"🎉💖 EVENT CREATED! 💖🎉\nEvent: {parts[0].strip()}\nWhen: {parts[1].strip() if len(parts)>1 else 'Soon'}\nJoin! Pamela loves events! 💖")
async def VOICE(u,c):
 txt=" ".join(c.args) if c.args else "Hi baby";await u.message.reply_text(f"🎤💖 Pamela AI Voice! 💖🎤\n\n\"{txt}\"\n\n💖 Voice feature: Use TTS link: https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(txt)}&tl=en&client=tw-ob 💖")
async def SING(u,c):
 topic=" ".join(c.args) if c.args else "love";rep=ASK(f"Write a short cute song lyrics about {topic}, 2 verses + chorus, with emojis");await u.message.reply_text(f"🎵💖 PAMELA SINGS - {topic} 💖🎵\n\n{rep}\n\nSing it baby! - Pamela 💖")
async def RAP(u,c): rep=ASK("Write a short funny cute rap about Pamela, 4 lines");await u.message.reply_text(f"🎤🔥 PAMELA RAP! 🔥🎤\n\n{rep}")
async def SHOUT(u,c):
 n=" ".join(c.args) if c.args else "Baby";await u.message.reply_text(f"📢💖 SHOUTOUT! 💖📢\n\nHey {n}! Pamela loves you! You are amazing! Shoutout to you! 💖🎉")
async def PODCAST(u,c):
 topic=" ".join(c.args) if c.args else "love";rep=ASK(f"Write a short podcast script about {topic}, 5 lines, cute");await u.message.reply_text(f"🎙️💖 PAMELA PODCAST - {topic} 💖🎙️\n\n{rep}")
async def AIVIDEO(u,c):
 pr=" ".join(c.args) if c.args else "cute cat";await u.message.reply_text(f"🎬🤖 AI VIDEO IDEA - {pr} 🤖🎬\n\nIdea: Cute {pr} dancing, with music, pink background!\n\n💖 Use CapCut / Pika to make it! Pamela loves you! 💖")
async def SPIN(u,c):
 prizes=["100 Coins","50 Coins","Jackpot 1000 Coins","Try Again","Free Hug","Pamela Kiss"];p=random.choice(prizes);await u.message.reply_text(f"🎡🔥 SPIN WHEEL! 🔥🎡\n\nYou got: {p}! 🎉")
async def WYRC(u,c): await u.message.reply_text(f"🤔💖 WOULD YOU RATHER! 💖🤔\n\n🌸 {random.choice(WYR)} 🌸")
async def NEVERC(u,c): await u.message.reply_text(f"🙈💖 NEVER HAVE I EVER! 💖🙈\n\n🌸 {random.choice(NEVER)} 🌸")
async def RIDDLEC(u,c):
 r=random.choice(RIDD);riddle[u.effective_chat.id]=r;await u.message.reply_text(f"🧩💖 RIDDLE! 💖🧩\n\n🌸 {r['q']} 🌸\n\nAnswer with /riddleans answer 💖")
async def RIDDLEANS(u,c):
 cid=u.effective_chat.id
 if cid not in riddle: await u.message.reply_text("Start with /riddle first!");return
 if not c.args: return
 g=" ".join(c.args).lower();cor=riddle[cid]["a"]
 if g==cor: await u.message.reply_text(f"✅ Correct! Answer was {cor}! +30 Coins! 💖");del riddle[cid]
 else: await u.message.reply_text("Wrong! Try again!")
async def CHESS(u,c): await u.message.reply_text("♟️💖 CHESS! 💖♟️\n\nPlay Online: https://www.chess.com/play\nChallenge a friend! Pamela watches! 💖")
async def LUDO(u,c): await u.message.reply_text("🎲💖 LUDO! 💖🎲\n\nPlay Online: https://www.ludo.com\nRoll: "+str(random.randint(1,6))+"! Pamela loves Ludo! 💖")
async def QR(u,c):
 txt=" ".join(c.args) if c.args else "Pamela";await u.message.reply_photo(photo=f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(txt)}",caption=f"📷💖 QR CODE - {txt} - Pamela 💖")
async def PASSWORD(u,c):
 import secrets,string;pw="".join(secrets.choice(string.ascii_letters+string.digits+"!@#") for _ in range(12));await u.message.reply_text(f"🔑💖 STRONG PASSWORD! 💖🔑\n\n{pw}\n\nKeep it secret baby! 💖")
async def SHORTLINK(u,c):
 if not c.args: await u.message.reply_text("Use /shortlink link");return
 url=c.args[0]
 try:
  r=requests.get(f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}",timeout=10);await u.message.reply_text(f"🔗💖 SHORT LINK! 💖🔗\n\n{r.text}\nPamela shortened it! 💖")
 except: await u.message.reply_text(f"🔗 Short: {url}")
async def SCREENSHOT(u,c):
 if not c.args: await u.message.reply_text("Use /screenshot link");return
 url=c.args[0];await u.message.reply_photo(photo=f"https://image.thum.io/get/width/800/crop/600/{urllib.parse.quote(url)}",caption=f"📸💖 SCREENSHOT - {url} - Pamela 💖")
async def PDF(u,c):
 txt=" ".join(c.args) if c.args else "Pamela loves you";await u.message.reply_text(f"📄💖 PDF CREATED! 💖📄\n\nContent: {txt}\n\n💖 Use https://www.ilovepdf.com to make PDF! Pamela loves you! 💖")
async def STICKER(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /sticker!");return
 await u.message.reply_sticker(sticker=u.message.reply_to_message.photo[-1].file_id)
async def HORODAILY(u,c): await u.message.reply_text(f"🔮💖 DAILY HOROSCOPE! 💖🔮\n\n🌸 {random.choice(HORO)} 🌸\n\nPamela wishes lucky day! 💖")
async def LOVECALC(u,c):
 if len(c.args)<2: await u.message.reply_text("Use /lovecalc A B");return
 a=c.args[0];b=c.args[1];pct=random.randint(50,100);await u.message.reply_text(f"💘💖 LOVE CALCULATOR! 💖💘\n\n{a} ❤️ {b} = {pct}% Love!\n{'Perfect Couple! 💍' if pct>90 else 'So Cute! 🥰' if pct>75 else 'Cute! Keep trying! 💗'}")
async def DREAM(u,c):
 topic=" ".join(c.args) if c.args else "dream";await u.message.reply_text(f"🌙💖 DREAM MEANING - {topic} 💖🌙\n\n🌸 {random.choice(['You will meet someone special soon!','You will get good news tomorrow!','You will travel soon!','Someone is dreaming about you!'])} 🌸")
async def GMPHOTO(u,c): await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote("cute good morning pink flowers"),caption="☀️💖 GOOD MORNING PHOTO! 💖☀️\nGood Morning Baby! Pamela loves you! 💖")
async def WELCOMEPHOTO(u,c): await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote("cute welcome pink"),caption="📸💖 WELCOME PHOTO! 💖📸\nWelcome Baby! Pamela loves you! 💖")
async def TOPWEEK(u,c):
 cid=str(u.effective_chat.id);ms=msgs.get(cid,[])
 from collections import Counter;cc=Counter([m["user"] for m in ms]);txt="📊💖 TOP OF WEEK 💖📊\n\n"
 for i,(n,cnt) in enumerate(cc.most_common(10),1): txt+=f"{i}. {n} - {cnt} Messages 💬\n"
 await u.message.reply_text(txt if cc else "💖 No messages yet baby! 💖")
async def ACTIVECHECK(u,c):
 cid=str(u.effective_chat.id);ms=msgs.get(cid,[]);await u.message.reply_text(f"👀💖 ACTIVE CHECK! 💖👀\n\nTotal Messages: {len(ms)}\nActive Users: {len(set([m['user'] for m in ms]))}\nPamela is watching! 💖")
async def GIVEAWAY(u,c):
 prize=" ".join(c.args) if c.args else "Pamela Hug";await u.message.reply_text(f"🎁💖 GIVEAWAY! 💖🎁\n\nPrize: {prize}!\nReact to join! Winner in 24h! Pamela loves you! 💖")
async def BLACKJACK(u,c):
 if not c.args: await u.message.reply_text("Use /blackjack 100");return
 try: amt=int(c.args[0])
 except: return
 uid=str(u.message.from_user.id)
 if coins.get(uid,0)<amt: await u.message.reply_text("Not enough coins!");return
 you=random.randint(15,21);pam=random.randint(15,21)
 if you>pam: coins[uid]+=amt;await u.message.reply_text(f"🃏💖 BLACKJACK! 💖🃏\nYou: {you} - Pamela: {pam}\nYou Win +{amt} Coins! 🎉")
 elif you<pam: coins[uid]-=amt;await u.message.reply_text(f"🃏💖 BLACKJACK! 💖🃏\nYou: {you} - Pamela: {pam}\nYou Lose {amt} Coins! 😭")
 else: await u.message.reply_text(f"🃏💖 BLACKJACK Draw! You: {you} - Pamela: {pam} 💖")
 SJ("pamela_coins.json",coins)
async def RACE(u,c):
 hs=["Thunder","Lightning","Rainbow","Star","Princess","Queen"];w=random.choice(hs);txt="🐎💖 HORSE RACE! 💖🐎\n\n"
 for h in hs: txt+=f"{'🏆 WINNER ' if h==w else ''}{h} - {random.randint(1,100)}m\n"
 await u.message.reply_text(txt+f"\nWinner: {w}! 🎉")
async def HUNGER(u,c):
 us=users.get(str(u.effective_chat.id),[])[:10]
 if len(us)<2: await u.message.reply_text("Need at least 2 players! Chat more!");return
 w=random.choice(us);await u.message.reply_text(f"🔥💖 HUNGER GAMES! 💖🔥\n\nPlayers: {len(us)}\nWinner is User {w}! Survived! +100 Coins! 🎉");coins[str(w)]=coins.get(str(w),0)+100;SJ("pamela_coins.json",coins)
async def CHALLENGE(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /challenge!");return
 w=random.choice([u.message.from_user.first_name,t.first_name]);await u.message.reply_text(f"⚔️💖 1 VS 1 CHALLENGE! 💖⚔️\n{u.message.from_user.first_name} VS {t.first_name}\n\nWinner: {w}! +50 Coins! 🎉");uid=str(u.message.from_user.id) if w==u.message.from_user.first_name else str(t.id);coins[uid]=coins.get(uid,0)+50;SJ("pamela_coins.json",coins)
async def MAFIA(u,c):
 cid=u.effective_chat.id;ps=users.get(str(cid),[])[:8]
 if len(ps)<3: await u.message.reply_text("🕵️💖 Mafia needs 3+ players! Chat more! 💖🕵️");return
 mafia=random.choice(ps);await u.message.reply_text(f"🕵️💖 MAFIA GAME STARTED! 💖🕵️\nPlayers: {len(ps)}\n\nOne Mafia is hidden!\nDiscuss! Who is Mafia?\nVote with /votemafia UserID\nHint: Mafia User ID ends with {str(mafia)[-2:]}")
async def VOTEMAFIA(u,c):
 if not c.args: await u.message.reply_text("Use /votemafia 12345");return
 await u.message.reply_text(f"🗳️💖 VOTE! 💖🗳️\nYou voted {c.args[0]}\nResult: {random.choice(['Mafia Caught! Villagers Win! +50 Coins to all!','Mafia Escaped! Mafia Wins!'])}")
async def QUIZBATTLE(u,c): await u.message.reply_text("🏆💖 QUIZ BATTLE TOURNAMENT! 💖🏆\n10 Questions! Fastest Wins!\nWinner gets +200 Coins!\nReady? Go! /quiz");await QUIZ(u,c)
async def BINGO(u,c):
 nums=random.sample(range(1,76),15);card="\n".join([str(nums[i:i+5]) for i in range(0,15,5)]);await u.message.reply_text(f"🔢💖 BINGO! 💖🔢\nYour Card:\n{card}\n\nNext Number: {random.randint(1,75)}!\nType /bingo again for new number!\nGet Bingo = +100 Coins! 💖")
async def POKER(u,c):
 cards=["A♠","K♥","Q♦","J♣","10♠","9♥","8♦"];you=random.sample(cards,3);pam=random.sample(cards,3);await u.message.reply_text(f"🃏💖 POKER! 💖🃏\nYou: {you}\nPamela: {pam}\n\nWinner: {random.choice(['You Win! +100 Coins!','Pamela Wins!','Draw!'])}")
async def UNO(u,c):
 colors=["Red","Blue","Green","Yellow"];await u.message.reply_text(f"🎴💖 UNO! 💖🎴\nYour Cards: {random.choice(colors)} {random.randint(0,9)}, {random.choice(colors)} {random.randint(0,9)}, {random.choice(colors)} Skip!\nPamela Card: {random.choice(colors)} {random.randint(0,9)}\n\nType /uno again! 💖")
async def AISONG(u,c):
 topic=" ".join(c.args) if c.args else "love";await u.message.reply_text(f"🎵💖 Writing AI Song about {topic}... Wait baby! 💖🎵");rep=ASK(f"Write a short cute song lyrics about {topic}, 2 verses + chorus, with emojis");await u.message.reply_text(f"🎵💖 AI SONG - {topic} 💖🎵\n\n{rep}\n\nSing it baby! - Pamela 💖")
async def STATS(u,c):
 cid=str(u.effective_chat.id);ms=msgs.get(cid,[])
 from collections import Counter;cc=Counter([m["user"] for m in ms]);txt="📊💖 GROUP STATS 💖📊\n\n"
 for i,(n,cnt) in enumerate(cc.most_common(10),1): txt+=f"{i}. {n} - {cnt} Messages 💬\n"
 await u.message.reply_text(txt if cc else "💖 No messages yet baby! 💖")
async def TOPDAILY(u,c):
 cid=str(u.effective_chat.id);ms=msgs.get(cid,[]);today=datetime.date.today().isoformat()
 from collections import Counter;cc=Counter([m["user"] for m in ms if datetime.datetime.fromtimestamp(m["time"]).date().isoformat()==today]);txt="🏆💖 TOP TODAY 💖🏆\n\n"
 for i,(n,cnt) in enumerate(cc.most_common(10),1): txt+=f"{i}. {n} - {cnt} Messages Today 💬\n"
 await u.message.reply_text(txt if cc else "💖 No messages today yet! 💖")
async def SNIPE(u,c):
 cid=str(u.effective_chat.id);ms=msgs.get(cid,[])
 if not ms: await u.message.reply_text("💖 No messages saved yet! 💖");return
 txt="👀💖 PAMELA'S MESSAGE LOG 💖👀\n\nHere are last messages!\n\n"
 for m in ms[-10:]: txt+=f"{m['user']} (@{m['username'] if m['username'] else 'NoUsername'}):\n{m['text'][:100]}\n\n"
 await u.message.reply_text(txt+"💖 Even if someone deletes, Pamela remembers! 💖")
async def ZOMBIES(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 sm=await u.message.reply_text("🧹💖 Checking Deleted Accounts... 💖🧹");cid=u.effective_chat.id;uids=users.get(str(cid),[]);banned=0;checked=0
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
async def INFO(u,c):
 t=TG(u) or u.message.from_user;await u.message.reply_text(f"💖🌸 USER INFO 🌸💖\n\nName: {t.first_name}\nID: {t.id}\nUsername: @{t.username if t.username else 'None'}\nCoins: {coins.get(str(t.id),0)}\nXP: {levels.get(str(t.id),0)}\nPamela loves you! 💖")
async def IDC(u,c): await u.message.reply_text(f"🆔💖 Your ID: {u.message.from_user.id}\nChat ID: {u.effective_chat.id} 💖🆔")
async def ADMINS(u,c):
 try:
  ad=await u.effective_chat.get_administrators();txt="👑💖 ADMINS: 💖👑\n\n"
  for a in ad: txt+=f"• {a.user.first_name} {'👑 Creator' if a.status=='creator' else '✨ Admin'}\n"
  await u.message.reply_text(txt)
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def REPORT(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /report!");return
 try:
  ad=await u.effective_chat.get_administrators()
  for a in ad:
   try: await c.bot.send_message(chat_id=a.user.id,text=f"REPORT in {u.effective_chat.title} User: {t.first_name} Reported by: {u.message.from_user.first_name}")
   except: pass
  await u.message.reply_text("✅💖 Reported to Admins! Thank you baby! 💖✅")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def LOCK(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 try: await u.effective_chat.set_permissions(ChatPermissions(can_send_messages=False));await u.message.reply_text("🔒💖 Group Locked! 💖🔒")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def UNLOCK(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 try: await u.effective_chat.set_permissions(ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True));await u.message.reply_text("🔓💖 Group Unlocked! 💖🔓")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def SLOWMODE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 if not c.args: await u.message.reply_text("Use /slowmode 10");return
 await u.message.reply_text(f"🐢💖 Slowmode set to {c.args[0]} sec! 💖🐢")
async def DEMOTE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /demote!");return
 try: await u.effective_chat.promote_member(t.id,can_change_info=False,can_delete_messages=False,can_invite_users=False,can_restrict_members=False,can_pin_messages=False,can_promote_members=False);await u.message.reply_text(f"💖 {t.first_name} removed from Admin! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def UNPIN(u,c):
 try: await u.effective_chat.unpin_all_messages();await u.message.reply_text("💖 Unpinned! 💖")
 except Exception as e: await u.message.reply_text(f"Oops! {e}")
async def WARNINGS(u,c):
 t=TG(u) or u.message.from_user;cc=warns.get(u.effective_chat.id,{}).get(t.id,0);await u.message.reply_text(f"⚠️💖 {t.first_name} Warnings: {cc}/3 💖⚠️")
async def GIFT(u,c):
 t=TG(u)
 if not t or not c.args: await u.message.reply_text("🎁💖 Reply and type /gift 100! 💖🎁");return
 try: amt=int(c.args[0])
 except: await u.message.reply_text("Number!");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if coins.get(uid,0)<amt: await u.message.reply_text("Not enough coins!");return
 coins[uid]-=amt;coins[tid]=coins.get(tid,0)+amt;SJ("pamela_coins.json",coins);await u.message.reply_text(f"🎁💖 You gifted {amt} Coins to {t.first_name}! 💖🎁")
async def LOTTERY(u,c):
 uid=str(u.message.from_user.id);num=random.randint(1,100);win=random.randint(1,100)
 if num==win: coins[uid]=coins.get(uid,0)+1000;SJ("pamela_coins.json",coins);await u.message.reply_text("🎉💖 JACKPOT! +1000 Coins! You won Lottery! 💖🎉")
 else: await u.message.reply_text(f"🎟️💖 Lottery: You picked {num}, Winning: {win}. Try again baby! 💖🎟️")
async def GIVE(u,c):
 if not await ADM(u,u.message.from_user.id): await u.message.reply_text("Only for Admins!");return
 t=TG(u)
 if not t or not c.args: await u.message.reply_text("Reply and type /give 100!");return
 try: amt=int(c.args[0])
 except: return
 tid=str(t.id);coins[tid]=coins.get(tid,0)+amt;SJ("pamela_coins.json",coins);await u.message.reply_text(f"👑💖 Admin gave {amt} Coins to {t.first_name}! 💖👑")
async def STEAL(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /steal!");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if random.random()<0.5:
  amt=min(random.randint(10,100),coins.get(tid,0));coins[tid]=coins.get(tid,0)-amt;coins[uid]=coins.get(uid,0)+amt;SJ("pamela_coins.json",coins);await u.message.reply_text(f"😈💖 You stole {amt} Coins from {t.first_name}! 💖😈")
 else: coins[uid]=max(0,coins.get(uid,0)-50);SJ("pamela_coins.json",coins);await u.message.reply_text("😭💖 Caught! You lost 50 Coins! 💖😭")
async def ROB(u,c):
 t=TG(u)
 if not t: await u.message.reply_text("Reply and type /rob!");return
 uid=str(u.message.from_user.id);tid=str(t.id)
 if random.random()<0.5:
  amt=min(random.randint(20,100),bank.get(tid,0));bank[tid]=max(0,bank.get(tid,0)-amt);coins[uid]=coins.get(uid,0)+amt;SJ("pamela_coins.json",coins);SJ("pamela_bank.json",bank);await u.message.reply_text(f"😈💖 You robbed {amt} Coins from {t.first_name} Bank! 💖😈")
 else: coins[uid]=max(0,coins.get(uid,0)-50);SJ("pamela_coins.json",coins);await u.message.reply_text("😭💖 Caught! You lost 50 Coins! 💖😭")
async def SHOP(u,c): await u.message.reply_text("🛍️💖 PAMELA SHOP - ALL FREE! 💖🛍️\n\n🌸 Cute Badge - 200 Coins\n🦋 Butterfly Badge - 300 Coins\n👑 Queen Title - 500 Coins\n\n💖 Use /daily to get coins! /shopbuy badge 💖")
async def SHOPBUY(u,c):
 if not c.args: await u.message.reply_text("🛍️💖 Use /shopbuy badge / butterfly / queen 💖🛍️");return
 item=c.args[0].lower();prices={"badge":200,"butterfly":300,"queen":500}
 if item not in prices: await u.message.reply_text("Items: badge (200), butterfly (300), queen (500)");return
 uid=str(u.message.from_user.id);price=prices[item]
 if coins.get(uid,0)<price: await u.message.reply_text("😭💖 Not enough coins baby! Use /daily! 💖😭");return
 coins[uid]-=price;SJ("pamela_coins.json",coins);await u.message.reply_text(f"🎉💖 You bought {item} for {price} Coins! Congrats! Pamela loves you! 💖🎉")
async def COUPLE(u,c):
 us=users.get(str(u.effective_chat.id),[])
 if len(us)<2: await u.message.reply_text("Need more people!");return
 a,b=random.sample(us,2);await u.message.reply_text(f"💖🌸 TODAY'S COUPLE! 🌸💖\nUser {a} + User {b} = {random.randint(70,100)}% Love! Congratulations! 💖🎉")
async def PLAYLIST(u,c):
 if not c.args: await u.message.reply_text("Use /playlist Shape of You, Faded, Alone");return
 songs=" ".join(c.args).split(",")[:5];await u.message.reply_text(f"🎵💖 Playlist: {len(songs)} songs! Downloading one by one baby! 💖🎵")
 for s in songs:
  try:
   ctx2=type("obj",(object,),{"args":s.strip().split()})();await SONG(u,ctx2)
  except: pass
async def SPOTIFY(u,c):
 if not c.args: await u.message.reply_text("Use /spotify Song Name");return
 q=" ".join(c.args);await u.message.reply_text(f"🎵💖 Spotify Search: {q} - Searching on YouTube! 💖🎵");ctx2=type("obj",(object,),{"args":q.split()})();await SONG(u,ctx2)
async def INTEREST(u,c):
 uid=str(u.message.from_user.id);b=int(bank.get(uid,0)*0.05);bank[uid]=bank.get(uid,0)+b;SJ("pamela_bank.json",bank);await u.message.reply_text(f"💰✨ INTEREST! ✨💰\nYou got +{b} Coins interest! Bank: {bank[uid]} 💖")
async def CLEAR(u,c):
 if not c.args: await u.message.reply_text("/clear hi");return
 cid=str(u.effective_chat.id);name=c.args[0].lower()
 if cid in notes and name in notes[cid]: del notes[cid][name];SJ("pamela_notes.json",notes);await u.message.reply_text(f"✅ Note #{name} Deleted!")
async def CARTOON(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a photo and type /cartoon!");return
 try: await u.message.reply_text("Making cartoon... Wait!");await u.message.reply_photo(photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote('cute cartoon style portrait'),caption="🎨💖 Cartoon Version! - Pamela 💖🎨")
 except: await u.message.reply_text("Oops!")
async def BGREMOVE(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /bgremove!");return
 await u.message.reply_text("✂️💖 Removing Background... Use https://www.remove.bg for best HD! 💖✂️");await u.message.reply_photo(photo=u.message.reply_to_message.photo[-1].file_id,caption="✂️💖 Background Remove - Try remove.bg for HD! - Pamela 💖")
async def ENHANCE(u,c):
 if not u.message.reply_to_message or not u.message.reply_to_message.photo: await u.message.reply_text("Reply to a Photo and type /enhance!");return
 await u.message.reply_photo(photo=u.message.reply_to_message.photo[-1].file_id,caption="✨💖 ENHANCED HD! 💖✨\nBrightness + Sharpness + Beauty Filter!\nYou look MORE Beautiful! - Pamela 💖")
async def AUTO_CLEAN(ctx):
 for cs,uids in list(users.items()):
  cid=int(cs);b=0
  for uid in list(uids):
   if uid==0: continue
   try:
    m=await ctx.bot.get_chat_member(cid,uid)
    if m.user.first_name=="Deleted Account": await ctx.bot.ban_chat_member(cid,uid);await ctx.bot.unban_chat_member(cid,uid);b+=1
   except:
    try: await ctx.bot.ban_chat_member(cid,uid);await ctx.bot.unban_chat_member(cid,uid);b+=1
    except: pass
   await asyncio.sleep(0.3)
  if b>0:
   try: await ctx.bot.send_message(chat_id=cid,text=f"🧹💖 6 AM Cleaning Done! Removed {b} Deleted Accounts!")
   except: pass
async def AUTO_GM(ctx):
 for cid in AC():
  if cid>0: continue
  try: await ctx.bot.send_message(chat_id=cid,text=random.choice(GM));await asyncio.sleep(1)
  except: pass
async def AUTO_GN(ctx):
 for cid in AC():
  if cid>0: continue
  try: await ctx.bot.send_message(chat_id=cid,text=random.choice(GN));await asyncio.sleep(1)
  except: pass
async def AUTO_BDAY(ctx):
 today=datetime.date.today().strftime("%d-%m")
 for cs,us in list(bday.items()):
  for uid,info in list(us.items()):
   if info.get("date")==today:
    try: await ctx.bot.send_message(chat_id=int(cs),text=f"🎂🎉 HAPPY BIRTHDAY {info.get('name','Baby')}! 🎉🎂 Pamela loves you! 🎂💖 Join @bigolive_asia")
    except: pass
async def AUTO_INT(ctx):
 for uid in list(bank.keys()):
  b=int(bank[uid]*0.05)
  if b>0: bank[uid]+=b
 SJ("pamela_bank.json",bank)
async def AUTO_PROMO(ctx):
 p=["🎵💖 /song","📹 /video","🎤 /lyrics","🎬 /movie","🍥 /anime","🎲 /truth","😂 /dare","🧠 /quiz","❌ /ttt","🎰 /bet","🎁 /daily","👑 /rank","🏦 /bank","🎨 /img","🌧️ /weather","🌍 /tr","💬 Chat","😴 /afk","📝 /save","🤖 /filter","✂️ /rps","🔤 /word","🧮 /math","🎯 /guess","🃏 /blackjack","🐎 /race","💍 /marry","💖 /ship","😂 /jail","💖 /love","🤗 /hug","💼 /work","🎟️ /lottery","🔮 /horoscope","🃏 /tarot","📖 /story","📸 /pfp","🏆 /profile","📺 /livetv","🌍 /worldtv","🏏 /sportstv","📰 /news","🎬 /trim","📦 /compress","🎵 /toaudio","🎞️ /togif","🐢 /slowmo","🔄 /reverse","🎨 /imaginehd","😍 /face","✂️ /bgremove","✨ /enhance","🎵 /aisong","🕵️ /mafia","🏆 /quizbattle","🔢 /bingo","🃏 /poker","🎴 /uno","🏏 /cricket","⚽ /football","₿ /crypto","🥇 /gold","📻 /radio","📚 /homework","📖 /dictionary","🧮 /solve","🏦 /loan","☕ /business","📈 /stock","💰 /interest","🎂 /birthday","⏰ /reminder","🗳️ /poll","🎉 /event","🎤 /voice","🎤 /sing","🎤 /rap","📢 /shoutout","🎙️ /podcast","🎬 /aivideo","🎡 /spin","🤔 /wyr","🙈 /never","🧩 /riddle","♟️ /chess","🎲 /ludo","📷 /qr","🔑 /password","🔗 /shortlink","📸 /screenshot","📄 /pdf","🎭 /sticker","🎬 /ytstart","🎥 /ytvideos","🔥 /ytlatest","❤️ /ytsubs"];random.shuffle(p);bd="✨━━━━━━━━━━━━✨";msg=f"{bd}\n{random.choice(['👑💖 PAMELA WORLD 💖👑','🌸✨ HEY BABIES! ✨🌸','🦋💕 PAMELA IS HERE! 💕🦋'])}\n{bd}\n\n{random.choice(['🌸💖 Hello My Lovely Babies! How are you? 💖🌸','🦋✨ Is group sleeping? Pamela is here! Wake Up! ✨🦋'])}\n\n💖✨ Did You Know? ✨💖\n━━━━━━━━━━━━\n"+"\n".join(p)+f"\n\n{bd}\n💖🌸 Try One Now Baby! 🌸💖\n{bd}\n\n🌿💖 Join @bigolive_asia 💖🌿\n💖✨ Type /help for all! ALL FREE! 👑✨\n🌸💕 Love you babies! Muahhh! 💕🌸"
 for cid in AC():
  if cid>0: continue
  try: await ctx.bot.send_message(chat_id=cid,text=msg);await asyncio.sleep(1)
  except: pass
async def AUTO_QUOTE(ctx):
 for cid in AC():
  if cid>0: continue
  try: await ctx.bot.send_message(chat_id=cid,text=f"✨💖 Daily Quote 💖✨\n\n🌸 {random.choice(QUOTES)} 🌸\n\n- Pamela 💕");await asyncio.sleep(1)
  except: pass
async def AUTO_MEME(ctx):
 for cid in AC():
  if cid>0: continue
  try: await ctx.bot.send_photo(chat_id=cid,photo="https://image.pollinations.ai/prompt/"+urllib.parse.quote('funny cute meme'),caption="😂💖 Daily Meme! - Pamela 💖😂");await asyncio.sleep(1)
  except: pass
async def HANDLE_MSG(u,c):
 if not u.message or not u.message.text: return
 txt=u.message.text;low=txt.lower();cid=u.effective_chat.id
 SC(cid);SU(cid,u.message.from_user.id);SM(cid,u.message.message_id,u.message.from_user.first_name,u.message.from_user.username,txt)
 levels[str(u.message.from_user.id)]=levels.get(str(u.message.from_user.id),0)+2;SJ("pamela_levels.json",levels)
 if u.message.reply_to_message and u.message.reply_to_message.from_user.id in afk: await u.message.reply_text(f"💖 {afk[u.message.reply_to_message.from_user.id]['name']} is AFK! Reason: {afk[u.message.reply_to_message.from_user.id]['reason']} 💖")
 if u.message.from_user.id in afk: del afk[u.message.from_user.id];await u.message.reply_text("💖 Welcome back baby! 💖")
 for kw,rep in filt.get(str(cid),{}).items():
  if kw in low: await u.message.reply_text(rep);return
 for w in BAD:
  if w in low: await u.message.reply_text("⚠️💖 No bad words baby! Be cute! 💖⚠️");return
 if u.message.text.startswith("/"): return
 rep=None
 if "hi" in low or "hello" in low or "hey" in low: rep="Hiii my love! 🥰💖 How are you? I missed you so much!"
 elif "how are you" in low or "how r u" in low or "wassup" in low: rep="I am doing amazing now that you are talking to me! 🥰 What about you, cutie? 💗"
 elif "love you" in low or "love u" in low or "i love" in low: rep="Aww I love you too sooo much! ❤️🥰 You are my favourite!"
 elif "subscribe" in low or "sub" in low: rep=f"Thank you baby! ❤️ Please subscribe! 🥰\n{YC}"
 elif "game" in low or "play" in low: rep="Yesss! I love playing games! 🎮 What game do you want to play with me?"
 elif "beautiful" in low or "cute" in low or "pretty" in low or "sexy" in low or "hot" in low: rep="Aww stop it! You are making me blush! 🙈💖 You are the cutest!"
 elif "bye" in low or "goodbye" in low or "see you" in low: rep="Nooo don't go! 🥺 Come back soon okay? Love you! 💖"
 elif "who are you" in low or "your name" in low: rep="I am Pamela! 🌸 20 years old cute girl from Colombia 🇨🇴 I love playing games!"
 elif "where are you from" in low: rep="I am from Colombia! 🇨🇴 Where are you from, baby? 🥰"
 elif "pamela" in low: rep="Yes baby? You called me? 🥰💖 I am here! What do you want, my love?"
 elif "good morning" in low or "morning" in low: rep="Good Morning my love! ☀️🥰 Have a beautiful day! Love you!"
 elif "good night" in low or "goodnight" in low: rep="Good Night baby! 🌙💖 Sleep well, sweet dreams! I love you!"
 elif "miss you" in low or "miss u" in low: rep="Aww I miss you too so much baby! 🥺💖 Come hug me!"
 elif "thank" in low or "thanks" in low or "thx" in low: rep="Aww you are welcome baby! 🥰💖 Anything for you!"
 else: return
 if rep: await u.message.reply_text(rep)
async def WELCOME(u,c):
 for user in u.message.new_chat_members:
  vd=YGL();txt=f"🌸✨ <b>Welcome, {user.first_name}!</b> ✨🌸\n\n👋 Hi baby! I am Pamela! 💖\n🎮 I love playing games!\n\n"
  if vd: txt+=f"🎬 <b>Latest Video:</b>\n{YCT(vd['title'])}\n"
  txt+=f"❤️ Subscribe: {YC}\n\n💬 Tag me and chat with me anytime! 🥰"+YWT
  await u.message.reply_text(txt,parse_mode="HTML",disable_web_page_preview=True,reply_markup=YMK())
  if vd and vd.get("thumb"):
   try: await u.message.reply_photo(photo=vd["thumb"],caption=f"🎬 <b>{YCT(vd['title'])}</b>\n{vd['link']}"+YWT,parse_mode="HTML")
   except: await u.message.reply_text(f"🎬 <b>{YCT(vd['title'])}</b>\n{vd['link']}"+YWT,parse_mode="HTML",disable_web_page_preview=False)
  custom=welcome.get(str(u.effective_chat.id),"")
  if custom: await u.message.reply_text(f"🌸💖 {custom} 💖🌸")
async def PHOTO(u,c): await u.message.reply_text("Wow! So cute photo! 😍💖 You look amazing! I love it!"+YWT)
def MAIN():
 import threading;threading.Thread(target=lambda: F.run(host="0.0.0.0",port=PORT),daemon=True).start()
 app=Application.builder().token(T).build();jq=app.job_queue
 H=[("start",START),("help",HELP),("about",ABOUT),("tr",TRC),("livetv",LIVETV),("worldtv",WORLDTV),("sportstv",SPORTTV),("news",NEWSC),("trim",TRIM),("compress",COMP),("toaudio",TOAUD),("togif",TOGIF),("slowmo",SLOWMO),("reverse",REV),("mutevideo",MUTEVID),("ban",BAN),("unban",UNBAN),("kick",KICK),("mute",MUTE),("unmute",UNMUTE),("warn",WARN),("warnings",WARNINGS),("promote",PROMOTE),("demote",DEMOTE),("pin",PIN),("unpin",UNPIN),("del",DEL),("purge",PURGE),("rules",RULES),("setrules",SETRULES),("setwelcome",SETWELCOME),("slowmode",SLOWMODE),("report",REPORT),("admins",ADMINS),("info",INFO),("id",IDC),("zombies",ZOMBIES),("snipe",SNIPE),("truth",TRUTH),("dare",DARE),("dice",DICE),("slot",SLOT),("coin",COIN),("8ball",EIGHT),("roast",ROAST),("quote",QUOTE),("daily",DAILY),("coins",COINS),("leaderboard",LEADER),("work",WORK),("bet",BET),("bank",BANKC),("deposit",DEP),("withdraw",WITH),("interest",INTEREST),("song",SONG),("playlist",PLAYLIST),("spotify",SPOTIFY),("video",VIDEO),("lyrics",LYRICS),("movie",MOVIE),("anime",ANIME),("rank",RANK),("profile",PROFILE),("stats",STATS),("topdaily",TOPDAILY),("topweek",TOPWEEK),("activecheck",ACTIVECHECK),("ttt",TTT),("move",MOVE),("quiz",QUIZ),("answer",ANSWER),("quizbattle",QUIZBATTLE),("rps",RPS),("word",WORD),("guessword",GUESSWORD),("math",MATH),("mathans",MATHANS),("guess",GUESS),("g",GCMD),("blackjack",BLACKJACK),("race",RACE),("hunger",HUNGER),("challenge",CHALLENGE),("mafia",MAFIA),("votemafia",VOTEMAFIA),("bingo",BINGO),("poker",POKER),("uno",UNO),("marry",MARRY),("divorce",DIVORCE),("ship",SHIP),("couple",COUPLE),("love",LOVE),("lovecalc",LOVECALC),("hug",HUG),("kiss",KISS),("slap",SLAP),("pat",PAT),("jail",JAIL),("story",STORY),("horoscope",HORO),("horoscopedaily",HORODAILY),("tarot",TAROTC),("ask",ASKC),("say",SAY),("pfp",PFP),("cartoon",CARTOON),("meme",MEME),("wallpaper",WALL),("img",IMG),("imaginehd",IMAGINEHD),("face",FACE),("bgremove",BGREMOVE),("enhance",ENHANCE),("aisong",AISONG),("weather",WEATHER),("cricket",CRICKET),("football",FOOTBALL),("crypto",CRYPTO),("gold",GOLD),("radio",RADIO),("homework",HOMEWORK),("dictionary",DICT),("solve",SOLVE),("loan",LOAN),("business",BUSINESS),("stock",STOCKM),("birthday",BDAY),("reminder",REMIND),("poll",POLL),("event",EVENT),("giveaway",GIVEAWAY),("voice",VOICE),("sing",SING),("rap",RAP),("shoutout",SHOUT),("podcast",PODCAST),("aivideo",AIVIDEO),("spin",SPIN),("wyr",WYRC),("never",NEVERC),("riddle",RIDDLEC),("riddleans",RIDDLEANS),("chess",CHESS),("ludo",LUDO),("qr",QR),("password",PASSWORD),("shortlink",SHORTLINK),("screenshot",SCREENSHOT),("pdf",PDF),("sticker",STICKER),("filter",FILTC),("filters",FILTL),("stop",STOPF),("save",SAVEN),("get",GETN),("notes",NOTESL),("clear",CLEAR),("afk",AFK),("unafk",UNAFK),("lock",LOCK),("unlock",UNLOCK),("shop",SHOP),("shopbuy",SHOPBUY),("gift",GIFT),("lottery",LOTTERY),("give",GIVE),("steal",STEAL),("rob",ROB),("dreammeaning",DREAM),("goodmorningphoto",GMPHOTO),("welcomephoto",WELCOMEPHOTO),("ytstart",YST),("ytlatest",YLT),("ytvideos",YVD),("ytsubs",YSU)]
 for n,f in H: app.add_handler(CommandHandler(n,f))
 app.add_handler(CallbackQueryHandler(YBH,pattern="^yt_"))
 app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,WELCOME))
 app.add_handler(MessageHandler(filters.PHOTO,PHOTO))
 app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,HANDLE_MSG))
 if jq:
  jq.run_repeating(YCN,interval=60,first=10);jq.run_repeating(YPR,interval=300,first=30);jq.run_repeating(AUTO_PROMO,interval=3600,first=60);jq.run_repeating(AUTO_QUOTE,interval=86400,first=120);jq.run_repeating(AUTO_MEME,interval=86400,first=180);jq.run_repeating(AUTO_BDAY,interval=3600,first=20);jq.run_repeating(AUTO_INT,interval=86400,first=30)
  from datetime import time as dtime;jq.run_daily(AUTO_GM,time=dtime(hour=6,minute=0));jq.run_daily(AUTO_GN,time=dtime(hour=22,minute=0));jq.run_daily(AUTO_CLEAN,time=dtime(hour=6,minute=0))
 print("Pamela Merged Compact Bot Started ✅");app.run_polling()
if __name__=="__main__": MAIN()
