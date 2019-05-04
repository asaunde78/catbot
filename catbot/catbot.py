import discord, asyncio, random
from discord.ext import commands 
import datetime
description = 'This is CatBot'
bot = commands.Bot(command_prefix='~', description=description)

def isCatBot(string):
    cat = 'CATBOT'
    if len(string) < len(cat):
        return False
    for x in range(0, len(cat)):
        if string[x].capitalize() != cat[x]:
            return False
    return True
def intable(a):
    try:
        int(a)
        return int(a)
    except ValueError:
        return False
@bot.event
async def on_ready():
        print('logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('--------------')
        game = discord.Game('miaou')
        await bot.change_presence(status=discord.Status.online, activity=game)
        channel = bot.get_channel(573660693811691521)
        greeting = random.randint(1, 7)
        greetings = {1:"MIAOU!", 2:"CatBot reporting for duty!", 3:"CatBot back online!",4:"CatSystems turning on...", 5:"I am a CatBot", 6:"Miaou!", 7:"CatOS loading..."}
        await channel.send(greetings[greeting])
@bot.command()
async def h(ctx):
    
    messages = await ctx.history(limit = ).flatten()
    history  = random.randint(1,len(messages))
    for x in range(len(messages)-5, len(messages)):
        msg = messages[x].content.split()
        print(msg)
        if not '~h' in msg and messages[x].author.id != bot.user.id and messages[x].author.id != 493938037189902358:
            await ctx.send(messages[x].content + "\n by: " +str(messages[x].author))
@bot.command()
async def r(ctx, *, content):
    msg = content.split()
    times = intable(msg[0])
    if(times):
        msg.remove(msg[0])
    else:
        times = 1
    content = ' '.join(msg)
    for i in range(times):
        await ctx.send(content)
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id or message.author.id == 493938037189902358:
        return
    msg = message.content.split()
    for item in msg:
        if isCatBot(item) or item == bot.user.mention:
            responses = {1:"! I'm CatBot!", 2:"! You rang?", 3:"! That's my name. Don't wear it out!", 4:"! Did you just say my name?", 5:""}
            intros = {1:"Hi, ", 2:"Yo yo, ", 3:"Wazaaa, ", 4:"What's up, ", 5:"Yo, "}
            await message.channel.send(intros[random.randint(1,5)]+ message.author.mention + responses[random.randint(1,5)])
        if item == 'dm':
            await message.author.send("Hi! " + message.author.mention)
    await bot.process_commands(message)
from token_folder import token
bot.run(token)
