from dotenv import load_dotenv
import os, json, math, asyncio, time, random, Hint, Cleaner, discord
from discord.ext import commands

# Load your token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')


GTTServers = {} #creates a container for servers
IMAGESET_VANILLA = []

#Get imagelist
IMAGESET_VANILLA = []
with open("filenames.txt") as image_set_list:
    IMAGESET_VANILLA = image_set_list.read().split("\n")

# Setup Discord bot with all intents
intents = discord.Intents.all()
intents.message_content = True

# Create the bot with a prefix (for compatibility with text commands)
bot = commands.Bot(command_prefix=",", intents=intents)

# GTT per server class objecter
class GTTMaker:
    def __init__(self):
        self.original = ""
        self.answer = ""
        self.answer_capped = ""
        self.answer_split = []
        self.total_guesses = 0
        self.per_user_guesses = {}
        self.words_guessed = []
        self.time_started = int(time.time())
        self.local_scores = {}
    
    def __str__(self):
        return f"Answer: {self.answer} \nAnswer Array: {self.answer_split} \nAnswer Readable: {self.answer_capped}"

    def Roll(self):
        answer = random.choice(IMAGESET_VANILLA)
        cleaned_answer = Cleaner.clean_string(answer)
        self.original = answer
        self.answer = cleaned_answer
        self.answer_split = cleaned_answer.split()
        self.answer_capped = cleaned_answer.title()
    
    def Reset(self):
        self.Roll()
        self.time_started = int(time.time())
        self.total_guesses = 0
        self.per_user_guesses = {}
        self.words_guessed = []

class AnswerContainer:
    def __init__(self, answer: str):
        cleaned_answer = Cleaner.clean_string(answer)
        self.answer = cleaned_answer
        self.answer_split = cleaned_answer.split()
        self.answer_capped = cleaned_answer.title()
    
    def __str__(self):
        return f"Answer: {self.answer} \nAnswer Array: {self.answer_split} \nAnswer Readable: {self.answer_capped}"


# Slash command registration (sync)
@bot.event
async def on_ready():
    await bot.wait_until_ready()  # Just to be safe
    await bot.tree.sync()         # Registers the slash commands with Discord
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Slash commands synced!")

@bot.tree.command(name="quit", description="back to the gulag")
async def exit(interaction : discord.Interaction):
    print(f"Bot shutting down blame {interaction.user.display_name} from {interaction.guild.name}")
    await interaction.response.send_message("Shutting Down")
    await quit()

# ALL COMMANDS FOR NORMAL PLAYERS

#sending a picture
@bot.tree.command(name="image", description="Bumps the current image")
async def image(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    await send_image(interaction, "Guess this image:")

#answer command
@bot.tree.command(name="answer", description="amogus")
async def answer(interaction: discord.Interaction, answer: str):
    # tells discord that i gotchu and wait fo me
    await interaction.response.defer(ephemeral=False)
    guild_id = interaction.guild_id 
    user_id = interaction.user.id
    user_answer = AnswerContainer(answer)
    Current_Server = GTTServers.get(str(guild_id))
    # return if no active game
    if Current_Server == None:
        await interaction.followup.send("No Active GTT game")
        return
    Current_Server.total_guesses += 1

    # Number of guess detection
    GuessIndicator = "You have guessed one times"
    amount_of_guessses = Current_Server.per_user_guesses.get(str(user_id), 0)
    if amount_of_guessses == 3:
        await interaction.followup.send("You're out of guesses buckaroo")
        return
    
    if amount_of_guessses == 2:
        GuessIndicator = "You're out of guesses"
    if amount_of_guessses == 1:
        GuessIndicator = "You have one guess left"
    Current_Server.per_user_guesses[str(user_id)] = amount_of_guessses + 1

    # Check if the answer is right
    if sorted(user_answer.answer_split) == sorted(Current_Server.answer_split):
        await send_image(interaction, "Correct! How about this one?")
        return
    
    Current_Server.words_guessed = list((set(Current_Server.answer_split) & set(user_answer.answer_split)) | set(Current_Server.words_guessed))
    print(Current_Server.answer_split, user_answer.answer_split, Current_Server.words_guessed)

    await interaction.followup.send(GuessIndicator)
    
# Sends image
async def send_image(interaction: discord.Interaction, message):
    guild_id = interaction.guild_id
    user_id = interaction.user.id

    if GTTServers.get(guild_id) == None: # Makes the GTT game for that server if it dosnest exist
        GTTServers[str(guild_id)] = GTTMaker()
    CurrentServer = GTTServers.get(str(guild_id)) # Access the GTT game for that server
    CurrentServer.Reset()
    print(CurrentServer)
    print(interaction.guild.name)
    GTT_Image = discord.File(filename="Dont_Cheese_XD.png", spoiler= False, fp=f"IMAGESET_VANILLA/{CurrentServer.original}")

    await interaction.followup.send(message,file=GTT_Image)

# Start the bot
bot.run(TOKEN)