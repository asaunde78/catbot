import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal, Optional
import os
name = os.path.splitext(os.path.basename(__file__))[0]
import sys
sys.path.insert(1, '/home/asher/catscraper/blockerextension.crx')
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
        self.scraper = scraper(workers=1,server=True,folder=self.folder,fixname=False)
    @app_commands.command(name="collage",description="Genereates a collage of all the images from the google search")
    async def collage(
        self,
        interaction: discord.Interaction,
        search: str,
        show: bool = True,
        count: int = 12,
        squares: bool = True
        
    ):
        begin = time.time()
        await interaction.response.defer(ephemeral=not show)
        filesize = 15.0
        if count > 40:
            count = 40
        self.scraper.genimages(search,count,divide=True)
    
        collage = self.c.imagestocollage(filesize=filesize,count=count,squares=squares)
        end = time.time()
        print(f"[INFO] Generating the pictures and generating the collage took {end-begin} seconds")
        await interaction.followup.send(file=discord.File(self.folder + "/" + collage))
    @app_commands.command(name="getimages",description="Generates a gif of a google images search using my own google search scraper")
    async def getimages(
        self,
        interaction: discord.Interaction,
        search: str,
        show: bool = True,
        delay: float = 30.0,
        count: int = 12
        # quick: bool = False
        # ftype: Optional[Literal["png","jpg","webp"]] = "jpg"
    ):
        quick = False
        begin = time.time()
        await interaction.response.defer(ephemeral=not show)
        filesize = 15.0
        if count > 40:
            count = 40
        self.scraper.genimages(search,count,divide=True)
        if(not quick):
            gif = self.c.imagestogif(delay=delay,filesize=filesize)
        else:
            self.c.changeimagetype()
            gif = self.c.ffimagestogif(frametiming=delay)
        end = time.time()
        print(f"[INFO] Generating the pictures and generating the gif took {end-begin} seconds")
        await interaction.followup.send(file=discord.File(self.folder + "/" + gif))
    
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