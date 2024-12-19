import discord
from discord.ui import Button, View
from discord.ext import commands

class EventView(View):
    # Bot인자 추가 추후 확장성 생각
    def __init__(self, event_name: str, target_channel_id: int, bot: commands.Bot):
        super().__init__(timeout=None)  # 버튼 시간 제한 없음
        self.event_name = event_name
        self.message_id = None  # 메시지 ID는 나중에 설정
        self.target_channel_id = target_channel_id
        self.bot = bot # bot 객체 선언
        self.attendance = {} # 참여정보저장

    def get_attendance(self, message_id):
        if message_id not in self.attendance:
            self.attendance[message_id] = {"참여": []}
        return self.attendance[message_id]

    # 참여버튼 메소드
    @discord.ui.button(label="참여", style=discord.ButtonStyle.green)
    async def join_event(self, interaction: discord.Interaction, button: Button):
        """참여 버튼 클릭"""
        user = interaction.user
        
        # 디버깅 테스트중(12월 19일)
        print(f"DEBUG: self.message_id = {self.message_id}")
        self.get_attendance(self.message_id)
        print(f"DEBUG: attendance keys = {list(self.attendance.keys())}")

        # 메시지 ID 등록여부확인
        if self.message_id is None or self.message_id not in self.attendance:
            await interaction.response.send_message("메시지 ID가 초기화되지 않았습니다.", ephemeral=True)
            return

        # 참여리스트에 없는경우 참여리스트에 멤버 추가
        if user.name not in self.attendance[self.message_id]["참여"]:
            self.attendance[self.message_id]["참여"].append(user.name)

            # 참여자 리스트 업데이트
            participate_list = ", ".join(self.attendance[self.message_id]["참여"]) or "없음"
            
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
            target_channel = self.bot.get_channel(self.target_channel_id)
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

        if user.name in self.attendance[self.message_id]["참여"]:
            self.attendance[self.message_id]["참여"].remove(user.name)

            # 참여자 리스트 업데이트
            participate_list = ", ".join(self.attendance[self.message_id]["참여"]) or "없음"
            
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
            target_channel = self.bot.get_channel(self.target_channel_id)
            if target_channel:
                async for msg in target_channel.history():
                    if msg.id == self.message_id:
                        await msg.edit(embed=embed)
                        break

            await interaction.response.send_message("참여 취소 완료!", ephemeral=True)
        else:
            await interaction.response.send_message("참여하지 않으셨습니다.", ephemeral=True)