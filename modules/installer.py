import os
import subprocess
import time
import sys

def install(arg=None):
    try:
        if os.path.exists("/root/WAO-Abobot/.installed"):
            print("You don't need to use this command!")
        else:
            # Service-Dateien installieren
            service_folder = "/root/WAO-Abobot/services"
            for service_file in os.listdir(service_folder):
                full_path = os.path.join(service_folder, service_file)
                if os.path.isfile(full_path) and full_path.endswith(".service"):
                    subprocess.run(["sudo", "cp", full_path, "/etc/systemd/system/"])
                    subprocess.run(["sudo", "systemctl", "enable", os.path.basename(full_path)])
                    subprocess.run(["sudo", "systemctl", "start", os.path.basename(full_path)])

            # Services-Ordner löschen
            subprocess.run(["rm", "-r", service_folder])

            # Cronjob hinzufügen
            cron_command = "0 0 * * * /usr/bin/python3 /root/WAO-Abobot/bcl.py logclear"
            index_command = "0 * * * * /usr/bin/python3 /root/WAO-Abobot/bcl.py updatedb"
            subprocess.run(["bash", "-c", f"(crontab -l 2>/dev/null; echo '{cron_command}') | crontab -"])
            subprocess.run(["bash", "-c", f"(crontab -l 2>/dev/null; echo '{index_command}') | crontab -"])

            # Python 3 und pip installieren (falls nicht bereits installiert)
            subprocess.run(["sudo", "apt-get", "update"])
            subprocess.run(["sudo", "apt-get", "install", "-y", "python3", "python3-pip"])

            # Pakete aus requirements.txt installieren
            subprocess.run(["pip3", "install", "-r", "data/requirements.txt"])

            # Alle zuvor installierten Services neu starten
            for service_file in os.listdir("/etc/systemd/system"):
                if service_file.endswith(".service"):
                    subprocess.run(["sudo", "systemctl", "restart", os.path.basename(service_file, ".service")])

            subprocess.run(["touch", "/root/WAO-Abobot/.installed"])
            handle_exception("Installation successful!")
    except Exception as e:
        handle_exception(f"Installation FAILED! {e}")
        
def handle_exception(error_message):
    print(error_message)
    time.sleep(5)
    sys.exit()
