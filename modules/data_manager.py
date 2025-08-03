import json
from pathlib import Path
from modules.GTTUtils import *

BASE_DIR = Path(__file__).parent.parent
GTTSERVERS_PATH = BASE_DIR / "Data" / "GTTServers.json"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" / "IMAGESET_VANILLA"
Admins = [292608557335969793]
GTTServers = None

SERVER_SAVED_SCORES = {}

def get_saved_data() -> None:
    with open(GTTSERVERS_PATH, "r", encoding="utf-8") as file:
        SERVER_SAVED_SCORES = json.load(file)
    GTTServers = ServerContainer(SERVER_SAVED_SCORES)

def get_servers() -> None:
    GTTServers = ServerContainer()