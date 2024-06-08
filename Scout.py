import socket
import random
import time
import argparse

# Define the ports to scan
ports = [21, 22, 25, 465, 587]

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to scan ports on an IP
def scan_ports(ip, proxy=None):
    print(f"Scanning ports for IP: {ip}")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            if proxy:
                sock.connect((proxy, 80))
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port} is open on {ip}")
                try:
                    banner = sock.recv(1024).decode('utf-8').strip()
                    print(f"Banner for port {port} on {ip}: {banner}")
                except Exception as e:
                    print(f"Failed to retrieve banner for port {port} on {ip}: {e}")
            else:
                print(f"Port {port} is closed on {ip}")
        except Exception as e:
            print(f"Error scanning port {port} on {ip}: {e}")
        finally:
            sock.close()

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Scan random IPs for open ports")
    parser.add_argument("-p", "--proxy", help="Proxy server IP address")
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    proxy = args.proxy if args.proxy else None

    # Scan IPs continuously for 10 hours
    start_time = time.time()
    end_time = start_time + (10 * 60 * 60)  # 10 hours
    while time.time() < end_time:
        ip = generate_random_ip()
        scan_ports(ip, proxy)
        print("Waiting for next scan...")
        time.sleep(60)  # Wait for 1 minute between scans

if __name__ == "__main__":
    main()
