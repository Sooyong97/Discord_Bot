import discord
from discord.ext import commands
from View.EventView import EventView  # EventView 클래스 가져오기
from View.MemberSelectView import MemberSelectView  # MemberSelectView 클래스 가져오기

# attendance = {}  # 참여 정보 저장
events = {}  # 진행 중인 이벤트 저장

# `bot` 객체를 외부에서 가져오기 위해 이 파일에서 import 하여 사용
async def setup(bot: commands.Bot):
    # 이벤트 명령어 정의
    @bot.command(aliases=["이벤트", "파티", "팟"])
    async def event(ctx, event_name: str = None):
        """이벤트 생성 및 버튼 추가"""

        # 인자가 누락된 경우
        if event_name is None:
            # ctx.invoked_with 사용하여 실제 호출된 명령어 확인
            await ctx.send(f"{ctx.invoked_with} 이름을 입력해 주세요. 예: `!{ctx.invoked_with} 아브렐슈드`")
            return
        
        # Embed 메시지 생성
        embed = discord.Embed(
            title=f"📅 **{event_name}** 이벤트에 참여하시겠습니까?",
            description="**참여자**: 없음",
            color=discord.Color.blue()
        )

        # Discord 멤버호출
        members = [member.name for member in ctx.guild.members if not member.bot]
        select = discord.ui.Select(placeholder="참여할 멤버를 선택하세요!", options=[
            discord.SelectOption(label=member, value=member) for member in members
        ])

        # EventView 인스턴스 생성
        event_view = EventView(event_name, target_channel_id=1315838146071498923, bot=bot)  # 다른 채널 ID
        event_view.add_item(select)

        # # MemberSelectView 인스턴스 생성
        # member_select_view = MemberSelectView(ctx.guild)

        # 초기 메시지 전송
        message = await ctx.send(
            embed=embed,
            view=event_view,
        )

        # 디버깅 로그 확인중 (12월)
        print(f"DEBUG: Initializing attendance for message.id = {message.id}")

        # # 참여 정보 저장
        # attendance[message.id] = {"참여": []}
        # events[event_name] = message.id

        # 메시지 ID 초기화 후 EventView에 전달
        event_view.message_id = message.id  # 메시지 ID 초기화
        await message.edit(view=event_view)