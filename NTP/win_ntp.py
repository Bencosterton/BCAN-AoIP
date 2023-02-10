import socket
import struct
import sys
import time
import datetime
import win32api

IP_input = input("Enter the IP of the NTP master clock: ")
ntp_IP = str(IP_input)

server_list = [ntp_IP,'time.google.com']

def gettime_ntp(addr='time.google.com'):
    TIME1970 = 2208988800 
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = bytes('\x1b' + 47 * '\0','utf-8')
    try:
        client.settimeout(0.5)
        try:
            client.sendto( data, (addr, 123))
        except (OSError):
            print("That's not an address hosting a NTP clock")
            pass
        data, address = client.recvfrom( 1024 )
        if data:
            epoch_time = struct.unpack( '!12I', data )[10]
            epoch_time -= TIME1970
            return epoch_time
    except (socket.timeout, socket.gaierror, ConnectionResetError):
        return None


for server in server_list:
    epoch_time = gettime_ntp(server)
    try:
        if epoch_time is not None:
            utcTime = datetime.datetime.utcfromtimestamp(epoch_time)
            win32api.SetSystemTime(utcTime.year, utcTime.month, utcTime.weekday(), utcTime.day, utcTime.hour, utcTime.minute, utcTime.second, 0)
            localTime = datetime.datetime.fromtimestamp(epoch_time)
            print("Time updated to: " + localTime.strftime("%Y-%m-%d %H:%M") + " from " + server)
            break
        else:
            print("Could not find time from " + server)
    except Exception as e:
        print("You don't have permission to update system clock, run app as admin, skipping for now")
        pass
