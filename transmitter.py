import socket
import pyaudio
from threading import Thread
import time
import sys
import ntplib
from datetime import datetime, timezone

def wait(amount):
    time.sleep(amount)
    print()

NAME = socket.gethostname()
T_IP = socket.gethostbyname(NAME)

#Welcome message
print("""\
 _  _  _       _                                        ______   ______        ______  
| || || |     | |                          _           (____  \ / _____)  /\  |  ___ \ 
| || || | ____| | ____ ___  ____   ____   | |_  ___     ____)  ) /       /  \ | |   | |
| ||_|| |/ _  ) |/ ___) _ \|    \ / _  )  |  _)/ _ \   |  __  (| |      / /\ \| |   | |
| |___| ( (/ /| ( (__| |_| | | | ( (/ /   | |_| |_| |  | |__)  ) \_____| |__| | |   | |
 \______|\____)_|\____)___/|_|_|_|\____)   \___)___/   |______/ \______)______|_|   |_| 
  TRANSMITTER -""", NAME, T_IP,)

wait(1)

#Input Audio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

Au_Input = input("Which input are we using?: ")
Input = int(Au_Input)

#Input Network
IP_input = input("Give me an IP, dude: ")
IP = str(IP_input)
UDP = 6980
frames = []

#NTP Request
try:
    t = ntplib.NTPClient()
    response = t.request('time.google.com', version=3)
    response.offset
    #print (datetime.fromtimestamp(response.tx_time, timezone.utc))
except:
    pass


#Data send
def udpStream():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        if len(frames) > 0:
            udp.sendto(frames.pop(0), (IP, UDP))
            print ("Sending audio to",IP,"at",UDP)
            sys.stdout.flush()
            print ("Sending audio to",IP,"at",UDP," .")
            sys.stdout.flush()
            print ("Sending audio to",IP,"at",UDP," ..")
            sys.stdout.flush()
    udp.close()

def record(stream, CHUNK):
    while True:
        frames.append(stream.read(CHUNK))

if __name__ == "__main__":
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #Audio Codec (last two digits are the bit rate)
    CHANNELS = 2 #Stereo or Mono
    RATE = 48000 #Sampling Rate

    Audio = pyaudio.PyAudio()

    stream = Audio.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    input_device_index = Input,
                    )

    AudioThread = Thread(target = record, args = (stream, CHUNK,))
    udpThread = Thread(target = udpStream)
    AudioThread.start()
    udpThread.start()
    AudioThread.join()
    udpThread.join()
