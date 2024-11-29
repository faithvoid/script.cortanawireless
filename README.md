## Cortana Wireless - Wireless Setup Script for XBMC4Xbox

Cortana Wireless is a script for XBMC4Xbox/XBMC4Gamers that allows you to to use a Raspberry Pi as a ~$35 wireless card for your Xbox, connect/disconnect to wireless networks + check your wireless network statistics via your Xbox connected to a Raspberry Pi with wireless capabilities. This is meant to serve as a modern replacement to the very-outdated-and-very-overpriced Xbox MN-740 wireless adapter, which only supports Wireless G & WEP.

![cwd](https://github.com/user-attachments/assets/56d0af15-1c15-4ef5-a3b0-5c29a3906ead)


### Parts Needed:
- Raspberry Pi running Raspbian or DietPi (should work on any Raspberry Pi with wireless capabilities, would recommend a Pi Zero W for the smallest footprint.)

*Note that using an original Pi Zero W will limit you to 2.4GHz networks. It doesn't matter in theory as the Xbox maxes out at 100MB/s via ethernet anyway, but you won't be able to connect to 5GHz networks with a base Pi Zero W. This script can, in theory, be used on any Debian-based machine that presents a wlan0 and an eth0, but the specific target of this combination is a Raspberry Pi so YMMV.*

- USB ethernet adapter + microUSB OTG cable, if using a Pi Zero W/2W. (I personally would not recommend those generic miniUSB ethernet adapters as they all share the same MAC address, which can cause networking issues, along being known to just die quickly.)
- Ethernet cable connected between the USB ethernet cable + your Xbox (the shorter the better).
- (Optional) USB-to-Xbox adapter (this will let you power the Raspberry Pi directly from the Xbox via one of the controller ports! I can confirm the Pi Zero W gets enough power from it to power itself + a USB hub with an ethernet port!)
- (Very Optional) SH1106/SSD1306 LCD adapter for use with [Cortana Display](https://github.com/faithvoid/script.cortanadisplay).

The script runs in two parts, "CortanaWireless.py" & "share_wifi.sh" on the Raspberry Pi, which shares the Pi's connection to your Xbox and gives it access to it's network settings, and "default.py", the client-side script that allows you to interface with the Raspberry Pi's network settings. 

## Usage (Pi)
- Enter the line down below in your Pi's terminal after setting up your distro of choice!
- ``` curl -sL https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/install.sh | bash ```
  
## Usage (Xbox)
- Extract "default.py" from "releases" to "Q:\scripts\Cortana Wireless"
- Modify "default.py" so that the IP address points towards your Raspberry Pi's ethernet IP if you've manually changed anything (defaults to 192.168.137.1 after running "share_wifi.sh")
- Select "Connection Status", if you see an SSID or "off", the scripts are connected! If you get an error, make sure everything is set up correctly on the Pi.
- To connect to a wireless network, select "Connect To Network", select the SSID of the network you'd like to connect to, enter the password, and wait a few seconds for the "you're (probably) connected!" prompt to show up.
- To verify that you're connected to the new network, select "Connection Status" again, if you see the new SSID, you're connected! If not, try again.

## Usage (Other Clients)
This script comes with a very basic PC client that can be used on anything with Python 3 & requests. This has only been tested on Linux & Android via Pydroid, YMMV elsewhere. 
![Script running via PyDroid](https://github.com/user-attachments/assets/a7ce42d6-6513-4476-a60d-7d57258fe169)


## Issues:
- Because the built-in wireless adapter on the Raspberry Pi can't be bridged, your Xbox will be on a different subnet than the rest of your devices. For just playing online games and using online homebrew software this is fine, but this means you won't be able to FTP into your Xbox or possibly use System Link. If System Link doesn't work, XLink Kai will work incredibly well out of the box with zero configuration, just installing + running it on the Pi!
- It can take between 10-15 seconds to connect to a new wireless network. This is to be expected as whenever you connect to a network via this script, the entire wlan0 device is shut down and then brought back up after writing to wpa_supplicant.conf. I wouldn't worry about it too much, as I doubt anyone's going to be hopping between connections every 5 seconds, but definitely something to work on optimizing.
- Bluetooth build takes 10+ seconds to scan for devices. This is normal, as we need to give the Pi as much time as possible to detect all available BT devices.
- Modify Bluetooth implementation to show the user device names and not MAC addresses.
- This implementation is very insecure. The scripts run with sudo privileges, and the Flask server can receive commands from basically any client that sends the correct request to the correct port. Maybe don't run this on mission-critical devices or devices directly exposed to the web, but it's Fine for a device you just leave connected to your 20+ year old game console.

## TODO:
- Integrate [XboxWirelessAdapter by agarmash](https://github.com/agarmash/XboxWirelessAdapter) once both projects are a bit more mature, negating the need for an XBMC script altogether.
- Improve XBMC UI (specifically copying how the wireless manager looks in the Xbox dashboard) & webserver UI (for external access outside of the Xbox)
- Improve WiFi connect/disconnect speeds
- Better authentication?
- Implementing soundcard/3.5mm support to share Xbox audio (via RCA to 3.5mm or similar) to Bluetooth devices & a way to control which device they're paired to via XBMC would be a fun addition. (Halfway through!)
- Make a simple dashboard-agnostic homebrew .XBE with NXDK (with a .cfg file with the Pi IP) to control Pi(?) (I'm bad at C/C++, help.)
