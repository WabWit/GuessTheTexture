import json
import random
from modules import Cleaner
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
HINTLIST_PATH = BASE_DIR / "Data" / "hintlist.json"

#HintList Initializer
HINTLIST = {}
with open(HINTLIST_PATH, "r") as file:
    HINTLIST = json.load(file)

#Cleans the hintlist entries to be the same as answers
for hint in HINTLIST:
    CleanedHints = []
    for item in HINTLIST[hint][1]:
        CleanedHints.append(Cleaner.clean_string(item))
    HINTLIST[hint][1] = CleanedHints

#Main Hint Checker
def HintChecker(answer, words_found = []):
    answer_split = answer.split()
    PossibleHints = []
    not_found = list(set(answer_split) - set(words_found))
    first_clue = ""
    for hint in HINTLIST:
        if answer in HINTLIST[hint][1]:
            PossibleHints.append(HINTLIST[hint][0])
    
    if len(not_found) == 0:
        return "All words have been found"
    
    num_hints = len(PossibleHints)
    if num_hints != 0:
        first_clue = random.choice(PossibleHints)
    
    censored_words = []
    for word in not_found:
        word_split = list(word)
        word_length = len(word)
        num_to_replace = int(word_length/2)
        indices = random.sample(range(word_length), k = num_to_replace)
        print(f"word = {word} \nword_split = {word_split}\nword_length = {word_length}\nnum = {num_to_replace} \n indeces = {indices}")
        for i in indices:
            word_split[i] = "_"
        censored_words.append("".join(word_split))
    second_clue = " ".join(censored_words)
    if first_clue and second_clue:
        return f"{first_clue}. Missing words: {second_clue}"
    return f"Missing word is: {first_clue}{second_clue}"