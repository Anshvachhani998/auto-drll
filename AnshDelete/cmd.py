
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import API_ID, API_HASH

# Initialize the bot
bot = Client
app = Client

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
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import os

# Create folders if not exists
if not os.path.exists("videos"):
    os.makedirs("videos")

# Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to Text-to-Video Bot! Send me a text, and I'll create a video for you.")

# Text to Video Functionality
@app.on_message(filters.text & ~filters.command)
async def text_to_video(client, message):
    user_text = message.text
    await message.reply("Processing your video, please wait...")

    # Create video from text
    video_path = create_video(user_text)

    # Send the video to user
    await client.send_video(
        chat_id=message.chat.id,
        video=video_path,
        caption="Here's your video!"
    )

    # Clean up video
    os.remove(video_path)

# Video Creation Logic
def create_video(text):
    # Create an image
    img_width, img_height = 1280, 720
    img = Image.new("RGB", (img_width, img_height), color="black")
    draw = ImageDraw.Draw(img)

    # Add Text to the Image
    font = ImageFont.truetype("arial.ttf", 40)  # Use any font file
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (img_width - text_width) // 2
    text_y = (img_height - text_height) // 2
    draw.text((text_x, text_y), text, fill="white", font=font)

    # Save the image
    image_path = "videos/temp_image.png"
    img.save(image_path)

    # Create a video clip from the image
    clip = mp.ImageClip(image_path, duration=5)  # 5 seconds video
    clip = clip.set_fps(24).set_audio(None)  # No audio
    video_path = "videos/output_video.mp4"
    clip.write_videofile(video_path, codec="libx264")

    # Clean up temporary image
    os.remove(image_path)

    return video_path
