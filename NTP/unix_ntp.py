import ntplib
from datetime import datetime, timezone
import os
import time

def wait(amount):
    time.sleep(amount)
    print()


# NTP Clock Master
IP_input = input("Enter the IP of the NTP master clock: ")
ntp_IP = str(IP_input)

#while True:
try:
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(ntp_IP, version=3)
    current_time = datetime.fromtimestamp(response.tx_time)
    try:
        os.system('sudo date {} > /dev/null '.format(current_time.strftime('%m%d%H%M%Y'))) #macOS
        print("System time updated to: ", current_time)
        wait (5)
    except (OSError, TimeoutError):
        os.system('sudo date -s "{}"'.format(current_time.strftime('%Y-%m-%d %H:%M:%S'))) #deb
        print("System time updated to: ", current_time)
        wait (5)
except :
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request("time.google.com", version=3)
        current_time = datetime.fromtimestamp(response.tx_time)
        try:
            os.system('sudo date {} > /dev/null '.format(current_time.strftime('%m%d%H%M%Y'))) #macOS
            print("Failed to connect to given NTP server, time updated to Google NTP server: ", current_time)
            wait (5)
        except (OSError, TimeoutError):
            os.system('sudo date -s "{}"'.format(current_time.strftime('%Y-%m-%d %H:%M:%S'))) #deb
            print("Failed to connect to given NTP server, time updated to Google NTP server: ", current_time)
            wait (5)
    except ntplib.NTPException as e:
        print("Error updating system time: ", e)
