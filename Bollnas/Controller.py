from typing import Union
from scapy.all import ARP, Ether, srp

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/scan")
def scan_root():
    print('----- Scanning')
    ip_range = '192.168.1.0/24'
    devices = scan_network(ip_range)
    for device in devices:
       print(f"IP: {device['ip']}, MAC: {device['mac']}")
    print('----- end')
    return {'message':'ok'}

def scan_network(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

 


