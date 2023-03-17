import discord, asyncio, random
from token_folder import token

import os
import subprocess

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-l","--laptop", help="laptop mode doesn't turn on time",action=argparse.BooleanOptionalAction)
args = ap.parse_args()
test = args.laptop




class ManageClient(discord.Client):
    def __init__(self,test,*args,**kwargs):
        self.test = test
        super().__init__(*args,**kwargs)
        self.greetings = ["MIAOU!", "CatBot reporting for duty!", "CatBot back online!","CatSystems turning on...", "I am a CatBot", "Miaou!", "CatOS loading..."]
        self.responses = ["! I'm CatBot!", "! You rang?", "! That's my name. Don't wear it out!", "! Did you just say my name?", ""]
        
        if test:
            self.bots = ["chat", "league","basic"]
        else:
            self.bots = ["chat", "league","basic","time"]
    async def on_ready(self):
        #await tree.sync(guild=discord.Object(id=token.guild))
        print('logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        game = discord.Game('miaou')
        await self.change_presence(status=discord.Status.online, activity=game)
        channel = self.get_channel(796072509039837207)
        

        #modified for laptop
        #self.bots = ["chat","league","basic","time"]
        #self.bots = ["chat","league","basic"]#,"time"]
        
        ip = subprocess.check_output("hostname -I".split()).decode().strip("\n")

        e=discord.Embed(title=random.choice(self.greetings))
        
        e.set_footer(text="IP: asher@" +ip +"\n" + '\n'.join(["Waiting for: " + bot for bot in self.bots]))
        announce = await channel.send(embed=e)
        print(announce.id)
        await announce.add_reaction("✅")

        #os.system("pkill screen")
        for bot in self.bots:
            os.system(f"./run.sh {bot} {str(announce.id)}")


    
    async def on_message(self,message):
         
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return
        
client = ManageClient(test,intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

@tree.command(name="ping",description="pings the bot :3",guild = discord.Object(id=token.guild))
async def ping(interaction):
    await interaction.response.send_message("Pong")
@tree.context_menu(name="hehe",guild =discord.Object(id=token.guild))
async def hehe(interaction: discord.Interaction, msg: discord.Message):
    await interaction.response.send_message(":thumbsup:")

    
client.run(token.discordtoken)