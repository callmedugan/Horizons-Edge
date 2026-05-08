import json
from pyscript import document

def player_init():
    with open("data/player_start.json", "r") as f:
        config = json.load(f)
    
    stats = config["base_stats"]
    for stat_name, value in stats.items():
        set_stat(stat_name, value)
            
    return stats

def set_stat(stat_name, value):
    element = document.querySelector(f"#{stat_name}")
    
    if element:
        element.innerText = str(value)
        return True
    
    return False


player_stats = player_init()