# Made by Ben Costerton
# Contact bencosterton@gmail.com
import socket
import pyaudio
from threading import Thread
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
T_IP = socket.gethostbyname(NAME)

#Welcome message
print("""\
 ______   ______        ______     _______                             _                     
(____  \ / _____)  /\  |  ___ \   (_______)                           (_)_   _               
 ____)  ) /       /  \ | |   | |   _        ____ ____ ____   ___ ____  _| |_| |_  ____  ____ 
|  __  (| |      / /\ \| |   | |  | |      / ___) _  |  _ \ /___)    \| |  _)  _)/ _  )/ ___)
| |__)  ) \_____| |__| | |   | |  | |_____| |  ( ( | | | | |___ | | | | | |_| |_( (/ /| |    
|______/ \______)______|_|   |_|   \______)_|   \_||_|_| |_(___/|_|_|_|_|\___)___)____)_|    
""", NAME, T_IP,)

wait(1)

#Input Audio
Audio = pyaudio.PyAudio()
info = Audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (Audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", Audio.get_device_info_by_host_api_device_index(0, i).get('name'))

Au_Input = input("Which input are we using?: ")
Input = int(Au_Input)

#Input Network
IP_input = input("Give me an IP, dude: ")
IP = str(IP_input)
UDP = 14505
frames = []


#Data send
def udpStream():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        if len(frames) > 0:
            udp.sendto(frames.pop(0), (IP, UDP))
            for i in progressbar(range(10), f"Sending audio to {IP} at {UDP} ", 20):
                time.sleep(0)
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
