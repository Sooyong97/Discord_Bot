import discord
from discord.ext import commands
from View.EventView import EventView  # EventView 클래스 가져오기
from View.MemberSelectView import MemberSelectView  # MemberSelectView 클래스 가져오기

events = {}  # 진행 중인 이벤트 저장

# `bot` 객체를 외부에서 가져옴
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

        # EventView 인스턴스 생성
        event_view = EventView(event_name, target_channel_id=1315838146071498923, bot=bot, guild=ctx.guild)  # guild 추가

        # MemberSelectView 인스턴스 생성
        member_select_view = MemberSelectView(ctx.guild, event_view)  # event_view를 전달

        # 초기 메시지 전송
        message = await ctx.send(embed=embed, view=event_view)

        # 이벤트 정보 저장
        events[event_name] = message.id

        # EventView 메시지 ID 초기화
        event_view.message_id = message.id

        # EventView에 버튼을 추가 (기존 방식대로 버튼 추가)
        event_view.add_item(member_select_view.member_select)  # Select(드롭다운)만 추가

        # MemberSelectView를 독립적으로 전송 (상호작용을 위한 뷰)
        await ctx.send("참여자를 선택하세요.", view=member_select_view)