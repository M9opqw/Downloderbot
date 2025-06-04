import os
from pyrogram import Client, filters
from pyrogram.types import Message
import requests

API_ID = int(os.environ.get("API_ID", 12345678))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

app = Client("leech_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("أرسل رابط مباشر وسأقوم بتحميل الفيديو لك 📥")

@app.on_message(filters.text & ~filters.edited)
async def download_and_send_video(client, message: Message):
    url = message.text.strip()
    if url.startswith("http"):
        msg = await message.reply_text("جاري تحميل الفيديو...")
        try:
            response = requests.get(url)
            file_name = "video.mp4"
            with open(file_name, "wb") as f:
                f.write(response.content)
            thumb = "thumbnail.jpg" if os.path.exists("thumbnail.jpg") else None
            await message.reply_video(video=file_name, thumb=thumb, caption="تم التحميل ✅")
            os.remove(file_name)
        except Exception as e:
            await msg.edit(f"حدث خطأ: {e}")
    else:
        await message.reply_text("يرجى إرسال رابط مباشر صالح.")

app.run()