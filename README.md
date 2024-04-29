## Cortana Wireless - Wireless Setup Script for XBMC4Xbox

Cortana Wireless is a script for XBMC4Xbox/XBMC4Gamers that allows you to to use a Raspberry Pi as a ~$35 wireless card for your Xbox, connect/disconnect to wireless networks + check your wireless network statistics via your Xbox connected to a Raspberry Pi with wireless capabilities.

### Parts Needed:
- Raspberry Pi (should work on any Raspberry Pi with wireless capabilities, would recommend a Pi Zero W for the smallest footprint)
- USB ethernet adapter + microUSB OTG cable (I personally would not recommend those generic miniUSB ethernet adapters as they all share the same MAC address, which can cause networking issues, along being known to just die quickly.)
- (Optional) USB-to-Xbox adapter (this will let you power the Raspberry Pi directly from the Xbox via one of the controller ports!)

The script runs in two parts, "PiScript.py", which runs on the Raspberry Pi and gives your Xbox access to it's network features, and "default.py", the client-side script that allows you to interface with the Raspberry Pi's network.

To use the script, simply run "py PiScript.py" on the Raspberry Pi and run the "Cortana Wireless" script from the Scripts menu of XBMC. If you want the script to start up automatically when the Raspberry Pi starts, copy the "CortanaWireless.service" to /etc/systemd/user, then type "sudo systemctl enable CortanaWireless". 
