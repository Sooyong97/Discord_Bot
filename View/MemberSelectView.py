import discord
from discord.ui import Select, View

class MemberSelectView(View):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        
        options = [
            discord.SelectOption(label=member.display_name, value=str(member.id))
            for member in guild.members if not member.bot
        ]

        self.member_select = Select(
            placeholder="참여자를 선택하세요",
            options=options[:25],  # 최대 25명까지만 선택할 수 있게
        )
        self.member_select.callback = self.select_member_callback
        self.add_item(self.member_select)

    async def select_member_callback(self, interaction: discord.Interaction):
        selected_member_id = self.member_select.values[0]
        selected_member = self.guild.get_member(int(selected_member_id))
        
        await interaction.response.send_message(
            f"선택된 참여자: {selected_member.display_name}",
            ephemeral=True
        )