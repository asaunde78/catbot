import discord
from discord.ext import commands
from discord import app_commands
import requests
import json


name = "chatcat"
class Chatcat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"
        
        self.headers = {"Authorization": "Bearer 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","return_full_text":"false"}
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(self.bot.message)
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == self.bot.user.id or message.author.id == 493938037189902358:
            return
        replied = False
        a_reply = False
        if message.reference is not None:
            a_reply = True
            reply = await message.channel.fetch_message(message.reference.message_id)
            if(reply.author.id == self.bot.user.id):
                replied = True
        if replied:
            prompt = message.content
            text = self.gentext(self.setup_prompt(prompt,"chatbot"))
            if(len(text.strip()) == 0):
                text = "`api didn't return anything lol`"
            await message.channel.send(text)
    @app_commands.command(name="cbot",description="Talk to catbot")
    async def cbot(
        self,
        interaction: discord.Interaction,
        prompt: str
    ):
        await interaction.response.defer()#send_message("Loading...")
        text = self.gentext(self.setup_prompt(prompt,"chatbot"))
        if(len(text.strip()) == 0):
            text = "`api didn't return anything lol`"
        await interaction.followup.send(text)


    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        #print(response.content)
        return response.json()
    def setup_prompt(self,p,key):
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
    def gentext(self,p,expand_limit=5):
    
        out = self.query({"inputs":p})[0]["generated_text"][p.rindex("bot:")+(len("bot:"))+1:]
        check = out.split(".")
        
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
            return (self.gentext(self.setup_prompt(out,"finish"),expand_limit=expand_limit-1))
        else:
            return out
    
async def setup(bot: commands.Bot):
    global name
    await bot.add_cog(Chatcat(bot))
    
    print(f"{name} loaded")

    channel = bot.get_channel(796072509039837207)
    message = await channel.fetch_message(bot.message)
    await message.add_reaction("🗣️")
    e = discord.Embed(title=message.embeds[0].title)
    
    e.set_footer(text=message.embeds[0].footer.text.replace(f"Waiting for: {name}",f"{name} on!"))
    await message.edit(embed=e)