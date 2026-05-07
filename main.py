from pyscript import when, document # Use document for better DOM control
import json
from message import *

# Initialization
log_message("Welcome, adventurer.")

@when("keydown", "#player-input")
def handle_enter(event):
    # Only trigger if the key pressed was Enter
    if event.key == "Enter":
        # Get the input element and its value
        player_input = document.querySelector("#player-input")
        command = player_input.value.strip()
        
        if command:
            # 1. Echo the command to the log (like a terminal)
            log_message(f"> {command}")
            
            # 2. Clear the input box for the next command
            player_input.value = ""
            
            # 3. Process the logic (we'll connect your JSON here)
            process_command(command)

def process_command(command):
    # This is where your RPG logic will live
    # For now, let's just make it respond
    if command.lower() == "help":
        log_message("Available commands: look, search, help.")
    else:
        log_message(f"You tried to '{command}', but nothing happened.")

