from pyscript import document, when
from player import *
import json
import asyncio

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
    for key, choice_data in options.items():
        await log_message(key + ": " + choice_data["text"], "text-option")

async def process_user_message(message):
    global current_node
    options = current_node.get("options", {})

    formatted_message = message.lower()
    if formatted_message in options:
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
        if "xp_gain" in current_node:
            xp_gained = current_node["xp_gain"]
            if xp_gained > 0:
                increase_stat("xp", xp_gained)
                await log_message(f"Gained {xp_gained}xp!", "text-gold")

        #check for set fields to set play stats
        if "set" in current_node:
            await handle_set()
    
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
        
async def handle_set():
    set = current_node.get("set")
    for stat, value in set.items():
        #everything is capitalized anyways
        set_stat(stat, value)
        await log_message(f"{stat} set to {value}!", "text-gold")

async def handle_stat_check():
    global current_node
    has_req_stat = perform_stat_check(current_node["requirement"]["stat"], current_node["requirement"]["value"])
    if has_req_stat:
        await log_message(current_node["success"]["text"], "text-success")
        current_node = message_data[current_node["success"]["target"]]
    else:
        await log_message(current_node["failure"]["text"], "text-failure")
        current_node = message_data[current_node["failure"]["target"]]
    await log_current_node()


async def log_message(message, css_class="text-narrative", delay=0.003):
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