import discord
from discord import app_commands
from discord.ext import commands
from modules.Common_FNCS import *

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quit", description="back to the gulag")
    async def exit(interaction : discord.Interaction):
        
        if not await Check_Perms(interaction, "Admin"):
            await interaction.response.send_message("Admin only command!", ephemeral=True)
            return
        print(f"Bot shutting down blame {interaction.user.display_name} from {interaction.guild.name}")
        await interaction.response.defer()
        dump = {}
        for guild_id in GTTServers.keys():
            dump[str(guild_id)] = GTTServers[str(guild_id)].local_scores
        with open(GTTSERVERS_PATH, "w") as ServersFile:
            json.dump(dump, ServersFile)
        await interaction.followup.send("Shutting Down")
        await quit()

    @app_commands.command(name="start", description="Starts a GTT Game - Admin Only")
    async def start(interaction: discord.Interaction):
        guild_id = interaction.guild_id
        if not await Check_Perms(interaction, "Admin"):
            await interaction.response.send_message("You need to be an admin to start a game", ephemeral=True)
            return
        await interaction.response.defer()
        Current_Server = None
        if await check_game(interaction):
            Current_Server = GTTServers.get(str(guild_id))
            Current_Server.Reset()
        else:
            await interaction.followup.send("A game has already started")
            return
        await send_image(interaction, "Guess this image:")

async def setup(bot: commands.Bot) -> None:
    # finally, adding the cog to the bot
    await bot.add_cog(AdminCog(bot=bot))