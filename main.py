import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

prefix = "\\"

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
        result = " ".join(messageWithoutAdd)

        file = open(f"./lists/{message.guild.id}.txt", "a")
        file.write(result + "\n")
        file.close()

        await message.channel.send(f"Added {result} to the list!")

client.run(os.getenv('BOT_TOKEN'))