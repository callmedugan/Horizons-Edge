from pyscript import when, document # Use document for better DOM control
from message import *
from player import *

# inputs
@when("click", "#story-log")
def focus_input(event):
    document.querySelector("#player-input").focus()

@when("keydown", "#player-input")
def handle_enter(event):
    if not hasattr(event, "key") or event.key is None:
        return
    if event.key == "Enter":
        # Get the input element and its value
        player_input = document.querySelector("#player-input")
        command = player_input.value.strip()
        
        if command:
            log_message(f"> {command}")
            player_input.value = ""
            process_user_message(command)


# Game start
message_init()

