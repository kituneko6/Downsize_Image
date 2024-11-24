# %%

import discord
import Flet_GUI
from PIL import Image

TOKEN = "MTMwOTQyNjc3NDAwOTk3NDg3NA.GbU-Ka.BFIhX6b9EivPS2clVvUEYzuk-N9K6IrMLBF45o"

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print("ログインしました")


@client.events
async def on_massage(massage):
    if massage.auther.bot:    
        if massage.attachments:
            for attachment in massage.attachments:
                if attachment.url.endswith(("png","jpeg", "jpg")):
                    await massage.channel.send(attachment.url)

    
    if massage.content == "":
        image = Image.open('output.png')
        await massage.channel.send(file= discord.File(image))


    
client.run(TOKEN)
