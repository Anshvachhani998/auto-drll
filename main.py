import asyncio
from pyrogram import Client, filters
import os

API_ID = "21684037"
API_HASH = "cc4dda353688d66c94af69ca48a87bdb"
BOT_TOKEN = "7877654567:AAFLDysG33pCVLnUqfMwgTfLcKDKBfv_taQ"

CHANNEL_ID = -1002354362427

bot = Client("ansh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Welcome to the bot.")

@bot.on_start
async def on_bot_start(client):
    # Send a message to the admin when the bot starts
    try:
        await client.send_message(CHANNEL_ID, "Bot started successfully!")
    except Exception as e:
        print(f"Error sending start message to admin: {e}")
        
    bot.run()
