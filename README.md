## Cortana Wireless - Wireless Setup Script for XBMC4Xbox

Cortana Wireless is a script for XBMC4Xbox/XBMC4Gamers that allows you to to use a Raspberry Pi (or similar Debian-based machine) as a ~$35 wireless card for your Xbox, connect/disconnect to wireless networks + check your wireless network statistics via your Xbox connected to a Raspberry Pi with wireless capabilities. 

This is meant to serve as a modern replacement to the very-outdated-and-very-overpriced **Xbox MN-740** wireless adapter, which only supports Wireless G & WEP, with quality-of-life features like **insigniaDNS** and **XLink Kai** built right-in.

![Cortana Wireless Main Menu](/screenshots/1.png)
![Cortana Wireless - Wireless Menu](/screenshots/2.png) 
![Cortana Wireless - Connection Status](/screenshots/3.png)
![Cortana Wireless - Wireless Networks](/screenshots/4.png)
![Cortana Wireless - Bluetooth Menu](/screenshots/5.png)
![Cortana Wireless - Bluetooth Devices](/screenshots/6.png)
![Cortana Wireless - insigniaDNS Menu](/screenshots/7.png)
![Cortana Wireless - XLink Kai Menu](/screenshots/8.png)
![Cortana Wireless - Power Menu](/screenshots/9.png)

## Features:
- **insigniaDNS** & **XLink Kai** support built right, making connecting your Xbox online an absolute breeze. 
- Easy connection to any wireless network via the XBMC4Xbox script!
- Broadcast which games you're playing on Discord via [xbdStats!](https://github.com/MrMilenko/xbdStats) (requires [ShortcutRelayXBE](https://github.com/OfficialTeamUIX/ShortcutRelayXBE))
- Share your Xbox's audio from an RCA connection to a Bluetooth device such as a speaker or headset via the Bluetooth section! (Coming soon!)
- Want to use it on something that's not an Xbox? The Raspberry Pi scripts themselves are system-agnostic, just select "No" to installing XLink + insigniaDNS when prompted, plug your Pi into your old device's ethernet port and you're ready to go online!

## Parts Needed:
- Raspberry Pi running DietPi (should work on any Raspberry Pi or similar SBC with wireless capabilities, would recommend a Pi Zero W for the smallest footprint.)
- (Raspbian support coming soon!)

*Note that using an original Pi Zero W will limit you to 2.4GHz networks. It doesn't matter in theory as the Xbox maxes out at 100MB/s via ethernet anyway, but you won't be able to connect to 5GHz networks with a base Pi Zero W. This script can, in theory, be used on any Debian-based machine that presents a wlan0 and an eth0, but the specific target of this combination is a Raspberry Pi so YMMV.*

