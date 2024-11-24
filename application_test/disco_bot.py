# %%

import discord
from PIL import Image
import asyncio

TOKEN = "MTMwOTQyNjc3NDAwOTk3NDg3NA.G4v112.06AVIquouZ-nznSejhxXE4_zGtF9N3VOugKKSI"

client = discord.Client(intents=discord.Intents.default())
channel_id = 1310154336147472405
#channel_id = 1310154109558722561


@client.event
async def on_ready():
    print("ログインしました")
    channel = client.get_channel(channel_id)
    if channel is not None:
        await channel.send("ログインしました")
    else:
        print(f"チャンネルID {channel_id} が見つかりません。")


@client.event
async def on_message(message):
    if message.content == '/runbot':
        global channel
        global channel_id
        channel_id = message.channel.id
        channel = client.get_channel(channel_id)
        print(f"ID : {channel_id}")
        await message.channel.send(f"chan_ID:{channel_id}\n起動しました")


async def send_image(file_path):
    try:
        channel = client.get_channel(channel_id)
        message_sent = await channel.send(file=discord.File(file_path))
    except Exception as e:
        print(f"ERROR<send_image>:{e}")
    return message_sent.attachments[0].url if message_sent.attachments else None


def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(TOKEN))
