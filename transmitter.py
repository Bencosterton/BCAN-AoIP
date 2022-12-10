import pyaudio
import socket
from threading import Thread
import time
import sys

def wait(amount):
    time.sleep(amount)
    print()

#Welcome message
    print("""\
 _  _  _       _                                        ______   ______        ______  
| || || |     | |                          _           (____  \ / _____)  /\  |  ___ \ 
| || || | ____| | ____ ___  ____   ____   | |_  ___     ____)  ) /       /  \ | |   | |
| ||_|| |/ _  ) |/ ___) _ \|    \ / _  )  |  _)/ _ \   |  __  (| |      / /\ \| |   | |
| |___| ( (/ /| ( (__| |_| | | | ( (/ /   | |_| |_| |  | |__)  ) \_____| |__| | |   | |
 \______|\____)_|\____)___/|_|_|_|\____)   \___)___/   |______/ \______)______|_|   |_| 
  TRANSMITTER                  """)

wait(1)

IP_input = input("Give me an IP, dude: ")
IP = str(IP_input)
UDP_input = input("And which UDP port?: ")
UDP = int(UDP_input)

frames = []

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
                    )

#Initialize Threads
    AudioThread = Thread(target = record, args = (stream, CHUNK,))
    udpThread = Thread(target = udpStream)
    AudioThread.start()
    udpThread.start()
    AudioThread.join()
    udpThread.join()
