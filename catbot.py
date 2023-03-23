import discord

from discord.ext import commands

from token_folder import token
from discord.ext.commands import Greedy,Context
import os 

class catbot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.myguild = token.guild

client = catbot(command_prefix="~",intents=discord.Intents.all())

# client = commands.Bot(command_prefix="~",intents=discord.Intents.all())

@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: Context) -> None:
    s = await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.channel.send(f"Synced?{s}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
    await load_cogs()

client.run(token.discordtoken)