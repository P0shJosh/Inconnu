from ast import Num
import os

import discord
import random
from pymongo import MongoClient
from itertools import count, filterfalse
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
async def set(ctx, type, quantity):
  try:
    user = ctx.message.author.id
    record = mongo.stats.track.find_one({"user": user})
    if (type == "hp"):
      hp_total = ["0"] * int(quantity)
      if record == None:
        mongo.stats.track.insert_one({"user": user}, {"HP": hp_total})
      else:
        mongo.stats.track.update_one({"user": user}, {"$set": {"HP": hp_total}})
      await ctx.send(hp_total)
    if (type == "wp"):
      wp_total = [0] * int(quantity)
      if record == None:
        mongo.stats.track.insert_one({"user": user}, {"WP": wp_total})
      else:
        mongo.stats.track.update_one({"user": user}, {"$set": {"WP": wp_total}})
      await ctx.send(wp_total)
  except Exception as x:
    await ctx.send ("You've made a mistake there. Have a think.")
      
      
@inconnu.command()
async def hp(ctx, quantity, type):
  try:
    user = ctx.message.author.id
    record = mongo.stats.track.find_one({"user": user}, {"HP"})
    if (mongo.stats.track.find_one({"user": user}) == None):
      await ctx.send("You need to set your health limit first. Try '!set hp x' where x is your stamina + 3")
    else:
      if(type == "s"):
        currentHealth = record.pop("HP")
        currentHealth.sort()
        i = 0
        while i < int(quantity):
          if(currentHealth[i] == "0"):
            currentHealth[i] = "1"
          elif(currentHealth[i] == "1"):
            currentHealth[i] = "2"
          else:
            await ctx.send("No more for you, you enter torpor.")
            break
          i += 1
        currentHealth.sort(reverse=True)
        print(currentHealth)
        mongo.stats.track.update_one({"user": user}, {"$set": {"HP": currentHealth}})
        embed = discord.Embed(description="Current Health: " + "   ".join(currentHealth), color=0xCA0303)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
  except Exception as x:
    await ctx.send ("You've made a mistake there. Have a think.")
    

inconnu.run(TOKEN) 