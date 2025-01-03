import socket

def get_device_info(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return f"Hostname: {hostname}, IP Address: {ip}"
    except socket.herror:
        return f"IP Address: {ip} - Hostname could not be found"

# Example usage
ip_address = '192.168.1.1'
print(get_device_info(ip_address))