import os

import discord
import random
from discord.ext import commands
if os.path.exists("env.py"):
    import env


inconnu = commands.Bot(command_prefix = '!')
TOKEN = os.getenv('DISCORD_TOKEN')

@inconnu.event
async def on_ready():
    print('The bot is now ready for use!')


@inconnu.command()
async def hello(ctx):
    await ctx.send("Hello, I am Inconnu")


@inconnu.command()
async def roll(ctx, quantity, hunger):
  try:
    dice_pool = []
    hunger_pool = []
    for number in range(int(quantity)-int(hunger)):
       dice_pool.append(random.randint(1, 10))
    for number in range(int(hunger)):
       hunger_pool.append(random.randint(1, 10))
    results = ", ".join(str(number) for number in dice_pool)
    hunger_results = ", ".join(str(number) for number in hunger_pool)
    success = str(sum(number>5 for number in dice_pool)+sum(number>5 for number in hunger_pool))
    embed = discord.Embed(description="Dice Pool:" + " " + str(quantity), color=0xCA0303)
    embed.set_author(name=ctx.author.display_name + "'s roll", icon_url=ctx.author.avatar_url)
    embed.add_field(name="Number of successes:" + " " + success, value = results, inline=True)
    embed.add_field(name="Hunger", value = hunger_results, inline=True)
    await ctx.send(embed=embed)
  except Exception as x:
    await ctx.send("Idiot. !roll 'integer' with integer being your dice pool.")


inconnu.run(TOKEN) 