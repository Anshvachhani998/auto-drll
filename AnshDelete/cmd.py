import os
import asyncio 
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE

ALLOWED_GROUP_IDS = [-1002118198358]  # Replace with your group IDs

# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
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

# Delete messages in specific groups after 5 seconds
@Client.on_message(filters.chat(ALLOWED_GROUP_IDS) & ~filters.service)
async def delete_messages(client: Client, message: Message):
    try:
        await asyncio.sleep(5)  # Wait for 5 seconds
        await message.delete()  # Delete the message
    except Exception as e:
        print(f"Error deleting message: {e}")
