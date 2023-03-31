import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import json
from typing import List 
import random
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, TextClip
import requests
import pathlib

import os
name = os.path.splitext(os.path.basename(__file__))[0]
class Kittyleague(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.myguild = bot.myguild
        
        with open("/home/asher/leagueapi/champs/champs.json", "r") as r:
            self.champs = json.load(r)
        with open("/home/asher/leagueapi/champs/aliases.json", "r") as r:
            self.aliases = json.load(r)
        with open("/home/asher/leagueapi/items/items.json", "r") as r:
            self.items = json.load(r)
        with open("/home/asher/leagueapi/audio/audios.json", "r") as r:
            self.audios = json.load(r)

        
    def search(self, champ: str = None,tags: list =None,quote:str=None,skin:str=None):
        result = {}
        # if(champ):
        #     return {champ:self.audios[champ]}
        for name,champaudio in self.audios.items():
            result[name] = {}
            #print(name)
            if(champ):
                if not name == champ:
                    continue
            for linequote,data in champaudio.items():
                if(quote):
                    #print("hi")
                    if quote.lower() not in linequote.lower():
                        continue
                if(tags):
                    skip = False
                    for tag in tags:
                        if tag.lower() not in " ".join(data["Tags"]).lower():
                            #print(tag)
                            skip = True
                            break
                    if skip:
                        continue
                            
                if(skin):
                    #print("hi")
                    if skin not in data["Files"]:
                        continue
                #print(linequote)
                #print(data["Tags"])
                result[name][linequote] = data
            #print(result[name] if not name == "Aatrox" else "FART")
        for name,r in list(result.items()):
            if r == {}:
                #print("hello?")
                result.pop(name)
        return result
    def getRole(self, role):
        return [name for name,champ in self.champs.items() if role in champ["Info"]["Position(s)"] ]
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(self.bot.message)
    @app_commands.command(name="league-team",description="Generates a league of legends team")
    async def cteam(
        self,
        interaction
        )->None:
        roles = ["Bottom","Top","Middle","Support","Jungle"]
        team = {}
        order = random.sample(roles, 5)
        for x in range(len(order)):
            options = self.getRole(order[x])
            champ = ""
            while champ == "":
                temp = random.choice(options)
                if(not temp in team.values()):
                    champ = temp
                    team[order[x]] = champ
        await interaction.response.send_message(team)
    @app_commands.command(name="send-quote",description="Sends a video containing a picture of the champ and them saying the quote")
    @app_commands.rename(quote="contains")
    async def sendquote(
        self,
        interaction : discord.Interaction,
        champ: str = None,
        tags: str = None,
        quote: str = None,
        skin: str = None,
        show: bool = False
    ):      
        await interaction.response.defer(ephemeral=not show)
        asyncio.sleep(0.1)
        #champ = "Kalista"
        if(tags):
            tags = tags.split(",")
            print(tags)
        res = self.search(champ=champ,skin=skin,tags=tags,quote=quote)
        if len(list(res)) == 0:
            await interaction.followup.send("Coudln't find your search lol ;3")
            return
        print("Results: ", len(list(res)))

        name = random.choice(list(res.keys()))
        champdata = res[name]

        quote = random.choice(list(champdata.keys()))
        quotedata = champdata[quote]


        #print(quote,quotedata)
        if skin:
            link = quotedata["Files"][skin]
            skinname = skin
        else:
            skinname = random.choice(list(quotedata["Files"].keys()))
            link = quotedata["Files"][skinname]
        if(not skinname.isalpha()):
            s = skinname.split()
            skinname = " ".join([m for m in s if m.isalpha() or not(m.isnumeric() and int(m) < 2000)])
            print(skinname)
        #print(skinname)
        #print(quote,skinname)
        file_name = f"{quote}" +".ogg"
        # link = audios[champ][quote]["Files"]["Original"]
        print("Skin: ", skinname)
        pic = self.champs[name]["Skins"][skinname]["Splash"]

        #print("Skin: ", skin)
        #file_name = f"{quote}" +".ogg"
        # link = audios[champ][quote]["Files"]["Original"]
        #pic = self.champs[name]["Skins"][skin]["Splash"]
        pic_file = f"{name}" + ".jpg"
        with requests.get(link, allow_redirects=True) as response, open("leaguecontents/" + file_name, 'wb') as f:
            #print(response.text)
            data = response.content
            f.write(data)
        with requests.get(pic,allow_redirects=True) as response, open("leaguecontents/" + pic_file, "wb") as f:
            data = response.content
            f.write(data)
        audio_clip = AudioFileClip("leaguecontents/" + file_name)
        image_clip = ImageClip("leaguecontents/" + pic_file)

        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = 1
        # txt_clip = TextClip(quote+"\n-"+name,method="caption",color="white",size=(1215,150))
        txt_clip = TextClip(quote+"\n-"+name,stroke_width=1.5,stroke_color="black",method="caption",color="white",size=(1215,250),font="Roboto")


        # txt_clip = txt_clip.set_pos("center").set_duration(audio_clip.duration)
        txt_clip = txt_clip.set_pos(("center","bottom")).set_duration(audio_clip.duration)

        video_clip = CompositeVideoClip([video_clip, txt_clip])
        video_clip.duration = audio_clip.duration
        video_clip.write_videofile("leaguecontents/" + f"{name}"+".webm")

        await interaction.followup.send(file=discord.File("leaguecontents/" + f"{name}"+".webm"))

        pathlib.Path("leaguecontents/" + file_name).unlink(missing_ok=True)
        pathlib.Path("leaguecontents/" + pic_file).unlink(missing_ok=True)
        # pathlib.Path("leaguecontents/" + f"{name}"+".mp4").unlink(missing_ok=True)
    




    
    #@tree.command(name="champ-pic",description="Sends a pic of the given champion!",guild=discord.Object(id=token.guild))
    #@app_commands.command()#autocomplete(champ=champ_autocomplete)
    @app_commands.command(name="champ-pic",description="Sends a pic of the given champion!")
    async def champrender(
        self,
        interaction,
        champ: str
    ):
        await interaction.response.send_message(self.champs[self.aliases[champ.lower()]]["champ-render"],ephemeral=True)

    @champrender.autocomplete("champ")
    @sendquote.autocomplete("champ")
    async def champ_autocomple(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        champs = list(self.aliases.keys())
        return [
            app_commands.Choice(name=self.aliases[champ],value=self.aliases[champ])
            for champ in champs if current.lower() in champ.lower()
        ]
        

    


    
async def setup(bot: commands.Bot):
    global name
    await bot.add_cog(Kittyleague(bot))
    
    print(f"{name} loaded")

    channel = bot.get_channel(796072509039837207)
    message = await channel.fetch_message(bot.message)
    await message.add_reaction("🎮")
    e = discord.Embed(title=message.embeds[0].title)
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}",f"{name} on!"))
    await message.edit(embed=e)