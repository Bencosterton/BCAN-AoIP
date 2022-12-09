import pyaudio
import socket
from threading import Thread
from ipaddress import IPv4Interface
import time

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
  RECEIVER                  """)

wait(1)

IP_input = input("receiver IP: ")
IP = str(IP_input)

frames = []

def udpStream(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((IP, 6980)) # IP of receiver machine machine only

    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        frames.append(soundData)
        print("receiving audio...")
    udp.close()

def play(stream, CHUNK):
    BUFFER = 100
    while True:
            if len(frames) == BUFFER:
                while True:
                    stream.write(frames.pop(0), CHUNK)

if __name__ == "__main__":
    FORMAT = pyaudio.paInt24
    CHUNK = 2048
    CHANNELS = 2
    RATE = 48000

    Audio = pyaudio.PyAudio()

    stream = Audio.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )

    udpThread  = Thread(target = udpStream, args=(CHUNK,))
    AudioThread  = Thread(target = play, args=(stream, CHUNK,))
    udpThread .start()
    AudioThread.start()
    udpThread .join()
    AudioThread.join()
