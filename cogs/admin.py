import discord
from discord import app_commands
from discord.ext import commands
from modules.Common_FNCS import *
from modules.data_manager import *

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quit", description="back to the gulag")
    async def exit(self, interaction : discord.Interaction):
        
        if not await Check_Perms(interaction, "Admin"):
            await interaction.response.send_message("Admin only command!", ephemeral=True)
            return
        print(f"Bot shutting down blame {interaction.user.display_name} from {interaction.guild.name}")
        await interaction.response.defer()
        save_server_data()
        await interaction.followup.send("Shutting Down")
        await quit()

    @app_commands.command(name="start", description="Starts a GTT Game - Admin Only")
    async def start(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        if not await Check_Perms(interaction, "Admin"):
            await interaction.response.send_message("You need to be an admin to start a game", ephemeral=True)
            return
        await interaction.response.defer()
        Current_Server = None
        if not await is_game_active(interaction):
            Current_Server: GTTMaker = GTTServers.Get_Server(guild_id)
            Current_Server.Reset()
            print(Current_Server)
        else:
            await interaction.followup.send("A game has already started")
            return
        await send_image(interaction, "Guess this image:")



async def setup(bot: commands.Bot) -> None:
    # finally, adding the cog to the bot
    await bot.add_cog(AdminCog(bot=bot))


'''
    @app_commands.command(name="pingcd")
    @app_commands.checks.cooldown(1,5)
    async def pingcd(self, interaction: discord.Interaction):
        await interaction.response.send_message("PONGOLISIHOU")

    @pingcd.error
    async def on_test_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance( error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)
'''