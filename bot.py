import os

import discord
from discord.ext import commands
if os.path.exists("env.py"):
    import env


client = commands.Bot(command_prefix = '!')
TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print('The bot is now ready for use!')
    
@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am Inconnu")
    

client.run(TOKEN)