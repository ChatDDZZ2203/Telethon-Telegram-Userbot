import asyncio
import os
from flask import Flask, request
from telethon import TelegramClient, events
from telethon.sessions import StringSession

app = Flask(__name__)
client = TelegramClient(StringSession(os.getenv("LOGIN_STRING")),
                                      api_id=os.getenv("API_ID"),
                                      api_hash=os.getenv("API_HASH"))


@app.before_request
def main_handler():
    if request.form.get(os.getenv("PASS")):
        asyncio.run(main_definer())

async def main_definer():
  
    @client.on(events.NewMessage())
    async def handler(event):
        await client.send_message("@AUniqD", f"Hi from test Adaptable\n{event}")

    await client.start()
    await client.run_until_disconnected()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))





