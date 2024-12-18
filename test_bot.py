import discord
from discord.ext import commands
from discord.ui import Button, View, Select

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # 멤버 목록을 확인하도록함.
bot = commands.Bot(command_prefix="!", intents=intents)

attendance = {}  # 참여 정보 저장
events = {}  # 진행 중인 이벤트 저장

# 멤버 확인 및 선택 트리거
class MemberSelectView(View):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        
        options = [
            discord.SelectOption(label = member.display, value = str(member.id))
            for member in guild.members if not member.bot
            ]

        self.member_select = Select(
            placeholder="참여자를 선택하세요",
            options=options[:25],
            )
        self.member_select.callback = self.member_select_callback
        self.add_item(self.member_select)
        
        async def select_member_callback(self, interaction: discord.Interaction()):
            selected_member_id = self.member_select.values[0]
            selected_member = self.guild.get_member(int(selected_member_id))
            
            await interaction.response.send_message(
                f"선택된 참여자: {selected_member.display_name}", 
                phemeral=True
            )

# 버튼 뷰 정의
class EventView(View):
    def __init__(self, event_name: str, target_channel_id: int):
        super().__init__(timeout=None)  # 버튼 시간 제한 없음
        self.event_name = event_name
        self.message_id = None  # 메시지 ID는 나중에 설정
        self.target_channel_id = target_channel_id

    @discord.ui.button(label="참여", style=discord.ButtonStyle.green)
    async def join_event(self, interaction: discord.Interaction, button: Button):
        """참여 버튼 클릭"""
        user = interaction.user
        if self.message_id is None:
            await interaction.response.send_message("메시지 ID가 초기화되지 않았습니다.", ephemeral=True)
            return

        if user.name not in attendance[self.message_id]["참여"]:
            attendance[self.message_id]["참여"].append(user.name)

            # 참여자 리스트 업데이트
            participate_list = ", ".join(attendance[self.message_id]["참여"]) or "없음"
            
            # Embed 메시지 생성
            embed = discord.Embed(
                title=f"📅 **{self.event_name}** 레이드 참여",
                description=f"**참여자**: {participate_list}",
                color=discord.Color.green()
            )

            # 메시지 업데이트
            await interaction.message.edit(content=" ", embed=embed)

            # 버튼 비활성화
            button.disabled = True
            await interaction.message.edit(view=self)

            # 다른 채널 메시지 업데이트 (고정되지 않음)
            target_channel = bot.get_channel(self.target_channel_id)
            if target_channel:
                async for msg in target_channel.history():
                    if msg.id == self.message_id:
                        await msg.edit(embed=embed)
                        break

            await interaction.response.send_message("참여 완료!", ephemeral=True)
        else:
            await interaction.response.send_message("이미 참여하셨습니다.", ephemeral=True)

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def leave_event(self, interaction: discord.Interaction, button: Button):
        """취소 버튼 클릭"""
        user = interaction.user
        if self.message_id is None:
            await interaction.response.send_message("메시지 ID가 초기화되지 않았습니다.", ephemeral=True)
            return

        if user.name in attendance[self.message_id]["참여"]:
            attendance[self.message_id]["참여"].remove(user.name)

            # 참여자 리스트 업데이트
            participate_list = ", ".join(attendance[self.message_id]["참여"]) or "없음"
            
            # Embed 메시지 생성
            embed = discord.Embed(
                title=f"📅 **{self.event_name}** 참여",
                description=f"**참여자**: {participate_list}",
                color=discord.Color.red()
            )

            # 메시지 업데이트
            await interaction.message.edit(content=" ", embed=embed)

            # 버튼 활성화
            join_button = self.children[0]
            join_button.disabled = False
            await interaction.message.edit(view=self)

            # 다른 채널 메시지 업데이트 (고정되지 않음)
            target_channel = bot.get_channel(self.target_channel_id)
            if target_channel:
                async for msg in target_channel.history():
                    if msg.id == self.message_id:
                        await msg.edit(embed=embed)
                        break

            await interaction.response.send_message("참여 취소 완료!", ephemeral=True)
        else:
            await interaction.response.send_message("참여하지 않으셨습니다.", ephemeral=True)


@bot.command(aliases=["이벤트", "파티", "팟"])
async def event(ctx, event_name: str):
    """이벤트 생성 및 버튼 추가"""
    # Embed 메시지 생성
    embed = discord.Embed(
        title=f"📅 **{event_name}** 이벤트에 참여하시겠습니까?",
        description="**참여자**: 없음",
        color=discord.Color.blue()
    )
    
    members = [member.name for member in ctx.guild.members if not member.bot]
    print(members)
    select = Select(placeholder="참여할 멤버를 선택하세요!", options=[discord.SelectOption(label=member) for member in members])

    # EventView 인스턴스 생성
    event_view = EventView(event_name, target_channel_id=1315838146071498923)  # 다른 채널 ID
    event_view.add_item(select)

    # 초기 메시지 전송
    message = await ctx.send(
        embed=embed,
        view=event_view,
    )

    # 참여 정보 저장
    attendance[message.id] = {"참여": []}
    events[event_name] = message.id

    # 메시지 ID 초기화 후 EventView에 전달
    event_view.message_id = message.id  # 메시지 ID 초기화
    await message.edit(view=event_view)

@bot.event
async def on_ready():
    print(f"봇 로그인: {bot.user}")

# 봇 실행
bot.run("봇토큰")
