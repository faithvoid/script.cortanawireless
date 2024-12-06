#!/bin/bash

# Define interfaces
WIFI_INTERFACE="wlan0"
ETH_INTERFACE="eth0"

# Check if script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Enable IP forwarding
echo "Enabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf

# Set up NAT with iptables
echo "Setting up iptables for NAT..."
iptables --table nat -A POSTROUTING -o $WIFI_INTERFACE -j MASQUERADE
iptables -A FORWARD -i $ETH_INTERFACE -o $WIFI_INTERFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $WIFI_INTERFACE -o $ETH_INTERFACE -j ACCEPT

# Save iptables rules so they persist after reboot - Uncomment if needed!
#echo "Saving iptables rules..."
#iptables-save > /etc/iptables/rules.v4

# Configure NetworkManager to share the Ethernet connection
echo "Configuring NetworkManager to share Ethernet..."
nmcli connection modify "$WIFI_INTERFACE" ipv4.method shared
nmcli connection modify "$ETH_INTERFACE" ipv4.addresses "192.168.137.1/24"
nmcli connection modify "$ETH_INTERFACE" ipv4.gateway "192.168.137.1"
nmcli connection modify "$ETH_INTERFACE" ipv4.dns "8.8.8.8"
nmcli connection modify "$ETH_INTERFACE" connection.autoconnect yes

# Restart NetworkManager to apply changes
echo "Restarting NetworkManager..."
systemctl restart NetworkManager

# Print success message
echo "WiFi-to-Ethernet sharing is now enabled!"
echo "Clients connected to the Ethernet port will receive DHCP and have internet access."
