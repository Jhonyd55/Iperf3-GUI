import subprocess
import re
import matplotlib.pyplot as plt

class Iperf3Tester:
    def __init__(self, iperf3_path='iperf3/iperf3'):
        self.iperf3_path = iperf3_path

    def test_connection(self, server_ip, num_intervals=10, num_streams=1, direction='upload'):
        try:
            # Configurar el comando iperf3 según la dirección
            if direction == 'upload':
                command = [self.iperf3_path, '-c', server_ip, '-i', '1', '-t', str(num_intervals), '-P', str(num_streams)]
            elif direction == 'download':
                command = [self.iperf3_path, '-c', server_ip, '-i', '1', '-t', str(num_intervals), '-P', str(num_streams), '-R']
            else:
                raise ValueError("Dirección no válida. Use 'upload' o 'download'.")

            # Ejecutar el comando iperf3 y capturar la salida
            result = subprocess.check_output(command, universal_newlines=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error al ejecutar iperf3: {e.output}"

    def parse_result(self, result, result1):
        upload_speed = download_speed = None
        parsed_data_download,summary_data = self.parserdata(result)
        if summary_data:
            try:
                # El penúltimo par es de bajada y el último es de subida
                download_speed = (float(summary_data[-2][5]),summary_data[-2][7])
                
                
                # Manejar unidades MBytes y GBytes
                
                #if 'M' in summary_data[-2][7]:
                #    download_speed /= 1000  # Convertir Mbits/sec a Gbits/sec
                #if 'M' in summary_data[-1][7]:
                #    upload_speed /= 1000  # Convertir Mbits/sec a Gbits/sec

            except (IndexError, ValueError) as e:
                print(f"Error al procesar summary_data: {e}")
        parsed_data_upload,summary_data = self.parserdata(result1)

        # Extraer la velocidad total
        # Extraer la velocidad total de subida y bajada
        
        if summary_data:
            try:
                # El penúltimo par es de bajada y el último es de subida
                
                upload_speed = (float(summary_data[-1][5]), summary_data[-1][7])
                
                # Manejar unidades MBytes y GBytes
                
                #if 'M' in summary_data[-2][7]:
                #    download_speed /= 1000  # Convertir Mbits/sec a Gbits/sec
                #if 'M' in summary_data[-1][7]:
                #    upload_speed /= 1000  # Convertir Mbits/sec a Gbits/sec

            except (IndexError, ValueError) as e:
                print(f"Error al procesar summary_data: {e}")

        return parsed_data_download, parsed_data_upload, upload_speed, download_speed

    def parserdata(self,result):
        # Inicializar listas para los datos de intervalos y resumen
        interval_data = []
        summary_data = []

        # Dividir el resultado en líneas
        lines = result.splitlines()

        # Procesar las líneas de intervalos (de la 4 a la 13)
        for line in lines[3:-4]:
            match = re.match(
                 r'\[\s*\d+\]\s*(\d+\.\d+)-(\d+\.\d+)\s*sec\s*(\d+(\.\d+)?)\s*([KMGT]?Bytes)\s*(\d+(\.\d+)?)\s*([KMGT]?bits/sec)',  
                line
            )
            if match:
                interval_data.append(match.groups())

        # Procesar las líneas de resumen (últimas dos líneas)
        for line in lines[-4:]:
            match = re.match(
                r'\[\s*\d+\]\s*(\d+\.\d+)-(\d+\.\d+)\s*sec\s*(\d+(\.\d+)?)\s*([KMGT]?Bytes)\s*(\d+(\.\d+)?)\s*([KMGT]?bits/sec)', 
                line
            )
            if match:
                summary_data.append(match.groups())

        # Convertir los datos a un formato usable para graficar
        parsed_data = []
        for interval in interval_data:
            start_time = float(interval[0])
            end_time = float(interval[1])
            bandwidth = float(interval[5])
            if 'G' in interval[7]:
                bandwidth = bandwidth
            elif 'M' in interval[7]:
                bandwidth /= 1000
            parsed_data.append({
                'time': start_time,
                'bandwidth': bandwidth
            })

        return parsed_data, summary_data

    def plot_result(self, download_data, upload_data):
        # Crear listas para los datos de la gráfica
        #print(download_data)
        #print("------")
        #print(upload_data)
        download_times = [data['time'] for data in download_data]
        download_bandwidths = [data['bandwidth'] for data in download_data]

        # Crear la gráfica
        plt.figure(figsize=(10, 5))
        plt.plot(download_times, download_bandwidths, marker='o', color='b', linestyle='-', label='Ancho de banda de descarga')
        if upload_data:
            upload_times = [data['time'] for data in upload_data]
            upload_bandwidths = [data['bandwidth'] for data in upload_data]
            plt.plot(upload_times, upload_bandwidths, marker='o', color='r', linestyle='-', label='Ancho de banda de subida')
        
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Ancho de banda (Gbits/sec)')
        plt.title('Resultados de iperf3')
        plt.grid(True)
        plt.legend()

        # Mostrar la gráfica
        plt.show()


if __name__ == "__main__":
    # Crear una instancia de Iperf3Tester
    tester = Iperf3Tester()

    # Ejecutar una prueba de subida
    server_ip = '192.168.0.117'  # Ejemplo de IP del servidor
    num_intervals = 10  # Número de intervalos de tiempo para la prueba
    num_streams = 1  # Número de flujos simultáneos

    # Probar subida
    result_upload = tester.test_connection(server_ip, num_intervals, num_streams, direction='upload')
    #print("Resultado de subida:")
    #print(result_upload)
    
   

    # Probar bajada
    result_download = tester.test_connection(server_ip, num_intervals, num_streams, direction='download')
    #print("Resultado de bajada:")
    #print(result_download)
    parsed_data_download, parsed_data_upload, upload_speed, download_speed = tester.parse_result(result_upload,result_download)
    

    # Graficar los resultados
    tester.plot_result(parsed_data_download, parsed_data_upload)

    # Mostrar velocidades
    if upload_speed:
        print(f"Velocidad de subida: {upload_speed[0]} {upload_speed[1]}")
    if download_speed:
        print(f"Velocidad de bajada: {download_speed[0]} {download_speed[1]}")
