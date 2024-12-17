from discord.ext import commands
import commands  # commands.py에서 명령어 불러오기

# 봇 초기화
# 명령 시작은 "!"
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

# 명령어 실행
commands.setup(bot)

# 봇 실행
bot.run("YOUR_BOT_TOKEN")