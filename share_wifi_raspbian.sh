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

# Save iptables rules so they persist after reboot
echo "Saving iptables rules..."
iptables-save > /etc/iptables/rules.v4

# Configure dhcpcd to provide DHCP on Ethernet
echo "Configuring dhcpcd for Ethernet interface..."
cat <<EOL >> /etc/dhcpcd.conf

# Configure static IP for eth0 (Ethernet)
interface $ETH_INTERFACE
static ip_address=192.168.137.1/24
denyinterfaces eth0
EOL

# Restart dhcpcd service to apply the changes
echo "Restarting dhcpcd service..."
systemctl restart dhcpcd

# Assign a static IP to the Ethernet interface (optional, since dhcpcd is now handling it)
# This can be omitted if dhcpcd configures it
ifconfig $ETH_INTERFACE 192.168.137.1 netmask 255.255.255.0 up

# Print success message
echo "WiFi-to-Ethernet sharing is now enabled!"
echo "Clients connected to the Ethernet port will receive DHCP and have internet access."
