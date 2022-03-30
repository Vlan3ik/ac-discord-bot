import discord
import random
import json
import os
import io
import requests
from PIL  import Image , ImageFont ,ImageDraw
from random import randint
from discord.ext import commands, tasks
from discord_components import DiscordComponents,Button,ButtonStyle
from discord.ext import commands
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import re
import asyncio
import sqlite3
import time
import sys

class happy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.cooldown(1, 5, commands.BucketType.guild)
	@commands.command()
	async def serv(self,ctx):
		embed = discord.Embed(title=f"**Инфа срвера {ctx.guild.name} **",icon_url=self.bot.user.avatar_url, colour=discord.Colour.blue())
		embed.add_field(name=f"Имя сервера", value=f"{ctx.guild.name} ", inline=False)
		embed.add_field(name=f"Владелец сервера", value=f"{ctx.guild.owner} ", inline=False)
		embed.add_field(name=f"ID бота", value=f"{ctx.guild.id} ", inline=False)
		embed.add_field(name=f"Регион сервера", value=f"{ctx.guild.region}", inline=False)
		member = 0
		for i in ctx.guild.members:
			member = member +1
		role_count = len(ctx.guild.roles)
		embed.add_field(name=f"Участников на сервере", value=f"{member}", inline=False)
		embed.add_field(name='Левл верификации', value=str(ctx.guild.verification_level), inline=False)
		embed.add_field(name='Ролей на сервере', value=str(role_count), inline=False)
		embed.add_field(name='Создан в', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
		await ctx.reply(embed=embed)


	@commands.cooldown(1, 5, commands.BucketType.guild)
	@commands.command(aliases = ['Chess',"Ch","шахматы"])
	async def __Chess(self,ctx):
		data = {"max_age": 86400,"max_uses": 0,"target_application_id": 832012774040141894,"target_type": 2,"temporary": False,"validate": None}
		headers = {"Authorization": "Bot OTE1NjM4NjAyOTUwNjQ3ODg5.Yaeg5g.dtO0XkgRn-pavczXlhV0jECFxJg","Content-Type": "application/json"}
		if ctx.author.voice is not None:
			if ctx.author.voice.channel is not None:
				channel = ctx.author.voice.channel.id
			else:
				await ctx.send("Зайдите в канал")
		else:
			await ctx.send("Зайдите в канал")
		response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
		link = json.loads(response.content)
		await ctx.send(f"https://discord.com/invite/{link['code']}")

	@commands.cooldown(1, 5, commands.BucketType.guild)
	@commands.command(aliases = ['YT',"yt","YouTube"])
	async def __YT(self,ctx):
		data = {"max_age": 86400,"max_uses": 0,"target_application_id": 755600276941176913,"target_type": 2,"temporary": False,"validate": None}
		headers = {"Authorization": "Bot OTE1NjM4NjAyOTUwNjQ3ODg5.Yaeg5g.dtO0XkgRn-pavczXlhV0jECFxJg","Content-Type": "application/json"}
		if ctx.author.voice is not None:
			if ctx.author.voice.channel is not None:
				channel = ctx.author.voice.channel.id
			else:
				await ctx.send("Зайдите в канал")
		else:
			await ctx.send("Зайдите в канал")
		response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
		link = json.loads(response.content)
		await ctx.send(f"https://discord.com/invite/{link['code']}")

	@commands.cooldown(1, 5, commands.BucketType.guild)
	@commands.command(aliases = ['Betrayal',"Bt","rayal"])
	async def __Betrayal(self,ctx):
		data = {"max_age": 86400,"max_uses": 0,"target_application_id": 773336526917861400,"target_type": 2,"temporary": False,"validate": None}
		headers = {"Authorization": "Bot OTE1NjM4NjAyOTUwNjQ3ODg5.Yaeg5g.dtO0XkgRn-pavczXlhV0jECFxJg","Content-Type": "application/json"}
		if ctx.author.voice is not None:
			if ctx.author.voice.channel is not None:
				channel = ctx.author.voice.channel.id
			else:
				await ctx.send("Зайдите в канал")
		else:
			await ctx.send("Зайдите в канал")
		response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
		link = json.loads(response.content)
		await ctx.send(f"https://discord.com/invite/{link['code']}")




def setup(bot):
	bot.add_cog(happy(bot))