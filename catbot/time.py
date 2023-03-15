import discord, asyncio, random
from token_folder import token


import datetime

class TimeClient(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.clear = False
        self.next_clear = None

    def getnext(self):	
        now = datetime.datetime.now()
        next9 = now#datetime.datetime.now()
        next9 = next9.replace(hour=9,minute=0,second=0,microsecond=0)
        if(now > next9):
            next9 = next9.replace(day=next9.day+1) 
        return next9

    async def on_ready(self):
        print("catbot-time incoming... ")
        channel = self.get_channel(796072509039837207)
        await channel.send("catbot-time on")
    
    async def on_message(self,message):
         
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return

        if self.next_clear == None:
            with open("time.txt","w+") as r:
                try:
                    t = r.readlines()
                    
                    time = t[0].strip()
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
        

TimeClient(intents=discord.Intents.all()).run(token.discordtoken)