import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal, Optional
import os
name = os.path.splitext(os.path.basename(__file__))[0]
import sys
sys.path.insert(1, '/home/asher/catscraper')
sys.path.insert(1, '/home/asher/clippy')
import requests
import time
from clip import Clippy

import shutil
from runner import scraper
class Scrapercat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.folder = "scrapedpics"
        self.c = Clippy(folder=self.folder)
        self.scraper = scraper(workers=3)
    @app_commands.command(name="getimages",description="Generates a gif of a google images search using my own google search scraper")
    async def getimages(
        self,
        interaction: discord.Interaction,
        search: str,
        show: bool,
        frametiming: float = 1.0,
        ftype: Optional[Literal["png","jpg","webp"]] = "jpg"
    ):
        begin = time.time()
        await interaction.response.defer(ephemeral=not show)
        
        search  += f" filetype:{ftype}"
    
        images = self.scraper.genimages(search,3)
        
        for filename in os.listdir(self.folder):
            file_path = os.path.join(self.folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        for index,link in enumerate(images):
            print(link)
            with requests.get(link, allow_redirects=True) as response, open(self.folder + f"/image({index}).{ftype}", 'wb') as f:
                #print(response.text)
                data = response.content
                f.write(data)
        print("done writing")
        gif = self.c.imagestogif(f"image(%d).{ftype}",frametiming=frametiming)
        end = time.time()
        print(f"[INFO] Generating the pictures took {end-begin} seconds")
        await interaction.followup.send(file=discord.File(self.folder + "/" + gif))
    @app_commands.command(name="getlinks", description="Experimental :3")
    async def getlinks(
        self,
        interaction: discord.Interaction,
        search: str
    ):
        await interaction.response.defer(ephemeral=True)
        images = self.scraper.genimages(search,3)
        await interaction.followup.send(images)
    
async def setup(bot: commands.Bot):
    global name
    await bot.add_cog(Scrapercat(bot))
    
    print(f"{name} loaded")

    channel = bot.get_channel(796072509039837207)
    message = await channel.fetch_message(bot.message)
    await message.add_reaction("⛏️")
    e = discord.Embed(title=message.embeds[0].title)
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}",f"{name} on!"))
    await message.edit(embed=e)