import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

prefix = "\\"

def getListOfWords(guildId):
    file = open(f"./lists/{guildId}.txt", "r")
    words = file.readlines()

    for i in range(len(words)):
        words[i] = words[i].strip()

    return words

def addToFile(word, guildId):
    list = getListOfWords(guildId)

    if(len(word) > 32):
        return 1
    elif(list.count(word.lower()) > 0):
        return 2
    else:
        file = open(f"./lists/{guildId}.txt", "a")
        file.write(word.lower() + "\n")
        file.close()
        return 0

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith(f'{prefix}add'):
        messageWithoutAdd = message.content.split(" ")
        messageWithoutAdd.pop(0)
        word = " ".join(messageWithoutAdd)

        errors = addToFile(word, message.guild.id)

        if(errors == 1):
            await message.channel.send(f"{word} has more than 32 characters!")
        elif(errors == 2):
            await message.channel.send(f"{word} has already been added!")
        else:
            await message.channel.send(f"Added {word} to the list!")


    if message.content.startswith(f'{prefix}show'):
        wordsList = getListOfWords(message.guild.id)
        await message.channel.send(f"Your words (there is {len(wordsList)} of them): \n ```{",".join(wordsList)}```")

client.run(os.getenv('BOT_TOKEN'))