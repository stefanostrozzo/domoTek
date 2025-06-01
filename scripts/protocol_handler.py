import importlib.util
import os
from datetime import datetime
import json

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
    
    # Costruisci il percorso assoluto al file dello scanner
    # Ottieni la directory dello script corrente (protocol_handler.py)
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    # Combina con il percorso relativo alla directory scanner
    scanner_script_path = os.path.join(current_script_dir, 'scanner', f"{config['module']}.py")

    # Importa il modulo dinamico usando il percorso assoluto
    spec = importlib.util.spec_from_file_location(
        config['module'],
        scanner_script_path # Usa il percorso assoluto qui
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
        json.dump([device.__dict__ for device in devices], f)

    return output_file

if __name__ == "__main__":
    import sys
    import os # Assicurati che os sia importato qui per os.path.exists o altri usi futuri se necessario
    if len(sys.argv) > 1:
        protocol_name = sys.argv[1] # Prende il nome del protocollo come primo argomento da riga di comando
        try:
            output_file_path = run_protocol_scan(protocol_name)
            print(output_file_path) # Stampa il percorso del file di output sulla console standard
        except ValueError as e:
            print(f"Errore: {e}", file=sys.stderr) # Usa sys.stderr qui
            sys.exit(1) # Esci con codice di errore
        except Exception as e:
            print(f"Errore generico durante la scansione: {e}", file=sys.stderr) # Usa sys.stderr qui
            sys.exit(1)
    else:
        print("Utilizzo: python protocol_handler.py <nome_protocollo>", file=sys.stderr) # Usa sys.stderr qui
        sys.exit(1)
