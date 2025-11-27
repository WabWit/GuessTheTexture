import discord
from discord import app_commands
from discord.ext import commands
from modules.Common_FNCS import *
from modules.data_manager import *

class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="image", description="Bumps the current image")
    async def image(self, interaction: discord.Interaction):
        if not await is_game_active(interaction):
            await interaction.response.send_message("No Active GTT Game, go tell <@292608557335969793> to start one")
            return
        await interaction.response.defer()
        await send_image(interaction, "Here is the image:")

    '''
    @image.error
    async def image_error(interaction, error):
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.response.send("TOO FAST!")
    '''
    @app_commands.command(name="score", description="Checks a player's score")
    async def score(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild_id = str(interaction.guild_id) 
        user_id = str(interaction.user.id)
        # return if no active game
        if GTTServers.Get_Server(guild_id) == None:
            await interaction.followup.send("No Previous GTT Game")
            return
        Current_Server: GTTMaker = GTTServers.Get_Server(guild_id)    
        player_score = Current_Server.local_scores.get(user_id, 0)
        await interaction.followup.send(f"Your score is {player_score}")
    
async def setup(bot: commands.Bot) -> None:
    # finally, adding the cog to the bot
    await bot.add_cog(PlayerCog(bot=bot))        