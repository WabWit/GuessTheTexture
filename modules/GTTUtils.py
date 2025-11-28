import time
import random
import discord
from discord.ext import commands
from modules import Cleaner
from pathlib import Path
#from modules.Unbound_FNCS import Get_Time_Difference
#from modules.data_manager import save_server_data

BASE_DIR = Path(__file__).parent.parent
FILENAMES_PATH = BASE_DIR / "Data" / "filenames.txt"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" /"IMAGESET_VANILLA"

IMAGESET_VANILLA = []
with open(FILENAMES_PATH, encoding="utf-8") as image_set_list:
    IMAGESET_VANILLA = image_set_list.read().split("\n")

# GTT per server class objecter
class GTTMaker:
    def __init__(self, local_scores: dict = None):
        if local_scores is None:
            local_scores = {}
        print("initialized")
        self.original = ""
        self.answer = ""
        self.answer_capped = ""
        self.answer_split = []
        self.total_guesses = 0
        self.per_user_guesses = {}
        self.words_guessed = []
        Time = {
            "Debounce": int(time.time()),
            "Rolled": int(time.time()),
            "SaveTimer": int(time.time())
            }
        self.time_list = Time
        self.local_scores = local_scores
    
    def __str__(self):
        return f"Answer: {self.answer} \nAnswer Array: {self.answer_split} \nAnswer Readable: {self.answer_capped}"

    def Roll(self):
        answer = random.choice(IMAGESET_VANILLA)
        file_path = IMAGESET_VANILLA_PATH / answer

        while not file_path.is_file():
            print(f"WARNING, {answer} DOES NOT EXIST! Rerolling now")
            answer = random.choice(IMAGESET_VANILLA)
            file_path = IMAGESET_VANILLA_PATH / answer
            time.sleep(1)

        cleaned_answer = Cleaner.clean_string(answer)
        self.original = answer
        self.answer = cleaned_answer
        self.answer_split = cleaned_answer.split()
        self.answer_capped = cleaned_answer.title()

        print(self.original)
    
    def Reset(self):
        self.Roll()
        self.TimeReset()
        self.total_guesses = 0
        self.per_user_guesses = {}
        self.words_guessed = []

        #if Get_Time_Difference(self.time_list["SaveTimer"]) >= 30:
        #    save_server_data()
        #    print("Auto-saved server data")
        #    self.time_list["SaveTimer"] = int(time.time())

    def TimeReset(self, to_reset_list = None):
        if to_reset_list is None:
            # Reset Mandatory timers
            to_reset_list = ["Debounce", "Rolled"]
        for to_reset in to_reset_list:
            match to_reset:
                case "Debounce":
                    self.time_list["Debounce"] = int(time.time())
                    return
                case "Rolled":
                    self.time_list["Rolled"] = int(time.time())
                    return
                case _:
                    print(f"{to_reset} Does not exist in time_list, fix ur code dumbas")

    def AddPoints(self, player_id, amount = 1): 
        # Add points. default 1
        player_score = self.local_scores.get(str(player_id), 0)
        self.local_scores[str(player_id)] = player_score + amount

class AnswerContainer:
    def __init__(self, answer: str):
        cleaned_answer = Cleaner.clean_string(answer)
        self.answer = cleaned_answer
        self.answer_split = cleaned_answer.split()
        self.answer_capped = cleaned_answer.title()
    
    def __str__(self):
        return f"Answer: {self.answer} \nAnswer Array: {self.answer_split} \nAnswer Readable: {self.answer_capped}"
    
class CooldownManager:
    def __init__(self):
        self._cd = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.guild)

    def check(self, interaction: discord.Interaction):
        bucket = self._cd.get_bucket(interaction)
        retry_after = bucket.update_rate_limit()
        return retry_after

class ServerContainer:
    def __init__(self, servers: dict = None):
        self.server_list = {}
        if servers == None:
            return
        self.Add_Multiple_Servers(servers)

    def Add_Server(self, guild_id: str, local_scores: dict = None) -> None:
        print("im so deep")
        print(local_scores)
        if local_scores == None:
            local_scores = {}
        self.server_list[guild_id] = GTTMaker(local_scores)

    def Add_Multiple_Servers(self, server_list: dict = None) -> None:
        if server_list == None:
            print("SERVER LIST IS EMPTY, RETURNING WITH NO NEW SERVERS")
            return

        print("wawawaw")
        for guild_id in server_list.keys():
            print("im in")
            self.Add_Server(guild_id, server_list[guild_id])
        print(self.server_list)

    def Get_Server(self, guild_id: str) -> GTTMaker:
        current_server = self.server_list.get(guild_id)
        if current_server == None:
            self.Add_Server(guild_id)
            current_server = self.server_list.get(guild_id)
        return current_server

        