import json
from pathlib import Path
from modules.GTTUtils import *

BASE_DIR = Path(__file__).parent.parent
GTTSERVERS_PATH = BASE_DIR / "Data" / "GTTServers.json"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" / "IMAGESET_VANILLA"
Admins = [292608557335969793]
GTTServers = ServerContainer()

def get_saved_data() -> None:
    SERVER_SAVED_SCORES = {}
    with open(GTTSERVERS_PATH, "r", encoding="utf-8") as file:
        SERVER_SAVED_SCORES = json.load(file)
        print(SERVER_SAVED_SCORES)
    GTTServers.Add_Multiple_Servers(SERVER_SAVED_SCORES)

def save_server_data() -> None:
    dump = {}
    for guild_id in GTTServers.server_list.keys():
        dump[str(guild_id)] = GTTServers.server_list[str(guild_id)].local_scores
    with open(GTTSERVERS_PATH, "w") as ServersFile:
        json.dump(dump, ServersFile)
