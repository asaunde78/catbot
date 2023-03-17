import discord, asyncio, random
from token_folder import token


import requests
import json

import argparse
import os
ap = argparse.ArgumentParser()
ap.add_argument("-s","--source", help="the source message id")
args = ap.parse_args()
if args.source:
    source = int(args.source)
else:
    source = -1


class BasicClient(discord.Client):
    def __init__(self,source,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.letters = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}
        self.word = 'nice'
        self.intros = ["Hi, ", "Yo yo, ", "Wazaaa, ", "What's up, ", "Yo, "]
        self.answers = ["Yes!! :3","No.. :( Sorry :3","Ask again later... mrow :3","Hmm... I'm not sure. :3","Oh for sure ;3","No way, dude!! :3","I'm just a cat! idk! :3","Kitty say is: YES!!! :3","Kitty say is: NO!!!!! ;3"]
        self.name = os.path.basename(__file__).strip(".py")
        self.source_message = source

    async def on_ready(self):
        #print('catbot-basic incoming... ')
        #channel = self.get_channel(796072509039837207)
        #await channel.send("catbot-basic on")
        channel = self.get_channel(796072509039837207)
        #await channel.send("catbot-template on")
        if not source == -1:
            message = await channel.fetch_message(self.source_message)
            await message.add_reaction("😂")
            e = discord.Embed(title=message.embeds[0].title)
            
            e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {self.name}",f"{self.name} on!"))
            await message.edit(embed=e)
        else:
            await channel.send(f"catbot-{self.name} on")
    
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
            if(reply.author.id == self.user.id):
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

client = BasicClient(source,intents=discord.Intents.all())


client.run(token.discordtoken)