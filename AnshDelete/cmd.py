import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import API_ID, API_HASH
import yt_dlp

# Initialize the bot
bot = Client

# Temporary storage for URLs
URL_STORAGE = {}

# Download folder
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Start Command
@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url="https://t.me/Legend_BoyCC")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        f"👋 Hi {message.from_user.mention}, I am your Video Downloader Bot.\n\n"
        "Send me a video link to start downloading!",
        reply_markup=reply_markup
    )

# Link Command
@bot.on_message(filters.text & ~filters.command(start))
async def handle_video_link(client: Client, message: Message):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.reply_text("❌ Please send a valid URL.")
        return

    # Generate a unique ID for the URL
    unique_id = str(len(URL_STORAGE) + 1)
    URL_STORAGE[unique_id] = url

    # Ask for quality selection
    buttons = [
        [InlineKeyboardButton("144p", callback_data=f"quality_144p|{unique_id}")],
        [InlineKeyboardButton("240p", callback_data=f"quality_240p|{unique_id}")],
        [InlineKeyboardButton("360p", callback_data=f"quality_360p|{unique_id}")],
        [InlineKeyboardButton("480p", callback_data=f"quality_480p|{unique_id}")],
        [InlineKeyboardButton("720p", callback_data=f"quality_720p|{unique_id}")],
        [InlineKeyboardButton("1080p", callback_data=f"quality_1080p|{unique_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        "Please select the video quality:",
        reply_markup=reply_markup
    )

# Quality Selection Callback
@bot.on_callback_query()
async def quality_callback(client: Client, callback_query):
    data = callback_query.data
    quality, unique_id = data.split("|")

    # Get the original URL using the unique_id
    url = URL_STORAGE.get(unique_id)

    if not url:
        await callback_query.message.edit_text("❌ URL not found.")
        return

    # Send processing message
    await callback_query.message.edit_text("Downloading video... Please wait.")

    # Map quality to format
    quality_map = {
        "quality_144p": "dash-8",
        "quality_240p": "dash-8",
        "quality_360p": "dash-7",
        "quality_480p": "dash-6",
        "quality_720p": "dash-3",
        "quality_1080p": "dash-1",
    }
    video_format = quality_map.get(quality, "dash-3")

    # yt-dlp options
    ydl_opts = {
        "format": f"{video_format}[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", "video").replace(" ", "_")
            video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")

        # Send the video file to the user
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=video_path,
            caption="Here is your downloaded video!"
        )

        # Clean up the downloaded file
        os.remove(video_path)
        await callback_query.message.delete()

    except Exception as e:
        await callback_query.message.edit_text(f"❌ Failed to download video: {e}")
