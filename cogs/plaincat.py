import discord
from discord.ext import commands
from discord import app_commands
import random
import requests
import json
import os,shutil
name = os.path.splitext(os.path.basename(__file__))[0]
import sys
from google_images_search import GoogleImagesSearch
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/asher/clippy')


from clip import Clippy

class Plaincat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.clip = Clippy(folder = "images/")
        self.guild = self.bot.myguild
        self.tenortoken = bot.tenortoken
        self.cx = bot.cx
        self.apikey = bot.apikey
    
        self.letters = {'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿'}
        self.word = 'nice'
        self.responses = ["! I'm CatBot!", "! You rang?", "! That's my name. Don't wear it out!", "! Did you just say my name?", ""]
        self.intros = ["Hi, ", "Yo yo, ", "Wazaaa, ", "What's up, ", "Yo, "]
        self.answers = ["Yes!! :3","No.. :( Sorry :3","Ask again later... mrow :3","Hmm... I'm not sure. :3","Oh for sure ;3","No way, dude!! :3","I'm just a cat! idk! :3","Kitty say is: YES!!! :3","Kitty say is: NO!!!!! ;3"]
        

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(self.bot.message)
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == self.bot.user.id or message.author.id == 493938037189902358:
            return
        msg = message.content.split()
        print(message.author.display_name+": "+ message.content)
        for item in msg:
            if item.upper() == self.word.upper() or item == self.bot.user.mention:
                for a in list(self.word):
                    if(a in self.letters):
                        await message.add_reaction(self.letters[a])
            if item == self.bot.user.mention:
                
                await message.channel.send(random.choice(self.intros)+ message.author.mention + random.choice(self.responses))
    @app_commands.command(name="csay",description="Makes catbot say whatever you want!")
    async def csay(
        self,
        interaction: discord.Interaction,
        message: str
    ) -> None:
        await interaction.response.send_message("Okay I'll say that :3",ephemeral=True)
        await interaction.channel.send(message)
    
    @app_commands.command(name="gifgen", description="Turns the gif magic, ON! ;3 ")
    async def gengifs(
        self,
        interaction: discord.Interaction,
        search: str,
        count: int = 10,
        fps: int = 12,
        show: bool = False
    ):
        folder = 'images/'
        await interaction.response.defer(ephemeral=not show)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        imagesearch = GoogleImagesSearch(self.apikey,self.cx)
        _search_params = {
            'q':search,
            "num":count,
            "fileType":"png"
        }
        imagesearch.search(search_params=_search_params,path_to_dir=folder,width=800,height=600,custom_image_name="image")
        
        
        await interaction.followup.send(file=discord.File( folder + self.clip.imagestogif("image(%d).png",framerate=fps)))
        

        
        
    @app_commands.command(name="question",description="Magic 8-Ball style answers the given question")
    async def question(
        self,
        interaction: discord.Interaction,
        query: str
    ) -> None:
        random.seed(abs(hash(query)))
        out = random.choice(self.answers)
        random.seed()
        await interaction.response.send_message(out)
    

    @app_commands.command(name="change-word",description="Changes the \"Word of the Day\"")
    async def changeword(
        self,
        interaction: discord.Interaction,
        word: str
    ) -> None:
        self.word = word
        await interaction.response.send_message(f"Changed word to {word}")

    @app_commands.command(name="gif",description="Sends a gif using the given query")
    async def gif(
        self,
        interaction: discord.Interaction,
        query: str
    ) -> None:
        params = {'q':query}
        params['key']=self.tenortoken
        print(params)
        #params['q']="hello"
        response = requests.get("https://api.tenor.co/v2/search",params = params)
        results = json.loads(response.text)
        #['media'][0]['gif']['url']
        await interaction.response.send_message(random.choice(results['results'])['itemurl'])


    
async def setup(bot: commands.Bot):
    global name
    await bot.add_cog(Plaincat(bot))
    #print(f"Guild: {bot.myguild}")

    print(f"{name} loaded")

    channel = bot.get_channel(796072509039837207)
    message = await channel.fetch_message(bot.message)
    await message.add_reaction("🐱")
    e = discord.Embed(title=message.embeds[0].title)
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}",f"{name} on!"))
    await message.edit(embed=e)
    