import discord
from discord.ui import Button, View
from discord.ext import commands
from View.MemberSelectView import MemberSelectView # 멤버 선택 뷰

class EventView(View):
    # Bot인자 추가 추후 확장성 생각
    def __init__(self, event_name: str, target_channel_id: int, bot: commands.Bot, guild):
        super().__init__(timeout=None)  # 버튼 시간 제한 없음
        self.event_name = event_name
        self.message_id = None  # 메시지 ID는 나중에 설정
        self.target_channel_id = target_channel_id
        self.bot = bot # bot 객체 선언
        self.attendance = {} # 참여정보저장
        self.guild = guild

    def get_attendance(self, message_id):
        if message_id not in self.attendance:
            self.attendance[message_id] = {"참여": []}
        return self.attendance[message_id]
    
    # 선택한 멤버를 참여자로 추가
    def add_participant(self, member):
        self.get_attendance(self.message_id)
        if member.display_name not in self.attendance[self.message_id]["참여"]:
            self.attendance[self.message_id]["참여"].append(member.display_name)

    # 참여버튼 메소드
    @discord.ui.button(label="참여", style=discord.ButtonStyle.green)
    async def join_event(self, interaction: discord.Interaction, button: Button):
        """참여 버튼 클릭"""
        user = interaction.user
        self.get_attendance(self.message_id)

        # 메세지 업데이트 함수 분리
        # 사용자가 이미 참여한 경우
        if user.name in self.attendance[self.message_id]["참여"]:
            await interaction.response.send_message("이미 참여하셨습니다.", ephemeral=True)
            return
        
        # 참여자가 아니면 참여 추가
        self.attendance[self.message_id]["참여"].append(user.name)
        await self.update_message(interaction)
        await interaction.response.send_message("참여 완료!", ephemeral=True)

        # 취소 버튼 활성화, 참여 버튼 비활성화
        await self.update_buttons(interaction)

    # 취소버튼 메소드
    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def leave_event(self, interaction: discord.Interaction, button: Button):
        """취소 버튼 클릭"""
        user = interaction.user

        # 사용자가 참여하지 않은 경우
        if user.name not in self.attendance[self.message_id]["참여"]:
            await interaction.response.send_message("참여하지 않으셨습니다.", ephemeral=True)
            return
        
        # 참여 취소
        self.attendance[self.message_id]["참여"].remove(user.name)
        await self.update_message(interaction)
        await interaction.response.send_message("참여 취소 완료!", ephemeral=True)

        # 참여 버튼 활성화, 취소 버튼 비활성화
        await self.update_buttons(interaction)


    # 메세지 업데이트
    async def update_message(self, interaction):
        """Embed 메시지 업데이트"""
        participate_list = ", ".join(self.attendance[self.message_id]["참여"]) or "없음"
        embed = discord.Embed(
            title=f"📅 **{self.event_name}** 참여",
            description=f"**참여자**: {participate_list}",
            color=discord.Color.green()
        )
        await interaction.message.edit(content=" ", embed=embed)

    # 버튼 업데이트
    async def update_buttons(self, interaction):
        """버튼 상태를 업데이트하여 참여 상태에 따라 버튼을 변경"""
        user = interaction.user
        button_labels = []

        # Button만을 대상으로 처리하도록 수정
        for button in self.children:
            if isinstance(button, discord.ui.Button):  # Button 객체만 처리
                button_labels.append(button.label)

        if user.name in self.attendance[self.message_id]["참여"]:
            # 사용자가 참여한 경우, 참여 버튼 비활성화, 취소 버튼 활성화
            if "참여" in button_labels:
                self.children[0].disabled = True  # '참여' 버튼 비활성화
            if "취소" not in button_labels:
                self.children[1].disabled = False  # '취소' 버튼 활성화
        else:
            # 사용자가 참여하지 않은 경우, 참여 버튼 활성화, 취소 버튼 비활성화
            if "참여" not in button_labels:
                self.children[0].disabled = False  # '참여' 버튼 활성화
            if "취소" in button_labels:
                self.children[1].disabled = True  # '취소' 버튼 비활성화
        
        # 버튼 상태 업데이트
        await interaction.message.edit(view=self)
