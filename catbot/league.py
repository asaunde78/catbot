
import discord, asyncio, random
from token_folder import token

from bs4 import BeautifulSoup
import requests
import pathlib

import argparse
import os
ap = argparse.ArgumentParser()
ap.add_argument("-s","--source", help="the source message id")
args = ap.parse_args()
if args.source:
    source = int(args.source)
else:
    source = -1


class LeagueClient(discord.Client):
    def __init__(self,source,*args,**kwargs):
        super().__init__(*args,**kwargs)
        with open("/home/asher/leagueapi/leagueapi/champs/champs.json", "r") as r:
            self.champs = json.load(r)
        self.name = os.path.basename(__file__).strip(".py")
        self.source_message = source
    async def on_ready(self):
        #print('catbot-league incoming... ')
        #channel = self.get_channel(796072509039837207)
        #await channel.send("catbot-league on")
        channel = self.get_channel(796072509039837207)
        #await channel.send("catbot-template on")
        if not source == -1:
            message = await channel.fetch_message(self.source_message)
            await message.add_reaction("🎮")
            e = discord.Embed(title=message.embeds[0].title)
            
            e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {self.name}",f"{self.name} on!"))
            await message.edit(embed=e)
        else:
            await channel.send(f"catbot-{self.name} on")

    async def on_message(self, message):
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return
        
        
        

            

LeagueClient(source,intents=discord.Intents.all()).run(token.discordtoken)