from scapy.all import ARP, Ether, srp,sr,TCP,IP

def scan_network(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    print(sr(IP(dst="192.168.1.28")/TCP(dport=19122,flags="FPU") ))        

    return devices

# Example usage
ip_range = '192.168.1.0/24'
devices = scan_network(ip_range)
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}")