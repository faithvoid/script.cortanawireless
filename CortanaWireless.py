from flask import Flask, request, jsonify
import subprocess
import os
import time
app = Flask(__name__)

# Function to get the current WiFi status (Online/Offline)
def get_wifi_status():
    try:
        result = subprocess.check_output(['iwgetid']).decode('utf-8').strip()
        if result:
            return {"status": "Online", "network": result.split('ESSID:\"')[-1].strip('\"')}
        else:
            return {"status": "Offline"}
    except subprocess.CalledProcessError:
        return {"status": "Offline"}

# Function to get detailed connection information (SSID, Signal Strength)
def get_connection_info():
    try:
        # Get the current SSID and signal strength
        result = subprocess.check_output(['iwconfig', 'wlan0']).decode('utf-8')
        ssid = None
        signal_strength = None
        
        for line in result.splitlines():
            if "ESSID" in line:
                ssid = line.split('ESSID:')[-1].strip('"')
            elif "Signal level" in line:
                signal_strength = line.split('Signal level=')[-1].split(' ')[0]
        
        return {"ssid": ssid, "signal_strength": signal_strength}
    except subprocess.CalledProcessError:
        return {"error": "Unable to retrieve connection information"}

# Function to disconnect from the current WiFi network
def disconnect_from_network():
    try:
        subprocess.call(['sudo', 'ifconfig', 'wlan0', 'down'])
        subprocess.call(['sudo', 'ifconfig', 'wlan0', 'up'])
        return {"message": "Disconnected from current network"}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to get the WiFi status (Online/Offline)
@app.route('/status', methods=['GET'])
def status():
    return jsonify(get_wifi_status())

# Endpoint to get connection information (SSID and signal strength)
@app.route('/connection_info', methods=['GET'])
def connection_info():
    return jsonify(get_connection_info())

# Endpoint to scan for available WiFi networks
@app.route('/scan', methods=['GET'])
def scan():
    try:
        networks = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan']).decode('utf-8')
        ssid_list = []
        for line in networks.split('\n'):
            if "ESSID:" in line:
                ssid = line.split('ESSID:')[-1].strip('\"')
                if ssid:
                    ssid_list.append(ssid)
        return jsonify({"networks": ssid_list})
    except Exception as e:
        return jsonify({"error": str(e)})


def connect():
    data = request.json
    ssid = data.get('ssid')
    password = data.get('password')

    if not ssid:
        return jsonify({"error": "SSID is required"}), 400

    try:
        # Disconnect from any current network (forcefully)
        os.system("nmcli device disconnect wlan0")

        # Clear any existing DHCP lease
        os.system("sudo dhclient -r wlan0")

        # Add a short delay to ensure the Wi-Fi interface is free to reset
        time.sleep(2)

        # Clear out the old network configuration from wpa_supplicant
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as file:
            lines = file.readlines()
        # Remove all existing network configurations (ensure it's clear for the new connection)
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as file:
            file.writelines([line for line in lines if "network=" not in line])

        # Update the wpa_supplicant.conf file with new network information
        config = f'network={{\n    ssid=\"{ssid}\"\n    psk=\"{password}\"\n}}'
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as file:
            file.write(config)

        # Restart the Wi-Fi interface
        os.system("sudo ifdown wlan0")
        time.sleep(1)
        os.system("sudo ifup wlan0")

        # Request a new DHCP lease (if required)
        os.system("sudo dhclient wlan0")

        # Ensure the interface reconnects properly
        result = os.popen(f"nmcli dev wifi connect '{ssid}' password '{password}'").read()

        # Log connection attempt for debugging
        with open("/tmp/wifi_log.txt", "a") as log:
            log.write(f"Attempted connection to SSID: {ssid}\n")
            log.write(result + "\n")

        return jsonify({"message": "Connection attempt in progress"})

    except Exception as e:
        # Log error for debugging
        with open("/tmp/wifi_log.txt", "a") as log:
            log.write(f"Connection error: {str(e)}\n")
        return jsonify({"error": str(e)})

# Endpoint to disconnect from the current WiFi network
@app.route('/disconnect', methods=['GET'])
def disconnect():
    return jsonify(disconnect_from_network())

