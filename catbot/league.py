
import discord, asyncio, random
from token_folder import token

from bs4 import BeautifulSoup
import requests

class LeagueClient(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        url = "https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki"

        htmldoc = requests.get(url).content.decode("utf-8")
        soup = BeautifulSoup(htmldoc, 'html.parser')
        #print(soup.__class__)
        roster = soup.find(class_="champion_roster")
        champs = roster.find_all("li")
        champlist = []
        for i, champ in enumerate(champs):
            c_ = champ.find("span")
            c=c_["data-champion"]
            img = c_.find("a").find("img")["data-src"]
            #print(img["data-src"])
            champlist.append([c,img])
        self.champlist = champlist
    async def on_ready(self):
        print('catbot-league incoming... ')
        channel = self.get_channel(796072509039837207)
        await channel.send("catbot-league on")

    async def on_message(self, message):
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return
        
        if message.content.startswith("cteam"):
            team = random.sample(self.champlist,5)
            embeds = [discord.Embed().set_footer(text=member[0]).set_image(url=member[1]) for member in team]
            await message.channel.send("Here's your team lol :3",embeds=embeds)
        if message.content.startswith("clol"):
            c = random.choice(self.champlist)
            print(c[0])
            e = discord.Embed()
            e.set_image(url=c[1])
            e.set_footer(text=c[0])
            await message.channel.send(embed=e)
            

LeagueClient(intents=discord.Intents.all()).run(token.discordtoken)