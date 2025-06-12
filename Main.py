from dotenv import load_dotenv
import os, json, math, asyncio, time, random, Hint, Cleaner, discord, GTTUtils
from discord.ext import commands

# Load your token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

GTTServers = {} #creates a container for servers
Admins = [292608557335969793]

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
    perms = await Check_Perms(interaction, "Admin")
    if perms:
        return
    print(f"Bot shutting down blame {interaction.user.display_name} from {interaction.guild.name}")
    await interaction.response.send_message("Shutting Down")
    await quit()

# ALL COMMANDS FOR NORMAL PLAYERS

@bot.tree.command(name="start", description="Bumps the current image")
async def start(interaction: discord.Interaction):
    perms = await Check_Perms(interaction, "Admin")
    if perms:
        return
    await interaction.response.defer(ephemeral=False)
    await roll_send_image(interaction, "Guess this image:")

#sending a picture
@bot.tree.command(name="image", description="Bumps the current image")
async def image(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    await send_image(interaction, "Here is the image:")

#answer command
@bot.tree.command(name="answer", description="amogus")
async def answer(interaction: discord.Interaction, answer: str):
    # tells discord that i gotchu and wait fo me
    await interaction.response.defer(ephemeral=False)
    guild_id = interaction.guild_id 
    user_id = interaction.user.id
    user_answer = GTTUtils.AnswerContainer(answer)
    Current_Server = GTTServers.get(str(guild_id))
    # return if no active game
    if Current_Server == None:
        await interaction.followup.send("No Active GTT game")
        return
    Current_Server.total_guesses += 1
    print(Current_Server.local_scores)
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
        Current_Server.Add_Score(user_id, 1)
        await roll_send_image(interaction, f"Correct! The answer was: {Current_Server.answer_capped}, How about this one?")
        print(Current_Server.local_scores)
        return
    right_words = list(set(Current_Server.answer_split) & set(user_answer.answer_split))
    Current_Server.words_guessed = list(set(right_words) | set(Current_Server.words_guessed))
    
    print(Current_Server.answer_split, user_answer.answer_split, Current_Server.words_guessed)
    if right_words == []: #just sees if u r so incredibly wrong and does an early return
        await interaction.followup.send(f"Incorrect. {GuessIndicator}")
        return
    await interaction.followup.send(f"Incorrect. {GuessIndicator}Correct words: {' '.join(right_words)}")

    if Current_Server.total_guesses >= 2: # for hints
        hint_string = ""
        possible_hints = Hint.HintChecker(Current_Server.answer)
        if possible_hints:
            hint_string = random.choice(possible_hints)
        await interaction.followup.send(f"Looks like yall are having trouble, heres a hint: {hint_string}")

#check score, broke btw so go fix mofo
@bot.tree.command(name="score", description="amogus")
async def score(interaction: discord.Interaction, player: str):
    await interaction.response.defer(ephemeral=False)
    guild_id = interaction.guild_id 
    user_id = interaction.user.id
    Current_Server = GTTServers.get(str(guild_id))
    # return if no active game
    if Current_Server == None:
        await interaction.followup.send("No Active GTT Game")
        return
    player_score = Current_Server.local_scores.get(str(user_id), 0)
    await interaction.followup.send(f"Your score is {player_score}")

# Async Functions

# rerolls and sends image
async def roll_send_image(interaction: discord.Interaction, message):
    guild_id = interaction.guild_id
    user_id = interaction.user.id

    if GTTServers.get(guild_id) == None: # Makes the GTT game for that server if it dosnest exist
        GTTServers[str(guild_id)] = GTTUtils.GTTMaker()
    CurrentServer = GTTServers.get(str(guild_id)) # Access the GTT game for that server
    CurrentServer.Reset()
    print(CurrentServer)
    print(interaction.guild.name)
    GTT_Image = discord.File(filename="Dont_Cheese_XD.png", spoiler= False, fp=f"IMAGESET_VANILLA/{CurrentServer.original}")

    await interaction.followup.send(message,file=GTT_Image)

# bumps the image
async def send_image(interaction: discord.Interaction, message):
    guild_id = interaction.guild_id
    user_id = interaction.user.id

    if GTTServers.get(guild_id) == None: # Makes the GTT game for that server if it dosnest exist
        GTTServers[str(guild_id)] = GTTUtils.GTTMaker()
        await interaction.followup.send("No Active GTT Game")
        return

    CurrentServer = GTTServers.get(str(guild_id)) # Access the GTT game for that server
    if CurrentServer.original == None: # To see if there is a game that has started
        await interaction.followup.send("No Active GTT Game")
        return
    
    print(CurrentServer)
    print(interaction.guild.name)
    GTT_Image = discord.File(filename="Dont_Cheese_XD.png", spoiler= False, fp=f"IMAGESET_VANILLA/{CurrentServer.original}")

    await interaction.followup.send(message,file=GTT_Image)

# check permisions, return false if nuh uh
async def Check_Perms(interaction, type = "Admin"):
    if type == "Admin":
        if interaction.user.id not in Admins:
            await interaction.followup.send("You aint no admin!")
            return False
# Start the bot
bot.run(TOKEN)