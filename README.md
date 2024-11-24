## Cortana Wireless - Wireless Setup Script for XBMC4Xbox

Cortana Wireless is a script for XBMC4Xbox/XBMC4Gamers that allows you to to use a Raspberry Pi as a ~$35 wireless card for your Xbox, connect/disconnect to wireless networks + check your wireless network statistics via your Xbox connected to a Raspberry Pi with wireless capabilities. This is meant to serve as a modern replacement to the very-outdated-and-very-overpriced Xbox MN-740 wireless adapter, which only supports Wireless G & WEP.

### Parts Needed:
- Raspberry Pi running Raspbian or DietPi (should work on any Raspberry Pi with wireless capabilities, would recommend a Pi Zero W for the smallest footprint.)
- 
(Note that using an original Pi Zero W will limit you to 2.4GHz networks. It doesn't matter in theory as the Xbox maxes out at 100MB/s via ethernet anyway, but you won't be able to connect to 5GHz networks with a base Pi Zero W.)

(*This script can, in theory, be used on any Debian-based machine that presents a wlan0 and an eth0, but the specific target of this combination is a Raspberry Pi so YMMV.*)

- USB ethernet adapter + microUSB OTG cable, if using a Pi Zero W/2W. (I personally would not recommend those generic miniUSB ethernet adapters as they all share the same MAC address, which can cause networking issues, along being known to just die quickly.)
- Ethernet cable connected between the USB ethernet cable + your Xbox (the shorter the better).
- (Optional) USB-to-Xbox adapter (this will let you power the Raspberry Pi directly from the Xbox via one of the controller ports! I can confirm the Pi Zero W gets enough power from it to power itself + a USB hub with an ethernet port!)

The script runs in two parts, "CortanaWireless.py" & "share_wifi.sh" on the Raspberry Pi, which shares the Pi's connection to your Xbox and gives it access to it's network settings, and "default.py", the client-side script that allows you to interface with the Raspberry Pi's network settings. 

## Usage (Pi)
- Download "share_wifi.sh" & "CortanaWireless.py" (optionally, "CortanaWireless.service")
- On your Raspberry Pi, install python3, python3-flask, dnsmasq, iptables & net-tools if you don't have them already (sudo apt install python3 python3-flask dnsmasq iptables net-tools)
- Once complete, go into the directory you've saved the scripts into via your terminal.
- Type "chmod +x share_wifi.sh" to allow the script to launch.
- Type "sudo ./share_wifi.sh" and your Pi should begin sharing it's wlan0 connection to eth0!
- If you want to control your Raspberry Pi's wireless settings via XBMC, you'll need to run the Python script as root (sudo su && python3 CortanaWireless.py) [also maybe don't do this on a production machine, never run strange scripts as root blah blah etc etc].
- (Optional) If you want to run the scripts every time on boot, copy "CortanaWireless.service" and "XboxWiFi.service" to /etc/systemd/system, point the paths under "Exec=" to where you've stored "CortanaWireless.py" and "share_wifi.sh", and run "systemctl enable CortanaWireless && systemctl enable XboxWiFi".

## Usage (Xbox)
- Extract "default.py" to "Q:\scripts\Cortana Wireless"
- Modify "default.py" so that the IP address points towards your Raspberry Pi's ethernet IP (192.168.137.1 after running "share_wifi.sh")
- Select "Connection Status", if you see an SSID or "off", the scripts are connected! If you get an error, make sure everything is set up correctly on the Pi.
- To connect to a wireless network, select "Connect To Network", select the SSID of the network you'd like to connect to, enter the password, and wait a few seconds for the "you're (probably) connected!" prompt to show up.
- To verify that you're connected to the new network, select "Connection Status" again, if you see the new SSID, you're connected! If not, try again.

## Issues:
- Because the built-in wireless adapter on the Raspberry Pi can't be bridged, your Xbox will be on a different subnet than the rest of your devices. For just playing online games and using online homebrew software this is fine, but this means you won't be able to FTP into your Xbox or possibly use System Link.
- It can take between 10-15 seconds to connect to a new wireless network. This is to be expected as whenever you connect to a network via this script, the entire wlan0 device is shut down and then brought back up after writing to wpa_supplicant.conf. I wouldn't worry about it too much, as I doubt anyone's going to be hopping between connections every 5 seconds, but definitely something to work on optimizing. 
- This is hella insecure. Using sudo on scripts you don't know is risky. That being said, this is the only way I could get all of this to work, and it sure does work. I'm not using my Pi for anything mission-critical so it works great for me.

## TODO:
- Integrate [XboxWirelessAdapter by agarmash](https://github.com/agarmash/XboxWirelessAdapter) once both projects are a bit more mature, negating the need for an XBMC script altogether.
- Improve XBMC UI (specifically copying how the wireless manager looks in the Xbox dashboard) & webserver UI (for external access outside of the Xbox)
- Improve WiFi connect/disconnect speeds
