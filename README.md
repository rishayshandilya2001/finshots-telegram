# Finshots → Telegram Daily Sender

Har din Finshots ka latest post automatically Telegram pe aa jayega. Koi server nahi, koi app khula rakhne ki zarurat nahi.

## Kaise kaam karta hai (quick overview)

1. Finshots ki RSS feed (`finshots.in/rss/`) se latest post uthata hai
2. Telegram bot ke through wo post aapko bhej deta hai
3. GitHub Actions roz ek fixed time pe khud yeh script chala deta hai — free, forever, bina kisi server ke

---

## Step 1 — Telegram Bot banao (5 min)

**Kyun:** Bot hi wo cheez hai jo aapko message "bhejega". Bina bot ke Telegram API ko pata nahi chalega ki message kis account se aa raha hai.

1. Telegram kholo, `@BotFather` ko search karo, chat start karo
2. `/newbot` bhejo
3. Bot ka naam aur username do (username `_bot` se end hona chahiye, e.g. `rishay_finshots_bot`)
4. BotFather ek **token** dega jaisa: `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   → Yeh save kar lo, isi ko `TELEGRAM_BOT_TOKEN` bologe

## Step 2 — Apna Chat ID nikaalo

**Kyun:** Bot ko pata hona chahiye *kise* message bhejna hai — chat ID hi wo address hai.

1. Apne naye bot ko Telegram pe search karo, `/start` bhejo (koi bhi message bhej do)
2. Browser me yeh URL kholo (apna token daal ke):
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. JSON response me `"chat":{"id": 123456789, ...}` dikhega — yeh number hi aapka `TELEGRAM_CHAT_ID` hai

## Step 3 — GitHub repo banao

**Kyun:** GitHub Actions repo ke andar hi chalta hai — code aur automation dono ek jagah rehte hain.

1. GitHub pe naya repo banao (e.g. `finshots-telegram`)
2. Is folder ke saare files (`send_finshots.py`, `requirements.txt`, `.github/workflows/daily.yml`) us repo me push kar do

## Step 4 — Secrets add karo

**Kyun:** Bot token aur chat ID sensitive hote hain — inhe code me likhna galat hai (koi bhi repo dekh ke aapke bot ko hijack kar sakta hai). GitHub Secrets inhe encrypted rakhta hai.

1. Repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** → naam `TELEGRAM_BOT_TOKEN`, value apna token
3. Wahi se ek aur secret: naam `TELEGRAM_CHAT_ID`, value apna chat ID

## Step 5 — Test karo

**Kyun:** Roz ke schedule ka wait kiye bina turant check karna hai ki sab sahi chal raha hai ya nahi.

1. Repo → **Actions** tab → **Send Finshots Daily to Telegram** workflow select karo
2. **Run workflow** button dabao (manual trigger)
3. Kuch second me Telegram pe message aa jana chahiye

## Step 6 — Bas, ab yeh khud chalega

Workflow roz **8:00 AM IST** pe automatically chalega (`daily.yml` me cron schedule set hai). Time change karna ho toh `daily.yml` me `cron: "30 2 * * *"` line edit karo — pehla number minute hai, dusra hour, dono UTC me (IST = UTC + 5:30).

---

## Notes

- Finshots Friday ko doosra newsletter (Finshots Markets) bhi bhejta hai, lekin unki main RSS feed sirf daily story track karti hai — jaisa website pe dikhta hai
- Agar kabhi message duplicate lage ya na aaye, `sent_log.txt` file check karo — usme wo links hain jo already bheje ja chuke hain
- GitHub Actions free tier me public repos ke liye unlimited minutes hain; private repo rakhoge toh bhi itna chhota daily job free tier me aasani se aa jayega
