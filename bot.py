import discord
import random
import json
import os
import asyncio
import requests
from random import randint , choice
from discord.ext import commands
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Button, ButtonStyle
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import sys
import sqlite3
from config import setings
from PIL import Image
connection = sqlite3.connect('server.db')
cursor = connection.cursor()

TOKEN = setings["token"]
PREFIX = setings["prefix"]
version = setings["vers"]

bot = commands.AutoShardedBot(
    command_prefix=PREFIX, intents=discord.Intents.all())
client = bot
bot.remove_command('help')


@bot.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS bot (uptime INT)""")
    cursor.execute(f"INSERT INTO bot VALUES (0)")
    cursor.execute("UPDATE bot SET uptime =  {}".format(0))
    cursor.execute("""CREATE TABLE IF NOT EXISTS stats (id INT , name TEXT , win int, losing int , totalcpvp int ,  totalopen int)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS player (id INT , name TEXT, pvp int , regir int ,  lvl int , randkit int , money int , stashpvpkits int , regirpvpkits int)""")
    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM player WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO player VALUES ({member.id}, '{str(member.name)}' , 0 , 0 , 0 , 5 , 2 , 0 , 0 )")
            if cursor.execute(f"SELECT id FROM stats WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO stats VALUES ({member.id}, '{str(member.name)}' , 0 , 0 , 0 , 0)")
    connection.commit()
    print('Bot is ready')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('+help'))
    while True:
        cursor.execute(f'SELECT uptime FROM bot')
        do = cursor.fetchone()[0]
        do += 1
        cursor.execute("UPDATE bot SET uptime = uptime + {}".format(1))
        print(f"uptime {do} минут" )
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'+help | uptime {do} min | version {version}'))
        connection.commit()
        await asyncio.sleep(60)


@bot.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM player WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO player VALUES ({member.id}, '{str(member.name)}' , 0 , 0 , 0 , 5 , 2 , 0 , 0 )")
    if cursor.execute(f"SELECT id FROM stats WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO stats VALUES ({member.id}, '{str(member.name)}' , 0 , 0 , 0 , 0)")
    connection.commit()


#------------------------------



@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(aliases = ['i',"me","player"])
async def _player(ctx):
    cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
    if cursor == None:
        balance = 0
        cursor.execute(f"INSERT INTO player VALUES ({ctx.author.id}, '{ctx.author}' , 0 , 0 , 0 , 2)")
        ursor.execute(f"INSERT INTO stats VALUES ({member.id}, '{ctx.author}' , 0 , 0 , 0 , 0)")
        connection.commit()
        print(ctx.author)
    else:
        name = cursor.fetchone()[0]
        cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
        pvpkit = cursor.fetchone()[0]
        cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
        regirkit = cursor.fetchone()[0]
        cursor.execute(f'SELECT lvl FROM player WHERE id={ctx.author.id}')
        lvl = cursor.fetchone()[0]
        cursor.execute(f'SELECT randkit FROM player WHERE id={ctx.author.id}')
        randkit = cursor.fetchone()[0]
        cursor.execute(f'SELECT money FROM player WHERE id={ctx.author.id}')
        money = cursor.fetchone()[0]
        cursor.execute(f'SELECT regirpvpkits FROM player WHERE id={ctx.author.id}')
        regirpvpkits = cursor.fetchone()[0]
        cursor.execute(f'SELECT stashpvpkits FROM player WHERE id={ctx.author.id}')
        stashpvpkits = cursor.fetchone()[0]
        cursor.execute(f'SELECT win FROM stats WHERE id={ctx.author.id}')
        win = cursor.fetchone()[0]
        cursor.execute(f'SELECT losing FROM stats WHERE id={ctx.author.id}')
        losing = cursor.fetchone()[0]
        cursor.execute(f'SELECT totalcpvp FROM stats WHERE id={ctx.author.id}')
        totalcpvp = cursor.fetchone()[0]
        cursor.execute(f'SELECT totalopen FROM stats WHERE id={ctx.author.id}')
        totalopen = cursor.fetchone()[0]
        embed = discord.Embed(title=f"Привет {ctx.author.name}", description="Статистика", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
        embed.add_field(name=f"Имя вашего героя", value=f"{name} ({lvl} lvl) - {money}$", inline=True)
        embed.add_field(name=f"Количество китов", value=f"Pvp kits - {pvpkit}\Regear kits - {regirkit}\nRand kits - {randkit}", inline=True)
        embed.add_field(name=f"Стеш", value=f"Pvp kits - {stashpvpkits}\Regear kits - {regirpvpkits}", inline=True)
        embed.add_field(name=f"Полная статистика", value=f"----------", inline=False)
        embed.add_field(name=f"Всего cpvp - {totalcpvp}", value=f"Побед: {win}\nПроигрышей: {losing}", inline=True)
        embed.add_field(name=f"Всего открыто случайных китов", value=totalopen, inline=True)
        await ctx.send(embed = embed)
        connection.commit()

@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(aliases = ['open',"randkit","o"])
async def _openkit(ctx, amout: int = 1):
    cursor.execute(f'SELECT randkit FROM player WHERE id={ctx.author.id}')
    if cursor == None:
        balance = 0
        cursor.execute(f"INSERT INTO player VALUES ({ctx.author.id}, '{ctx.author}' , 0 , 0 , 0 , 5)")
        connection.commit()
        print(ctx.author)
    else:
        total = cursor.fetchone()[0]
        if amout == "all":
            amout = total
        if int(total) <= 0:
            cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
            name = cursor.fetchone()[0]
            await ctx.send(f"{name} у вас 0 рандомных китов")
            amout = -1
        if amout == 1 :
            cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
            name = cursor.fetchone()[0]
            if random.randint(1, 4) == 1:
                kit = "Pvp"
            else:
                kit = "Regear"
            cursor.execute("UPDATE player SET randkit = randkit - {} WHERE id = {}".format(1,ctx.author.id))
            cursor.execute("UPDATE stats SET totalopen = totalopen + {} WHERE id = {}".format(1,ctx.author.id))
            cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
            pvpkit = cursor.fetchone()[0]
            cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
            regirkit = cursor.fetchone()[0]
            if regirkit + pvpkit + 1 > 27:
                await ctx.send(f"{name} вам выпал {kit}\nВам не хватило место для всех китов . Они были перемещены на стеш")
                if kit == "Pvp":
                    cursor.execute("UPDATE player SET stashpvpkits = stashpvpkits + {} WHERE id = {}".format(1,ctx.author.id))
                else:
                    cursor.execute("UPDATE player SET regirpvpkits = regirpvpkits + {} WHERE id = {}".format(1,ctx.author.id))
            else:
                await ctx.send(f"{name} вам выпал {kit}")
                if kit == "Pvp":
                    cursor.execute("UPDATE player SET pvp = pvp + {} WHERE id = {}".format(1,ctx.author.id))
                else:
                    cursor.execute("UPDATE player SET regir = regir + {} WHERE id = {}".format(1,ctx.author.id))

        else:
            pvp = 0
            regir = 0
            if int(total) < amout:
                cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
                name = cursor.fetchone()[0]
                await ctx.send(f"{name} у вас нету {amout} рандомных китов")
                amout = -1
            while amout >= 1:
                amout -= 1
                cursor.execute("UPDATE stats SET totalopen = totalopen + {} WHERE id = {}".format(1,ctx.author.id))
                if random.randint(1, 4) == 1:
                    kit = "Pvp"
                    cursor.execute("UPDATE player SET randkit = randkit - {} WHERE id = {}".format(1,ctx.author.id))
                    pvp += 1
                else:
                    kit = "Regear "
                    cursor.execute("UPDATE player SET randkit = randkit - {} WHERE id = {}".format(1,ctx.author.id))
                    regir += 1
            cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
            name = cursor.fetchone()[0]
            if amout != -1:
                cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
                pvpkit = cursor.fetchone()[0]
                cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
                regirkit = cursor.fetchone()[0]
                if int(regirkit) + int(pvpkit) + int(pvp) + int(regir) > 27:
                    await ctx.send(f"{name} вам выпало {pvp} - пвп китов {regir} - регир китов\nВам не хватило место для всех китов . Они были перемещены на стеш")
                    cursor.execute("UPDATE player SET stashpvpkits = stashpvpkits + {} WHERE id = {}".format(int(pvp),ctx.author.id))
                    cursor.execute("UPDATE player SET regirpvpkits = regirpvpkits + {} WHERE id = {}".format(int(regir),ctx.author.id))
                else:
                    await ctx.send(f"{name} вам выпало {pvp} - пвп китов {regir} - регир китов")
                    cursor.execute("UPDATE player SET pvp = pvp + {} WHERE id = {}".format(int(pvp),ctx.author.id))
                    cursor.execute("UPDATE player SET regir = regir + {} WHERE id = {}".format(int(regir),ctx.author.id))
        connection.commit()


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(aliases = ['rename',"changename","playername"])
async def _name(ctx, *, name):
    p = 0
    for i in name:
        p += 1
    if p <= 13:
        cursor.execute("UPDATE player SET name = '{}' WHERE id = {}".format(name,ctx.author.id))
        cursor.execute("UPDATE stats SET name = '{}' WHERE id = {}".format(name,ctx.author.id))
        await ctx.send(f"Теперь твоего персонажа зовут {name}")
        connection.commit()
    else:
        await ctx.send(f"Ваш ник слишком большой ")


@commands.cooldown(1, 3600, commands.BucketType.user)
@bot.command()
async def freekits(ctx):
    await ctx.send(embed = discord.Embed(title=('Тебе было выдано 2 случайных китов'),description="**Пиши через час**"))
    cursor.execute("UPDATE player SET randkit = randkit + {} WHERE id = {}".format(2,ctx.author.id))
    connection.commit()


@commands.cooldown(1, 3600, commands.BucketType.user)
@bot.command()
async def steshhunt(ctx):
    chiso = random.randint(1, 1000)
    if chiso == 1:
        guild = choice(client.guilds)
        member = choice(guild.members)
        cursor.execute(f'SELECT regirpvpkits FROM player WHERE id={member.id}')
        regirpvpkits = cursor.fetchone()[0]
        cursor.execute(f'SELECT stashpvpkits FROM player WHERE id={member.id}')
        stashpvpkits = cursor.fetchone()[0]
        cursor.execute("UPDATE player SET stashpvpkits = stashpvpkits + {} WHERE id = {}".format(stashpvpkits,ctx.author.id))
        cursor.execute("UPDATE player SET regirpvpkits = regirpvpkits + {} WHERE id = {}".format(regirpvpkits,ctx.author.id))
        cursor.execute("UPDATE player SET stashpvpkits = stashpvpkits - {} WHERE id = {}".format(stashpvpkits,member.id))
        cursor.execute("UPDATE player SET regirpvpkits = regirpvpkits - {} WHERE id = {}".format(regirpvpkits,member.id))
        embed = discord.Embed(title="ВЫ НАШЛИ СТЕШ!", description=f"Это стеш {member}!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
        embed.add_field(name=f"Там было", value=f"Pvp kits - {stashpvpkits}\Regear kits - {regirpvpkits}", inline=True)
        await ctx.send(embed = embed)
    else:
        await ctx.send(f"Вы не нашли стеш")

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def cpvp(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"Вы не написали игрока с которым хотите cpvp")
    else:
        if member == ctx.author:
            await ctx.send(f"Вы не можете cpvp сам собой")
        else:
            cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
            name1 = cursor.fetchone()[0]
            cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
            pvpkit1 = int(cursor.fetchone()[0])
            cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
            regirkit1 = int(cursor.fetchone()[0])
            cursor.execute(f'SELECT lvl FROM player WHERE id={ctx.author.id}')
            lvl1 = int(cursor.fetchone()[0])
            cursor.execute(f'SELECT randkit FROM player WHERE id={ctx.author.id}')
            randkit1 = cursor.fetchone()[0]
            cursor.execute(f'SELECT name FROM player WHERE id={member.id}')
            name2 = cursor.fetchone()[0]
            cursor.execute(f'SELECT pvp FROM player WHERE id={member.id}')
            pvpkit2 = int(cursor.fetchone()[0])
            cursor.execute(f'SELECT regir FROM player WHERE id={member.id}')
            regirkit2 = int(cursor.fetchone()[0])
            cursor.execute(f'SELECT lvl FROM player WHERE id={member.id}')
            lvl2 = int(cursor.fetchone()[0])
            cursor.execute(f'SELECT randkit FROM player WHERE id={member.id}')
            randkit2 = cursor.fetchone()[0]
            #-----
            plus1 = 50
            plus2 = 50
            d1 = None
            if lvl1 < lvl2:
                d1 = True
                plus1 -= lvl2 - lvl1
                plus2 += lvl2 - lvl1
            elif lvl1 > lvl2:
                d1 = False
                plus1 += lvl2 - lvl1
                plus2 -= lvl2 - lvl1
            if regirkit1 >= 1:
                if regirkit2 < 1:
                    plus1 += 25
                    plus2 -= 25
            else:
                if regirkit2 >= 1:
                    plus1 -= 25
                    plus2 += 25
            if pvpkit1 >= 1:
                if pvpkit2 < 1:
                    plus1 += 50
                    plus2 -= 50
            else:
                if pvpkit2 >= 1:
                    plus1 -= 50
                    plus2 += 50

            chiso = random.randint(1, 100)
            if chiso - plus1 <= 0:
                winer = ctx.author
                nowiner = member
            else:
                winer = member
                nowiner = ctx.author
            cursor.execute(f'SELECT pvp FROM player WHERE id={nowiner.id}')
            pvpkit1 = cursor.fetchone()[0]
            if pvpkit1 >= 1:
                cursor.execute("UPDATE player SET pvp = pvp - {} WHERE id = {}".format(1,nowiner.id))
            cursor.execute(f'SELECT regir FROM player WHERE id={nowiner.id}')
            regirkit1 = cursor.fetchone()[0]
            if pvpkit1 >= 1:
                cursor.execute("UPDATE player SET regir = regir - {} WHERE id = {}".format(1,nowiner.id))
            cursor.execute("UPDATE stats SET win = win + {} WHERE id = {}".format(1,winer.id))
            cursor.execute("UPDATE stats SET losing = losing + {} WHERE id = {}".format(1,nowiner.id))
            cursor.execute("UPDATE stats SET totalcpvp = totalcpvp + {} WHERE id = {}".format(1,winer.id))
            cursor.execute("UPDATE stats SET totalcpvp = totalcpvp + {} WHERE id = {}".format(1,nowiner.id))
            #-----
            embed = discord.Embed(title=f"{name1} VS {name2}", description="Статистика cpvp", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
            if d1 == True and winer == ctx.author:
                cursor.execute("UPDATE player SET lvl = lvl + {} WHERE id = {}".format(1,winer.id))
                embed.add_field(name=f"Победитель {winer}", value=f"+1 уровень \n Пвп и регир кит вернулись обратно", inline=True)
                cursor.execute("UPDATE player SET randkit = randkit + {} WHERE id = {}".format(1,winer.id))
            elif d1 == False and winer == ctx.author:
                embed.add_field(name=f"Победитель {winer}", value=f"Пвп и регир кит вернулись обратно", inline=True)
                cursor.execute("UPDATE player SET randkit = randkit + {} WHERE id = {}".format(1,nowiner.id))
            elif d1 == False and winer == member:
                cursor.execute("UPDATE player SET lvl = lvl + {} WHERE id = {}".format(1,winer.id))
                embed.add_field(name=f"Победитель {winer}", value=f"+1 уровень \n Пвп и регир кит вернулись обратно", inline=True)
                cursor.execute("UPDATE player SET randkit = randkit + {} WHERE id = {}".format(1,winer.id))
            elif d1 == True and winer == member:
                embed.add_field(name=f"Победитель {winer}", value=f"Пвп и регир кит вернулись обратно", inline=True)
                cursor.execute("UPDATE player SET randkit = randkit + {} WHERE id = {}".format(1,nowiner.id))
            elif d1 is None :
                cursor.execute("UPDATE player SET lvl = lvl + {} WHERE id = {}".format(1,winer.id))
                embed.add_field(name=f"Победитель {winer}", value=f"+1 уровень \n Пвп и регир кит вернулись обратно", inline=True)
                cursor.execute("UPDATE player SET randkit = randkit + {} WHERE id = {}".format(1,winer.id))
            embed.add_field(name=f"Шансы", value=f"{plus1} \ {plus2}", inline=True)
            await ctx.send(embed = embed)
            connection.commit()


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(aliases = ['top',"l","lider"])
async def __top(ctx,top: int = 5):
    if top > 10:
        await ctx.send("Топ 10 максимум")
    else:
        Emb = discord.Embed(title= f"Топ {top} игркоков по lvl")
        cointer = 0
        for row in cursor.execute(f"SELECT name,lvl FROM player ORDER BY lvl DESC LIMIT {top} "):
            cointer += 1
            Emb.add_field(name = f"# {cointer} | **{row[0]}**",
                value = f"lvl : {row[1]}" , inline= True )
        cointer = 0
        Emb.add_field(name = f"Топ {top} игркоков по победам",value = f"--------" , inline= False )
        for row in cursor.execute(f"SELECT name ,  win FROM stats ORDER BY win DESC LIMIT {top} "):
            cointer += 1
            Emb.add_field(name = f"# {cointer} | **{row[0]}**",
                value = f"Wins : {row[1]}" , inline= True )
        await ctx.send(embed = Emb)

@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
async def botinfo(ctx):
    totalserver = 0
    totalrandopen = 0
    totalplayers = 0
    totalcpvp = 0
    activeservers = client.guilds
    for guild in activeservers:
        totalserver += 1
    for row in cursor.execute(f"SELECT totalcpvp ,totalopen FROM stats"):
        totalplayers += 1
        totalcpvp += row[0]
        totalrandopen += row[1]
    totalcpvp = totalcpvp/2
    cursor.execute(f'SELECT uptime FROM bot')
    do = cursor.fetchone()[0]
    embed = discord.Embed(title="Привет!", description="Полная статистика бота!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
    embed.add_field(name=f"Всего серверов", value=totalserver, inline=True)
    embed.add_field(name=f"Всего играют в нашем боте", value=totalplayers, inline=True)
    embed.add_field(name=f"Всего сыграно cpvp", value=totalcpvp, inline=True)
    embed.add_field(name=f"Всего открыто Rand kit", value=totalrandopen, inline=True)
    embed.add_field(name=f"Бот работает стабильно уже", value=f"{do} минут", inline=True)
    embed.add_field(name=f"Сервер поддержки бота", value="https://discord.gg/bkK8gcDjnH", inline=True)
    await ctx.reply(embed=embed)

@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
async def buy(ctx , kit , amout: int = 1):
    if kit == "pvp" and amout > 0 :
        cursor.execute(f'SELECT money FROM player WHERE id={ctx.author.id}')
        money = cursor.fetchone()[0]
        if money < 5 * amout:
            await ctx.reply("У тебя нету столько денег")
        else:
            chena = 5 * amout
            cursor.execute("UPDATE player SET money = money - {} WHERE id = {}".format(chena,ctx.author.id))
            cursor.execute("UPDATE player SET pvp = pvp + {} WHERE id = {}".format(amout,ctx.author.id))
            await ctx.reply(f"Спасибо за покупку \n{amout} {kit} китов было куплено за {chena}")
    elif kit == "regear" and amout > 0 :
        cursor.execute(f'SELECT money FROM player WHERE id={ctx.author.id}')
        money = cursor.fetchone()[0]
        if money < 1 * amout:
            await ctx.reply("У тебя нету столько денег")
        else:
            chena = 1 * amout
            cursor.execute("UPDATE player SET money = money - {} WHERE id = {}".format(chena,ctx.author.id))
            cursor.execute("UPDATE player SET regir = regir + {} WHERE id = {}".format(amout,ctx.author.id))
            await ctx.reply(f"Спасибо за покупку \n{amout} {kit} китов было куплено за {chena}")
    else:
        await ctx.reply("У меня есть только pvp и regear киты")
    connection.commit()

@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
async def sell(ctx , kit , amout: int = 1):
    if kit == "pvp" and amout > 0 :
        cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
        money = cursor.fetchone()[0]
        if money < amout:
            await ctx.reply("У тебя нету столько китов")
        else:
            chena = 2.5 * amout
            cursor.execute("UPDATE player SET money = money + {} WHERE id = {}".format(chena,ctx.author.id))
            cursor.execute("UPDATE player SET pvp = pvp - {} WHERE id = {}".format(amout,ctx.author.id))
            await ctx.reply(f"Спасибо за покупку \n{amout} {kit} китов было продано за {chena}")
    elif kit == "regear" and amout > 0 :
        cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
        money = cursor.fetchone()[0]
        if money < amout:
            await ctx.reply("У тебя нету столько китов")
        else:
            chena = 0.5 * amout
            cursor.execute("UPDATE player SET money = money + {} WHERE id = {}".format(chena,ctx.author.id))
            cursor.execute("UPDATE player SET regir = regir - {} WHERE id = {}".format(amout,ctx.author.id))
            await ctx.reply(f"Спасибо за покупку \n{amout} {kit} китов было продано за {chena}")
    else:
        await ctx.reply("Мы покупаем только pvp и regear киты")
    connection.commit()


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command()
async def stesh(ctx , who ,  kit , amout: int = 1):
    if who == "give" and amout > 0.9 :
        if kit == "pvp":
            cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
            money = cursor.fetchone()[0]
            if money < amout:
                await ctx.reply("У тебя нету столько китов")
            else:
                cursor.execute("UPDATE player SET pvp = pvp - {} WHERE id = {}".format(amout,ctx.author.id))
                cursor.execute("UPDATE player SET stashpvpkits = stashpvpkits + {} WHERE id = {}".format(amout,ctx.author.id))
                await ctx.reply(f"{amout} {kit} китов было переведено на стеш ")
        elif kit == "regear":
            cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
            money = cursor.fetchone()[0]
            if money < amout:
                await ctx.reply("У тебя нету столько китов")
            else:
                cursor.execute("UPDATE player SET regir = regir - {} WHERE id = {}".format(amout,ctx.author.id))
                cursor.execute("UPDATE player SET regirpvpkits = regirpvpkits + {} WHERE id = {}".format(amout,ctx.author.id))
                await ctx.reply(f"{amout} {kit} китов было переведено на стеш ")
        else:
            await ctx.reply(f"Кита {kit} нету")
    elif who == "take" and amout > 0 :
        if kit == "pvp":
            cursor.execute(f'SELECT stashpvpkits FROM player WHERE id={ctx.author.id}')
            money = cursor.fetchone()[0]
            cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
            money2 = cursor.fetchone()[0]
            cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
            money3 = cursor.fetchone()[0]
            if money < amout:
                await ctx.reply("У тебя нету столько китов")
            elif money2 + money3 + amout > 27:
                await ctx.reply("Нету места")
            else:
                cursor.execute("UPDATE player SET pvp = pvp + {} WHERE id = {}".format(amout,ctx.author.id))
                cursor.execute("UPDATE player SET stashpvpkits = stashpvpkits - {} WHERE id = {}".format(amout,ctx.author.id))
                await ctx.reply(f"{amout} {kit} китов было переведено на стеш ")
        elif kit == "regear":
            cursor.execute(f'SELECT regirpvpkits FROM player WHERE id={ctx.author.id}')
            money = cursor.fetchone()[0]
            cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
            money2 = cursor.fetchone()[0]
            cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
            money3 = cursor.fetchone()[0]
            if money < amout:
                await ctx.reply("У тебя нету столько китов")
            elif money2 + money3 + amout > 27:
                await ctx.reply("Нету места")
            else:
                cursor.execute("UPDATE player SET regir = regir + {} WHERE id = {}".format(amout,ctx.author.id))
                cursor.execute("UPDATE player SET regirpvpkits = regirpvpkits - {} WHERE id = {}".format(amout,ctx.author.id))
                await ctx.reply(f"{amout} {kit} китов было переведено на стеш ")
        else:
            await ctx.reply(f"Кита {kit} нету")
    else:
        await ctx.reply(f"С стешом можно только take - забрать киты с стеша , give - положить киты на стеш")
    connection.commit()

@commands.cooldown(1, 25, commands.BucketType.guild)
@bot.command()
async def pay(ctx, member: discord.Member = None , amout: int = None):
    if member == ctx.author:
        await ctx.reply(f"Вы не можете дать деньги самому себе")
    else:
        if amout is None or amout < 0:
            await ctx.reply(f"Вы не верно ввели сумму")
        else:
            cursor.execute("UPDATE player SET money = money + {} WHERE id = {}".format(amout,member.id))
            cursor.execute("UPDATE player SET money = money - {} WHERE id = {}".format(amout,ctx.author.id))
            cursor.execute(f'SELECT name FROM player WHERE id={ctx.author.id}')
            name = cursor.fetchone()[0]
            await ctx.reply(f"{name} вы успешно перевели {amout}$ {member}")
            connection.commit()


@commands.cooldown(1, 25, commands.BucketType.guild)
@bot.command()
async def give(ctx , kit ,  member: discord.Member = None ,  amout:int = -1):
    if member == ctx.author:
        await ctx.reply(f"Вы не можете дать киты самому себе")
    else:
        if amout is None or amout < 0 :
            await ctx.reply(f"Вы не верно ввели количество")
        else:
            if kit == "pvp":
                cursor.execute(f'SELECT pvp FROM player WHERE id={ctx.author.id}')
                money1 = cursor.fetchone()[0]
                cursor.execute(f'SELECT pvp FROM player WHERE id={member.id}')
                money2 = cursor.fetchone()[0]
                cursor.execute(f'SELECT regir FROM player WHERE id={member.id}')
                money3 = cursor.fetchone()[0]
                if money1 < amout:
                    await ctx.reply("У тебя нету столько китов")
                elif money2 + money3 + amout > 27:
                    await ctx.reply(f"У {member} нету столько места")
                else:
                    cursor.execute("UPDATE player SET pvp = pvp + {} WHERE id = {}".format(amout,member.id))
                    cursor.execute("UPDATE player SET pvp = pvp - {} WHERE id = {}".format(amout,ctx.author.id))
                    await ctx.reply(f"Вы перевели {amout} {kit} китов {member}")
            if kit == "regear":
                cursor.execute(f'SELECT regir FROM player WHERE id={ctx.author.id}')
                money1 = cursor.fetchone()[0]
                cursor.execute(f'SELECT pvp FROM player WHERE id={member.id}')
                money2 = cursor.fetchone()[0]
                cursor.execute(f'SELECT regir FROM player WHERE id={member.id}')
                money3 = cursor.fetchone()[0]
                if money1 < amout:
                    await ctx.reply("У тебя нету столько китов")
                elif money2 + money3 + amout > 27:
                    await ctx.reply(f"У {member} нету столько места")
                else:
                    cursor.execute("UPDATE player SET regir = regir + {} WHERE id = {}".format(amout,member.id))
                    cursor.execute("UPDATE player SET regir = regir - {} WHERE id = {}".format(amout,ctx.author.id))
                    await ctx.reply(f"Вы перевели {amout} {kit} китов {member}")
                connection.commit()


@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
async def sex(ctx ,  member: discord.Member = None ):
    if member == ctx.author:
        await ctx.reply("Вы успешно подрочили")
    else:
        chiso = random.randint(1, 6)
        if chiso == 1:
            await ctx.reply(f"Лицо {ctx.author} было залито спермой {member}")
        elif chiso == 2:
            await ctx.reply(f"{member} после такой ночки с {ctx.author} больше не может спокойно сидеть")
        elif chiso == 3:
            await ctx.reply(f"{ctx.author} порвал попку {member}")
        elif chiso == 4:
            await ctx.reply(f"Что было ночью у {ctx.author} и {member} я видел на одном сайте с припиской xxx ")
        elif chiso == 5:
            await ctx.reply(f"{ctx.author} просто выебал {member}")
        elif chiso == 6:
            await ctx.reply(f"{member} просто выебал {ctx.author}")

#------------------------------

@bot.event
async def on_command_error(ctx, err):
    print(f"{err} - {datetime.datetime.utcnow()}")
    if isinstance(err, commands.BotMissingPermissions):
        Err2 = await ctx.send(
            embed=discord.Embed(description=f"У бота отсутствуют права: {' '.join(err.missing_perms)}\nВыдайте их ему для полного функционирования бота"))
        await asyncio.sleep(6)
        await Err2.delete()

    elif isinstance(err, commands.MissingPermissions):
        Err3 = await ctx.send(embed=discord.Embed(description=f"У вас недостаточно прав для запуска этой команды!"))
        await asyncio.sleep(6)
        await Err3.delete()

    elif isinstance(err, commands.UserInputError):
        Err4 = await ctx.send(embed=discord.Embed(description=f"Правильное использование команды {ctx.prefix}{ctx.command.name} {ctx.command.signature}`"))
        await asyncio.sleep(6)
        await Err4.delete()

    elif isinstance(err, commands.CommandOnCooldown):
        Err5 = await ctx.send(embed=discord.Embed(description=f"У вас еще не прошел кулдаун на команду {ctx.command}!\nПодождите еще {err.retry_after:.2f}"))
        await asyncio.sleep(6)
        await Err5.delete()

@client.event
async def on_guild_join(guild):
    print(" ")
    print("==============================================")
    print("[GUILD]   Бот присоединился к серверу!          ")
    print("[GUILD]   Информация о сервере                  ")
    print("==============================================")
    print(f'[GUILD]  Сервер           - {guild.name}       ')
    print(f'[GUILD]  Владелец сервера - {guild.owner}      ')
    print(f'[GUILD]  ID бота          - {guild.id}         ')
    print(f'[GUILD]  Расположение сервер - {guild.region}  ')
    print("==============================================")
    print(" ")
    for member in guild.members:
        if cursor.execute(f"SELECT id FROM player WHERE id = {member.id}").fetchone() is None:
            cursor.execute(f"INSERT INTO player VALUES ({member.id}, '{str(member.name)}' , 0 , 0 , 0 , 5 , 2 , 0 , 0 )")
        if cursor.execute(f"SELECT id FROM stats WHERE id = {member.id}").fetchone() is None:
            cursor.execute(f"INSERT INTO stats VALUES ({member.id}, '{str(member.name)}' , 0 , 0 , 0 , 0)")

for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        bot.load_extension(f"cogs.{fn[:-3]}")
        print(f"{fn[:-3]} ready")
bot.run(TOKEN)
