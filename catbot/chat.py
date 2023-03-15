import discord, asyncio, random
from token_folder import token

import requests
import json

class ChatClient(discord.Client):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"
        self.headers = {"Authorization": "Bearer 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","return_full_text":"false"}

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        print(response)
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
    async def on_ready(self):
        print("catbot-chat incoming... ")
        channel = self.get_channel(796072509039837207)
        await channel.send("catbot-chat on")
    
    async def on_message(self,message):
         
        if message.author.id == self.user.id or message.author.id == 493938037189902358:
            return
        replied = False
        a_reply = False
        if message.reference is not None:
            a_reply = True
            reply = await message.channel.fetch_message(message.reference.message_id)
            if(reply.author.id == self.user.id):
                replied = True
        if message.content.startswith("cbot ") or replied:
            prompt = message.content[(0 if replied else len("cbot ")):]
            text = self.gentext(self.setup_prompt(prompt,"chatbot"))
            
            if(len(text.strip()) == 0):
                text = "`api didn't return anything lol`"
            await message.channel.send(text)
        

ChatClient(intents=discord.Intents.all()).run(token.discordtoken)