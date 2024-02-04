import time
import requests
import os
from dotenv import load_dotenv
from colorama import Fore
import datetime

load_dotenv()
i = 0

# Settings
timeOut = int(os.environ.get("TIMEOUT"))
alert = os.environ.get("ALERT_TEXT")
hostCounter = int(os.environ.get("HOST_NUM"))

# Telegram settings
apiToken = os.environ.get("TOKEN_BOT")
chatID = os.environ.get("CHAT_ID")

# Send notification
def send_to_telegram(message):
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    except Exception as e:
        print(e)

# Logging failures
def SaveToFile(text="Script name: log.py\nFunction: write()\n"):
    with open(f'logs/{logdate}-log.txt', 'a+') as f:
        f.write(text)

print(Fore.YELLOW + "\n --> PingControl start <-- " + Fore.RESET)

while True:

    # Time
    logdate = str(datetime.date.today())
    logtime = datetime.datetime.today().strftime("%H:%M:%S")

    # Start cycle
    if i <= hostCounter:
        hostID = str(os.environ.get(f'HOST_{i}'))
        hostName = str(os.environ.get(f'HOST_NAME_{i}'))
        response = os.system("ping -n 1 " + hostID)
        if response == 0:
            # Ping - OK, proceeding to next host
            print(Fore.GREEN + logdate + " " + logtime + f"\n {hostName} - online!" + Fore.RESET)
            i += 1
        else:
            # Retry if filed
            print(Fore.RED + logdate + " " + logtime + f"\n {hostName} not responding" + Fore.RESET)
            print(Fore.RED + " >> Retrying..." + Fore.RESET)
            response = os.system("ping -n 1 " + hostID)
            if response == 0:
                # Retry Ping - OK, proceeding to next host
                print(Fore.GREEN + logdate + " " + logtime + f"\n {hostName} - request status OK!" + Fore.RESET)
                i += 1
            else:
                # Second ping failed, sending notification to TG and write log
                print(Fore.RED + logdate + " " + logtime + f"\n {hostName} - offline! \n >> Sending Admin notification..." + Fore.RESET)
                send_to_telegram(hostName + " : " + alert)
                text = f"{logdate} {logtime} /-/ Target IP: {hostID} : {hostName} /-/ Ping request lost \n"
                SaveToFile(text)
                i += 1
    else:
        # Waiting timeout for next cycle
        print(Fore.YELLOW + logdate + " " + logtime + "\n -- Ping timeout = " + str(timeOut) + " sec -- " + Fore.RESET)
        time.sleep(timeOut)
        i = 0





