import os
import time
import urllib2
import socket
import xbmc
import xbmcgui

# Define custom headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

# Function to test download speed
def test_download_speed(dialog):
    url = "https://github.com/BitDoctor/speed-test-file/raw/refs/heads/master/10mb.txt"  # Test file
    request = urllib2.Request(url, headers=HEADERS)
    
    # Open request
    response = urllib2.urlopen(request, timeout=10)
    file_size = int(response.headers['Content-Length'])  # File size in bytes
    block_size = 4096 * 1024  # Read in 4MB chunks - Reduce this to "2096 (2MB)" if you experience memory issues.
    downloaded_size = 0
    start_time = time.time()

    # Read data in chunks to simulate real-time download and update progress
    while True:
        chunk = response.read(block_size)
        if not chunk:
            break

        downloaded_size += len(chunk)
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            speed_kbps = (downloaded_size / elapsed_time) / 1024  # Convert to Kbps
            progress = int((downloaded_size / float(file_size)) * 100)
            dialog.update(progress, 
                          "Testing Speed...",
                          "Speed: {:.2f} Kbps".format(speed_kbps),
                          "Progress: {}%".format(progress))
    
        if dialog.iscanceled():
            return None  # Allow user to cancel

    # Calculate final download speed in Mbps
    end_time = time.time()
    total_time = end_time - start_time
    download_speed_mbps = (file_size * 8) / (total_time * 1024 * 1024)  # Convert to Mbps

    return download_speed_mbps

def test_ping(dialog):
    dialog.update(0, "Ping Test", "Please wait, calculating ping...")

    target = "8.8.8.8"  # Google DNS
    port = 53  # Use port 53 for DNS
    timeout = 2  # Timeout for each ping
    ping_times = []  # Store individual ping times
    start_time = time.time()

    while time.time() - start_time < 30:  # Run for 3 seconds
        try:
            # Start the timer for this ping
            ping_start = time.time()

            # Test connection
            socket.create_connection((target, port), timeout=timeout)

            # Calculate the ping time
            ping_end = time.time()
            ping = (ping_end - ping_start) * 1000  # Convert to ms
            ping_times.append(ping)

            # Update dialog with current status
            elapsed = time.time() - start_time
            ping_number = int(elapsed) + 1  # Convert elapsed to an integer and use it as the Ping #
            dialog.update(
                int((elapsed / 30) * 100),  # Progress percentage
                "Testing Ping...",
                "Current Ping: {:.2f} ms".format(ping),
                "Ping #: {} / 30".format(ping_number)
            )

        except socket.error:
            # Log failure as None (optional: add a placeholder value like 0)
            ping_times.append(None)

        time.sleep(1)  # Wait 1 second between pings

    # Calculate the average ping time (ignoring failed pings)
    successful_pings = [p for p in ping_times if p is not None]
    average_ping = sum(successful_pings) / len(successful_pings) if successful_pings else None

    # Update dialog with the final result
    if average_ping is not None:
        dialog.update(100, "Ping Test Complete", "Average Ping: {:.2f} ms".format(average_ping))
    else:
        dialog.update(100, "Ping Test Failed", "No successful pings.")

    time.sleep(1)  # Brief pause to allow user to see the update
    return average_ping

# Main function to run the speed test
def run_speed_test():
    dialog = xbmcgui.DialogProgress()
    dialog.create("Speed Test", "Starting the speed test, just a moment...")

    try:
        # Test download speed
        download_speed = test_download_speed(dialog)
        if download_speed is None:
            dialog.close()
            xbmcgui.Dialog().ok("Speed Test Cancelled", "The speed test was cancelled.")
            return

        # Test ping
        ping = test_ping(dialog)

        # Format results
        download_speed_text = "Download Speed: {:.2f} Mbps".format(download_speed)
        ping_text = "Ping: {:.2f} ms".format(ping if ping is not None else 0)

        # Show final results
        dialog.close()
        xbmcgui.Dialog().ok("Speed Test Results", download_speed_text, ping_text)

    finally:
        dialog.close()

if __name__ == '__main__':
    run_speed_test()
