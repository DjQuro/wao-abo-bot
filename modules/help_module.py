def help(arg=None):
    try:
        print(f"help - Print this dialog\n\n")
        print(f"updatedb - Updates the DJ database manually\n\n")
        print(f"logclear - Creates a Log-Cycle (Use it as a cron!)\n\n")
        print(f"reset - Clear errors and restart the whole bot\n\n")
        print(f"restart - Arguments: commander, announcer - Restart a component or the whole System\n\n")
        print(f"start - Arguments: commander, announcer - Start a component or the whole System\n\n")
        print(f"stop - Arguments: commander, announcer - Stop a component or the whole System\n\n")
        print(f"ban - Arguments: DJ - Blacklists a DJ\n\n")
        print(f"install - Installs the Services and dependencies - One time use!\n\n")
    except Exception as e:
        handle_exception(f"Error in help: {e}")
        
def handle_exception(error_message):
    print(error_message)
