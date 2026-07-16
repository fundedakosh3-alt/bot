import asyncio
import os
import sys
from flask import Flask
from threading import Thread
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import Message

# ==========================================
# 1. RENDER UCHUN VEB-SERVER (BEPUL TARIF)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_web():
    # Render avtomatik beradigan PORT o'zgaruvchisini o'qiydi
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# 2. SOZLAMALAR VA ID RAQAMLAR
# ==========================================
API_ID = 34452379
API_HASH = '25dae3c45785a28864f4a594a296e128'

# Atrof-muhit o'zgaruvchisidan String Sessionni o'qiymiz
STRING_SESSION = os.getenv("TG_STRING_SESSION")

if not STRING_SESSION:
    print("❌ XATO: TG_STRING_SESSION muhit o'zgaruvchisi topilmadi!")
    sys.exit(1)

# Guruh ID raqamlari (-100 prefiksi bilan)
MANBA_ID = -1004423905908         
MANZILLAR_ID = [-1003922838589, -1002179183026]

# ⏱ TEKSHIRISH INTERVALI: Har 10 soniyada
INTERVAL_SEKUND = 10              

# ==========================================
# 3. ASOSIY ASINXRON BOT FUNKSIYASI
# ==========================================
async def start_bot():
    # Python 3.14+ uchun faol event loopni olamiz
    loop = asyncio.get_running_loop()
    
    # TelegramClient obyektini loop ichida yaratamiz (RuntimeError oldini olish uchun)
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, loop=loop)
    
    print("Telegramga ulanish urinishi boshlanmoqda...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ XATO: Sessiya kaliti noto'g'ri yoki muddati o'tgan!")
        return
        
    print(f"🎉 Bot muvaffaqiyatli ishga tushdi! Har {INTERVAL_SEKUND} soniyada tekshiriladi.")
    
    # Oxirgi yuborilgan xabar ID sini saqlash uchun o'zgaruvchi
    last_forwarded_id = None

    while True:
        try:
            # Manba guruhdan faqat eng oxirgi 1 ta xabarni olamiz
            async for message in client.iter_messages(MANBA_ID, limit=1):
                if isinstance(message, Message):
                    
                    # Agar bu xabar ID si biz oxirgi marta yuborgan ID ga teng bo'lmasa -> YUBORAMIZ
                    if message.id != last_forwarded_id:
                        print(f"\n[Yangi xabar aniqlandi] ID: {message.id}. Guruhlarga uzatilmoqda...")
                        
                        for target_id in MANZILLAR_ID:
                            try:
                                await client.forward_messages(target_id, message)
                                print(f" -> [OK] -> {target_id}")
                                await asyncio.sleep(1.0) # Guruhlararo qisqa pauza (Spam filtrdan himoya)
                            except Exception as e:
                                print(f" -> Xato ({target_id}): {e}")
                                
                        # Shu xabarni oxirgi yuborilgan deb eslab qolamiz
                        last_forwarded_id = message.id
            
            # Bot tirikligini logda ko'rsatib turish uchun nuqta qo'yamiz
            print(".", end="", flush=True)
            
        except Exception as e:
            print(f"\n❌ Xatolik yuz berdi: {e}")
            
        # ⏱ 10 soniya kutish
        await asyncio.sleep(INTERVAL_SEKUND)

# ==========================================
# 4. DASTURNI ISHGA TUSHIRISH NUQTASI
# ==========================================
if __name__ == '__main__':
    # Flask veb-serverni alohida fondagi oqimda (daemon thread) yurgizamiz
    Thread(target=run_web, daemon=True).start()
    
    # Asosiy botni asyncio orqali ishga tushiramiz
    asyncio.run(start_bot())