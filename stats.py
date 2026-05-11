from pyscript import document, when
import json


with open("data/stats.json", "r") as f:
    stat_data = json.load(f)

# going to store the current node globally
level_data = stat_data["level_data"]
current_lvl = 1

def check_for_lvl_up(current_xp : int) -> bool:
    global current_lvl
    global level_data
    next_lvl = str(current_lvl + 1)
    xp_req_for_next_lvl = level_data[next_lvl]["xp_needed"]
    if current_xp >= xp_req_for_next_lvl:
        current_lvl += 1
        return True
    return False