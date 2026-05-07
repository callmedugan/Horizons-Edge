from pyscript import document

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
