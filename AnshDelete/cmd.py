import os
import asyncio 
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH
from database.db import db

ALLOWED_GROUP_IDS = [-1002118198358]  # Replace with your group IDs

# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url = "https://t.me/Legend_BoyCC")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"<b>👋 Hi {message.from_user.mention}, I am Msg Delete Bot.</b>", 
        reply_markup=reply_markup, 
        reply_to_message_id=message.id
    )



import os
import ffmpeg
import time

app = Client

# Function to resize and add black padding to make the video 9:16
def resize_video(input_video_path, output_video_path):
    ffmpeg.input(input_video_path).output(
        output_video_path,
        vf="scale=iw*min(720/iw\,1280/ih):ih*min(720/iw\,1280/ih),pad=720:1280:(ow-iw)/2:(oh-ih)/2:black"
    ).run()

@app.on_message(filters.video)
async def handle_video(client: Client, message: Message):
    # Send a "Processing" message to the user
    processing_msg = await message.reply("🚀 Processing your video... Please wait!")

    start_time = time.time()  # Start timer to measure processing time

    try:
        # Download the video sent by the user
        video_path = await message.download()

        # Define output path for resized video
        output_path = "resized_video.mp4"

        # Resize the video to 9:16 ratio with black borders
        resize_video(video_path, output_path)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Send the resized video back to the user with processing time
        await message.reply_video(output_path, caption=f"🚀 Video processed in {processing_time:.2f} seconds!")

    except Exception as e:
        # If any error occurs, send an error message
        await message.reply(f"⚠️ An error occurred: {str(e)}")

    finally:
        # Clean up downloaded files
        os.remove(video_path)
        os.remove(output_path)

        # Delete the "Processing" message after sending the resized video
        await processing_msg.delete()

