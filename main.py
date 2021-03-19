import discord
import os
import requests
import json
from riotwatcher import LolWatcher,ApiError
import random
from replit import db
from keep_alive import keep_alive

client=discord.Client()

curses=["...","..."]
responses=["Küfür yasaktır."]

def choose_hero(list):
  if len(list)==1:
    return("EE 1 tane yazdın onu oyna bari")
  quote="Bence "+random.choice(list)+" oyna kanka"
  return(quote)

def get_quote(nick):
  watcher = LolWatcher(os.getenv("API"))
  my_region = "tr1"
  me = watcher.summoner.by_name(my_region, f'{nick}')
  my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
  try:
    if  my_ranked_stats[0]["tier"] == "CHALLENGER":
      quote="Levelin: "+str(me["summonerLevel"])+" Rankın: "+ my_ranked_stats[0]["tier"]+" "+my_ranked_stats[0]["rank"]+" kardeşim e sporcu musun"
      return(quote)
    elif  my_ranked_stats[0]["tier"] == "GOLD":
      quote= "Levelin: "+str(me["summonerLevel"])+" Rankın: "+ my_ranked_stats[0]["tier"]+" "+my_ranked_stats[0]["rank"] + " helalin var hee"
      return(quote)
    elif (my_ranked_stats[0]["tier"] == "SILVER") or (my_ranked_stats[0]["tier"] == "BRONZE"):
      quote="Levelin: "+str(me["summonerLevel"])+" Rankın: "+ my_ranked_stats[0]["tier"]+" "+my_ranked_stats[0]["rank"]+" düzgün oyna şu oyunu"
      return(quote)
    elif my_ranked_stats[0]["tier"] == ("IRON"):
      quote="Levelin: "+str(me["summonerLevel"])+" Rankın: "+ my_ranked_stats[0]["tier"]+" "+my_ranked_stats[0]["rank"]+" sil oyunu sil sil sil"
      return(quote)
    else:
      quote="Levelin: "+str(me["summonerLevel"])+" Rankın: "+ my_ranked_stats[0]["tier"]+" "+my_ranked_stats[0]["rank"]+" Kardeşim şu oyunu bi bana da öğretiversene"
      return(quote)
  except:
    return("Doğru gir la")

@client.event
async def on_ready():
  print("{0.user} hazır".format(client))

@client.event
async def on_message(message):
  msg= message.content
  if message.author == client.user:
    return
  if msg.startswith("$yardım"):
    await message.channel.send(" '$nick:' komutuyla LOL'deki rankına bakabilirsin \n '$selam' komutuyla bana selam çakabilirsin \n '$rastgele:' komutuyla oynayacağın şampiyonu bana seçtirebilirsin \t Örnek Kullanım: $rastgele:Blitzcrank,Leona,Thresh")
  if msg.startswith("$nick:"):
    nick=str(msg).split(":")
    quote=get_quote(nick[1])
    await message.channel.send(quote)
  if msg.startswith("$selam"):
    await message.channel.send("Sana da selam")
  if any (word in msg.lower() for word in curses):
    with open("kufur_nick.txt","a") as kufur_nick:
      kufur_nick.write(str(msg)+" - ")
      kufur_nick.write(str(message.guild)+" - ")
      kufur_nick.write(str(message.author)+"\n")
    await message.channel.send(random.choice(responses))
    await message.delete()
  if msg.startswith("$rastgele:"):
    hero=str(msg).split(":")
    heroes=hero[1].split(",")
    list=[]
    for i in range(len(heroes)):
      list.append(heroes[i])
    await message.channel.send(choose_hero(list))
  
keep_alive()

client.run(os.getenv("TOKEN"))