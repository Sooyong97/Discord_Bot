from discord.ext import commands

def setup(bot):
    @bot.command(name="안녕")
    async def hello(ctx):
        await ctx.send("안녕하세요!")