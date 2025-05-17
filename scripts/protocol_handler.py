import importlib.util
import os
from datetime import datetime

PROTOCOLS = {
    'upnp': {
        'module': 'upnp_scanner',
        'output_dir': 'outputs/upnp'
    },
    'mqtt': {
        'module': 'mqtt_scanner',
        'output_dir': 'outputs/mqtt'
    },
    'modbus': {
        'module': 'modbus_scanner',
        'output_dir': 'outputs/modbus'
    }
}

def run_protocol_scan(protocol):
    if protocol not in PROTOCOLS:
        raise ValueError(f"Protocollo non supportato: {protocol}")

    config = PROTOCOLS[protocol]
    
    # Importa il modulo dinamico
    spec = importlib.util.spec_from_file_location(
        config['module'],
        f"scanner/{config['module']}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Esegui la scansione
    devices = module.scan()
    
    # Salva i risultati
    os.makedirs(config['output_dir'], exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{config['output_dir']}/{protocol}_scan_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(devices, f)
    
    return output_file