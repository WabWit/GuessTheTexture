# ASYNC FUNCTIONS
import discord
import json
from pathlib import Path
from modules.GTTUtils import *

BASE_DIR = Path(__file__).parent.parent
GTTSERVERS_PATH = BASE_DIR / "Data" / "GTTServers.json"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" / "IMAGESET_VANILLA"
GTTServers = {} #creates a container for servers
Admins = [292608557335969793]

# Check if a save file exists and use it
SERVER_SAVED_SCORES = {}
with open(GTTSERVERS_PATH, "r", encoding="utf-8") as file:
    SERVER_SAVED_SCORES = json.load(file)
for guild_id in SERVER_SAVED_SCORES.keys():
    GTTServers[guild_id] = GTTMaker(SERVER_SAVED_SCORES[guild_id])

# just sends the image
async def send_image(interaction: discord.Interaction, message) -> None:
    guild_id = interaction.guild_id
    CurrentServer = GTTServers.get(str(guild_id))
    print(CurrentServer)
    GTT_Image = discord.File(filename="Dont_Cheese_XD.png", spoiler= False, fp=f"{IMAGESET_VANILLA_PATH}/{CurrentServer.original}")
    await interaction.followup.send(message,file=GTT_Image)

# Checks if theres an active gtt game, if not then returns true
async def is_game_active(interaction: discord.Interaction) -> None:
    guild_id = interaction.guild_id

    if GTTServers.get(str(guild_id)) == None: # Makes the GTT game for that server if it dosnest exist
        GTTServers[str(guild_id)] = GTTMaker()
        return False

    CurrentServer = GTTServers.get(str(guild_id)) # Access the GTT game for that server
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