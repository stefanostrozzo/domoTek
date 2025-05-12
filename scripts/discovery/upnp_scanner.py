import socket
import json
from urllib.parse import urlparse

def scan_upnp(timeout=2):
    devices = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    
    # SSDP multicast message
    message = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST: 239.255.255.250:1900\r\n"
        "MAN: \"ssdp:discover\"\r\n"
        "MX: 2\r\n"
        "ST: upnp:rootdevice\r\n\r\n"
    ).encode()

    sock.sendto(message, ("239.255.255.250", 1900))
    
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            device_ip = addr[0]
            devices.append({
                "ip": device_ip,
                "type": "upnp",
                "raw_response": data.decode()
            })
    except socket.timeout:
        return devices

if __name__ == "__main__":
    print(json.dumps(scan_upnp()))