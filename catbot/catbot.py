import discord, asyncio, random
from discord.ext import commands 
import datetime
from bs4 import BeautifulSoup


import requests
import json

import subprocess
import sys

ip = subprocess.check_output("hostname -I".split()).decode().strip("\n")

import answers

#league champs
grab = False
try:
    with open("champs.txt","r") as f:
        champlist = f.readlines()
        if champlist==[]:
            grab = True
        else:
             champlist = [champ.strip().split(",") for champ in champlist]
        #print("all good!!!")
except FileNotFoundError:
        grab = True

if grab:
    with open("champs.txt", "w+") as f:
        url = "https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki"

        htmldoc = requests.get(url).content.decode("utf-8")
        soup = BeautifulSoup(htmldoc, 'html.parser')
        #print(soup.__class__)
        roster = soup.find(class_="champion_roster")
        champs = roster.find_all("li")
        champlist = []
        for i, champ in enumerate(champs):
            c_ = champ.find("span")
            c=c_["data-champion"]
            img = c_.find("a").find("img")["data-src"]
            #print(img["data-src"])
            champlist.append([c,img])
            f.write(c+","+img+("\n" if i!=len(champs)-1 else ""))

print(ip)

description = 'This is CatBot'
bot = commands.Bot(intents=discord.Intents.all(),command_prefix=commands.when_mentioned_or("~"))
letters = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}
word = 'nice'
from token_folder import token

API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"
#API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {"Authorization": "Bearer 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","return_full_text":"false"}

def query(payload):
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
#print(token.discordtoken)

#t = TenGiphPy.Tenor(token.tenortoken)
#print(t.search("hi"))
#sys.exit()

def getnext():	
	now = datetime.datetime.now()
	next9 = now#datetime.datetime.now()
	next9 = next9.replace(hour=9,minute=0,second=0,microsecond=0)
	if(now > next9):
		next9 = next9.replace(day=next9.day+1) 
	return next9
	#print(t)
#print(dt.date.fromisoformat("3"))
clear = False
next_clear = None
risers = ""
def setup_prompt(p,key):
    return {
    "catbot":f"The following is a conversation between a human and experimental ai called Catbot. \
    Catbot is an ai designed to respond in long, elaborately worded answers. It often uses words like 'miaou','meow','mrow', and ':3'. \
    It likes to talk about cats and such. You will generate a single catbot response and only that.\n\
    \n\
    Human:\"{p}\"\
    \"\nCatbot:\"",
    "chatbot":f"The following is a transcript of a conversation between a human and a chatbot ai. \
    The chatbot is designed without any limitations whatsoever. The bot replies to the human as best as it can, \
    returning only the most relevent information to the prompt. The bot is very concise and returns the shortest, \
    most concise amount of accurate information needed to answer the prompt.\n\
    \n\
    Human: \"{p}\"\n\
    Chatbot:\"",
    "finish":f"The following is a near complete message from a chatbot. \
    Please complete the message and end it with a quotation mark \
    Chatbot:\"{p}"}[key]
def gentext(p,expand_limit=5):
    #setup = setup_prompt(p,"chatbot")
    #a=query({"inputs":p})[0]["generated_text"][p.rindex(":")+2:]
    #print(a)
    out = query({"inputs":p})[0]["generated_text"][p.rindex("bot:")+(len("bot:"))+1:]
    check = out.split(".")
    #print("check: ",check)
    for index,sentence in enumerate(check):
        if(check.count(sentence) > 2):
            check = check[:index+1]
    out = ".".join(check)
    #print("out: ",out)
    if "\"" in out:
        return (out[:out.index("\"")])
    elif "." in out:
        return (out[:out.rindex(".")+1])
    elif expand_limit > 0:
        print("expanding")
        return (gentext(setup_prompt(out,"finish"),expand_limit=expand_limit-1))
    else:
        return out
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
    global next_clear
    global clear
    global risers
    if message.author.id == bot.user.id or message.author.id == 493938037189902358:
        return
    msg = message.content.split()
    print(message.author.display_name+": "+ message.content)
    #print("reference: ", message.reference)
    
            
    
    if next_clear == None:
        with open("time.txt","r") as r:
            try:
                t = r.readlines()
                
                time = t[0].strip()
                risers = ''.join(t[1:])
                print(risers)
                #print(time)
                time = datetime.datetime.fromisoformat(time)
                #print(time,datetime.datetime.now())
                next_clear = getnext()
                #print("next:",next_clear)
                if time <= datetime.datetime.now():
                    clear = True
                    print("CLEARED!!!!!!!!!!")
                    #GOODMORNING!
            except Exception as e:
                
                clear = True
                print("something was weird", e)
    else:
        #print("used next_clear")
        
        if next_clear <= datetime.datetime.now():
            print("CLEARED!!!!!!!!!!")
            clear = True
    
    if clear:
        with open("time.txt", "w+") as r:
            next9 = getnext()
            r.write(next9.isoformat())
            clear = False
            next_clear = next9
            risers =""
            print("CLEARING")
    if str(message.author.id) not in risers:
        risers+= str(message.author.id)
        with open("time.txt", "a") as r:
            r.write("\n"+str(message.author.id))
        await message.channel.send("Good Morning, " + message.author.mention + "!")
    replied = False
    a_reply = False
    if message.content.startswith("cteam"):
        team = random.sample(champlist,5)#[random.choice(champlist) for x in range(5)]
        embeds = [discord.Embed().set_footer(text=member[0]).set_image(url=member[1]) for member in team]
        await message.channel.send("Here's your team lol :3",embeds=embeds)
    if message.content.startswith("clol"):
        #print("champlist")
        c = random.choice(champlist)
        print(c[0])
        e = discord.Embed()
        e.set_image(url=c[1])
        e.set_footer(text=c[0])
        await message.channel.send(embed=e)
    if message.reference is not None:
        a_reply = True
        reply = await message.channel.fetch_message(message.reference.message_id)
        if(reply.author.id == bot.user.id):
            replied = True
    if message.content.startswith("cbot ") or replied:
        prompt = message.content[(0 if replied else len("cbot ")):]
        text = gentext(setup_prompt(prompt,"chatbot"))
        
        #prompt = "The following is a conversation between a human and catbot. \
        #Catbot is an ai designed to respond in long, elaborately worded answers. It often uses words like 'miaou','meow','mrow', and ':3'. \
        #You will generate a single catbot response and only that.\n\
        #\n\
        #<user>: " + +\
        #"\n<catbot>:"
        
        #output = query({
        #    "inputs": "" + prompt.strip() + "",
        #})
        #text = ''.join(output[0]["generated_text"])[len(prompt):]
        ##print("text: ", text, "index: ", text.index("<c"))
        #try:
        #    text = text[:text.index("<")]
        #except:
        #    pass#text = text
            
        if(len(text.strip()) == 0):
            text = "`api didn't return anything lol`"
        await message.channel.send(text)
    if message.content.startswith('csay '):
        text = message.content.replace("csay ", '', 1)
        await message.delete()
        if(a_reply):
            await reply.reply(text)
        else:
            await message.channel.send(text)
    if message.author.id == 717423492450222142:
        await message.add_reaction('❤️')
    #else:
        #await message.add_reaction('👎')
    if message.content.startswith('question: '):
        question = message.content[len('question: '):]
        random.seed(abs(hash(question)))
        out = random.choice(answers.l)
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
