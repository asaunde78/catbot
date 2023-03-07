import discord, asyncio, random
from discord.ext import commands 
import datetime


import requests
import json

import subprocess
import sys

ip = subprocess.check_output("hostname -I".split()).decode().strip("\n")




print(ip)

description = 'This is CatBot'
bot = commands.Bot(intents=discord.Intents.all(),command_prefix=commands.when_mentioned_or("~"))
letters = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}
word = 'nice'
from token_folder import token
#print(token.discordtoken)

#t = TenGiphPy.Tenor(token.tenortoken)
#print(t.search("hi"))
#sys.exit()
def isWord(string, word):
    cat = word.upper()
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
        channel = bot.get_channel(796072509039837207)
        greeting = random.randint(1, 7)
        greetings = {1:"MIAOU!", 2:"CatBot reporting for duty!", 3:"CatBot back online!",4:"CatSystems turning on...", 5:"I am a CatBot", 6:"Miaou!", 7:"CatOS loading..."}
        await channel.send(greetings[greeting]+ "\n IP: pi@" +ip)
@bot.event
async def on_message(message):
    global word
    global t
    if message.author.id == bot.user.id or message.author.id == 493938037189902358:
        return
    msg = message.content.split()
    print(message.content)
    
    if message.content.startswith('c say '):
        text = message.content.replace("c say ", '', 1)
        await message.delete()
        await message.channel.send(text)
    if message.author.id == 717423492450222142:
        await message.add_reaction('❤️')
    #else:
        #await message.add_reaction('👎')
    if message.content.startswith('question: '):
        question = message.content[len('question: '):]
        random.seed(abs(hash(question)))
        out = random.choice(["Yes!! :3","No.. :( Sorry :3", "Ask again later... mrow :3"])
        random.seed()
        await message.channel.send(out)
        
    if message.content.startswith('change word '):
        word = message.content.replace('change word ','')
    #if message.content.startswith('g '):
    #    gif = message.content.replace('g ', '', 1)
    #    gif = ''.join(gif)
    #    results = t.search(gif,limit=10)
    #    print(results)
    #    g = random.choice(results)
    #    print(g)
    #    await message.channel.send("HI!")
    if message.content.startswith('g '):
        gif = message.content.replace('g ', '', 1)
        gif = ''.join(gif)
        params = {'q':gif}
        params['key']=token.tenortoken
        #params['q']="hello"

        response = requests.get("https://api.tenor.co/v2/search",params = params)
        results = json.loads(response.text)
        #['media'][0]['gif']['url']
        await message.channel.send(random.choice(results['results'])['itemurl'])
    for item in msg:
        if isWord(item, word) or item == bot.user.mention:
            for a in list(word):
                if(a in letters):
                    await message.add_reaction(letters[a])
        if item == bot.user.mention:
            responses = {1:"! I'm CatBot!", 2:"! You rang?", 3:"! That's my name. Don't wear it out!", 4:"! Did you just say my name?", 5:""}
            intros = {1:"Hi, ", 2:"Yo yo, ", 3:"Wazaaa, ", 4:"What's up, ", 5:"Yo, "}
            await message.channel.send(intros[random.randint(1,5)]+ message.author.mention + responses[random.randint(1,5)])
    await bot.process_commands(message)

bot.run(token.discordtoken)
