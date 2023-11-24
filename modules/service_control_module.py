import os
import sys
        
def restart(arg=None):
    try:
        if arg:
            if arg:
                if arg == "commander":
                    service = commander
                elif arg == "announcer":
                    service = announcer
                elif arg == "index" or arg == "indexer":
                    service = indexer
                else:
                    handle_exception(f"Awww man... {arg} is not a service i know! Try commander, announcer, index or indexer")
                
                print(f"Restarting {service}... Please wait!")
                os.system(f"systemctl restart {service}.service")
                handle_exception(f"Restarting {service} was successful!")
        else:
            print(f"Restarting all Services... Please wait!")
            os.system("systemctl restart wao-announcer.service")
            os.system("systemctl restart wao-commander.service")
            os.system("systemctl restart wao-index.service")

            print("RESTART SUCCESSFUL!")
    except Exception as e:
        handle_exception(f"Error in restart: {e}")
        
def start(arg=None):
    try:
        if arg:
            if arg:
                if arg == "commander":
                    service = commander
                elif arg == "announcer":
                    service = announcer
                elif arg == "index" or arg == "indexer":
                    service = indexer
                else:
                    print(f"Awww man... {arg} is not a service i know! Try commander, announcer, index or indexer")
                    sys.exit()
                
                print(f"Starting {service}... Please wait!")
                os.system(f"systemctl start {service}.service")
                handle_exception(f"Starting {service} was successful!")
        else:
            print(f"Starting all Services... Please wait!")
            os.system("systemctl start wao-announcer.service")
            os.system("systemctl start wao-commander.service")
            os.system("systemctl start wao-index.service")

            print("START SUCCESSFUL!")
    except Exception as e:
        handle_exception(f"Error in start: {e}")
        
def stop(arg=None):
    try:
        if arg:
            if arg:
                if arg == "commander":
                    service = commander
                elif arg == "announcer":
                    service = announcer
                elif arg == "index" or arg == "indexer":
                    service = indexer
                else:
                    print(f"Awww man... {arg} is not a service i know! Try commander, announcer, index or indexer")
                    sys.exit()
                
                print(f"Stopping {service}... Please wait!")
                os.system(f"systemctl stop {service}.service")
                handle_exception(f"Stopping {service} was successful!")
        else:
            print(f"Stopping all Services... Please wait!")
            os.system("systemctl stop wao-announcer.service")
            os.system("systemctl stop wao-commander.service")
            os.system("systemctl stop wao-index.service")

            print("STOP SUCCESSFUL!")
    except Exception as e:
        handle_exception(f"Error in stop: {e}")

def handle_exception(error_message):
    print(error_message)