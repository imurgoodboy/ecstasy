import discord
from discord.ext import commands
from discord import app_commands

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("SlashCommands cog initialized.")  

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction):
        print("Hello command registered.")  
        await interaction.response.send_message("Hello!")  

    async def cog_load(self):
        print("SlashCommands cog loaded.")
        pass  #

async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCommands(bot))
