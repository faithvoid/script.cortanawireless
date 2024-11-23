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

# Install dnsmasq if not already installed
#echo "Installing dnsmasq..."
#apt update
#apt install -y dnsmasq

# Configure dnsmasq for DHCP on Ethernet
echo "Configuring dnsmasq..."
cat <<EOL > /etc/dnsmasq.conf
interface=$ETH_INTERFACE      # Listen on the Ethernet interface
dhcp-range=192.168.137.50,192.168.137.150,12h  # DHCP range for Ethernet clients
EOL

# Restart dnsmasq service
echo "Restarting dnsmasq..."
systemctl restart dnsmasq

# Assign a static IP to the Ethernet interface (optional)
echo "Assigning static IP to Ethernet interface..."
ifconfig $ETH_INTERFACE 192.168.137.1 netmask 255.255.255.0 up

# Print success message
echo "WiFi-to-Ethernet sharing is now enabled!"
echo "Clients connected to the Ethernet port will receive DHCP and have internet access."

# To stop the script, just reverse the changes or reboot
