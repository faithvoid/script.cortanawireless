import requests
import tkinter as tk
from tkinter import simpledialog, messagebox

# Prompt user to enter Raspberry Pi IP at the start
def get_raspberry_pi_ip():
    return simpledialog.askstring("Raspberry Pi IP", "Enter the Raspberry Pi IP address:")

raspberry_pi_ip = None  # Initialize raspberry_pi_ip as None

def get_full_url():
    global raspberry_pi_ip
    return f"http://{raspberry_pi_ip}:5000"  # Automatically append http:// and :5000

def get_wifi_status():
    try:
        response = requests.get(f"{get_full_url()}/status")
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "disconnected"}

def get_connection_info():
    try:
        response = requests.get(f"{get_full_url()}/connection_info")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Unable to retrieve connection information"}

def scan_networks():
    try:
        response = requests.get(f"{get_full_url()}/scan")
        return response.json().get('networks', [])
    except requests.exceptions.RequestException:
        return []

def connect_to_network(ssid, password):
    try:
        response = requests.post(f"{get_full_url()}/connect", json={"ssid": ssid, "password": password})
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect!"}

def shutdown_system():
    try:
        response = requests.get(f"{get_full_url()}/shutdown")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to shut down!"}

def reboot_system():
    try:
        response = requests.get(f"{get_full_url()}/reboot")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to reboot!"}

def start_xlink():
    try:
        response = requests.get(f"{get_full_url()}/startxlink")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to start XLink Kai!"}

def stop_xlink():
    try:
        response = requests.get(f"{get_full_url()}/stopxlink")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to stop XLink Kai!"}

def show_connection_info():
    connection_info = get_connection_info()
    if "error" in connection_info:
        messagebox.showerror("Error", connection_info["error"])
    else:
        messagebox.showinfo(
            "Connection Status",
            f"Status: {connection_info.get('status', 'N/A')}\n"
            f"SSID: {connection_info.get('ssid', 'N/A')}\n"
            f"Signal Strength: {connection_info.get('signal_strength', 'N/A')} dBm\n"
            f"IP Address: {connection_info.get('ip_address', 'N/A')}"
        )

def connect_to_wifi():
    networks = scan_networks()
    if not networks:
        messagebox.showerror("Error", "No networks found.")
        return

    def on_network_select(event):
        selected_ssid = network_listbox.get(network_listbox.curselection())
        password = simpledialog.askstring("Password", f"Enter password for {selected_ssid}", show='*')
        if password:
            result = connect_to_network(selected_ssid, password)
            messagebox.showinfo("Connection Status", result.get("message", result.get("error", "Unknown error")))
        else:
            messagebox.showerror("Error", "Password cannot be empty.")

    # Create a new window to list networks
    network_window = tk.Toplevel()
    network_window.title("Select Network")

    tk.Label(network_window, text="Available Networks:").pack()
    network_listbox = tk.Listbox(network_window)
    network_listbox.pack(fill=tk.BOTH, expand=True)
    for network in networks:
        network_listbox.insert(tk.END, network)

    network_listbox.bind("<Double-1>", on_network_select)

def shutdown():
    result = shutdown_system()
    messagebox.showinfo("Shutdown System", result.get("message", result.get("error", "Failed to shut down!")))

def reboot():
    result = reboot_system()
    messagebox.showinfo("Reboot System", result.get("message", result.get("error", "Failed to reboot!")))

def start_xlink_kai():
    result = start_xlink()
    messagebox.showinfo("Start XLink Kai", result.get("message", result.get("error", "Failed to start XLink Kai!")))

def stop_xlink_kai():
    result = stop_xlink()
    messagebox.showinfo("Stop XLink Kai", result.get("message", result.get("error", "Failed to stop XLink Kai!")))

def main():
    global raspberry_pi_ip  # Declare raspberry_pi_ip as global variable
    
    # Prompt for Raspberry Pi IP if not already set
    if not raspberry_pi_ip:
        raspberry_pi_ip = get_raspberry_pi_ip()
        if not raspberry_pi_ip:
            messagebox.showerror("Error", "You must enter a valid Raspberry Pi IP address!")
            return  # Exit if no IP is provided
    
    root = tk.Tk()
    root.title("Cortana Wireless")

    tk.Button(root, text="Connection Status", command=show_connection_info).pack(fill=tk.X)
    tk.Button(root, text="Connect To Network", command=connect_to_wifi).pack(fill=tk.X)
    tk.Button(root, text="Start XLink Kai", command=start_xlink_kai).pack(fill=tk.X)
    tk.Button(root, text="Stop XLink Kai", command=stop_xlink_kai).pack(fill=tk.X)
    tk.Button(root, text="Shutdown Raspberry Pi", command=shutdown).pack(fill=tk.X)
    tk.Button(root, text="Restart Raspberry Pi", command=reboot).pack(fill=tk.X)
    tk.Button(root, text="Exit", command=root.quit).pack(fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
