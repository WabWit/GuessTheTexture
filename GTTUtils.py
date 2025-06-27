import time, Cleaner, random

IMAGESET_VANILLA = []
with open("filenames.txt", encoding="utf-8") as image_set_list:
    IMAGESET_VANILLA = image_set_list.read().split("\n")

# GTT per server class objecter
class GTTMaker:
    def __init__(self, local_scores = None):
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
            "Rolled": int(time.time())
            }
        self.time_list = Time
        self.local_scores = local_scores
    
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
        self.TimeReset()
        self.total_guesses = 0
        self.per_user_guesses = {}
        self.words_guessed = []

    def AddPoints(self, player_id, amount = 1): 
        # Add points. default 1
        player_score = self.local_scores.get(str(player_id), 0)
        self.local_scores[str(player_id)] = player_score + amount

    def TimeReset(self, to_reset_list = None):
        if to_reset_list is None:
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

    def GetTimeDifference(self, type = "Debounce"):
        self_time = self.time_list.get(type)
        if self_time:
            return (int(time.time()) - self_time)
        else:
            raise Exception("Type Error")


class AnswerContainer:
    def __init__(self, answer: str):
        cleaned_answer = Cleaner.clean_string(answer)
        self.answer = cleaned_answer
        self.answer_split = cleaned_answer.split()
        self.answer_capped = cleaned_answer.title()
    
    def __str__(self):
        return f"Answer: {self.answer} \nAnswer Array: {self.answer_split} \nAnswer Readable: {self.answer_capped}"