- USB ethernet adapter + microUSB OTG cable, if using a Pi Zero W/2W. (I personally would not recommend those generic miniUSB ethernet adapters as they all share the same MAC address, which can cause networking issues, along being known to just die quickly.)
- Ethernet cable connected between the USB ethernet cable + your Xbox (the shorter the better).
- (Optional) USB-to-Xbox adapter (this will let you power the Raspberry Pi directly from the Xbox via one of the controller ports! I can confirm the Pi Zero W gets enough power from it to power itself + a USB hub with an ethernet port!)
- (Optional) USB Soundcard (if you want to connect your Xbox's audio to Bluetooth by using an RCA to 3.5mm adapter)
- (Very Optional) SH1106/SSD1306 LCD adapter for use with [Cortana Display](https://github.com/faithvoid/script.cortanadisplay).

The script runs in two parts, "CortanaWireless.py" & "share_wifi.sh" on the Raspberry Pi, which shares the Pi's connection to your Xbox and gives it access to it's network settings, and "default.py", the client-side script that allows you to interface with the Raspberry Pi's network settings. 

## Usage (Pi)
- Enter the line down below in your Pi's terminal after setting up your distro of choice (run as root by using "sudo su"!)!
- DietPi (currently working perfectly!): ``` wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/install.sh && chmod +x install.sh && ./install.sh ```
- Raspberry Pi OS (This doesn't work yet!): ``` wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/install_raspbian.sh && chmod +x install_raspbian.sh && ./install_raspbian.sh ```
- Change the "SHARED_SECRET" key in /opt/CortanaWireless/CortanaWireless.py to a unique password, one you'll share with the Xbox script! ESPECIALLY if your Pi is doing any sort of web / server hosting! (defaults to C0RT4N4).
- (Optional) If powering the Pi via your USB ports, I'd recommend enabling powersaving mode in dietpi-config/raspi-config to make sure your Pi uses as little power as possible (it'll still be fast enough to run everything in this script just fine!)
- (Optional) To control XLink Kai, enter the wireless IP address of your Raspberry Pi into your browser, followed by :34522, (ie; "http://192.168.1.2:34522/"). Further information on how to use the XLink Kai webUI can be found on the official XLink Kai page.
- (Optional) If using xbdStats, you'll have to modify "xbdStats.py" in /opt/CortanaWireless to include your Discord Client ID.

 
## Usage (Xbox)
- Extract "default.py" from "releases" to "Q:\scripts\Cortana Wireless"
- Modify "default.py" so that the IP address points towards your Raspberry Pi's ethernet IP if you've manually changed anything (defaults to 192.168.137.1 after running "share_wifi.sh")
- Change the "SHARED_SECRET" key in "default.py" to the same "SHARED_SECRET" key that you input into "CortanaWireless.py" earlier.
- Select "Connection Status", if you see an SSID or "off", the scripts are connected! If you get an error, make sure everything is set up correctly on the Pi.
- To connect to a wireless network, select "Connect To Network", select the SSID of the network you'd like to connect to, enter the password, and wait a few seconds for the "you're (probably) connected!" prompt to show up.
- To verify that you're connected to the new network, select "Connection Status" again, if you see the new SSID, you're connected! If not, try again.
- (Optional) If you installed insigniaDNS, leave your Dashboard IP settings on "Automatic" and set DNS #1 to "192.168.137.1" and DNS #2 to "8.8.8.8" (or your choice of DNS provider).

## Usage (Other Clients)
This script comes with a very basic PC client that can be used on anything with Python 3 & requests. This has only been tested on Linux & Android via Pydroid, YMMV elsewhere. (**This currently doesn't work due to auth changes, sorry!**)

![Script running via PyDroid](https://github.com/user-attachments/assets/a7ce42d6-6513-4476-a60d-7d57258fe169)


## Issues:
- Because the built-in wireless adapter on the Raspberry Pi can't be bridged, your Xbox will be on a different subnet than the rest of your devices. For just playing online games and using online homebrew software this is fine, but this means you won't be able to FTP into your Xbox or possibly use System Link. If System Link doesn't work, XLink Kai will work incredibly well out of the box with zero configuration, just installing + running it on the Pi!
- It can take between 10-15 seconds to connect to a new wireless network. This is to be expected as whenever you connect to a network via this script, the entire wlan0 device is shut down and then brought back up after writing to wpa_supplicant.conf. I wouldn't worry about it too much, as I doubt anyone's going to be hopping between connections every 5 seconds, but definitely something to work on optimizing.
- Bluetooth build takes 10+ seconds to scan for devices. This is normal, as we need to give the Pi as much time as possible to detect all available BT devices.
- Bluetooth latency is currently somewhere between 0.5 to 0.75 seconds. In it's current state I'd recommend using it primarily for music listening as the delay may be too great for videos and games. Can possibly be rectified by using a standalone adapter? But ideally the solution isn't "buy more hardware".
- This implementation is very insecure. The scripts run with sudo privileges, and the Flask server can receive commands from basically any client that sends the correct request & auth codes to the correct port. Maybe don't run this on mission-critical devices or devices directly exposed to the web, but it's Fine for a device you just leave connected to your 20+ year old game console.

## TODO:
- Add [xbdStats](https://github.com/MrMilenko/xbdStats) to installation options  for Discord Rich Presence support!
- Integrate [XboxWirelessAdapter by agarmash](https://github.com/agarmash/XboxWirelessAdapter) once both projects are a bit more mature, negating the need for an XBMC script altogether.
- Improve XBMC UI (specifically copying how the wireless manager looks in the Xbox dashboard) & webserver UI (for external access outside of the Xbox)
- Improve WiFi connect/disconnect speeds
- Add hidden network support
- Modify Bluetooth implementation to show the user device names and not MAC addresses.
- Implementing soundcard/3.5mm support to share Xbox audio (via RCA to 3.5mm or similar) to Bluetooth devices & a way to control which device they're paired to via XBMC would be a fun addition. (Halfway through!)
- Add custom command support for troubleshooting / funsies / etc.
- Add proper web UI for cross-platform / console-agnostic use.
- Fix authorization code for PC Python client.

## Credits:
- Insignia Team - For making an incredible Xbox Live replacement (I repurposed their version of insigniaDNS to only connect to "eth0" so you can set your DNS settings to the Raspberry Pi and forget about them!)
- XLink Kai Team - For making an incredible System Link replacement (this script installs their webUI Linux program!)
- OfficialTeamUIX + MrMilenko + Mobcat - xbdStats for Discord Rich Presence support.
- Bromigo - Thanks for the rigorous testing! Having another person being able to sanity-check things was a major help throughout this project.

## License:
- [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


