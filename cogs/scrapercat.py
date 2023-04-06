import discord
from discord.ext import commands
from discord import app_commands
import os
name = os.path.splitext(os.path.basename(__file__))[0]
import sys
sys.path.insert(1, '/home/asher/catscraper')
from runner import scraper
class Scrapercat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        self.scraper = scraper(workers=5)
    @app_commands.command(name="getimages", description="Experimental :3")
    async def getimages(
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
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}","{name} on!"))
    await message.edit(embed=e)