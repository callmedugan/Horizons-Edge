from pyscript import document, when
from player import *
import json
import asyncio

on_levelup_message = False

with open("data/messages.json", "r") as f:
    message_data = json.load(f)

# going to store the current node globally
current_node = message_data["class_selection"]

async def message_init():
    await log_current_node()

def remove_old_messages():
    log = document.querySelector("#story-log")
    log.replaceChildren()

async def restart():
    global current_node
    current_node = message_data["class_selection"]
    remove_old_messages()
    await log_current_node()

async def log_current_node():
    global current_node
    # log the main message
    await log_message(current_node["message"])
    #loop through options and log
    options = current_node.get("options", {})
    messages = []
    for key, choice_data in options.items():
        messages.append(key + ": " + choice_data["text"])
    
    if messages:
        await log_message("\n".join(messages), "text-option")

async def process_user_message(message):
    global current_node
    global on_levelup_message
    options = current_node.get("options", {})

    formatted_message = message.lower()
    #if on_levelup_message dont do any other checking
    if on_levelup_message:
        on_levelup_message = await handle_levelup(formatted_message)
        return

    elif formatted_message in options:
        #print the selected option
        await log_message(f"> {formatted_message}: {options[formatted_message]["text"]}", "text-player")
        #drill down to the respective target node name and set current node
        target_node_name = options[formatted_message]["target"]
        if target_node_name not in message_data:
            await log_message("Not implemented.", "text-system")
            await log_current_node()
            return

        #set current node to the target node and then get the new options
        current_node = message_data[target_node_name]
        options = current_node.get("options", {})
 
        #gain xp if a target node was found
        await handle_xp_gain(current_node)

        #check for set fields to set play stats
        if "set" in current_node:
            await handle_set()

        if on_levelup_message:
            await print_levelup_message()
            return
    
    else:
        #print the input raw text if not in an option
        await log_message(f"> {message}", "text-player")
        if message == "help":
            await log_message("Possible commands:", "text-system")
            await log_message("restart", "text-system")
        elif message == "restart":
            await restart()
        else:
            await log_message("Invalid response.", "text-system")
        return

    # log  new node
    await log_message(" ")
    await log_current_node()

    #check for stat checks and move the node tree forward
    if "requirement" in current_node:
        await handle_stat_check()
        
async def handle_xp_gain(node):
    global on_levelup_message
    if "xp_gain" in node:
        xp_gained = node["xp_gain"]
        if xp_gained > 0:
            increase_stat("xp", xp_gained)
            await log_message(f"Gained {xp_gained}xp!", "text-gold")
            on_levelup_message = check_for_lvl_up()

async def print_levelup_message():
    points = stats["stat_points"]
    msg = f"Your level has increased! You have {points} stat points. Choose the stat(s) you wish to increase:"
    msg += "\n1: STR"
    msg += "\n2: DEX"
    msg += "\n3: INT"
    msg += "\n4: LUK"
    await log_message(msg, "text-gold")

async def handle_levelup(message):
    if message == "1":
        spend_stat_point("str")
        await log_message(f"> 1: STR", "text-player")
    elif message == "2":
        spend_stat_point("dex")
        await log_message(f"> 2: DEX", "text-player")
    elif message == "3":
        spend_stat_point("int")
        await log_message(f"> 3: INT", "text-player")
    elif message == "4":
        spend_stat_point("luk")
        await log_message(f"> 4: LUK", "text-player")
    # check for more points    
    if stats["stat_points"] > 0:
        await log_message(f"You have {stats["stat_points"]} stat points remaining.", "text-gold")
        return True
    # log new node if points have been spent
    await log_message(" ")
    await log_current_node()
    return False

async def handle_set():
    set = current_node.get("set")
    messages = []
    for stat, value in set.items():
        #everything is capitalized anyways
        set_stat(stat, value)
        messages.append(f"{stat} set to {value}!")
    if messages:
        await log_message("\n".join(messages), "text-gold")

async def handle_stat_check():
    global current_node
    has_req_stat = perform_stat_check(current_node["requirement"]["stat"], current_node["requirement"]["value"])
    if has_req_stat:
        await log_message(current_node["success"]["text"], "text-success")
        await handle_xp_gain(current_node["success"])
        current_node = message_data[current_node["success"]["target"]]
    else:
        await log_message(current_node["failure"]["text"], "text-failure")
        current_node = message_data[current_node["failure"]["target"]]
    
    if on_levelup_message:
        await print_levelup_message()
    else:
        await log_current_node()


async def log_message(message, css_class="text-narrative", delay=0.001):
    log = document.querySelector("#story-log")
    
    #block input
    input_field = document.querySelector("#player-input")
    if input_field:
        input_field.disabled = True

    # Create a fresh paragraph for this specific message
    new_p = document.createElement("p")
    # add class for colored text
    new_p.classList.add(css_class)
    log.appendChild(new_p)
    
    space_buffer_count = 0

    for char in message:
        # need to buffer count spaces since they get trimmed in p elements when adding incrementally
        if char == " ":
            space_buffer_count += 1
        elif space_buffer_count > 0:
            new_text = ""
            for x in range(space_buffer_count):
                new_text += " "
            new_text += char
            new_p.innerText += new_text
            space_buffer_count = 0
        else:
            new_p.innerText += char
        # Auto-scroll so the newest letter is always visible
        log.scrollTop = log.scrollHeight
        # Yield control to the browser for the duration of the delay
        await asyncio.sleep(delay)

    # restore input 
    if input_field:
        input_field.disabled = False
        input_field.focus()


asyncio.ensure_future(message_init())