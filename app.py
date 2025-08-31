#dependecies 
import discord
import os
import requests
import json
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

#defined groups of words

sad_words = ["sad" ,"depressed", "unhappy", "angry" , "useless"]

good_words = ["cheer up",
                "everything will be better",
                "don't worry"]

banned_words = ["idiot",'stupid','i hate you']

protected_roles = ['Moderator', "Admin"]

# fetch quote function

def get_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = json.loads(response.text)
    quote = data[0]['q'] + " -" + data[0]["a"]
    return (quote)

#events

@client.event
async def on_ready():
    print("im ready")

@client.event
async def on_message(message):

    # if message is sent by user ignore
    if message.author == client.user:
        return
   
    
    #if a word from the banned words is used by a non admin or moderator, try to kick the user
    if any(word.lower() in message.content.lower() for word in banned_words) and not any(role.name in protected_roles for role in message.author.roles):
        try:
            await message.guild.kick(message.author)
            await message.channel.send(f"{message.author} was kicked for using a banned word")
        except Exception as e: 
            print(f"couldnt kick the user {e}")

    #if $banned words is sent list the banned words
    if message.content.startswith("banned words"):
        await message.channel.send(banned_words)

    #if $inspire is sent give a quote
    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    #if a sad word is used sent a happy phrase
    if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(good_words))

#Token needs to be defined with your bot Token
client.run(os.getenv("Token"))