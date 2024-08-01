import os
import json
import subprocess

class file_json:
    def __init__(self, config_file='server_config.json'):
        self.config_file = config_file
        self.server_ip = None
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.create_default_config_file()
        self.read_config_file()

    def create_default_config_file(self):
        self.server_ip = '192.168.0.117'
        config_data = {'server_ip': self.server_ip}
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f)
        print(f"Archivo {self.config_file} creado con la IP por defecto {self.server_ip}.")

    def read_config_file(self):
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
        self.server_ip = config_data['server_ip']
        print(f"IP del servidor leída desde el archivo: {self.server_ip}")

    def modify_server_ip(self, new_ip):
        self.server_ip = new_ip
        config_data = {'server_ip': self.server_ip}
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f)
        print(f"IP del servidor modificada a: {self.server_ip}")

    def is_server_available(self):
        try:
            output = subprocess.check_output(['ping', '-c', '1', self.server_ip], universal_newlines=True)
            if "1 received" in output:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False

    def perform_iperf3_test(self):
        # Aquí se puede implementar la lógica para realizar el test de velocidad con iperf3
        pass

if __name__ == "__main__":
    client = file_json()

    if client.is_server_available():
        print(f"El servidor {client.server_ip} está disponible.")
        # Llamar al método para realizar el test de velocidad con iperf3
        client.perform_iperf3_test()
    else:
        print(f"El servidor {client.server_ip} no está disponible.")
    
    # Ejemplo de cómo modificar la IP del servidor
    ##new_ip = '192.168.0.117'
    ##client.modify_server_ip(new_ip)
