import discord, asyncio, random
from token_folder import token


import datetime
import traceback 
import argparse
import os
ap = argparse.ArgumentParser()
ap.add_argument("-s","--source", help="the source message id")
args = ap.parse_args()
if args.source:
    source = int(args.source)
else:
    source = -1

class TimeClient(discord.Client):
    def __init__(self,source,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.clear = False
        self.next_clear = None
        self.name = os.path.basename(__file__).strip(".py")
        self.source_message = source

    def getnext(self):	
        now = datetime.datetime.now()
        next9 = now#datetime.datetime.now()
        next9 = next9.replace(hour=9,minute=0,second=0,microsecond=0)
        if(now > next9):
            next9 = next9.replace(day=next9.day+1) 
        return next9

    async def on_ready(self):
        #print("catbot-time incoming... ")
        #channel = self.get_channel(796072509039837207)
        #await channel.send("catbot-time on")
        channel = self.get_channel(796072509039837207)
        #await channel.send("catbot-template on")
        if not source == -1:
            message = await channel.fetch_message(self.source_message)
            await message.add_reaction("⏰")
            e = discord.Embed(title=message.embeds[0].title)
            
            e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {self.name}",f"{self.name} on!"))
            await message.edit(embed=e)
        else:
            await channel.send(f"catbot-{self.name} on")
    
    async def on_message(self,message):
         
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return

        if self.next_clear == None:
            with open("time.txt","r+") as r:
                try:
                    t = r.readlines()
                    #print(t)
                    if(t!=[]):
                        #print(t)
                        time = t[0].strip()
                    else:
                        time = datetime.datetime.now().isoformat()
                    self.risers = ''.join(t[1:])
                    print(self.risers)
                    #print(time)
                    time = datetime.datetime.fromisoformat(time)
                    #print(time,datetime.datetime.now())
                    self.next_clear = self.getnext()
                    #print("next:",next_clear)
                    if time <= datetime.datetime.now():
                        self.clear = True
                        print("CLEARED!!!!!!!!!!")
                        #GOODMORNING!
                except Exception as e:
                    
                    self.clear = True
                    print("something was weird", e)
                    traceback.print_exc()
        else:
            #print("used next_clear")
            
            if self.next_clear <= datetime.datetime.now():
                print("CLEARED!!!!!!!!!!")
                self.clear = True
    
        if self.clear:
            with open("time.txt", "w+") as r:
                next9 = self.getnext()
                r.write(next9.isoformat())
                self.clear = False
                self.next_clear = next9
                self.risers =""
                print("CLEARING")
        if str(message.author.id) not in self.risers:
            self.risers+= str(message.author.id)
            with open("time.txt", "a") as r:
                r.write("\n"+str(message.author.id))
            await message.channel.send("Good Morning, " + message.author.mention + "!")
        

TimeClient(source,intents=discord.Intents.all()).run(token.discordtoken)