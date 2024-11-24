## Cortana Wireless - Wireless Setup Script for XBMC4Xbox

Cortana Wireless is a script for XBMC4Xbox/XBMC4Gamers that allows you to to use a Raspberry Pi as a ~$35 wireless card for your Xbox, connect/disconnect to wireless networks + check your wireless network statistics via your Xbox connected to a Raspberry Pi with wireless capabilities.

### Parts Needed:
- Raspberry Pi (should work on any Raspberry Pi with wireless capabilities, would recommend a Pi Zero W for the smallest footprint)
- USB ethernet adapter (+ microUSB OTG cable if using a Pi Zero, I personally would not recommend those generic miniUSB ethernet adapters as they all share the same MAC address, which can cause networking issues, along being known to just die quickly.)
- Ethernet cable connected between the USB ethernet cable + your Xbox.
- (Optional) USB-to-Xbox adapter (this will let you power the Raspberry Pi directly from the Xbox via one of the controller ports!)

The script runs in two parts, "PiScript.py", which runs on the Raspberry Pi and gives your Xbox access to it's network features, and "default.py", the client-side script that allows you to interface with the Raspberry Pi's network.

## Usage (Pi)
- Download "share_wifi.sh" & "CortanaWireless-Pi.py" (optionally, "CortanaWireless.service")
- On your Raspberry Pi, install python3, python3-flask, dnsmasq, iptables & net-tools if you don't have them already (sudo apt install python3 python3-flask dnsmasq iptables net-tools)
- Once complete, go into the directory you've saved the scripts into via your terminal.
- Type "chmod +x share_wifi.sh" to allow the script to launch.
- Type "sudo ./share_wifi.sh" and your Pi should begin sharing it's wlan0 connection to eth0!
- If you want to control your Raspberry Pi's wireless settings via XBMC, you'll need to run the Python script as root (sudo su && python3 CortanaWireless-Pi.py) [also maybe don't do this on a production machine, never run strange scripts as root blah blah etc etc].

## Usage (Xbox)
- Extract "default.py" to "Q:\scripts\Cortana Wireless"
- Select "Connection Status", if you see an SSID or "off", you're connected! If you get an error, make sure everything is set up correctly on the Pi.
- To connect to a wireless network, select "Connect To Network", select the SSID of the network you'd like to connect to, enter the password, and wait a few seconds for the "you're (probably) connected!" prompt to show up.
- To verify that you're connected to the new network, select "Connection Status" again, if you see the new SSID, you're connected! If not, try again.

## Issues:
- Because the built-in wireless adapter on the Raspberry Pi can't be bridged, your Xbox will be on a different subnet than the rest of your devices. For just playing online games and using online homebrew software this is fine, but this means you won't be able to FTP into your Xbox or possibly use System Link.
