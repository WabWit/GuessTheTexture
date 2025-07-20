import discord
from discord import app_commands
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "real")
    async def RealCMD(self, interaction: discord.Interaction):
        await interaction.response.send_message("IT WORKS YOU IDIOT!!")

async def setup(bot: commands.Bot) -> None:
    # finally, adding the cog to the bot
    await bot.add_cog(AdminCog(bot=bot))