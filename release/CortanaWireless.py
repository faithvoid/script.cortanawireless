from flask import Flask, request, jsonify
import subprocess
import os

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
#def disconnect_from_network():
#    try:
#        subprocess.call(['sudo', 'ifdown', 'wlan0'])
#        subprocess.call(['sudo', 'ifup','wlan0'])
#        return {"message": "Disconnected from current network"}
#    except Exception as e:
#        return {"error": str(e)}

# Function to shut down the Raspberry Pi

def shutdown_system():
    try:
        subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        return {"message": "Raspberry Pi is shutting down!"}
    except Exception as e:
        return {"error": str(e)}

# Function to reboot the Raspberry Pi
def reboot_system():
    try:
        subprocess.call(['sudo', 'reboot', '-h', 'now'])
        return {"message": "Raspberry Pi is rebooting!"}
    except Exception as e:
        return {"error": str(e)}

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

# Endpoint to connect to a new WiFi network
@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    ssid = data.get('ssid')
    password = data.get('password')

    if not ssid:
        return jsonify({"error": "SSID is required"}), 400

    try:
        # Update the wpa_supplicant.conf file with new network information
        config = f'network={{\n    ssid=\"{ssid}\"\n    psk=\"{password}\"\n}}'
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as file:
            file.write(config)

        # Restart WiFi service to apply new settings
        subprocess.call(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])
        subprocess.call(['sudo', 'ifdown', 'wlan0'])
        subprocess.call(['sudo', 'ifup', 'wlan0'])
        return jsonify({"message": "You're (probably) connected!"})
    except Exception as e:
        return jsonify({"error": str(e)})

## Endpoint to disconnect from the current WiFi network
#@app.route('/disconnect', methods=['GET'])
#def disconnect():
#    return jsonify(disconnect_from_network())

# Endpoint to shut down the Raspberry Pi
@app.route('/shutdown', methods=['GET'])
def shutdown():
    return jsonify(shutdown_system())

# Endpoint to reboot the Raspberry Pi
@app.route('/reboot', methods=['GET'])
def reboot():
    return jsonify(reboot_system())

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
    6. /shutdown - Shut down the Raspberry Pi.
    7. /reboot - Restart the Raspberry Pi.
    8. /xlinkstart - Start XLink Kai (if installed)
    9. /xlinkstop - Stop XLink Kai (if installed & running)
    """

if __name__ == '__main__':
    # Start the Flask web server on the Raspberry Pi (accessible from any IP)
    app.run(host='0.0.0.0', port=5000)
