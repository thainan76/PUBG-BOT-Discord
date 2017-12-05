import discord
from discord.ext import commands
import pypubg
from pypubg import core
import asyncio
import requests
import aiohttp
from datetime import datetime
import pdb
from ratelimit import rate_limited
import json

api = core.PUBGAPI("ecb0deba-710c-411f-9342-630875d48a9e")
bot = commands.Bot(command_prefix='!')

@bot.event
@asyncio.coroutine
def on_ready():
    print ("Pronto quando você estiver!")
    print ("Estou rondando com o bot " + bot.user.name)
    print ("ID: " + bot.user.id)
    yield from bot.change_presence(game=discord.Game(name='!rank'))


@asyncio.coroutine
def get_stats_resp(username):
    headers = {"TRN-Api-Key": "ecb0deba-710c-411f-9342-630875d48a9e"}
    r = yield from aiohttp.get("https://pubgtracker.com/api/profile/pc/" + username, headers=headers)
    return r

def get_stat(stats, group, field, region, season):
    for grp in stats:
       if check_region_group_exists(stats, group, region, season):
         if grp["Match"] == group and grp["Region"] == region and grp["Season"] == season:
            for stat in grp["Stats"]:
                if stat["field"] == field:
                  return stat

def check_region_group_exists(stats, group, region, season):
    for grp in stats:
        if grp["Match"] == group and grp["Region"] == region and grp["Season"] == season:
            return True
    return False


async def pubHelp(ctx):
    print("FUNCINANDO")
    await bot.say("Comandos: \n\n**!pubStats**   ---> *[NICKCHAR] para saber seu rating*"
                            +"\n**!pubUrl**       ---> *para mostrar a URL do bot*")

async def ranka(ctx, username:str):
   try:
       print(api.player("Aminesia"))

   except:
      await bot.say(ctx.message.author.mention+", digite seu nick corretamente, não conseguimos localizar dados para a conta "+username+".")


