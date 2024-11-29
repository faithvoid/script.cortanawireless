import xbmcgui
import xbmc
import requests

# IP address of the Raspberry Pi running the Flask server
raspberry_pi_ip = "http://192.168.1.113:5000"  # Replace with your Raspberry Pi IP

def get_wifi_status():
    """Get current WiFi status from the Flask server."""
    try:
        response = requests.get("{}/status".format(raspberry_pi_ip))
        status = response.json()
        return status
    except requests.exceptions.RequestException:
        return {"status": "disconnected"}

def get_connection_info():
    """Get current WiFi connection information (SSID, Signal Strength, IP Address)."""
    try:
        response = requests.get("{}/connection_info".format(raspberry_pi_ip))
        connection_info = response.json()
        return connection_info
    except requests.exceptions.RequestException:
        return {"error": "Unable to retrieve connection information"}

def scan_networks():
    """Scan for available WiFi networks via Flask server."""
    try:
        response = requests.get("{}/scan".format(raspberry_pi_ip))
        networks = response.json()
        return networks.get('networks', [])
    except requests.exceptions.RequestException:
        return []

def connect_to_network(ssid, password):
    """Send the SSID and password to Flask server to connect."""
    try:
        response = requests.post("{}/connect".format(raspberry_pi_ip), json={"ssid": ssid, "password": password})
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect!"}

#def disconnect_from_network():
#    """Disconnect from the current WiFi network."""
#    try:
#        response = requests.get("{}/disconnect".format(raspberry_pi_ip))
#        return response.json()
#    except requests.exceptions.RequestException:
#        return {"error": "Failed to disconnect!"}

def shutdown_system():
    """Shut down the Raspberry Pi."""
    try:
        response = requests.get("{}/shutdown".format(raspberry_pi_ip))
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to shut down!"}

def reboot_system():
    """Reboot the Raspberry Pi."""
    try:
        response = requests.get("{}/reboot".format(raspberry_pi_ip))
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to reboot!"}

def start_xlink():
    """Start XLink Kai."""
    try:
        response = requests.get("{}/startxlink".format(raspberry_pi_ip))
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to start XLink Kai! Are you sure you have it installed?"}

def stop_xlink():
    """Stop XLink Kai."""
    try:
        response = requests.get("{}/stopxlink".format(raspberry_pi_ip))
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to stop XLink Kai!"}

def show_wifi_settings():
    """Main function to interact with the user for WiFi settings."""
    dialog = xbmcgui.Dialog()
    
    # Display a menu with WiFi options
    options = [
        "Connection Status",
        "Connect To Network",
#        "Disconnect From Network",
	"Start XLink Kai",
	"Stop XLink Kai",
        "Shutdown Raspberry Pi",
        "Restart Raspberry Pi"
    ]
    
    selected_option = dialog.select("Cortana Wireless", options)
    
    if selected_option == -1:
        return  # User cancelled
    
    if selected_option == 0:  # Connection Status
        connection_info = get_connection_info()  # Fetch connection details
        if "error" in connection_info:
            dialog.ok('Connection Status', connection_info["error"])
        else:
            dialog.ok(
                'Connection Status',
                '| {} | Name: {} | Signal: {} dBm | IP: {} |'.format(
                    connection_info.get('status', 'N/A'),  # Online/Offline
                    connection_info.get('ssid', 'N/A'),  # SSID of the network
                    connection_info.get('signal_strength', 'N/A'),  # Signal strength
                    connection_info.get('ip_address', 'N/A')  # IP address
                )
            )

    
    elif selected_option == 1:  # Connect to Network
        networks = scan_networks()
        if not networks:
            dialog.ok('No Networks Found', 'Unable to find any WiFi networks.')
            return
        
        # Let the user select a WiFi network
        selected_ssid_index = dialog.select('Available WiFi Network(s)', networks)
        
        if selected_ssid_index == -1:
            return  # User cancelled
        
        ssid = networks[selected_ssid_index]

        # Prompt for password using xbmc.Keyboard
        keyboard = xbmc.Keyboard('', 'Enter Password')
        keyboard.doModal()
        if keyboard.isConfirmed():
            password = keyboard.getText()
        else:
            dialog.ok('Error', 'Password entry canceled.')
            return
        
        # Connect to the selected network
        result = connect_to_network(ssid, password)
        dialog.ok('Connection Status', result.get("message", result.get("Error!", "Unknown error")))

    elif selected_option == 2:  # Start XLink Kai
        result = start_xlink()
        dialog.ok('Starting XLink Kai', result.get("", result.get("Error!", "Could not start XLink Kai! Are you sure it's installed?")))

    elif selected_option == 3:  # Stop XLink Kai
        result = stop_xlink()
        dialog.ok('Closing XLink Kai', result.get("message", result.get("Error!", "Could not start XLink Kai! Are you sure it's installed?")))

    elif selected_option == 4:  # Shutdown
        result = shutdown_system()
        dialog.ok('Shutting Down', result.get("message", result.get("Error!", "Unknown error")))

    elif selected_option == 5:  # Reboot
        result = reboot_system()
        dialog.ok('Restarting', result.get("message", result.get("Error", "Unknown error")))


if __name__ == '__main__':
    show_wifi_settings()
