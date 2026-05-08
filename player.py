import json
from pyscript import document

def player_init():
    with open("data/player_start.json", "r") as f:
        config = json.load(f)
    
    stats = config["base_stats"]
    for stat_name, value in stats.items():
        __set_stat(stat_name, value)
            
    return stats

def __set_stat(stat_name, value):
    element = document.querySelector(f"#{stat_name}")
    if element:
        element.innerText = str(value)
        return True
    return False

def increase_stat(stat_name, value):
    global player_stats
    if stat_name in player_stats:
        player_stats[stat_name] += value
        __set_stat(stat_name, player_stats[stat_name])

def perform_stat_check(stat_name, value):
    if stat_name in player_stats:
        return player_stats[stat_name] >= value
    return False

player_stats = player_init()