@bot.command(pass_context=True)
async def rank(ctx, username: str):
     status = api.player(username)
     dic1 = get_stat(status["Stats"], "solo", "Rating", "sa", "2017-pre6")
     dic2 = get_stat(status["Stats"], "duo", "Rating", "sa", "2017-pre6")
     dic3 = get_stat(status["Stats"], "squad", "Rating", "sa", "2017-pre6")

     if dic1:
         rating1 = int(dic1["value"])
         modo_solo = "solo"
         print(rating1)
     else:
         rating1 = 0
         modo_solo = "solo"
         print(rating1)

     if dic2:
         rating2 = int(dic2["value"])
         modo_duo = "duo"
         print(rating2)
     else:
         rating2 = 0
         modo_duo = "duo"
         print(rating2)

     if dic3:
         rating3 = int(dic3["value"])
         modo_squad = "squad"
         print(rating3)
     else:
         rating3 = 0
         modo_squad = "squad"
         print(rating3)

     if rating1 > rating2 and rating1 > rating3:
         rating = int(dic1["value"])
         a = dic1["displayValue"]
         modo = modo_solo
     elif rating2 > rating1 and rating2 > rating3:
         rating = int(dic2["value"])
         a = dic2["displayValue"]
         modo = modo_duo
     elif rating3 > rating1 and rating3 > rating2:
         rating = int(dic3["value"])
         a = dic3["displayValue"]
         modo = modo_squad
     else:
         rating = 0
         a = str(rating)
         modo = "solo"

     if rating == 0 or rating <= 1500:
         ranking = " "
         rank_server = "Rating: 0 - 1500"
         num1 = "0"
         num2 = "1500"
     elif rating == 1501 or rating <=1800:
         ranking = ":third_place:"
         rank_server = "Rating: 1501 - 1800"
         num1 = "1501"
         num2 = "1800"
     elif rating == 1801 or rating <=2000:
         ranking = ":second_place:"
         rank_server = "Rating: 1801 - 2000"
         num1 = "1801"
         num2 = "2000"
     elif rating == 2001 or rating <=2200:
         ranking = ":first_place:"
         rank_server = "Rating: 2001 - 2200"
         num1 = "2001"
         num2 = "2200"
     else:
         ranking = ":trophy:"
         rank_server = "Rating: 2200 - mais"
         num1 = "2200"
         num2 = "mais"

     if  rank_server == "Rating: 1501 - 1800":
         role_add = discord.utils.get(ctx.message.server.roles, name=rank_server)
         role_remove_0_1500 = discord.utils.get(ctx.message.server.roles, name="Rating: 0 - 1500")
         role_remove_1801_2000 = discord.utils.get(ctx.message.server.roles, name="Rating: 1801 - 2000")
         role_remove_2001_2200 = discord.utils.get(ctx.message.server.roles, name="Rating: 2001 - 2200")
         role_remove_2200_mais = discord.utils.get(ctx.message.server.roles, name="Rating: 2200 - mais")
         await bot.remove_roles(ctx.message.author, role_remove_0_1500)
         await bot.remove_roles(ctx.message.author, role_remove_1801_2000)
         await bot.remove_roles(ctx.message.author, role_remove_2001_2200)
         await bot.remove_roles(ctx.message.author, role_remove_2200_mais)
         await bot.add_roles(ctx.message.author, role_add)
         print("FUNCIONOU 1")
     elif rank_server == "Rating: 1801 - 2000":
         role_add = discord.utils.get(ctx.message.server.roles, name=rank_server)
         role_remove_0_1500 = discord.utils.get(ctx.message.server.roles, name="Rating: 0 - 1500")
         role_remove_1501_1800 = discord.utils.get(ctx.message.server.roles, name="Rating: 1501 - 1800")
         role_remove_2001_2200 = discord.utils.get(ctx.message.server.roles, name="Rating: 2001 - 2200")
         role_remove_2200_mais = discord.utils.get(ctx.message.server.roles, name="Rating: 2200 - mais")
         await bot.remove_roles(ctx.message.author, role_remove_0_1500)
         await bot.remove_roles(ctx.message.author, role_remove_1501_1800)
         await bot.remove_roles(ctx.message.author, role_remove_2001_2200)
         await bot.remove_roles(ctx.message.author, role_remove_2200_mais)
         await bot.add_roles(ctx.message.author, role_add)
         print("FUNCIONOU 2")
     elif rank_server == "Rating: 0 - 1500":
         role_add = discord.utils.get(ctx.message.server.roles, name=rank_server)
         role_remove_1801_2000 = discord.utils.get(ctx.message.server.roles, name="Rating: 1801 - 2000")
         role_remove_1501_1800 = discord.utils.get(ctx.message.server.roles, name="Rating: 1501 - 1800")
         role_remove_2001_2200 = discord.utils.get(ctx.message.server.roles, name="Rating: 2001 - 2200")
         role_remove_2200_mais = discord.utils.get(ctx.message.server.roles, name="Rating: 2200 - mais")
         await bot.remove_roles(ctx.message.author, role_remove_2001_2200)
         await bot.remove_roles(ctx.message.author, role_remove_1801_2000)
         await bot.remove_roles(ctx.message.author, role_remove_2200_mais)
         await bot.remove_roles(ctx.message.author, role_remove_1501_1800)
         await bot.add_roles(ctx.message.author, role_add)
         print("FUNCIONOU 3")
     elif rank_server == "Rating: 2001 - 2200":
         role_add = discord.utils.get(ctx.message.server.roles, name=rank_server)
         role_remove_0_1500 = discord.utils.get(ctx.message.server.roles, name="Rating: 0 - 1500")
         role_remove_1501_1800 = discord.utils.get(ctx.message.server.roles, name="Rating: 1501 - 1800")
         role_remove_1801_2000 = discord.utils.get(ctx.message.server.roles, name="Rating: 1801 - 2000")
         role_remove_2200_mais = discord.utils.get(ctx.message.server.roles, name="Rating: 2200 - mais")
         await bot.remove_roles(ctx.message.author, role_remove_0_1500)
         await bot.remove_roles(ctx.message.author, role_remove_1501_1800)
         await bot.remove_roles(ctx.message.author, role_remove_1801_2000)
         await bot.remove_roles(ctx.message.author, role_remove_2200_mais)
         await bot.add_roles(ctx.message.author, role_add)
         print("FUNCIONOU 4")
     else:
         role_add = discord.utils.get(ctx.message.server.roles, name="Rating: 2200 - mais")
         role_remove_0_1500 = discord.utils.get(ctx.message.server.roles, name="Rating: 0 - 1500")
         role_remove_1501_1800 = discord.utils.get(ctx.message.server.roles, name="Rating: 1501 - 1800")
         role_remove_2001_2200 = discord.utils.get(ctx.message.server.roles, name="Rating: 2001 - 2200")
         role_remove_1801_2000 = discord.utils.get(ctx.message.server.roles, name="Rating: 1801 - 2000")
         await bot.remove_roles(ctx.message.author, role_remove_0_1500)
         await bot.remove_roles(ctx.message.author, role_remove_1501_1800)
         await bot.remove_roles(ctx.message.author, role_remove_1801_2000)
         await bot.remove_roles(ctx.message.author, role_remove_2001_2200)
         await bot.add_roles(ctx.message.author, role_add)
         print("FUNCIONOU 5")


     season = "2017-pre6"
     regiao = "sa"
     json_Rating = a
     t  = "\nSeu rating maximo para o nick: <" + username + "> é de: " + json_Rating + ", na Região: " + regiao.upper()+ ", na Season: " + season
     t += ", no Modo: " + modo.upper() + "."
     t += "\nSeu rank foi alterado para:" + ranking + "Rating - " + num1 + " a " + num2
     text = str(t)
     await bot.say("Olá " + ctx.message.author.mention + " !" + text)
       
bot.run('Mzg2MzkxNjUyMjAzMzY0MzUz.DQicGA.X5A-IxgOoZobP5d4gFuCZgSGp0U')
