import asyncio
import os
import sys
from flask import Flask
from threading import Thread
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import Message

# Render uchun kichik soxta veb-server (bepul tarif talabi)
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_web():
    # Render o'zi beradigan PORT o'zgaruvchisini o'qiydi
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
INTERVAL_SEKUND = 30              

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ XATO: Sessiya kaliti noto'g'ri!")
        return
        
    print("🎉 Bepul Web Service'da muvaffaqiyatli ishga tushdi!")
    last_forwarded_id = None

    while True:
        try:
            async for message in client.iter_messages(MANBA_ID, limit=1):
                if isinstance(message, Message) and message.id != last_forwarded_id:
                    for target_id in MANZILLAR_ID:
                        try:
                            await client.forward_messages(target_id, message)
                            await asyncio.sleep(1.5)
                        except Exception as e:
                            print(f"Xato: {e}")
                    last_forwarded_id = message.id
                else:
                    print(".", end="", flush=True)
        except Exception as e:
            print(f"Xatolik: {e}")
            
        await asyncio.sleep(INTERVAL_SEKUND)

if __name__ == '__main__':
    # Veb-serverni alohida oqimda (thread) yurgizamiz
    Thread(target=run_web).start()
    # Asosiy botni ishga tushiramiz
    client.loop.run_until_complete(main())