# BCAN
Send UDP stream over any network between any os

![image](https://user-images.githubusercontent.com/21957617/206717972-94a0e5f4-df21-4798-85d8-a3a9f745b81a.png)

BCAN is an ongoing project.
The need to send audio over a private network, between different OS, without using existing Dante or Ravenna network arose, so this is a working solution. 
Welcome to BCAN

# To Do

A list of things that need to be done 

### CLI Interface
Usable Multi OS CLI interface 
- [x] Windows 10
- [x] Ubuntu Studio 22.04*
- [x] macOS

*Running app on Linux (tested with Ubuntu Studio 22.04) some erros flag reference ALSA, but it does still work.

### Run on WiFi and Eth
- [x] WiFi
- [x] Eth

### Capable of accepting or changing unicast IP addresses
- [x] Done

### MiMo
Will need to be able to send multiple inputs to multiple outputs.
Unicast and Multicast
- [ ] Multi Input
- [x] Multi Output

### Sync
- [ ] PTPv2
- [x] NTP

### Dicovery
- [ ] Implementation of SAP or mDNS

### Subscription Ledger
Will need to be able to see what is being sent and where.
First from a specific server. then for the entire network.




#### Requirments
python-pyaudio
