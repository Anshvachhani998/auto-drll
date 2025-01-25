from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):

    def __init__(self):
        super().__init__(
            "Ansh Login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Anshlogin"),
            workers=50,
            sleep_threshold=10
        )

      
    async def start(self):    
        await super().start()
        channel_id = -1002354362427
        await self.send_message(channel_id, "Bot started successfully!")
        print('Bot Started Powered By Ansh Vachhani')

    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

Bot().run()
