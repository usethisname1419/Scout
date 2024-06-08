import socket
import random
import time
import argparse

# Define the ports to scan
ports = [21, 22, 25, 465, 587]

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to parse the proxy list from a text file
def parse_proxy_list(file_path):
    proxy_list = []
    with open(file_path, 'r') as file:
        for line in file:
            proxy = line.strip()
            proxy_list.append(proxy)
    return proxy_list

# Function to extract proxy IP and port from the proxy string
def extract_proxy_info(proxy):
    proxy_ip, proxy_port = proxy.split(':')
    return proxy_ip, int(proxy_port)

# Function to scan ports on an IP using a proxy
def scan_ports(ip, proxy_ip, proxy_port):
    print(f"Scanning ports for IP: {ip} using proxy: {proxy_ip}:{proxy_port}")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((proxy_ip, proxy_port))
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
            print(f"Error scanning port {port} on {ip} using proxy {proxy_ip}:{proxy_port}: {e}")
        finally:
            sock.close()

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Scan random IPs for open ports using proxies")
    parser.add_argument("-f", "--file", help="Path to the file containing proxy:port pairs")
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    file_path = args.file

    if not file_path:
        print("Please provide a path to the file containing proxy:port pairs.")
        return

    proxy_list = parse_proxy_list(file_path)
    if not proxy_list:
        print("Proxy list is empty or invalid.")
        return

    # Scan IPs continuously for 10 hours
    start_time = time.time()
    end_time = start_time + (10 * 60 * 60)  # 10 hours
    proxy_index = 0
    while time.time() < end_time:
        ip = generate_random_ip()
        proxy = proxy_list[proxy_index % len(proxy_list)]
        proxy_ip, proxy_port = extract_proxy_info(proxy)
        scan_ports(ip, proxy_ip, proxy_port)
        proxy_index += 1
        print("Waiting for next scan...")
        time.sleep(3)  # Wait for 1 minute between scans

if __name__ == "__main__":
    main()
