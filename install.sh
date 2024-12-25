#!/bin/bash

# Ensure the script runs with superuser privileges
if [ "$(id -u)" -ne 0; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Function to check if a package is installed
is_installed() {
    dpkg -l | grep -qw "$1"
}

# Ask the user what they'd like to install
echo "- Cortana Wireless -"
read -p "Would you like to install InsigniaDNS? (y/n): " install_insigniaDNS
read -p "Would you like to install XLink Kai? (y/n): " install_xlink

# Install required packages
echo "Checking for required packages..."
packages=(python3 python3-flask dnsmasq iptables net-tools)
for pkg in "${packages[@]}"; do
    if is_installed "$pkg"; then
        echo "$pkg is already installed. Skipping."
    else
        echo "$pkg is not installed. Installing..."
        apt install -y "$pkg"
    fi
done

# Install InsigniaDNS if selected
if [[ "$install_insigniaDNS" == "y" ]]; then
    echo "Checking for insigniaDNS dependencies..."
    insignia_dependencies=(python3-dnslib python3-requests)
    for dep in "${insignia_dependencies[@]}"; do
        if is_installed "$dep"; then
            echo "$dep is already installed. Skipping."
        else
            echo "$dep is not installed. Installing..."
            apt install -y "$dep"
        fi
    done

    wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/insigniaDNS.py
    mv insigniaDNS.py /opt/CortanaWireless/

    wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/insigniaDNS.service
    cp insigniaDNS.service /etc/systemd/system/
    systemctl enable insigniaDNS.service
    systemctl start insigniaDNS.service
    enable_insigniaDNS=true
else
    enable_insigniaDNS=false
    echo "Skipping insigniaDNS installation."
fi

# Install XLink Kai if selected
if [[ "$install_xlink" == "y" ]]; then
    echo "Checking for XLink Kai dependencies..."
    dependencies=(ca-certificates curl gnupg)
    for dep in "${dependencies[@]}"; do
        if is_installed "$dep"; then
            echo "$dep is already installed. Skipping."
        else
            echo "$dep is not installed. Installing..."
            apt install -y "$dep"
        fi
    done
    
    mkdir -m 0755 -p /etc/apt/keyrings
    rm -f /etc/apt/keyrings/teamxlink.gpg
    curl -fsSL https://dist.teamxlink.co.uk/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/teamxlink.gpg
    chmod a+r /etc/apt/keyrings/teamxlink.gpg
    echo  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/teamxlink.gpg] https://dist.teamxlink.co.uk/linux/debian/static/deb/release/ /" | tee /etc/apt/sources.list.d/teamxlink.list
    apt-get update
    if is_installed xlinkkai; then
        echo "xlinkkai is already installed. Skipping."
    else
        apt-get install -y xlinkkai
    fi
    enable_kai=true
else
    enable_kai=false
    echo "Skipping XLink Kai installation."
fi

# Download required files
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/release/CortanaWireless.py
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/release/CortanaWireless.service
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/release/CortanaWirelessRemote.service
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/release/KaiEngine.service
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/release/share_wifi.sh
mkdir /opt/CortanaWireless

# Copy service files to systemd directory
cp CortanaWireless.service CortanaWirelessRemote.service /etc/systemd/system/
cp share_wifi.sh CortanaWireless.py /opt/CortanaWireless
if [[ "$enable_kai" == true ]]; then
    cp KaiEngine.service /etc/systemd/system/
fi

# Enable and start services
systemctl enable CortanaWireless.service CortanaWirelessRemote.service
systemctl start CortanaWireless.service CortanaWirelessRemote.service
if [[ "$enable_kai" == true ]]; then
    systemctl enable KaiEngine.service
    systemctl start KaiEngine.service
fi

# Remove copied files
rm CortanaWireless.py
rm CortanaWireless.service
rm CortanaWirelessRemote.service
rm KaiEngine.service
rm share_wifi.sh

# Inform the user that the setup is complete
echo "Cortana Wireless setup complete. Services have been started and enabled."
