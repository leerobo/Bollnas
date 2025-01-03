import ipaddress

def get_network_info(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        network = ipaddress.ip_network(ip + '/24', strict=False)
        return f"IP Address: {ip}, Network: {network}"
    except ValueError:
        return f"Invalid IP Address: {ip}"

# Example usage
ip_address = '192.168.1.28'
print(get_network_info(ip_address))