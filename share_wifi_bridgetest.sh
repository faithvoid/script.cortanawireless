#!/bin/bash

# Define interfaces
WIFI_INTERFACE="wlan0"
ETH_INTERFACE="eth0"
BRIDGE_INTERFACE="br0"

# Check if script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Install required packages
echo "Checking for required packages..."
packages=(bridge-utils)
for pkg in "${packages[@]}"; do
    if dpkg -l | grep -qw "$pkg"; then
        echo "$pkg is already installed. Skipping."
    else
        echo "$pkg is not installed. Installing..."
        apt install -y "$pkg"
    fi
done

# Shut down the eth0 interface
echo "Bringing down $ETH_INTERFACE..."
ifconfig $ETH_INTERFACE down

# Create the bridge interface
if brctl show | grep -q $BRIDGE_INTERFACE; then
    echo "Bridge interface $BRIDGE_INTERFACE already exists."
else
    echo "Creating bridge interface $BRIDGE_INTERFACE..."
    brctl addbr $BRIDGE_INTERFACE
fi

# Add wlan0 and eth0 interfaces to the bridge
echo "Adding $WIFI_INTERFACE and $ETH_INTERFACE to the bridge..."
brctl addif $BRIDGE_INTERFACE $WIFI_INTERFACE $ETH_INTERFACE

# Start up the br0 interface
echo "Bringing up $BRIDGE_INTERFACE..."
ifconfig $BRIDGE_INTERFACE up

# Ensure Wi-Fi is up (if not already managed by another tool like NetworkManager)
echo "Bringing up $WIFI_INTERFACE..."
ifconfig $WIFI_INTERFACE up

# Assign DHCP to the bridge (optional, if not managed by another service)
echo "Requesting DHCP for the bridge interface..."
dhclient $BRIDGE_INTERFACE

# Print success message
echo "WiFi-to-Ethernet bridge is now enabled!"
echo "Clients connected to the Ethernet port will receive DHCP and have internet access on the same subnet as the Pi."
