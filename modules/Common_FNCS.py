# ASYNC FUNCTIONS
import discord
import json
from pathlib import Path
from modules.GTTUtils import *
from modules.data_manager import *

BASE_DIR = Path(__file__).parent.parent
GTTSERVERS_PATH = BASE_DIR / "Data" / "GTTServers.json"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" / "IMAGESET_VANILLA"
Admins = [292608557335969793]

# Check if a save file exists and use it

# just sends the image
async def send_image(interaction: discord.Interaction, message) -> None:
    guild_id = str(interaction.guild_id)
    CurrentServer = GTTServers.Get_Server(guild_id)
    print(CurrentServer)
    print(CurrentServer.original)
    GTT_Image = discord.File(filename="Dont_Cheese_XD.png", spoiler= False, fp=f"{IMAGESET_VANILLA_PATH}/{CurrentServer.original}")
    await interaction.followup.send(message,file=GTT_Image)

# Checks if theres an active gtt game, if not then returns true
async def is_game_active(interaction: discord.Interaction) -> None:
    guild_id = str(interaction.guild_id)

    if GTTServers.Get_Server(guild_id) == None: # Makes the GTT game for that server if it dosnest exist
        GTTServers.Add_Server(guild_id)
        print("here a")
        return False

    CurrentServer = GTTServers.Get_Server(guild_id) # Access the GTT game for that server
    if not CurrentServer.original: # To see if there is a game that has started
        return False
    
    return True

# check permisions, return false if nuh uh
async def Check_Perms(interaction, type = "Admin") -> bool:
    if type == "Admin":
        if interaction.user.id not in Admins:
            return False
        return True
# Start the bot