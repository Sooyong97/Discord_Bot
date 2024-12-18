import discord
from discord.ext import commands
import asyncio

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # 멤버 목록을 확인하도록 함.
bot = commands.Bot(command_prefix="!", intents=intents)

# 봇이 준비될 때 이벤트
@bot.event
async def on_ready():
    print(f"봇 로그인: {bot.user}")

# 확장 모듈 로드 함수
async def load_extensions():
    # 비동기적으로 확장 모듈 로드
    await bot.load_extension('event')  # event.py 확장 모듈 로드

# 봇 실행
if __name__ == "__main__":
    # 비동기적으로 확장 모듈을 로드하고 봇 실행
    asyncio.run(load_extensions())  # 확장 모듈 로드
    bot.run("Token")  # 토큰을 사용해 봇 실행  # 토큰을 사용해 봇 실행
