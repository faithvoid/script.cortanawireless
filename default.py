import xbmcgui
import xbmc
import requests

# IP address of the Raspberry Pi running the Flask server
raspberry_pi_ip = "http://192.168.137.1:5000"  # Replace with your Raspberry Pi IP

# Shared secret password, make sure to change this to something unique!
SHARED_SECRET = "C0RT4N4"

def get_headers():
    """Return headers including the authorization password."""
    return {"Authorization": SHARED_SECRET}

def get_wifi_status():
    """Get current WiFi status from the Flask server."""
    try:
        response = requests.get("{}/status".format(raspberry_pi_ip), headers=get_headers())
        status = response.json()
        return status
    except requests.exceptions.RequestException:
        return {"status": "disconnected"}

def get_connection_info():
    """Get current WiFi connection information (SSID, Signal Strength, IP Address)."""
    try:
        response = requests.get("{}/connection_info".format(raspberry_pi_ip), headers=get_headers())
        connection_info = response.json()
        return connection_info
    except requests.exceptions.RequestException:
        return {"error": "Unable to retrieve connection information"}

def scan_networks():
    """Scan for available WiFi networks via Flask server."""
    try:
        response = requests.get("{}/scan".format(raspberry_pi_ip), headers=get_headers())
        networks = response.json()
        return networks.get('networks', [])
    except requests.exceptions.RequestException:
        return []

