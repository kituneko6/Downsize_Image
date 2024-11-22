# %%

import discode
from Flet_GUI import image_data
from PIL import Image

TOKEN = "MTMwOTQyNjc3NDAwOTk3NDg3NA.GwhQff.lw-EBf3EQVJXWzr9Zgy0cEUBYcT0ahB_CJrvm0"

client = discode.Client()

@client.event
async def on_ready():
    print("ログインしました")


@client.events
async def on_massage(massage):
    global image_url
    if massage.auther.bot:    
        if massage.attachments:
            for attachment in massage.attachments:
                if attachment.url.endswith(("png","jpeg", "jpg")):
                    await massage.chan

    
    if massage.content == "":
        image = Image.open(image_data)
        await massage.channel.send(file= discode.File(image))
        

        




client.run(TOKEN)



