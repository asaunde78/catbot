import discord
from discord.ext import commands
from discord import app_commands
import os
name = os.path.splitext(os.path.basename(__file__))[0]
class Template(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
async def setup(bot: commands.Bot):
    global name
    await bot.add_cog(Template(bot))
    
    print(f"{name} loaded")

    channel = bot.get_channel(796072509039837207)
    message = await channel.fetch_message(bot.message)
    await message.add_reaction("🐱")
    e = discord.Embed(title=message.embeds[0].title)
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}",f"{name} on!"))
    await message.edit(embed=e)