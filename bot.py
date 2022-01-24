import os

import discord
import random
from pymongo import MongoClient
from discord.ext import commands
if os.path.exists("env.py"):
    import env


inconnu = commands.Bot(command_prefix = '!')
MongoDB = os.getenv("MONGO")
mongo = MongoClient(MongoDB)
TOKEN = os.getenv('DISCORD_TOKEN')

@inconnu.event
async def on_ready():
    print('The bot is now ready for use!')



@inconnu.command()
async def hello(ctx):
    await ctx.send("Hello, I am Inconnu")


@inconnu.command()
async def roll(ctx, quantity, hunger=""):
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


@inconnu.command()
async def hp(ctx, mod, quantity, type):
  try:
    user = ctx.message.author.id
    record = mongo.stats.track.find_one({"user": user})
    if record != None:
      if mod == "set":
        hp_total = [None] * int(quantity)
        mongo.stats.track.replace_one({"user": user}, {"total HP": hp_total})
        await ctx.send(hp_total)
      elif mod == "dam":
        hp_total = [None] * int(quantity)
        await ctx.send(user)
      elif mod == "heal":
        hp_total = [None] * int(quantity)
        await ctx.send(hp_total)
      else:
        await ctx.send ("Try '!hp help' for how to write the commands.")
    else:
      if mod == "set":
        hp_total = [None] * int(quantity)
        post = {"user": user, "total HP": hp_total}
        mongo.stats.track.insert_one(post)
        await ctx.send(post)
      else: 
        await ctx.send("You need to set your hp first")
  except Exception as x:
    await ctx.send ("You've made a mistake there. Have a think.")
    

inconnu.run(TOKEN) 