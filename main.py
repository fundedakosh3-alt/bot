import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.patched import Message
from telethon.errors import ChatWriteForbiddenError, ChannelPrivateError, FloodWaitError

# API ma'lumotlar
API_ID = 34452379
API_HASH = '25dae3c45785a28864f4a594a296e128'

# Xavfsizlik uchun ulanish kalitini Render tizimidan yashirincha o'qiymiz
STRING_SESSION = os.getenv("TG_STRING_SESSION")

if not STRING_SESSION:
    print("❌ XATO: TG_STRING_SESSION muhit o'zgaruvchisi topilmadi!")
    sys.exit(1)

# Siz bergan ID raqamlar (-100 prefiksi bilan)
MANBA_ID = -1004423905908         # 4423905908 - xabar olinadigan joy

MANZILLAR_ID = [
    -1003922838589,               # 3922838589 - yuboriladigan 1-guruh
    -1002179183026                # 2179183026 - yuboriladigan 2-guruh
]

INTERVAL_SEKUND = 30              # Har 30 soniyada yangi xabarlarni tekshiradi

# To'g'ridan-to'g'ri StringSession orqali yaratamiz (Proksi shart emas)
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def main():
    print("Telegramga ulanish urinishi boshlanmoqda...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ XATO: Sessiya kaliti noto'g'ri yoki muddati o'tgan!")
        return
        
    print("🎉 Muvaffaqiyatli ulandi! Render serverida ishga tushdi.")
    print(f"📥 Manba: {MANBA_ID} | 📤 Manzillar: {MANZILLAR_ID}\n")

    # Oxirgi yuborilgan xabar ID sini eslab qolish uchun
    last_forwarded_id = None

    while True:
        try:
            # Manba chatdan eng oxirgi xabarni olamiz
            async for message in client.iter_messages(MANBA_ID, limit=1):
                if isinstance(message, Message):
                    
                    # Agar bu xabar yangi bo'lsa (avval yuborilmagan bo'lsa)
                    if message.id != last_forwarded_id:
                        print(f"\n[Yangi Xabar] ID: {message.id} aniqlandi. Guruhlarga uzatilmoqda...")
                        
                        # Guruhlarga navbat bilan yuborish
                        for target_id in MANZILLAR_ID:
                            try:
                                await client.forward_messages(target_id, message)
                                print(f" -> [YUBORILDI] -> {target_id}")
                                await asyncio.sleep(1.5) # Spam filtrga tushmaslik uchun
                            except ChatWriteForbiddenError:
                                print(f" -> [XATO] {target_id} guruhiga yozish huquqingiz yo'q!")
                            except ChannelPrivateError:
                                print(f" -> [XATO] {target_id} guruhiga kirish taqiqlangan!")
                            except FloodWaitError as e:
                                print(f" -> [LIMIT] Telegram cheklov qo'ydi. {e.seconds} soniya kutish kerak.")
                                await asyncio.sleep(e.seconds)
                        
                        # Oxirgi xabar ID sini yangilaymiz
                        last_forwarded_id = message.id
                    else:
                        print(".", end="", flush=True) # Yangi xabar yo'qligini bildirish uchun
                    
        except Exception as e:
            print(f"\n❌ Xatolik yuz berdi: {e}")

        # Belgilangan vaqt bo'yicha kutish
        await asyncio.sleep(INTERVAL_SEKUND)

if __name__ == '__main__':
    client.loop.run_until_complete(main())