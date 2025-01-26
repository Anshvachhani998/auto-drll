
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

from pyrogram import Client, filters
import os
import youtube_dl

# Command to download video
@Client.on_message(filters.command("download") & filters.private)
async def download_video(client, message):
    try:
        # Extracting video URL and quality from command
        args = message.text.split()
        if len(args) < 3:
            await message.reply_text("Usage: /download <video_url> <quality (e.g., 720p)>")
            return

        video_url = args[1]
        quality = args[2]
        download_path = "./downloads"
        os.makedirs(download_path, exist_ok=True)

        # Map quality to format
        video_format = ''
        if quality == '144p':
            video_format = 'dash-8'
        elif quality == '240p':
            video_format = 'dash-8'
        elif quality == '360p':
            video_format = 'dash-7'
        elif quality == '480p':
            video_format = 'dash-6'
        elif quality == '540p':
            video_format = 'dash-5'
        elif quality == '720p':
            video_format = 'dash-3'
        elif quality == '1080p':
            video_format = 'dash-1'
        else:
            await message.reply_text("Invalid quality. Use one of: 144p, 240p, 360p, 480p, 540p, 720p, 1080p.")
            return

        ydl_opts = {
            'format': f'{video_format}[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        }

        await message.reply_text("Downloading video, please wait...")

        # Download video using youtube-dl
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)

            # Send the downloaded video to the user
            await message.reply_video(video=file_name, caption="Here is your video!")

            # Cleanup downloaded file
            os.remove(file_name)

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


