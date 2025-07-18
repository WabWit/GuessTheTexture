#Main code that does most logic and discord handling
import os
import json
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from pathlib import Path
from modules import GTTUtils
from modules import Hint
from modules.Common_FNCS import *

# Load your token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

BASE_DIR = Path(__file__).parent
GTTSERVERS_PATH = BASE_DIR / "Data" / "GTTServers.json"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" / "IMAGESET_VANILLA"

# Setup Discord bot with all intents
intents = discord.Intents.all()
intents.message_content = True

# Create the bot with a prefix (for compatibility with text commands)
bot = commands.Bot(command_prefix=",", intents=intents)

# Slash command registration (sync)
@bot.event
async def on_ready():
    await bot.wait_until_ready()  # Just to be safe
    await bot.tree.sync()         # Registers the slash commands with Discord
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Slash commands synced!")

@bot.tree.command(name="quit", description="back to the gulag")
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

@bot.tree.command(name="start", description="Starts a GTT Game - Admin Only")
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

# ALL COMMANDS FOR NORMAL PLAYERS
#sending a picture
@bot.tree.command(name="image", description="Bumps the current image")
async def image(interaction: discord.Interaction):
    if await check_game(interaction):
        await interaction.response.send_message("No Active GTT Game, go tell <@292608557335969793> to start one")
        return
    guild_id = interaction.guild_id
    CurrentServer = GTTServers.get(str(guild_id))
    await interaction.response.defer()
    await send_image(interaction, "Here is the image:")

@image.error
async def image_error(interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send("TOO FAST!")

#answer command
@bot.tree.command(name="answer", description="are you sure?")
async def answer(interaction: discord.Interaction, answer: str):
    # tells discord that i gotchu and wait fo me
    await interaction.response.defer()
    guild_id = interaction.guild_id 
    user_id = interaction.user.id
    user_answer = GTTUtils.AnswerContainer(answer)
    Current_Server = GTTServers.get(str(guild_id))
    # return if no active game
    if await check_game(interaction):
        await interaction.followup.send("No Active GTT game")
        return
    Current_Server.total_guesses += 1
    # Number of guess detection
    GuessIndicator = ""
    amount_of_guessses = Current_Server.per_user_guesses.get(str(user_id), 0)
    if amount_of_guessses == 3:
        await interaction.followup.send("You're out of guesses buckaroo.")
        return
    
    if amount_of_guessses == 2:
        GuessIndicator = "You're out of guesses. "
    if amount_of_guessses == 1:
        GuessIndicator = "You have one guess left. "
    Current_Server.per_user_guesses[str(user_id)] = amount_of_guessses + 1

    # Check if the answer is right
    if sorted(user_answer.answer_split) == sorted(Current_Server.answer_split):
        Current_Server.AddPoints(user_id, 1)
        await interaction.followup.send(f"Correct! The answer was: {Current_Server.answer_capped}")
        Current_Server.Reset()
        await send_image(interaction, "For the next image:")
        return
    right_words = list(set(Current_Server.answer_split) & set(user_answer.answer_split))
    Current_Server.words_guessed = list(set(right_words) | set(Current_Server.words_guessed))
    
    print(Current_Server.answer_split, user_answer.answer_split, Current_Server.words_guessed)
    if right_words == []: #just sees if u r so incredibly wrong and does an early return
        await interaction.followup.send(f"Incorrect. {GuessIndicator}")
        return
    await interaction.followup.send(f"Almost right. {GuessIndicator}Correct words: {' '.join(right_words)}")

    if Current_Server.total_guesses < 2: # for hints
        return
    
    hint_string = Hint.HintChecker(Current_Server.answer, Current_Server.words_guessed)  
    await interaction.followup.send(discord.utils.escape_markdown(f"Looks like yall are having trouble, heres a hint: {hint_string}"))

#check score
@bot.tree.command(name="score", description="Checks a player's score")
async def score(interaction: discord.Interaction):
    await interaction.response.defer()
    guild_id = interaction.guild_id 
    user_id = interaction.user.id
    Current_Server = GTTServers.get(str(guild_id))
    # return if no active game
    if Current_Server == None:
        await interaction.followup.send("No Active GTT Game")
        return
    
    player_score = Current_Server.local_scores.get(str(user_id), 0)
    await interaction.followup.send(f"Your score is {player_score}")

bot.run(TOKEN)