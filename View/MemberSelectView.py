import discord
from discord.ui import Select, View

class MemberSelectView(View):
    # Event View 객체 추가
    def __init__(self, guild, event_view):
        super().__init__()
        self.guild = guild
        self.event_view = event_view
        
        options = [
            discord.SelectOption(label=member.display_name, value=str(member.id))
            for member in guild.members if not member.bot
        ]

        self.member_select = Select(
            placeholder="참여자를 선택하세요",
            options=options[:25],  # 최대 25명까지 보임
            min_values=1, # 최소 1명 이상 선택
            max_values=16 # 최대 16명 선택 가능
        )
        self.member_select.callback = self.select_member_callback
        self.add_item(self.member_select)

    async def select_member_callback(self, interaction: discord.Interaction):
        # 선택된 멤버 리스트
        selected_member_ids = self.member_select.values
        selected_members = [self.guild.get_member(int(member_id)) for member_id in selected_member_ids]
        
        # 선택된 멤버들을 EventView를 통해 참여자로 추가
        for member in selected_members:
            self.event_view.add_participant(member)

        # 선택 결과 리턴
        await interaction.response.send_message(
            f"선택된 참여자들: {', '.join([member.display_name for member in selected_members])}",
            ephemeral=True
        )