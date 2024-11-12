from pyrogram import Client, filters
import asyncio

API_ID = "21684037"
API_HASH = "cc4dda353688d66c94af69ca48a87bdb"
BOT_TOKEN = "8164925669:AAFrDltyWMahWLEtvnVbdx8-s1PjC-DpL8E"

CHANNEL_IDS = [-1002224233447]
GROUP_IDS = [-1002068352969, -1001930038276, -1001983504851, -1002003442851, -1001719021558]

app = Client("ansh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Welcome to the bot.")

@app.on_message(filters.chat(CHANNEL_IDS))
async def delete_channel_messages(client, message):
    try:
        await asyncio.sleep(14400)
        await message.delete()
        print(f"Deleted message from channel: {message.text}")
    except Exception as e:
        print(f"Error deleting message from channel: {e}")

@app.on_message(filters.chat(GROUP_IDS))
async def delete_group_messages(client, message):
    try:
        await asyncio.sleep(300)
        await message.delete()
        print(f"Deleted message from group: {message.text}")
    except Exception as e:
        print(f"Error deleting message from group: {e}")

if __name__ == "__main__":
    app.run()  # Run the bot directly without Flask or threads
