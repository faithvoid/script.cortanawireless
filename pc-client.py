import requests

raspberry_pi_ip = "http://192.168.255.255:5000"  # Replace with your Raspberry Pi IP

def get_wifi_status():
    try:
        response = requests.get(f"{raspberry_pi_ip}/status")
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "disconnected"}

def get_connection_info():
    try:
        response = requests.get(f"{raspberry_pi_ip}/connection_info")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Unable to retrieve connection information"}

def scan_networks():
    try:
        response = requests.get(f"{raspberry_pi_ip}/scan")
        return response.json().get('networks', [])
    except requests.exceptions.RequestException:
        return []

def connect_to_network(ssid, password):
    try:
        response = requests.post(f"{raspberry_pi_ip}/connect", json={"ssid": ssid, "password": password})
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect!"}

def shutdown_system():
    try:
        response = requests.get(f"{raspberry_pi_ip}/shutdown")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to shut down!"}

def reboot_system():
    try:
        response = requests.get(f"{raspberry_pi_ip}/reboot")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to reboot!"}

def start_xlink():
    try:
        response = requests.get(f"{raspberry_pi_ip}/startxlink")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to start XLink Kai!"}

def stop_xlink():
    try:
        response = requests.get(f"{raspberry_pi_ip}/stopxlink")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to stop XLink Kai!"}

def main_menu():
    while True:
        print("\nCortana Wireless Options:")
        print("1. Connection Status")
        print("2. Connect To Network")
        print("3. Start XLink Kai")
        print("4. Stop XLink Kai")
        print("5. Shutdown Raspberry Pi")
        print("6. Restart Raspberry Pi")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            connection_info = get_connection_info()
            if "error" in connection_info:
                print("Error:", connection_info["error"])
            else:
                print("Connection Status:")
                print(f"  Status: {connection_info.get('status', 'N/A')}\n  SSID: {connection_info.get('ssid', 'N/A')}\n  Signal Strength: {connection_info.get('signal_strength', 'N/A')} dBm\n  IP Address: {connection_info.get('ip_address', 'N/A')}")

        elif choice == "2":
            networks = scan_networks()
            if not networks:
                print("No networks found.")
                continue

            print("Available Networks:")
            for i, network in enumerate(networks):
                print(f"  {i + 1}. {network}")

            try:
                selected_index = int(input("Select a network: ")) - 1
                if selected_index < 0 or selected_index >= len(networks):
                    print("Invalid selection.")
                    continue

                ssid = networks[selected_index]
                password = input(f"Enter password for {ssid}: ")

                result = connect_to_network(ssid, password)
                print("Connection Status:", result.get("message", result.get("error", "Unknown error")))

            except ValueError:
                print("Invalid input.")

        elif choice == "3":
            result = start_xlink()
            print("Start XLink Kai:", result.get("message", result.get("error", "Failed to start XLink Kai!")))

        elif choice == "4":
            result = stop_xlink()
            print("Stop XLink Kai:", result.get("message", result.get("error", "Failed to stop XLink Kai!")))

        elif choice == "5":
            result = shutdown_system()
            print("Shutdown System:", result.get("message", result.get("error", "Failed to shut down!")))

        elif choice == "6":
            result = reboot_system()
            print("Reboot System:", result.get("message", result.get("error", "Failed to reboot!")))

        elif choice == "7":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
