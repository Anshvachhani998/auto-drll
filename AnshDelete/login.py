import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    PhoneNumberInvalid, 
    PhoneCodeInvalid, 
    PhoneCodeExpired, 
    SessionPasswordNeeded, 
    PasswordHashInvalid
)
from config import API_ID, API_HASH
from database.db import db
from pyrogram.errors import Exception as PyrogramError



SESSION_STRING_SIZE = 351
ALLOWED_GROUP_IDS = [-1002118198358]  # Replace with your group ID(s)

# Define the bot client (using user session string)
@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client, message):
    user_data = await db.get_session(message.from_user.id)  
    if user_data is None:
        return 
    await db.set_session(message.from_user.id, session=None)  
    await message.reply("**Logout Successfully** ♦")

# Login functionality
@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def main(bot: Client, message: Message):
    user_data = await db.get_session(message.from_user.id)
    if user_data is not None:
        await message.reply("**You Are Already Logged In. First /logout Your Old Session. Then Log In Again.**")
        return 
    
    # Request user phone number
    user_id = int(message.from_user.id)
    phone_number_msg = await bot.ask(chat_id=user_id, text="<b>Please send your phone number which includes country code</b>\n<b>Example:</b> <code>+13124562345, +9171828181889</code>")
    
    if phone_number_msg.text == '/cancel':
        return await phone_number_msg.reply('<b>Process cancelled!</b>')
    
    phone_number = phone_number_msg.text
    client = Client(":memory:", API_ID, API_HASH)
    await client.connect()
    await phone_number_msg.reply("Sending OTP...")

    # Try sending OTP
    try:
        code = await client.send_code(phone_number)
        phone_code_msg = await bot.ask(user_id, "Please check for OTP and send it here. Format: `1 2 3 4 5`.\n\n**Enter /cancel to cancel**", filters=filters.text, timeout=600)
    except PhoneNumberInvalid:
        await phone_number_msg.reply('`PHONE_NUMBER` **is invalid.**')
        return

    if phone_code_msg.text == '/cancel':
        return await phone_code_msg.reply('<b>Process cancelled!</b>')

    # Attempt sign-in with OTP
    try:
        phone_code = phone_code_msg.text.replace(" ", "")
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await phone_code_msg.reply('**OTP is invalid.**')
        return
    except PhoneCodeExpired:
        await phone_code_msg.reply('**OTP has expired.**')
        return
    except SessionPasswordNeeded:
        two_step_msg = await bot.ask(user_id, '**Your account has two-step verification enabled. Please provide the password. Enter /cancel to cancel.**', filters=filters.text, timeout=300)
        if two_step_msg.text == '/cancel':
            return await two_step_msg.reply('<b>Process cancelled!</b>')
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('**Invalid Password Provided**')
            return
    
    # Store the session string
    string_session = await client.export_session_string()
    await client.disconnect()

    if len(string_session) < SESSION_STRING_SIZE:
        return await message.reply('<b>Invalid session string</b>')

    try:
        user_data = await db.get_session(message.from_user.id)
        if user_data is None:
            await db.set_session(message.from_user.id, session=string_session)
    except Exception as e:
        return await message.reply_text(f"<b>ERROR IN LOGIN:</b> `{e}`")

    await bot.send_message(message.from_user.id, "<b>Account Login Successful.\n\nIf You Get Any Error Related To AUTH KEY, First /logout and /login Again</b>")

@Client.on_message(filters.chat(ALLOWED_GROUP_IDS) & ~filters.private)
async def delete_messages(client: Client, message: Message):
    # Get the user's session string from the database
    user_data = await db.get_session(message.from_user.id)
    
    if user_data is None:
        return  # User is not logged in, so ignore the messages

    # Create a new client instance for the user using their session string
    try:
        user_client = Client(":memory:", session_string=user_data['session'], api_id=API_ID, api_hash=API_HASH)
        await user_client.connect()

        # Wait for 5 seconds (or adjust as needed)
        await asyncio.sleep(5)

        # Delete the message using the user's client
        await user_client.delete_messages(message.chat.id, message.message_id)
        print(f"Message deleted by user: {message.text}")

        # Disconnect the user client after operation
        await user_client.disconnect()

    except PyrogramError as e:
        print(f"Error deleting message as user: {e}")


