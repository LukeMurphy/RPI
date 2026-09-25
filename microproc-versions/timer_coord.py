import time
import random
import math
import machine
import network
import ntptime
import requests
from interstate75 import DISPLAY_INTERSTATE75_64X64, Interstate75

pieceToPlay = "drawing_marks"
timeToPlay = 20
playT1 = time.time()
playT2 = time.time()

# Check and import the Network SSID and Password from secrets.py
try:
    from secrets import WIFI_PASSWORD, WIFI_SSID

    if WIFI_SSID == "":
        raise ValueError("WIFI_SSID in 'secrets.py' is empty!")
    if WIFI_PASSWORD == "":
        raise ValueError("WIFI_PASSWORD in 'secrets.py' is empty!")
except ImportError:
    raise ImportError("'secrets.py' is missing from your Plasma 2350 W!")
except ValueError as e:
    print(e)

rtc = machine.RTC()

DAYS = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]

# Enable the Wireless
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


def network_connect(SSID, PSK):

    # Number of attempts to make before timeout
    max_wait = 5

    # Sets the Wireless LED pulsing and attempts to connect to your local network.
    print("connecting...")
    wlan.config(pm=0xA11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(SSID, PSK)

    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting for connection...")
        time.sleep(1)

    # Handle connection error. Switches the Warn LED on.
    if wlan.status() != 3:
        print("Unable to connect. Attempting connection again")

    else:
        print(f"wlan status: {wlan.status()}")


# Function to sync the Pico RTC using NTP
def sync_time():

    try:
        network_connect(WIFI_SSID, WIFI_PASSWORD)
    except NameError:
        print("Create secrets.py with your WiFi credentials")

    if wlan.status() < 0 or wlan.status() >= 3:
        try:
            ntptime.settime()
        except OSError:
            print("Unable to sync with NTP server. Check network and try again.")
        return True


#sync_time()
#current_t = rtc.datetime()
#print(current_t)

def getPieceToPlay():
    global pieceToPlay
    # url = "https://lukelab.com/projects/rpi-controls/micropys/piece-to-play.php"
    url = "https://lamshell.opalstacked.com/lukelab/"
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}
    headers={'Accept': 'application/json'}
    # response = requests.get(url=url, headers=headers)
    try:
        # comment: 
        response = requests.get(url=url)
        # Get response code
        print(response.status_code)
        if pieceToPlay != response.text :
            pieceToPlay = response.text
            print(pieceToPlay)
            with open("./piecetoplay.txt", "w") as fh :
                fh.write(pieceToPlay)
    except Exception as e:
        print(e)
    # end try

try:
    network_connect(WIFI_SSID, WIFI_PASSWORD)
except NameError:
    print("Create secrets.py with your WiFi credentials")
    


# print("Done")
