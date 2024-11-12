from pyrogram import Client, filters
from aiohttp import web
import asyncio
import threading

API_ID = "21684037"
API_HASH = "cc4dda353688d66c94af69ca48a87bdb"
BOT_TOKEN = "8164925669:AAFrDltyWMahWLEtvnVbdx8-s1PjC-DpL8E"

CHANNEL_IDS = [-1002224233447]
GROUP_IDS = [-1002068352969, -1001930038276, -1001983504851, -1002003442851, -1001719021558]

# Initialize Pyrogram Client
app = Client("ansh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define bot commands
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Welcome to the bot.")

@app.on_message(filters.chat(CHANNEL_IDS))
async def delete_channel_messages(client, message):
    try:
        await asyncio.sleep(14400)  # Wait for 4 hours
        await message.delete()
        print(f"Deleted message from channel: {message.text}")
    except Exception as e:
        print(f"Error deleting message from channel: {e}")

@app.on_message(filters.chat(GROUP_IDS))
async def delete_group_messages(client, message):
    try:
        await asyncio.sleep(300)  # Wait for 5 minutes
        await message.delete()
        print(f"Deleted message from group: {message.text}")
    except Exception as e:
        print(f"Error deleting message from group: {e}")

# Health check handler for aiohttp
async def health_check(request):
    return web.Response(text="Bot is running")

# Function to set up the aiohttp web server
async def web_server():
    server = web.Application()
    server.router.add_get("/", health_check)
    runner = web.AppRunner(server)
    await runner.setup()
    bind_address = "0.0.0.0"
    port = 8000
    site = web.TCPSite(runner, bind_address, port)
    await site.start()
    print(f"Health check server started at http://{bind_address}:{port}")
    while True:
        await asyncio.sleep(3600)  # Keep running to serve the health check

# Main function to run bot and web server concurrently
async def main():
    # Create tasks for both the bot and the web server
    bot_task = asyncio.create_task(app.run())
    web_task = asyncio.create_task(web_server())

    # Wait for both tasks to finish (they run indefinitely)
    await bot_task
    await web_task

if __name__ == "__main__":
    # Run both the bot and the web server in an asyncio event loop
    asyncio.run(main())
