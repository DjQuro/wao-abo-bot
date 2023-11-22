def help(arg=None):
    try:
        print(f"help - Print this dialog")
        print(f"updatedb - Updates the DJ database manually")
        print(f"logclear - Creates a Log-Cycle (Use it as a cron!)")
        print(f"reset - Clear errors and restart the whole bot")
        print(f"restart - Arguments: commander, announcer, index or indexer - Restart a component or the whole System")
        print(f"start - Arguments: commander, announcer, index or indexer - Start a component or the whole System")
        print(f"stop - Arguments: commander, announcer, index or indexer - Stop a component or the whole System")
        print(f"ban - Arguments: DJ - Blacklists a DJ")
        print(f"install - Installs the Services and dependencies - One time use!")
    except Exception as e:
        handle_exception(f"Error in help: {e}")
        
def handle_exception(error_message):
    print(error_message)