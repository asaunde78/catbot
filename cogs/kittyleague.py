import discord
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

    def getRole(self, role):
        return [name for name,champ in self.champs["Champions"].items() if role in champ["Info"]["Position(s)"] ]
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
    async def sendquote(
        self,
        interaction : discord.Interaction
    ):      
        await interaction.response.defer()
        champ = random.choice(list(self.audios.items()))
        line = random.choice(list(champ[1].items()))
        # print(,,)
        name = champ[0]
        quote = line[0]
        link = list(line[1]["Files"].values())[0]


        file_name = f"{quote}" +".ogg"
        # link = audios[champ][quote]["Files"]["Original"]
        pic = self.champs["Champions"][name]["banner-link"]
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
        txt_clip = TextClip(quote,method="caption",color="white",size=(1215,150))


        txt_clip = txt_clip.set_pos("center").set_duration(audio_clip.duration)
        video_clip = CompositeVideoClip([video_clip, txt_clip])
        video_clip.duration = audio_clip.duration
        video_clip.write_videofile("leaguecontents/" + f"{name}"+".mp4")

        await interaction.followup.send(file=discord.File("leaguecontents/" + f"{name}"+".mp4"))

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
        await interaction.response.send_message(self.champs["Champions"][self.aliases[champ.lower()]]["champ-render"],ephemeral=True)

    @champrender.autocomplete("champ")
    async def champ_autocomple(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        champs = list(self.aliases.keys())
        return [
            app_commands.Choice(name=self.aliases[champ],value=champ)
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