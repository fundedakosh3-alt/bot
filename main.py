import asyncio
import os
import sys
from flask import Flask
from threading import Thread
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import Message

# ==========================================
# 1. VEB-SERVER (RENDER UCHUN)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# 2. SOZLAMALAR
# ==========================================
API_ID = 34452379
API_HASH = '25dae3c45785a28864f4a594a296e128'
STRING_SESSION = os.getenv("TG_STRING_SESSION")

if not STRING_SESSION:
    print("❌ XATO: TG_STRING_SESSION topilmadi!")
    sys.exit(1)

MANBA_ID = -1004423905908         
MANZILLAR_ID = [-1003922838589, -1002179183026]
INTERVAL_SEKUND = 10              

# ==========================================
# 3. ASOSIY BOT LOGIKASI
# ==========================================
async def start_bot():
    loop = asyncio.get_running_loop()
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, loop=loop)
    
    print("Telegramga ulanish urinishi boshlanmoqda...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ XATO: Sessiya kaliti noto'g'ri!")
        return
        
    print(f"🎉 Bot muvaffaqiyatli ishga tushdi! Har {INTERVAL_SEKUND} soniyada tekshiriladi.")
    
    last_forwarded_id = None

    while True:
        try:
            # 10 soniya ichida kelgan bo'lishi mumkin bo'lgan oxirgi 15 ta xabarni olamiz
            messages = await client.get_messages(MANBA_ID, limit=15)
            
            if messages:
                # 1-QADAM: Bot endi yonganda eng oxirgi eski xabar ID sini eslab qoladi va yubormaydi
                if last_forwarded_id is None:
                    last_forwarded_id = messages[0].id
                    print(f"📌 Boshlang'ich nuqta belgilandi (ID: {last_forwarded_id}). Eski xabarlar tegmaymiz.")
                
                # 2-QADAM: Xabarlarni eskidan yangiga qarab tekshiramiz
                else:
                    for message in reversed(messages):
                        if isinstance(message, Message):
                            # Faqat rostdan ham yangi bo'lgan (ID katta) xabarlar o'tadi
                            if message.id > last_forwarded_id:
                                print(f"\n✅ [YANGI XABAR] ID: {message.id} -> Guruhlarga uzatilmoqda...")
                                
                                for target_id in MANZILLAR_ID:
                                    try:
                                        await client.forward_messages(target_id, message)
                                        print(f" -> [OK] -> {target_id}")
                                        await asyncio.sleep(1.0)
                                    except Exception as e:
                                        print(f" -> Xato ({target_id}): {e}")
                                        
                                # Oxirgi muvaffaqiyatli xabar ID sini yangilaymiz
                                last_forwarded_id = message.id
            
            print(".", end="", flush=True)
            
        except Exception as e:
            print(f"\n❌ Xatolik: {e}")
            
        await asyncio.sleep(INTERVAL_SEKUND)

# ==========================================
# 4. ISHGA TUSHIRISH
# ==========================================
if __name__ == '__main__':
    Thread(target=run_web, daemon=True).start()
    asyncio.run(start_bot())