import os

import discord
import random
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


@client.command()
async def roll(ctx, quantity):
  try:
    dice_pool = []
    for number in range(int(quantity)):
       dice_pool.append(random.randint(1, 10))
    results = ", ".join(str(number) for number in dice_pool)
    success = str(sum(number>5 for number in dice_pool))
    await ctx.send("Number of successes:" + success + "```" + results + "```")
  except Exception as x:
    await ctx.send("Idiot. !roll 'integer' with integer being your dice pool.")

client.run(TOKEN)