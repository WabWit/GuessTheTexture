import json
from pathlib import Path
from modules.GTTUtils import *

BASE_DIR = Path(__file__).parent.parent
GTTSERVERS_PATH = BASE_DIR / "Data" / "GTTServers.json"
IMAGESET_VANILLA_PATH = BASE_DIR / "Data" / "IMAGESET_VANILLA"
Admins = [292608557335969793]
GTTServers = None

def get_servers() -> None:
    GTTServers = ServerContainer()