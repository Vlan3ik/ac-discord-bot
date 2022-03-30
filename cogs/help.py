import discord
import datetime
from discord.ext import commands
import bot

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.guild)
	async def help(self, ctx , what: str = "none"):
		if what == "none":
			embed = discord.Embed(title="Help!", description="Кратко я игровой бот!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
			embed.add_field(name=f"Вы играете за своего майнкрафт персонажа . У вас есть 3 вида китов . Pvp kit , Regear  kit , Rand (Random) kit", value=f"Список всех команд: {bot.PREFIX}help commands", inline=True)
			await ctx.reply(embed=embed)
		elif what == "commands" or what == "c1":
			embed = discord.Embed(title="Help!", description="Список всех команд!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
			embed.add_field(name=f"{bot.PREFIX}i", value=f"Команда: {bot.PREFIX}i \n Эта команда покажет вам вашего персонажа !", inline=True)
			embed.add_field(name=f"{bot.PREFIX}open", value=f"Команда: {bot.PREFIX}open (если больше одного то количество) \n Открытие случайного кита!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}rename", value=f"Команда: {bot.PREFIX}rename (ник) \n Поменять ник своему персонажу (максимум 13 символов)!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}freekits", value=f"Команда: {bot.PREFIX}freekits \n Получить 2 случайных кита (раз в час)!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}cpvp", value=f"Команда: {bot.PREFIX}cpvp (игрок) \n Устроить cpvp  с кем либо . При победе +лвл +случаный кит!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}top", value=f"Команда: {bot.PREFIX}top \n Посмотрерть топы игрково по lvl и по победам!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}shop", value=f"Команда: {bot.PREFIX}shop \n Магазин для покупки и продажи китов!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}help commands2", value=f"Команда: {bot.PREFIX}help commands2 \n Дургие команды!", inline=True)
			await ctx.reply(embed=embed)
		elif what == "commands2" or what == "c2":
			embed = discord.Embed(title="**Help!**", description="Ещё команды для бота!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
			embed.add_field(name=f"{bot.PREFIX}stesh (take or give) (pvp or regear) (сколько)", value=f"Команда: {bot.PREFIX}stesh (take or give) (pvp or regear) (сколько) \n Положить или забрать киты со стеша . Знайте ваш стеш могу найти!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}shop", value=f"Команда: {bot.PREFIX}shop \n Магазин для покупки и продажи китов!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}steshhunt", value=f"Команда: {bot.PREFIX}steshhunt \n Раз в час вы можете искать стеш (шанс 1 к 1000)!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}pay", value=f"Команда: {bot.PREFIX}pay (участник) (сколько) \n Отправить сколько то денег другому игроку!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}give", value=f"Команда: {bot.PREFIX}give (кит) (участник) (сколько) \n Отправить китов другому игроку!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}help commands3", value=f"Команда: {bot.PREFIX}help commands2 \n Дургие команды!", inline=True)
			await ctx.reply(embed=embed)
		elif what == "commands3" or what == "c3":
			embed = discord.Embed(title="**Развлекательные**", description="Список всех Развлекательных команд!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
			embed.add_field(name=f"{bot.PREFIX}YT", value=f"Команда: {bot.PREFIX}YT ,\n Заходи в голосовой канал и смотри ютуб!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}Bt", value=f"Команда: {bot.PREFIX}YT ,\n Заходи в голосовой канал и играй!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}Ch", value=f"Команда: {bot.PREFIX}YT ,\n Ещё одна игра для голосовых каналов!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}serv", value=f"Команда: {bot.PREFIX}serv ,\n Информация о сервере!", inline=True)
			embed.add_field(name=f"{bot.PREFIX}botinfo", value=f"Команда: {bot.PREFIX}botinfo ,\n Информация о боте!", inline=True)
			await ctx.reply(embed=embed)

	@commands.command()
	@commands.cooldown(1, 25, commands.BucketType.guild)
	async def shop(self, ctx ):
		embed = discord.Embed(title="AC SHOP!", description="Самый честный магазин!", timestamp=datetime.datetime.utcnow(), colour=discord.Colour.blue())
		embed.add_field(name=f"PVP KIT - 5$ продажа", value=f"Команда: {bot.PREFIX}buy pvp ,\n С вашего счёт спишуться 5$ и вы получите свой кит!", inline=True)
		embed.add_field(name=f"Regear KIT - 1$ продажа", value=f"Команда: {bot.PREFIX}buy regear ,\n С вашего счёт спишуться 1$ и вы получите свой кит!", inline=True)
		embed.add_field(name=f"PVP KIT - 2.5$ покупка", value=f"Команда: {bot.PREFIX}sell pvp ,\n Вам зачислят ваши 2.5$ и заберут кит!", inline=True)
		embed.add_field(name=f"Regear KIT - 0.5$ покупка", value=f"Команда: {bot.PREFIX}sell regear ,\n ам зачислят ваши 0.5$ и заберут кит!", inline=True)
		await ctx.reply(embed=embed)




def setup(bot):
	bot.add_cog(Help(bot))