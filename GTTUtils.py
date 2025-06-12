import time, Cleaner, random

IMAGESET_VANILLA = []
with open("filenames.txt") as image_set_list:
    IMAGESET_VANILLA = image_set_list.read().split("\n")

# GTT per server class objecter
class GTTMaker:
    def __init__(self):
        print("initialized")
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

    def Add_Points(self, player_id, amount = int):
        player_score = self.local_scores.get(str(player_id), 0)
        self.local_scores[str(player_id)] = player_score + 1 


class AnswerContainer:
    def __init__(self, answer: str):
        cleaned_answer = Cleaner.clean_string(answer)
        self.answer = cleaned_answer
        self.answer_split = cleaned_answer.split()
        self.answer_capped = cleaned_answer.title()
    
    def __str__(self):
        return f"Answer: {self.answer} \nAnswer Array: {self.answer_split} \nAnswer Readable: {self.answer_capped}"