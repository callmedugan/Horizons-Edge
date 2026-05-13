import json
from pyscript import document

stats = {
    "class": "",
    "hp": 10,
    "max-hp": 10,
    "mp": 5,
    "max-mp": 5,
    "str": 1,
    "dex": 1,
    "int": 1,
    "luk": 1,
    "level": 1,
    "xp": 0,
    "stat_points": 0
}

def spend_stat_point(stat_name):
    global stats
    if stats["stat_points"] <= 0:
        return
    if stat_name in stats:
        stats[stat_name] += 1
        __update_stat_element(stat_name, stats[stat_name])
        stats["stat_points"] -= 1
        __update_stat_element("stat_points", stats["stat_points"])

def set_stat(stat_name, new_value):
    global stats
    if stat_name in stats:
        stats[stat_name] = new_value
        __update_stat_element(stat_name, stats[stat_name])

def increase_stat(stat_name, value):
    global stats
    if stat_name in stats:
        stats[stat_name] += value
        __update_stat_element(stat_name, stats[stat_name])

def update_all_stat_elements():
    for stat_name in stats:
        element = document.querySelector(f"#{stat_name}")
        if element:
            element.innerText = str(stats[stat_name])

def __update_stat_element(stat_name, value):
    element = document.querySelector(f"#{stat_name}")
    if element:
        element.innerText = str(value)

def perform_stat_check(stat_name, value):
    global stats
    if stat_name in stats:
        return stats[stat_name] >= value
    return False            

def check_for_lvl_up() -> bool:
    global stats
    global stat_data
    next_lvl_data = stat_data["level_data"][str(stats["level"] + 1)]
    xp_req_for_next_lvl = next_lvl_data["xp_needed"]
    if stats["xp"] >= xp_req_for_next_lvl:
        stats["stat_points"] += next_lvl_data["stat_points_on_lvl_up"]
        stats["hp"] += next_lvl_data["hp_on_lvl_up"]
        stats["max-hp"] += next_lvl_data["hp_on_lvl_up"]
        stats["mp"] += next_lvl_data["mp_on_lvl_up"]
        stats["max-mp"] += next_lvl_data["mp_on_lvl_up"]
        stats["level"] += 1
        update_all_stat_elements()
        return True
    return False


# get the stat data
with open("data/stats.json", "r") as f:
    stat_data = json.load(f)

# save the player stats
for stat_name, value in stats.items():
    set_stat(stat_name, value)
