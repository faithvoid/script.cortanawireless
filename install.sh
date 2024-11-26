#!/bin/bash

# Ensure the script runs with superuser privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

# Function to check if a package is installed
is_installed() {
    dpkg -l | grep -qw "$1"
}

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

# Ask the user if they want to install XLink Kai
read -p "Would you like to install XLink Kai? (yes/no): " install_xlink
if [[ "$install_xlink" == "yes" ]]; then
    # Install XLink Kai dependencies and package
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
    echo  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/teamxlink.gpg] https://dist.teamxlink.co.uk/linux/debian/static/deb/release/ /" | tee /etc/apt/sources.list.d/teamxlink.list > /dev/null
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
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/CortanaWireless.py
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/CortanaWireless.service
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/CortanaWirelessRemote.service
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/KaiEngine.service
wget https://raw.githubusercontent.com/faithvoid/script.cortanawireless/refs/heads/main/share_wifi.sh

# Copy service files to systemd directory
cp CortanaWireless.service CortanaWirelessRemote.service /etc/systemd/system/
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

# Inform the user that the setup is complete
echo "Cortana Wireless setup complete. Services have been started and enabled."
