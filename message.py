from pyscript import document
from player import *
import json

with open("data/messages.json", "r") as f:
    message_data = json.load(f)

current_node = message_data["class_selection"]


def message_init():
    log_current_node()

def log_message(message):
    # Target the container
    log = document.querySelector("#story-log")
    # Create a fresh paragraph element
    new_p = document.createElement("p")
    new_p.innerText = message
    # Add it to the log
    log.appendChild(new_p)
    # Auto-scroll to the bottom
    log.scrollTop = log.scrollHeight

def remove_old_messages():
    log = document.querySelector("#story-log")
    log.replaceChildren()

def log_current_node():
    global current_node
    options = current_node.get("options", {})
    
    log_message(current_node["message"])

    for key, choice_data in options.items():
        log_message(key + ": " + choice_data["text"])



def process_user_message(message):
    global current_node
    options = current_node.get("options", {})

    remove_old_messages()

    formatted_message = message.lower()
    if formatted_message in options:
        #drill down to the respective target node name and set current node
        target_node_name = options[formatted_message]["target"]
        if target_node_name not in message_data:
            log_message("Not implemented.")
            log_current_node()
            return

        #set current node to the target node and then get the new options
        current_node = message_data[target_node_name]
        options = current_node.get("options", {})

        #gain xp if a target node was found
        if "xp_gain" in current_node:
            xp_gained = current_node["xp_gain"]
            if xp_gained > 0:
                increase_stat("xp", xp_gained)
                log_message(f"Gained {xp_gained}xp!")
    
    else:
        log_message("Invalid response.")

    # log  new node
    log_message(" ")
    log_current_node()
    


    #check for stat checks
    if "requirement" in current_node:
        has_req_stat = perform_stat_check(current_node["requirement"]["stat"], current_node["requirement"]["value"])
        if has_req_stat:
            log_message(current_node["success"]["text"])
            current_node = message_data[current_node["success"]["target"]]
        else:
            log_message(current_node["failure"]["text"])
            current_node = message_data[current_node["failure"]["target"]]
        log_current_node()