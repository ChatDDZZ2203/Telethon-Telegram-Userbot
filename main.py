import os
import asyncio
# import threading
import requests
from flask import Flask, request
from telethon import TelegramClient, events
from telethon.sessions import StringSession

app = Flask(__name__)
client = TelegramClient(
    StringSession(os.environ['SESSION_STRING']),
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"])
TG_MY_ID = int(os.environ["TG_MY_ID"])
LOGS = [int(u) for u in os.environ["LOGS"].split(", ")]
ip_address = requests.get('http://ipinfo.io/ip').text.strip()

@app.before_request
def main_handler():
    ID = request.form.get(os.environ["MAIN_PASS"])
    if ID == "RUN":
        if not client.is_connected():
#             print("the client is not connected")
            # main = threading.Thread(target=run_main_def)
            # main.start()
            asyncio.run(main_def())
    return "I`m here"


async def send_log(m):
    await client.send_message(entity=LOGS[0], reply_to=LOGS[1], message=m)

# def run_main_def():
#     print("got here")
#     asyncio.run(main_def())

async def main_def():
    await client.connect()
    try:
#         print("po")
#         print('here, connected...')
        await send_log(f"Connected from {ip_address}")

        @client.on(events.NewMessage(chats=["@download_it_bot"], incoming=True))
        async def delete_trash_messages(e):
            if e.message.reply_markup and e.message.reply_markup.rows[0].buttons[0].text == "🔥 Активировать Бота 🔥":
                await client.delete_messages(entity="@download_it_bot", message_ids=[e.message.id])
                await send_log(f"Deleted this message from @download_it_bot:\n{e.message.message}")

        await client.run_until_disconnected()

    except Exception as er:
        await send_log(f"Error in main_def:\n{er}")
        raise er


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 3000)))