def connect_to_network(ssid, password):
    """Send the SSID and password to Flask server to connect."""
    try:
        response = requests.post("{}/connect".format(raspberry_pi_ip), json={"ssid": ssid, "password": password}, headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect!"}

def scan_bluetooth_devices():
    """Scan for available Bluetooth devices via Flask server."""
    try:
        response = requests.get("{}/bluetooth_scan".format(raspberry_pi_ip), headers=get_headers())
        devices = response.json()
        return devices.get('devices', [])
    except requests.exceptions.RequestException:
        return []

def connect_to_bluetooth_device(mac_address):
    """Connect to a Bluetooth device by MAC address via Flask server."""
    try:
        response = requests.post("{}/connect_bluetooth".format(raspberry_pi_ip), json={"mac_address": mac_address}, headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect!"}

def shutdown_system():
    """Shut down the Raspberry Pi."""
    try:
        response = requests.get("{}/shutdown".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to shut down!"}

def reboot_system():
    """Reboot the Raspberry Pi."""
    try:
        response = requests.get("{}/reboot".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to reboot!"}

def start_xlinkkai():
    """Start XLink Kai."""
    try:
        response = requests.get("{}/startxlinkkai".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to start XLink Kai! Are you sure you have it installed?"}

def stop_xlinkkai():
    """Stop XLink Kai."""
    try:
        response = requests.get("{}/stopxlinkkai".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to stop XLink Kai!"}

def enable_xlinkkai():
    """Enable XLink Kai."""
    try:
        response = requests.get("{}/enablexlinkkai".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to enable XLink Kai! Are you sure you have it installed?"}

def disable_xlinkkai():
    """Disable XLink Kai."""
    try:
        response = requests.get("{}/disablexlinkkai".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to disable XLink Kai!"}

def start_insigniadns():
    """Start insigniaDNS."""
    try:
        response = requests.get("{}/startinsigniadns".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to start insigniaDNS! Are you sure you have it installed?"}

def stop_insigniadns():
    """Stop insigniaDNS."""
    try:
        response = requests.get("{}/stopinsigniadns".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to stop insigniaDNS!"}

def enable_insigniadns():
    """Start insigniaDNS."""
    try:
        response = requests.get("{}/enableinsigniadns".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to enable insigniaDNS! Are you sure you have it installed?"}

def disable_insigniadns():
    """Stop insigniaDNS."""
    try:
        response = requests.get("{}/disableinsigniadns".format(raspberry_pi_ip), headers=get_headers())
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to disable insigniaDNS!"}


def show_wifi_settings():
    """Main function to interact with the user for WiFi settings."""
    dialog = xbmcgui.Dialog()
    
    main_menu = [
        "Wireless Settings",
        "Bluetooth Settings",
        "insigniaDNS",
	"XLink Kai",
        "Power Options"
    ]
    
    wifi_options = [
        "Connection Status",
        "Connect To Network"
    ]
    
    bluetooth_options = [
        "Connect To Bluetooth Device"
    ]
    
    xlinkkai_options = [
        "Start XLink Kai",
        "Stop XLink Kai",
	"Enable XLink Kai",
	"Disable XLink Kai"
    ]
    
    insigniadns_options = [
        "Start insigniaDNS",
        "Stop insigniaDNS",
	"Enable insigniaDNS",
	"Disable insigniaDNS"
    ]
    
    power_options = [
        "Shutdown Raspberry Pi",
        "Restart Raspberry Pi"
    ]
    
    menu_stack = [main_menu]
    
    while menu_stack:
        current_menu = menu_stack[-1]
        selected_option = dialog.select("Cortana Wireless", current_menu)
        
        if selected_option == -1:
            menu_stack.pop()
            continue
        
        if current_menu == main_menu:
            if selected_option == 0:
                menu_stack.append(wifi_options)
            elif selected_option == 1:
                menu_stack.append(bluetooth_options)
            elif selected_option == 2:
                menu_stack.append(insigniadns_options)
            elif selected_option == 3:
                menu_stack.append(xlinkkai_options)
            elif selected_option == 4:
                menu_stack.append(power_options)
        
        elif current_menu == wifi_options:
            if selected_option == 0:  # Connection Status
                connection_info = get_connection_info()  # Fetch connection details
                if "error" in connection_info:
                    dialog.ok('Connection Status', connection_info["error"])
                else:
                    dialog.ok(
                            connection_info.get('status', 'N/A'),  # Online/Offline
                        'Name: {}| Signal: {} dBm | IP: {} '.format(
                            connection_info.get('ssid', 'N/A'),  # SSID of the network
                            connection_info.get('signal_strength', 'N/A'),  # Signal strength
                            connection_info.get('ip_address', 'N/A')  # IP address
                        )
                    )

            elif selected_option == 1:  # Connect to Network
                networks = scan_networks()
                if not networks:
                    dialog.ok('No Networks Found', 'Unable to find any WiFi networks.')
                    continue
                
                # Let the user select a WiFi network
                selected_ssid_index = dialog.select('Available WiFi Network(s)', networks)
                
                if selected_ssid_index == -1:
                    continue  # User cancelled
                
                ssid = networks[selected_ssid_index]

                # Prompt for password using xbmc.Keyboard
                keyboard = xbmc.Keyboard('', 'Enter Password')
                keyboard.doModal()
                if keyboard.isConfirmed():
                    password = keyboard.getText()
                else:
                    dialog.ok('Error', 'Password entry canceled.')
                    continue
                
                # Connect to the selected network
                result = connect_to_network(ssid, password)
                dialog.ok('Connection Status', result.get("message", result.get("Error!", "Unknown error")))

        elif current_menu == bluetooth_options:
            if selected_option == 0:  # Connect to Bluetooth Device
                devices = scan_bluetooth_devices()
                if not devices:
                    dialog.ok('No Bluetooth Devices Found', 'Unable to find any Bluetooth devices.')
                    continue
                
                # Format device names and display in the dialog (using str.format for Python 2.7 compatibility)
                device_names = ["{} ({})".format(device['device_name'], device['mac_address']) for device in devices]
                selected_device_index = dialog.select('Available Bluetooth Devices', device_names)
                
                if selected_device_index == -1:
                    continue  # User cancelled
                
                # Get the mac_address directly from the selected device (no need for split)
                mac_address = devices[selected_device_index]['mac_address']
                
                result = connect_to_bluetooth_device(mac_address)
                dialog.ok('Bluetooth Connection Status', result.get("message", result.get("error", "Unknown error")))

        elif current_menu == xlinkkai_options:
            if selected_option == 0:  # Start XLink Kai
                result = start_xlinkkai()
                dialog.ok('Starting XLink Kai', result.get("message", result.get("Error!", "Could not start XLink Kai! Are you sure it's installed?")))

            elif selected_option == 1:  # Stop XLink Kai
                result = stop_xlinkkai()
                dialog.ok('Stop XLink Kai', result.get("message", result.get("Error!", "Could not stop XLink Kai! Are you sure it's installed?")))

            elif selected_option == 2:  # Enable XLink Kai
                result = enable_xlinkkai()
                dialog.ok('Enabling XLink Kai', result.get("message", result.get("Error!", "Could not enable XLink Kai! Are you sure it's installed?")))

            elif selected_option == 3:  # Disable XLink Kai
                result = disable_xlinkkai()
                dialog.ok('Disabling XLink Kai', result.get("message", result.get("Error!", "Could not disable XLink Kai! Are you sure it's installed?")))

        elif current_menu == insigniadns_options:
            if selected_option == 0:  # Start insigniaDNS
                result = start_insigniadns()
                dialog.ok('Starting insigniaDNS', result.get("message", result.get("Error!", "Could not start insigniaDNS! Are you sure it's installed?")))

            elif selected_option == 1:  # Stop insigniaDNS
                result = stop_insigniadns()
                dialog.ok('Stop insigniaDNS', result.get("message", result.get("Error!", "Could not stop insigniaDNS! Are you sure it's installed?")))

            elif selected_option == 2:  # Enable insigniaDNS
                result = enable_insigniadns()
                dialog.ok('Enabling insigniaDNS', result.get("message", result.get("Error!", "Could not enable insigniaDNS! Are you sure it's installed?")))

            elif selected_option == 3:  # Disable insigniaDNS
                result = disable_insigniadns()
                dialog.ok('Disabling insigniaDNS', result.get("message", result.get("Error!", "Could not disable insigniaDNS! Are you sure it's installed?")))

        elif current_menu == power_options:
            if selected_option == 0:  # Shutdown
                result = shutdown_system()
                dialog.ok('Shutting Down', result.get("message", result.get("Error!", "Unknown error")))

            elif selected_option == 1:  # Reboot
                result = reboot_system()
                dialog.ok('Restarting', result.get("message", result.get("Error", "Unknown error")))

if __name__ == '__main__':
    show_wifi_settings()
