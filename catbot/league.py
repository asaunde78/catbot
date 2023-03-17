
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
        url = "https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki"

        htmldoc = requests.get(url).content.decode("utf-8")
        soup = BeautifulSoup(htmldoc, 'html.parser')
        #print(soup.__class__)
        roster = soup.find(class_="champion_roster")
        champs = roster.find_all("li")
        champlist = []
        lolchamps = []
        for i, champ in enumerate(champs):
            c_ = champ.find("span")
            c=c_["data-champion"]
            img = c_.find("a").find("img")["data-src"]
            #print(img["data-src"])
            champlist.append([c,img])
            lolchamps.append(c)
        self.champlist = champlist
        self.lolchamps = lolchamps

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
        if message.content.startswith("cskin"):
            champ = message.content[len("cskin"):].strip()
            
            if champ == "":
                nice = random.choice(self.lolchamps)
                inp = "_".join((nice).split())

            else:
                i = [word.capitalize() for word in champ.strip().split()]
                nice = " ".join(i)
                inp = '_'.join(i)
            
            if(nice in self.lolchamps):
                url = f"https://leagueoflegends.fandom.com/wiki/{inp}/LoL/Cosmetics"

                htmldoc = requests.get(url).content.decode("utf-8")
                soup = BeautifulSoup(htmldoc, 'html.parser')

                skins = soup.find_all("div",class_="skin-icon")
                skin = random.choice(skins)
                imgs = skin.find("a")["href"]
                name = skin.find("img")["data-image-name"]
                e=discord.Embed(color=discord.Colour.light_gray())
                e.set_image(url=imgs)
                e.set_footer(text=name)
                await message.channel.send(embed=e)
            else:
                await message.channel.send("Sorry I don't know that champ :3")
        if message.content.startswith("caudio"):

            champ = message.content[len("caudio"):].strip()
            
            if champ == "":
                nice = random.choice(self.lolchamps)
                inp = "_".join((nice).split())

            else:
                i = [word.capitalize() for word in champ.strip().split()]
                nice = " ".join(i)
                inp = '_'.join(i)
            
            if(nice in self.lolchamps):
                url = f"https://leagueoflegends.fandom.com/wiki/{inp}/LoL/Audio"
                #print(url)
                htmldoc = requests.get(url).content.decode("utf-8")
                soup = BeautifulSoup(htmldoc, 'html.parser')
                
                audios = soup.find_all("li")
                name = [[audio.find("i"), audio.find("audio")] for audio in audios]

                a = []
                for val in name:
                    if not None in val:
                        a.append(val)
                audio = random.choice(a)
                #audio["value"]
                #print(a)
                name = "_".join(audio[0].text.split())
                file_name = f"{name}" +".ogg"
                audio = audio[1]["src"]


                with requests.get(audio, allow_redirects=True) as response, open(file_name, 'wb') as f:
                    #print(response.text)
                    data = response.content
                    f.write(data)
                    await message.channel.send(file=discord.File(file_name))
                pathlib.Path(file_name).unlink(missing_ok=True)
                
            else:
                await message.channel.send("Sorry I don't know that champ :3")
            #-------
            
        

            

LeagueClient(source,intents=discord.Intents.all()).run(token.discordtoken)