import socket
import random
import time

# Define the ports to scan
ports = [21, 22, 25, 465, 587]

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to scan ports on an IP
def scan_ports(ip):
    print(f"Scanning ports for IP: {ip}")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
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

# Scan IPs continuously for 10 hours
start_time = time.time()
end_time = start_time + (10 * 60 * 60)  # 10 hours
while time.time() < end_time:
    ip = generate_random_ip()
    scan_ports(ip)
    print("Waiting for next scan...")
    time.sleep(60)  # Wait for 1 minute between scans
