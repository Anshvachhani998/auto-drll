import asyncio
from pyrogram import Client, filters
import os
from flask import Flask

API_ID = "21684037"
API_HASH = "cc4dda353688d66c94af69ca48a87bdb"
BOT_TOKEN = "8164925669:AAFrDltyWMahWLEtvnVbdx8-s1PjC-DpL8E"

CHANNEL_IDS = [-1002224233447]
GROUP_IDS = [-1002068352969, -1001930038276, -1001983504851, -1002003442851, -1001719021558]

app = Client("ansh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

web_app = Flask(__name__)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Welcome to the bot.")

@app.on_message(filters.chat(CHANNEL_IDS))
async def delete_channel_messages(client, message):
    try:
        await asyncio.sleep(14400)  # Simulate waiting time
        await message.delete()
        print(f"Deleted message from channel: {message.text}") 
    except Exception as e:
        print(f"Error deleting message from channel: {e}")

@app.on_message(filters.chat(GROUP_IDS))
async def delete_group_messages(client, message):
    try:
        await asyncio.sleep(300)  # Simulate waiting time
        await message.delete()
        print(f"Deleted message from group: {message.text}")
    except Exception as e:
        print(f"Error deleting message from group: {e}")

# This function ensures the bot is responsive for health checks
async def health_check():
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    # Run Pyrogram bot
    app.run()  # This starts the Pyrogram bot

    # Running the health check task
    loop.create_task(health_check())  # Keep running health check task
    
    # Run Flask app on the dynamic port
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if no port is set
    web_app.run(host="0.0.0.0", port=port)  # Listen on the dynamic port
