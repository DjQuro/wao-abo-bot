import os
import sys
import threading
import time

def loading_animation():
    # Drehzeichen (Spinner)
    spinner = "|/-\\"
    idx = 0

    while not stop_event.is_set():
        sys.stdout.write("\rLoading " + spinner[idx])
        sys.stdout.flush()
        time.sleep(0.1)
        idx = (idx + 1) % len(spinner)

    # Lösche die Ladeanimation, wenn gestoppt
    sys.stdout.write("\r")
    sys.stdout.flush()

def restart(arg=None):
    try:
        if arg:
            if arg:
                if arg == "commander":
                    service = commander
                else:
                    handle_exception(f"Awww man... {arg} is not a service I know! Try commander, announcer, index, or indexer")

                print(f"Restarting {service}... Please wait!")
                loading_thread = threading.Thread(target=loading_animation)
                loading_thread.start()
                os.system(f"systemctl restart {service}.service")
                stop_event.set()
                handle_exception(f"Restarting {service} was successful!")
        else:
            print("Restarting all Services... Please wait!")
            loading_thread = threading.Thread(target=loading_animation)
            loading_thread.start()
            os.system("systemctl restart wao-commander.service")
            stop_event.set()
            print("RESTART SUCCESSFUL!")

    except Exception as e:
        handle_exception(f"Error in restart: {e}")

def start(arg=None):
    try:
        if arg:
            if arg:
                if arg == "commander":
                    service = commander
                else:
                    print(f"Awww man... {arg} is not a service I know! Try commander, announcer, index, or indexer")
                    sys.exit()

                print(f"Starting {service}... Please wait!")
                loading_thread = threading.Thread(target=loading_animation)
                loading_thread.start()
                os.system(f"systemctl start {service}.service")
                stop_event.set()
                handle_exception(f"Starting {service} was successful!")
        else:
            print("Starting all Services... Please wait!")
            loading_thread = threading.Thread(target=loading_animation)
            loading_thread.start()
            os.system("systemctl start wao-commander.service")
            stop_event.set()
            print("START SUCCESSFUL!")

    except Exception as e:
        handle_exception(f"Error in start: {e}")

def stop(arg=None):
    try:
        if arg:
            if arg:
                if arg == "commander":
                    service = commander
                else:
                    print(f"Awww man... {arg} is not a service I know! Try commander, announcer, index, or indexer")
                    sys.exit()

                print(f"Stopping {service}... Please wait!")
                loading_thread = threading.Thread(target=loading_animation)
                loading_thread.start()
                os.system(f"systemctl stop {service}.service")
                stop_event.set()
                handle_exception(f"Stopping {service} was successful!")
        else:
            print("Stopping all Services... Please wait!")
            loading_thread = threading.Thread(target=loading_animation)
            loading_thread.start()
            os.system("systemctl stop wao-commander.service")
            stop_event.set()
            print("STOP SUCCESSFUL!")

    except Exception as e:
        handle_exception(f"Error in stop: {e}")

def handle_exception(error_message):
    print(error_message)

# Initialisiere stop_event
stop_event = threading.Event()

# Setze die Service-Namen
commander = "wao-commander"
announcer = "wao-announcer"