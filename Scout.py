import socket
import random
import time
import argparse

# Define the ports to scan
ports = [21, 22, 25, 465, 587]

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to scan ports on an IP using a proxy
def scan_ports(ip, proxy=None, log_file=None):
    print(f"Scanning ports for IP: {ip}")
    results = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            if proxy:
                sock.connect((proxy, 80))
            result = sock.connect_ex((ip, port))
            if result == 0:
                results.append(f"Port {port} is open on {ip}")
                try:
                    banner = sock.recv(1024).decode('utf-8').strip()
                    results.append(f"Banner for port {port} on {ip}: {banner}")
                except Exception as e:
                    results.append(f"Failed to retrieve banner for port {port} on {ip}: {e}")
            else:
                results.append(f"Port {port} is closed on {ip}")
        except Exception as e:
            results.append(f"Error scanning port {port} on {ip}: {e}")
        finally:
            sock.close()
    
    # Print status
    for result in results:
        print(result)
    
    # Log to file
    if log_file:
        try:
            with open(log_file, 'a') as f:
                f.write(f"\nResults for IP: {ip}\n")
                for result in results:
                    f.write(result + '\n')
                f.write("="*50 + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Scan random IPs for open ports")
    parser.add_argument("-p", "--proxy", help="Proxy server IP address")
    parser.add_argument("-l", "--log", help="Log file name")
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    proxy = args.proxy if args.proxy else None
    log_file = args.log if args.log else None

    # Scan IPs continuously for 10 hours
    start_time = time.time()
    end_time = start_time + (10 * 60 * 60)  # 10 hours
    while time.time() < end_time:
        ip = generate_random_ip()
        try:
            scan_ports(ip, proxy, log_file)
            print("Waiting for next scan...")
            time.sleep(3)  # Wait for 1 minute between scans
        except KeyboardInterrupt:
            print("Scan interrupted by user.")
            break
        except Exception as e:
            print(f"Error during scan: {e}")

if __name__ == "__main__":
    main()
