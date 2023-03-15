import discord, asyncio, random
from token_folder import token

import subprocess
import sys


class BasicClient(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.letters = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}
        self.word = 'nice'
        self.greetings = ["MIAOU!", "CatBot reporting for duty!", "CatBot back online!","CatSystems turning on...", "I am a CatBot", "Miaou!", "CatOS loading..."]
        self.responses = ["! I'm CatBot!", "! You rang?", "! That's my name. Don't wear it out!", "! Did you just say my name?", ""]
        self.intros = ["Hi, ", "Yo yo, ", "Wazaaa, ", "What's up, ", "Yo, "]
        self.answers = ["Yes!! :3","No.. :( Sorry :3","Ask again later... mrow :3","Hmm... I'm not sure. :3","Oh for sure ;3","No way, dude!! :3","I'm just a cat! idk! :3","Kitty say is: YES!!! :3","Kitty say is: NO!!!!! ;3"]

    async def on_ready(self):
        print('logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        game = discord.Game('miaou')
        await self.change_presence(status=discord.Status.online, activity=game)
        channel = self.get_channel(796072509039837207)
        
        ip = subprocess.check_output("hostname -I".split()).decode().strip("\n")
        await channel.send(random.choice(self.greetings)+ "\n IP: asher@" +ip)
    
    async def on_message(self,message):
         
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return
        msg = message.content.split()
        print(message.author.display_name+": "+ message.content)
        
        replied = False
        a_reply = False
        
        if message.reference is not None:
            a_reply = True
            reply = await message.channel.fetch_message(message.reference.message_id)
            if(reply.author.id == bot.user.id):
                replied = True


        if message.content.startswith('csay '):
            text = message.content.replace("csay ", '', 1)
            await message.delete()
            if(a_reply):
                await reply.reply(text)
            else:
                await message.channel.send(text)


        if message.content.startswith('question: '):
            question = message.content[len('question: '):]
            random.seed(abs(hash(question)))
            out = random.choice(self.answers)
            random.seed()
            await message.channel.send(out)


        if message.content.startswith('change word '):
            self.word = message.content.replace('change word ','')


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
            if item.upper() == self.word.upper() or item == self.user.mention:
                for a in list(self.word):
                    if(a in self.letters):
                        await message.add_reaction(self.letters[a])
            if item == self.user.mention:
                
                await message.channel.send(random.choice(self.intros)+ message.author.mention + random.choice(self.responses))


BasicClient(intents=discord.Intents.all()).run(token.discordtoken)