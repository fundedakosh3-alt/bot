import asyncio
import os
import sys
from flask import Flask
from threading import Thread
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import Message

# Render uchun veb-server
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# API va sozlamalar
API_ID = 34452379
API_HASH = '25dae3c45785a28864f4a594a296e128'
STRING_SESSION = os.getenv("TG_STRING_SESSION")

if not STRING_SESSION:
    print("❌ XATO: TG_STRING_SESSION topilmadi!")
    sys.exit(1)

MANBA_ID = -1004423905908         
MANZILLAR_ID = [-1003922838589, -1002179183026]

# ⏱ INTERVAL SHU YERDA: Roppa-rosa 10 soniya
INTERVAL_SEKUND = 10              

async def start_bot():
    loop = asyncio.get_running_loop()
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, loop=loop)
    
    print("Telegramga ulanish urinishi boshlanmoqda...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ XATO: Sessiya kaliti noto'g'ri!")
        return
        
    print(f"🎉 Bot muvaffaqiyatli ishga tushdi! Har {INTERVAL_SEKUND} soniyada tekshiriladi.")
    
    # Eng oxirgi yuborilgan xabar ID sini saqlash (boshida None)
    last_forwarded_id = None

    while True:
        try:
            # Oxirgi 5 ta xabarni paket qilib oladi (xabarlar tiqilib qolmasligi uchun)
            messages = await client.get_messages(MANBA_ID, limit=5)
            
            if messages:
                # Agar bot birinchi marta yonayotgan bo'lsa, manbadagi eng oxirgi xabar ID sini oladi
                if last_forwarded_id is None:
                    last_forwarded_id = messages[0].id
                    print(f"📌 Boshlang'ich nuqta belgilandi. Oxirgi xabar ID: {last_forwarded_id}")
                
                # Xabarlarni eskidan yangiga qarab tekshiramiz
                for message in reversed(messages):
                    if isinstance(message, Message):
                        # Faqat biz oxirgi marta yuborgan xabardan yangiroq (ID si katta) bo'lsa yuboradi
                        if message.id > last_forwarded_id:
                            print(f"\n[Yangi xabar] ID: {message.id} aniqlandi. Uzatilmoqda...")
                            
                            for target_id in MANZILLAR_ID:
                                try:
                                    await client.forward_messages(target_id, message)
                                    await asyncio.sleep(1.0) # Spam filtrdan himoya
                                except Exception as e:
                                    print(f" -> Xato ({target_id}): {e}")
                                    
                            # Oxirgi yuborilgan ID ni yangilaymiz
                            last_forwarded_id = message.id
            
            print(".", end="", flush=True) # Bot ishlayotganini logda ko'rsatish uchun
            
        except Exception as e:
            print(f"\n❌ Xatolik yuz berdi: {e}")
            
        # ⏱ 10 soniya kutish
        await asyncio.sleep(INTERVAL_SEKUND)

if __name__ == '__main__':
    Thread(target=run_web, daemon=True).start()
    asyncio.run(start_bot())