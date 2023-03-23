import discord

from discord.ext import commands

from token_folder import token
from discord.ext.commands import Greedy,Context
from discord import app_commands
import os 

class catbot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.myguild = token.guild
        self.tenortoken = token.tenortoken

client = catbot(command_prefix="~",intents=discord.Intents.all())

# client = commands.Bot(command_prefix="~",intents=discord.Intents.all())

# @app_commands.command(name="test")
# async def test(
#     interaction: discord.Interaction,
#     text: str
# ) -> None:
#     await interaction.response.send_message(text)

@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: Context) -> None:
    ctx.bot.tree.copy_global_to(guild=ctx.guild)
    s = await ctx.bot.tree.sync(guild=ctx.guild)
    print(ctx.bot.tree)
    print(ctx.guild.__class__)
    await ctx.channel.send(f"Synced {len(s)}")
@client.command()
@commands.guild_only()
@commands.is_owner()
async def desync(
    ctx: Context,
    glo: bool = True
) -> None:
    if(glo):
        c = ctx.bot.tree.clear_commands(guild=None)
        s = await ctx.bot.tree.sync(guild=None)
    else:
        c = ctx.bot.tree.clear_commands(guild=ctx.guild)
        s = await ctx.bot.tree.sync(guild=ctx.guild)
    #ctx.bot.tree.sync()
    await ctx.channel.send(f"Cleared {c}")

@client.command()
@commands.guild_only()
@commands.is_owner()
async def fetch(
    ctx: Context,
    glo: bool = True
) -> None:
    if(glo):
        c = await ctx.bot.tree.fetch_commands(guild=None)
    else:
        c = await ctx.bot.tree.fetch_commands(guild=ctx.guild)
    #ctx.bot.tree.sync()
    await ctx.channel.send(f"Featched {c}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print("Catbot getting ready")
    await load_cogs()

client.run(token.discordtoken)