import json
from pyscript import document

def set_stat(stat_name, new_value):
    global player_stats
    if stat_name in player_stats:
        player_stats[stat_name] = new_value
        __update_stat_element(stat_name, player_stats[stat_name])

def increase_stat(stat_name, value):
    global player_stats
    if stat_name in player_stats:
        player_stats[stat_name] += value
        __update_stat_element(stat_name, player_stats[stat_name])

def __update_stat_element(stat_name, value):
    element = document.querySelector(f"#{stat_name}")
    if element:
        element.innerText = str(value)

def perform_stat_check(stat_name, value):
    if stat_name in player_stats:
        return player_stats[stat_name] >= value
    return False

with open("data/player_start.json", "r") as f:
    config = json.load(f)
    
player_stats = config["base_stats"]
for stat_name, value in player_stats.items():
    set_stat(stat_name, value)
            
