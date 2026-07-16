import asyncio
import os
import sys
from flask import Flask
from threading import Thread
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import Message

app = Flask('')
@app.route('/')
def home(): return "Bot ishlamoqda!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

API_ID = 34452379
API_HASH = '25dae3c45785a28864f4a594a296e128'
STRING_SESSION = os.getenv("TG_STRING_SESSION")
MANBA_ID = -1004423905908
MANZILLAR_ID = [-1003922838589, -1002179183026]

async def start_bot():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.connect()
    
    print("Bot ulandi. Har 10 soniyada manbani tekshirmoqda...")
    last_id = 0 # Boshlang'ich qiymat

    while True:
        try:
            # Eng oxirgi 1 ta xabarni olamiz
            async for message in client.iter_messages(MANBA_ID, limit=1):
                # Diagnostika uchun log
                print(f"Manbada topilgan oxirgi xabar ID: {message.id}")
                
                if last_id == 0:
                    last_id = message.id
                    print("Boshlang'ich nuqta qo'yildi.")
                elif message.id > last_id:
                    print(f"YANGI XABAR ANIQLANDI! ID: {message.id}")
                    for target_id in MANZILLAR_ID:
                        await client.forward_messages(target_id, message)
                    last_id = message.id
                else:
                    print("Yangi xabar yo'q.")
        except Exception as e:
            print(f"Xatolik: {e}")
            
        await asyncio.sleep(10)

if __name__ == '__main__':
    Thread(target=run_web, daemon=True).start()
    asyncio.run(start_bot())