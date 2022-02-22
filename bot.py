from ast import Num
from asyncio.windows_events import NULL
import os

import discord
import random
from pymongo import MongoClient
from itertools import count, filterfalse
from discord.ext import commands
if os.path.exists("env.py"):
    import env


inconnu = commands.Bot(command_prefix = '/')
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
    await ctx.send("Idiot. !roll 'n' with n being your dice pool.")


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
      wp_total = ["0"] * int(quantity)
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
      currentHealth = record.pop("HP")
      currentHealth.sort()
      i = 0
      if(type == "s"):
        while i < int(quantity):
          if(len(currentHealth) <= i ):
            n = i - int(quantity)
          else:
            n = i
          if(currentHealth[n] == "0"):
            currentHealth[n] = "1"
          elif(currentHealth[n] == "1"):
            currentHealth[n] = "2"
          else:
            await ctx.send("No more for you, you enter torpor.")
            break
          i += 1
      elif(type == "a"):
        while i < int(quantity):
          if(len(currentHealth) <= i ):
            n = i - int(quantity)
          else:
            n = i
          if(currentHealth[n] == "2"):
            await ctx.send("No more for you, you enter torpor.")
            break
          else:
            currentHealth[n] = "2"
            i += 1
    currentHealth.sort(reverse=True)
    mongo.stats.track.update_one({"user": user}, {"$set": {"HP": currentHealth}})
    x = 0
    while x < len(currentHealth):
      if(currentHealth[x] == "0"):
        currentHealth[x] = "☐"
      elif(currentHealth[x] == "1"):
        currentHealth[x] = "◪"
      elif(currentHealth[x] == "2"):
        currentHealth[x] = "☒"
      x += 1
    embed = discord.Embed(description="**Current Health**: " + "   ".join(currentHealth), color=0xCA0303)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  except Exception as x:
    await ctx.send ("You've made a mistake there. Have a think.")

      
@inconnu.command()
async def wp(ctx, quantity, type):
  try:
    user = ctx.message.author.id
    record = mongo.stats.track.find_one({"user": user}, {"WP"})
    if (mongo.stats.track.find_one({"user": user}) == None):
      await ctx.send("You need to set your will limit first. Try '!set wp x' where x is your resolve + con")
    else:
      currentWill = record.pop("WP")
      currentWill.sort()
      i = 0
      if(type == "s"):
        while i < int(quantity):
          if(len(currentWill) <= i ):
            n = i - int(quantity)
          else:
            n = i
          if(currentWill[n] == "0"):
            currentWill[n] = "1"
          elif(currentWill[n] == "1"):
            currentWill[n] = "2"
          else:
            await ctx.send("No more for you, you enter torpor.")
            break
          i += 1
      elif(type == "a"):
        while i < int(quantity):
          if(len(currentWill) <= i ):
            n = i - int(quantity)
          else:
            n = i
          if(currentWill[n] == "2"):
            await ctx.send("No more for you, you enter torpor.")
            break
          else:
            currentWill[n] = "2"
            i += 1
    currentWill.sort(reverse=True)
    mongo.stats.track.update_one({"user": user}, {"$set": {"WP": currentWill}})
    x = 0
    while x < len(currentWill):
      if(currentWill[x] == "0"):
        currentWill[x] = "☐"
      elif(currentWill[x] == "1"):
        currentWill[x] = "◪"
      elif(currentWill[x] == "2"):
        currentWill[x] = "☒"
      x += 1
    embed = discord.Embed(description="**Current Will**: " + "   ".join(currentWill), color=0xCA0303)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  except Exception as x:
    await ctx.send ("You've made a mistake there. Have a think.")


inconnu.run(TOKEN) 