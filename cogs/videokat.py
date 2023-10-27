import discord
from discord.ext import commands
from discord import app_commands
import random
import requests
from cogs.tools.videotogif import converter
import os,shutil
name = os.path.splitext(os.path.basename(__file__))[0]
import sys

    # caution: path[0] is reserved for script path (or '' in REPL)


sys.path.insert(1, '/home/asher/glimpse')
from glimpse import glimpser
class Videokat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = self.bot.myguild
        self.glimpser = glimpser()
        self.converter = converter()



    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == self.bot.user.id or message.author.id == 493938037189902358:
            return
        # print(message.embeds)
        for v in (v.video for v in message.embeds if v.video is not None):
            print(v.url)

            video_data = requests.get(v.url).content
            
            with open("gifgen/input.mp4", "wb") as handler:
                handler.write(video_data)
            self.converter.convert()
            
            await message.channel.send(file=discord.File("gifgen/gifgen.gif"))

            # if f is None:
            #     return
            # if not f.endswith((".mp4")):
            #     file_helper.remove(f)
            #     return
            
            
            # file_helper.remove(out)
        

    @app_commands.command(name="glimpse",description="Take a glimpse of a youtube video")
    async def glimpse(
        self,
        interaction: discord.Interaction,
        url: str,
        clips : int, 
        time : float = 0.0,
        sort :bool = False, 
        random_gap :float =10.0
    ) -> None:
        
        await interaction.response.defer(ephemeral=False)
        self.glimpser.genVideo(
            url,
            clips, 
            time,
            sort, 
            random_gap
        )
        
        
        await interaction.followup.send(file=discord.File("output_demuxer.mp4"))
        

        
    
async def setup(bot: commands.Bot):
    global name
    await bot.add_cog(Videokat(bot))
    #print(f"Guild: {bot.myguild}")

    print(f"{name} loaded")

    channel = bot.get_channel(796072509039837207)
    message = await channel.fetch_message(bot.message)
    await message.add_reaction("🎥")
    e = discord.Embed(title=message.embeds[0].title)
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}",f"{name} on!"))
    await message.edit(embed=e)
    