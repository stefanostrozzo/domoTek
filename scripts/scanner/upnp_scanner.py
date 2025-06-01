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
import sys
import logging

# Configura il logging su file
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\outputs', 'upnp_scan_debug.log')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

def scan(timeout: int = 3, retries: int = 2) -> List[UPnPDevice]:
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

    logging.debug(f"Avvio scansione con timeout={timeout}s, retries={retries}.")
    print(f"Debug UPnP: Avvio scansione con timeout={timeout}s, retries={retries}. (stderr)", file=sys.stderr)

    for i in range(retries):
        logging.debug(f"Tentativo {i + 1}/{retries}...")
        print(f"Debug UPnP: Tentativo {i + 1}/{retries}... (stderr)", file=sys.stderr)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.settimeout(timeout)
            
            logging.debug(f"Invio messaggio SSDP a 239.255.255.250:1900")
            print(f"Debug UPnP: Invio messaggio SSDP a 239.255.255.250:1900 (stderr)", file=sys.stderr)
            sock.sendto(message, ("239.255.255.250", 1900))
            
            start_time = time.time()
            logging.debug(f"In attesa risposte per {timeout} secondi...")
            print(f"Debug UPnP: In attesa risposte per {timeout} secondi... (stderr)", file=sys.stderr)
            while time.time() - start_time < timeout:
                try:
                    data, addr = sock.recvfrom(4096)
                    response = data.decode('utf-8', errors='ignore')
                    logging.debug(f"Ricevuta risposta raw (da {addr}):\n---\n{response[:500]}...\n---")
                    print(f"Debug UPnP: Ricevuta risposta raw (da {addr}):\n---\n{response[:500]}...\n--- (stderr)", file=sys.stderr) # Log risp raw (truncata)
                    
                    device_info = parse_upnp_response(response)
                    logging.debug(f"Info parsate: {device_info}")
                    print(f"Debug UPnP: Info parsate: {device_info} (stderr)", file=sys.stderr)

                    # Assicurati che device_info sia un dizionario valido prima di procedere
                    if not isinstance(device_info, dict):
                         logging.debug(f"parse_upnp_response non ha restituito un dizionario valido.")
                         print(f"Debug UPnP: parse_upnp_response non ha restituito un dizionario valido. (stderr)", file=sys.stderr)
                         continue # Salta questa risposta

                    device_info['ip'] = device_info.get('ip') or addr[0] # Usa .get per sicurezza
                    
                    # Evita duplicati usando UUID o IP:Porta
                    device_id = device_info.get('uuid') or (f"{device_info.get('ip')}:{device_info.get('port')}" if device_info.get('ip') else None)
                    logging.debug(f"Generato device_id: {device_id}")
                    print(f"Debug UPnP: Generato device_id: {device_id} (stderr)", file=sys.stderr)

                    if not device_id:
                        logging.debug("Dispositivo saltato - device_id vuoto.")
                        print("Debug UPnP: Dispositivo saltato - device_id vuoto. (stderr)", file=sys.stderr)
                        continue

                    if device_id not in unique_devices:
                        unique_devices.add(device_id)
                        try:
                           # Usa un dizionario filtrato per evitare KeyError con parametri mancanti in UPnPDevice
                           # Assicurati che tutti i campi richiesti da UPnPDevice siano presenti o gestiti con None
                           device_data_for_dataclass = {
                               field.name: device_info.get(field.name) for field in UPnPDevice.__dataclass_fields__
                           }
                           # Gestisci esplicitamente 'services' che potrebbe essere None se parse_upnp_response fallisce in parte
                           if device_data_for_dataclass.get('services') is None:
                               device_data_for_dataclass['services'] = []

                           devices.append(UPnPDevice(**device_data_for_dataclass))
                           logging.debug(f"Trovato dispositivo unico e aggiunto: {device_id}")
                           print(f"Debug UPnP: Trovato dispositivo unico e aggiunto: {device_id} (stderr)", file=sys.stderr)
                        except TypeError as te:
                           logging.error(f"Errore creando UPnPDevice per {device_id}: {te}. Dati: {device_info}")
                           print(f"Errore creando UPnPDevice per {device_id}: {te}. Dati: {device_info} (stderr)", file=sys.stderr)
                        
                except socket.timeout:
                    logging.debug("Timeout ricezione risposte.")
                    print("Debug UPnP: Timeout ricezione risposte. (stderr)", file=sys.stderr)
                    break
                except Exception as e:
                    logging.error(f"Errore processing response: {str(e)}")
                    print(f"Errore processing response: {str(e)} (stderr)", file=sys.stderr)
                    continue
                    
        except Exception as e:
            logging.error(f"Errore durante la scansione: {str(e)}")
            print(f"Errore durante la scansione: {str(e)} (stderr)", file=sys.stderr)
        finally:
            if 'sock' in locals() and sock:
                sock.close()
            # time.sleep(0.5)  # Breve pausa tra i tentativi (opzionale)

    logging.debug(f"Scansione completata. Trovati {len(devices)} dispositivi.")
    print(f"Debug UPnP: Scansione completata. Trovati {len(devices)} dispositivi. (stderr)", file=sys.stderr)
    return devices

def save_to_json(devices: List[UPnPDevice], filename: str = 'upnp_scan.json'):
    """Salva i risultati in formato JSON"""
    with open(filename, 'w') as f:
        json.dump([device.__dict__ for device in devices], f, indent=2)

def main():
    import sys
    devices = scan()
    
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