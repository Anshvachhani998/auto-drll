import os

# Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6274601797:AAEFGZmOoKIcAWThUyipXZ-JX1GbFdlUXzk")

# Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", "21684037"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "cc4dda353688d66c94af69ca48a87bdb")

# Your Owner / Admin Id For Broadcast 
ADMINS = int(os.environ.get("ADMINS", "6073523936"))

DB_URI = os.environ.get("DB_URI", "mongodb+srv://Ansh089:Ansh089@cluster0.y8tpouc.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "Anshlogin")
