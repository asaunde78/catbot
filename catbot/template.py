import discord, asyncio, random
from token_folder import token



class TemplateClient(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    async def on_ready(self):
        print("catbot-template incoming... ")
        channel = self.get_channel(796072509039837207)
        await channel.send("catbot-template on")
    
    async def on_message(self,message):
         
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return
        

TemplateClient(intents=discord.Intents.all()).run(token.discordtoken)