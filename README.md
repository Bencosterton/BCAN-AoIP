# BCAN
Send UDP audio stream over any network between any OS

![image](https://user-images.githubusercontent.com/21957617/206717972-94a0e5f4-df21-4798-85d8-a3a9f745b81a.png)

BCAN is an ongoing project.
The need to send audio over a private network, between different OS, without using existing Dante or Ravenna network arose, so this is a working solution. 
Welcome to BCAN

# To Do

A list of things that need to be done 

### CLI Interface
Usable Multi OS CLI interface 
- [x] Windows 10
- [x] Linux - Debian*
- [x] macOS

*When running app on Linux some erros flag reference ALSA, but it does still work. Check install.txt for dependancies.

### Run on WiFi and Eth
- [x] WiFi
- [x] Eth

### Capable of accepting or changing unicast IP addresses
- [x] Done

### MiMo
Will need to be able to send multiple inputs to multiple outputs.
Unicast and Multicast
- [x] Multi Input*
- [x] Multi Output*

* A given machine can use multiple inputs, and multiple output simultaniously, however, a transmitter cannot send multiple inputs to independent outputs on a single receiver. A connection between two given machines will only have one logical stream of audio. 

### Input and Output device selection
- [x] Input selection
- [x] Output selection

### Sync
- [ ] PTPv2
- [x] NTP

### Dicovery
- [ ] Implementation of SAP or mDNS

### Subscription Ledger
Will need to be able to see what is being sent and where.
First from a specific server. then for the entire network.




#### Requirments
- python-pyaudio
- python-ntplib
