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
    
    print("Bot takrorlash rejimida ishga tushdi.")
    last_sent_id = None

    while True:
        try:
            # Har safar eng oxirgi xabarni olamiz
            async for message in client.iter_messages(MANBA_ID, limit=1):
                if isinstance(message, Message):
                    # Agar bu yangi xabar bo'lsa yoki avvalgisidan farqli bo'lsa
                    # Yoki shunchaki oxirgi xabarni qayta yuborish uchun:
                    print(f"Xabar aniqlandi: {message.id}. Guruhlarga yuborilmoqda...")
                    
                    for target_id in MANZILLAR_ID:
                        try:
                            # Forward o'rniga send_message/edit ishlatish mumkin, 
                            # lekin oddiy forward har doim ham ishlaydi:
                            await client.forward_messages(target_id, message)
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Yuborishda xato: {e}")
                    
                    last_sent_id = message.id
        except Exception as e:
            print(f"Xatolik: {e}")
            
        await asyncio.sleep(10) # ROPA-ROSA 10 soniya interval

if __name__ == '__main__':
    Thread(target=run_web, daemon=True).start()
    asyncio.run(start_bot())