# Bluetooth scanning function
def scan_bluetooth_devices():
    """Scan for nearby Bluetooth devices."""
    try:
        # Enable Bluetooth power
#        subprocess.call(['timeout', '5s', 'bluetoothctl', 'power', 'on'])
#        time.sleep(1)

        # Start scanning for devices for 5 seconds
        subprocess.call(['timeout', '10s', 'bluetoothctl', 'scan', 'on'])
        
        # Wait for 5 seconds while the scan happens
        time.sleep(5)
        
        # Stop scanning after the timeout
        subprocess.call(['bluetoothctl', 'scan', 'off'])

        # Now, let's collect the list of discovered devices
        devices = subprocess.check_output(['bluetoothctl', 'devices']).decode('utf-8')

        # Parse out the devices from the output
        device_list = []
        for line in devices.splitlines():
            if "Device" in line:
                # Extract the MAC address and device name
                parts = line.split(' ')
                mac_address = parts[1]  # The MAC address is the second part
                device_name = ' '.join(parts[2:])  # The rest is the device name
                device_list.append({'mac_address': mac_address, 'device_name': device_name})

        return {"devices": device_list}
    except subprocess.CalledProcessError as e:
        return {"error": "Bluetooth scan failed: {}".format(str(e))}
    except Exception as e:
        return {"error": "An error occurred during Bluetooth scanning: {}".format(str(e))}

# Bluetooth connection function
def connect_bluetooth_device(mac_address):
    """Connect to a Bluetooth device by MAC address."""
    try:
        # Verify the device is in the available list
        devices = subprocess.check_output(['bluetoothctl', 'devices']).decode('utf-8')
        if mac_address not in devices:
            return {"error": f"Device {mac_address} not available in the device list."}

        # Start discovery to ensure the device is visible
        subprocess.call(['bluetoothctl', 'discoverable', 'on'])
        time.sleep(1)

        # Attempt to connect to the device
        result = subprocess.check_output(['bluetoothctl', 'connect', mac_address]).decode('utf-8')

        if "Connection successful" in result:
            return {"message": f"Connected to {mac_address}"}
        else:
            return {"error": f"Failed to connect to {mac_address}: {result.strip()}"}
        
    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to connect to {mac_address}: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred while connecting to Bluetooth device: {str(e)}"}

@app.route('/bluetooth_scan', methods=['GET'])
def bluetooth_scan():
    return jsonify(scan_bluetooth_devices())

@app.route('/connect_bluetooth', methods=['POST'])
def connect_bluetooth():
    data = request.json
    mac_address = data.get('mac_address')

    if not mac_address:
        return jsonify({"error": "MAC Address is required"}), 400

    return jsonify(connect_bluetooth_device(mac_address))

# XLink section

# Function to start XLink Kai
def start_xlink():
    try:
        subprocess.call(['sudo', 'kaiengine'])
        return {"message": "Starting XLink Kai!"}
    except Exception as e:
        return {"error": str(e)}

# Function to stop XLink Kai
def stop_xlink():
    try:
        subprocess.call(['sudo', 'killall', 'kaiengine'])
        return {"message": "Closing XLink Kai!"}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to start XLink Kai
@app.route('/startxlink', methods=['GET'])
def startxlink():
    return jsonify(start_xlink())

# Endpoint to stop XLink Kai
@app.route('/stopxlink', methods=['GET'])
def stopxlink():
    return jsonify(stop_xlink())

# Default route for home page
@app.route('/', methods=['GET'])
def home():
    return """
    Welcome to the Raspberry Pi WiFi Manager API. Choose an option:
    1. /status - Get Connection Status (Online/Offline)
    2. /connection_info - Get Connection Information (SSID, Signal Strength)
    3. /scan - Scan for available WiFi Networks
    4. /connect - Connect to a new WiFi Network (POST with SSID and Password)
    5. /disconnect - Disconnect from current WiFi Network
    6. /bluetooth_scan - Scan for Bluetooth Devices
    7. /connect_bluetooth - Connect to a Bluetooth Device (POST with MAC Address)
    """

if __name__ == '__main__':
    # Start the Flask web server on the Raspberry Pi (accessible from any IP)
    app.run(host='0.0.0.0', port=5000)
