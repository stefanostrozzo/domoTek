#!/usr/bin/env python3
"""
UPnP Device Scanner migliorato
Scansione rete locale per dispositivi UPnP con parsing dettagliato
"""

import socket
import json
import re
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import List, Dict, Optional
import time
import os
from datetime import datetime

@dataclass
class UPnPDevice:
    ip: str
    port: Optional[int]
    uuid: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    device_type: Optional[str]
    services: List[Dict[str, str]]
    location_url: Optional[str]
    server_info: Optional[str]
    cache_control: Optional[int]

def parse_upnp_response(response: str) -> Dict:
    """Estrae informazioni strutturate dalla risposta UPnP"""
    headers = {
        'ip': None,
        'port': None,
        'uuid': None,
        'manufacturer': None,
        'model': None,
        'device_type': None,
        'services': [],
        'location_url': None,
        'server_info': None,
        'cache_control': None
    }

    # Estrai indirizzo e porta dalla LOCATION
    location_match = re.search(r'LOCATION:\s*(http://[^\r]+)', response, re.IGNORECASE)
    if location_match:
        headers['location_url'] = location_match.group(1)
        try:
            parsed = urlparse(location_match.group(1))
            headers['ip'] = parsed.hostname
            headers['port'] = parsed.port
        except:
            pass

    # Estrai UUID
    usn_match = re.search(r'USN:\s*uuid:([0-9a-fA-F-]+)', response, re.IGNORECASE)
    if usn_match:
        headers['uuid'] = usn_match.group(1)

    # Estrai server info
    server_match = re.search(r'SERVER:\s*([^\r]+)', response, re.IGNORECASE)
    if server_match:
        headers['server_info'] = server_match.group(1)
        # Prova a estrarre produttore e modello
        parts = re.split(r'[/\(\)]', server_match.group(1))
        if len(parts) > 0:
            headers['manufacturer'] = parts[0].strip()
        if len(parts) > 2:
            headers['model'] = parts[2].split(',')[0].strip()

    # Estrai tipo dispositivo
    st_match = re.search(r'ST:\s*([^\r]+)', response, re.IGNORECASE)
    if st_match:
        headers['device_type'] = st_match.group(1).strip()

    # Estrai cache control
    cache_match = re.search(r'CACHE-CONTROL:\s*max-age=(\d+)', response, re.IGNORECASE)
    if cache_match:
        headers['cache_control'] = int(cache_match.group(1))

    # Identifica servizi base dalla risposta
    if 'AVTransport' in response:
        headers['services'].append({'type': 'AVTransport', 'version': 1})
    if 'RenderingControl' in response:
        headers['services'].append({'type': 'RenderingControl', 'version': 1})

    return headers

def scan_upnp_network(timeout: int = 3, retries: int = 2) -> List[UPnPDevice]:
    """Scansione rete per dispositivi UPnP"""
    devices = []
    unique_devices = set()

    # Messaggio SSDP standard
    message = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST: 239.255.255.250:1900\r\n"
        "MAN: \"ssdp:discover\"\r\n"
        "MX: 2\r\n"
        "ST: upnp:rootdevice\r\n"
        "\r\n"
    ).encode()

    for _ in range(retries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.settimeout(timeout)
            
            sock.sendto(message, ("239.255.255.250", 1900))
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    data, addr = sock.recvfrom(4096)
                    response = data.decode('utf-8', errors='ignore')
                    
                    device_info = parse_upnp_response(response)
                    device_info['ip'] = device_info['ip'] or addr[0]
                    
                    # Evita duplicati usando UUID o IP:Porta
                    device_id = device_info.get('uuid') or f"{device_info['ip']}:{device_info['port']}"
                    if device_id not in unique_devices:
                        unique_devices.add(device_id)
                        devices.append(UPnPDevice(**device_info))
                        
                except socket.timeout:
                    break
                except Exception as e:
                    print(f"Errore processing response: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Errore durante la scansione: {str(e)}")
        finally:
            sock.close()
            time.sleep(0.5)  # Breve pausa tra i tentativi

    return devices

def save_to_json(devices: List[UPnPDevice], filename: str = 'upnp_scan.json'):
    """Salva i risultati in formato JSON"""
    with open(filename, 'w') as f:
        json.dump([device.__dict__ for device in devices], f, indent=2)

def main():
    import sys
    devices = scan_upnp_network()
    
    result = {
        "protocol": "upnp",
        "timestamp": datetime.now().isoformat(),
        "devices": [d.__dict__ for d in devices],
        "count": len(devices)
    }

    # Solo in modalità JSON stampa l'output pulito
    if '--json' in sys.argv:
        print(json.dumps(result))
        return

    if not devices:
        return

    print(f"Trovati {len(devices)} dispositivi")
    output_file = f"output/upnp_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f)
    print(f"Salvato in {output_file}")

if __name__ == "__main__":
    main()