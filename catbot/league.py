
import discord, asyncio, random
from token_folder import token
from discord import app_commands
from bs4 import BeautifulSoup
import requests
import pathlib
import json
from typing import List 

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
        with open("/home/asher/leagueapi/champs/champs.json", "r") as r:
            self.champs = json.load(r)
        with open("/home/asher/leagueapi/champs/aliases.json", "r") as r:
            self.aliases = json.load(r)
        with open("/home/asher/leagueapi/items/items.json", "r") as r:
            self.items = json.load(r)
        self.name = os.path.basename(__file__).strip(".py")
        self.source_message = source
    def getRole(self, role):
        return [name for name,champ in self.champs["Champions"].items() if role in champ["Info"]["Position(s)"] ]
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
        if message.content.startswith("csync") and message.author.id == 179741296464887808:
            print("syncing...")
            await tree.sync(guild=discord.Object(id=token.guild))
            
           

client = LeagueClient(source,intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)
@tree.command(name="league-team",description="Generates a league of legends team",guild = discord.Object(id=token.guild))
async def cteam(interaction):
    roles = ["Bottom","Top","Middle","Support","Jungle"]
    team = {}
    order = random.sample(roles, 5)
    for x in range(len(order)):
        options = client.getRole(order[x])
        champ = ""
        while champ == "":
            temp = random.choice(options)
            if(not temp in team.values()):
                champ = temp
                team[order[x]] = champ
    await interaction.response.send_message(team)



#@tree.command(name="champ-pic",description="Sends a pic of the given champion!",guild=discord.Object(id=token.guild))
#@app_commands.command()#autocomplete(champ=champ_autocomplete)
@tree.command(name="champ-pic",description="Sends a pic of the given champion!",guild=discord.Object(id=token.guild))
async def champrender(interaction, champ: str):
    await interaction.response.send_message(client.champs["Champions"][client.aliases[champ.lower()]]["champ-render"],ephemeral=True)

@champrender.autocomplete("champ")
async def champ_autocomple(
    interaction: discord.Interaction,
     current: str
) -> List[app_commands.Choice[str]]:
    champs = list(client.aliases.keys())
    return [
        app_commands.Choice(name=client.aliases[champ],value=champ)
        for champ in champs if current.lower() in champ.lower()
    ]





client.run(token.discordtoken)