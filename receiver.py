# Made by Ben Costerton
# Contact bencosterton@gmail.com
import pyaudio
import socket
from threading import Thread
from ipaddress import IPv4Interface
import time
import sys
try:
    import win_ntp
except ImportError:
    import unix_ntp

#Windows ntp
try:
    win_ntp.gettime_ntp()
except:
    pass
    
def wait(amount):
    time.sleep(amount)
    print()
    
def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print(flush=True, file=out, end="\r")

NAME = socket.gethostname()
R_IP = socket.gethostbyname(NAME)


#Welcome message
print("""\
 ______   ______        ______     ______                                    
(____  \ / _____)  /\  |  ___ \   |  ___ \                (_)                 
 ____)  ) /       /  \ | |   | |  |  ___) ) ____ ____ ____ _ _   _ ____  ____ 
|  __  (| |      / /\ \| |   | |  |  ___ ( / _  ) ___) _  ) | | | / _  )/ ___)
| |__)  ) \_____| |__| | |   | |  | |   | ( (/ ( (__( (/ /| |\ V ( (/ /| |    
|______/ \______)______|_|   |_|  |_|   |_|\____)____)____)_| \_/ \____)_|                                                                                  
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

#Data receive

def udpStream(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        udp.bind((IP, 14505))
    except (OSError):
        print("Wrong IP, this needs to be the IP of the NIC you are receving audio at")
    
    while True:
        soundData, addr = udp.recvfrom(CHUNK*CHANNELS*2)
        frames.append(soundData)
        for i in progressbar(range(10), f"receiving audio from{addr} ", 20):
                time.sleep(0)
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
