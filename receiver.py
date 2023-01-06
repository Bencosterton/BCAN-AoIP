import pyaudio
import socket
from threading import Thread
from ipaddress import IPv4Interface
import time
import sys
import ntplib
from datetime import datetime, timezone

def wait(amount):
    time.sleep(amount)
    print()
    
NAME = socket.gethostname()
R_IP = socket.gethostbyname(NAME)


#Welcome message
print("""\
 _  _  _       _                                        ______   ______        ______  
| || || |     | |                          _           (____  \ / _____)  /\  |  ___ \ 
| || || | ____| | ____ ___  ____   ____   | |_  ___     ____)  ) /       /  \ | |   | |
| ||_|| |/ _  ) |/ ___) _ \|    \ / _  )  |  _)/ _ \   |  __  (| |      / /\ \| |   | |
| |___| ( (/ /| ( (__| |_| | | | ( (/ /   | |_| |_| |  | |__)  ) \_____| |__| | |   | |
 \______|\____)_|\____)___/|_|_|_|\____)   \___)___/   |______/ \______)______|_|   |_| 
  RECEIVER -""", NAME, R_IP)

wait(1)

#Audio output
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
	if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
		print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

Au_Output = input("Which output are we using?: ")
Output = int(Au_Output)

#Network output
IP_input = input("receiver IP: ")
IP = str(IP_input)
frames = []

#Timing

#try:
#    t = ntplib.NTPClient()
#    response = t.request('time.google.com', version=3)
#    response.offset
    #print (datetime.fromtimestamp(response.tx_time, timezone.utc))
#except:
#    pass

#Data receive

def udpStream(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((IP, 6980))
    
    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        frames.append(soundData)
        print(f"receiving audio from{addr}...")
    udp.close()

def play(stream, CHUNK):
    BUFFER = 100
    while True:
            if len(frames) == BUFFER:
                while True:
                    stream.write(frames.pop(0), CHUNK)

if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 2
    RATE = 48000

    Audio = pyaudio.PyAudio()

    stream = Audio.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
		            output_device_index = Output,
                    )

    udpThread  = Thread(target = udpStream, args=(CHUNK,))
    AudioThread  = Thread(target = play, args=(stream, CHUNK,))
    udpThread .start()
    AudioThread.start()
    udpThread .join()
    AudioThread.join()
