import tkinter as tk
from tkinter import ttk, messagebox, Menu
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from file_json import file_json
from Iperf3Tester import Iperf3Tester

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Iperf3 GUI")

        self.server_config = file_json()
        self.iperf3_tester = Iperf3Tester()

        self.server_ip_var = tk.StringVar(value=self.server_config.server_ip)
        self.test_time_var = tk.StringVar(value="10")
        self.upload_speed_var = tk.StringVar(value="")
        self.download_speed_var = tk.StringVar(value="")

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Server IP:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.server_ip_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Actualizar IP", command=self.update_server_ip).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame, text="Tiempo de prueba (s):").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.test_time_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text="Iniciar Prueba", command=self.start_test).grid(row=2, column=0, columnspan=3, pady=10)

        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        tk.Button(frame, text="Reset", command=self.reset).grid(row=3, column=0, columnspan=3, pady=10)

        tk.Label(frame, text="Velocidad de subida:").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(frame, textvariable=self.upload_speed_var).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Velocidad de bajada:").grid(row=5, column=0, padx=5, pady=5)
        tk.Label(frame, textvariable=self.download_speed_var).grid(row=5, column=1, padx=5, pady=5)

        # Pie de página
        footer = tk.Label(self.root, text="Hecho por Jhony Durán")
        footer.pack(side=tk.BOTTOM, pady=10)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Instrucciones de uso", command=self.show_instructions)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)

    
    def show_instructions(self):
        instructions = """
        Instrucciones de Uso:

        1. Preparación:
        - Asegúrate de tener un equipo o servidor corriendo 'iperf3 -s'.
          Esto se hace por el CMD en el equipo que escucha.

        2. Configuración:
        - Corre el programa en el equipo que oye.
          Introduce la IP del servidor que está escuchando
          en el campo 'Server IP'.

        - Puedes guardar la IP del servidor para futuros test
          al presionar el botón 'actualizar IP'
        - Especifica el tiempo deseado para tu prueba en el campo 'Tiempo de
          prueba (s)'.

        3. Ejecutar Prueba:
        - Haz clic en el botón 'Iniciar Prueba' para comenzar.

        Nota: Puedes encontrar 'iperf3.exe' en la carpeta 'iperf3' o 
            descargarlo desde Internet.
            
        """

        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instrucciones de uso")

        text_widget = tk.Text(instructions_window, wrap='word', padx=10, pady=10)
        text_widget.insert('1.0', instructions)
        text_widget.config(state='disabled')
        text_widget.pack(expand=True, fill='both')

        close_button = tk.Button(instructions_window, text="Cerrar", command=instructions_window.destroy)
        close_button.pack(pady=10)

    def show_about(self):
        messagebox.showinfo("Acerca de", "Iperf3 GUI\nHecho por Jhony Durán")

    def update_server_ip(self):
        new_ip = self.server_ip_var.get()
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Actualizando IP...")
        tk.Label(progress_window, text="Actualizando la IP del servidor, por favor espere...").pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, length=300, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start()

        def update_ip():
            try:
                self.server_config.set_server_ip(new_ip)
                messagebox.showinfo("Actualización", "IP del servidor actualizada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la IP: {e}")
            finally:
                progress_bar.stop()
                progress_window.destroy()

        threading.Thread(target=update_ip).start()

    def start_test(self):
        test_time = int(self.test_time_var.get())
        server_ip = self.server_ip_var.get()
        self.initGUI()
        self.show_loading(test_time * 2 + 2)

        def run_tests():
            result_upload = self.iperf3_tester.test_connection(server_ip, num_intervals=test_time, num_streams=1, direction='upload')
            result_download = self.iperf3_tester.test_connection(server_ip, test_time, 1, direction='download')
            parsed_data_download, parsed_data_upload, upload_speed, download_speed = self.iperf3_tester.parse_result(result_upload, result_download)

            self.update_plot(parsed_data_download, parsed_data_upload)

            if upload_speed:
                self.upload_speed_var.set(f"{upload_speed[0]} {upload_speed[1]}")
            if download_speed:
                self.download_speed_var.set(f"{download_speed[0]} {download_speed[1]}")

            self.loading_window.destroy()

        threading.Thread(target=run_tests).start()

    def update_plot(self, download_data, upload_data):
        self.ax.clear()

        if download_data:
            download_times = [data['time'] for data in download_data]
            download_bandwidths = [data['bandwidth'] for data in download_data]
            self.ax.plot(download_times, download_bandwidths, marker='o', color='b', linestyle='-', label='Ancho de banda de descarga')

            for data in download_data:
                self.ax.annotate(f"{data['bandwidth']}", (data['time'], data['bandwidth']), textcoords="offset points", xytext=(0,10), ha='center')

        if upload_data:
            upload_times = [data['time'] for data in upload_data]
            upload_bandwidths = [data['bandwidth'] for data in upload_data]
            self.ax.plot(upload_times, upload_bandwidths, marker='o', color='r', linestyle='-', label='Ancho de banda de subida')

            for data in upload_data:
                self.ax.annotate(f"{data['bandwidth']}", (data['time'], data['bandwidth']), textcoords="offset points", xytext=(0,10), ha='center')

        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Ancho de banda (Gbits/sec)')
        self.ax.set_title('Resultados de iperf3')
        self.ax.grid(True)
        self.ax.legend()

        self.canvas.draw()

    def reset(self):
        self.server_ip_var.set(self.server_config.server_ip)
        self.test_time_var.set("10")
        self.upload_speed_var.set("")
        self.download_speed_var.set("")
        self.ax.clear()
        self.canvas.draw()
    
    def initGUI(self):
        self.upload_speed_var.set("")
        self.download_speed_var.set("")
        self.ax.clear()
        self.canvas.draw()

    def show_loading(self, duration):
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Ejecutando prueba...")
        tk.Label(self.loading_window, text="Ejecutando prueba, por favor espere...").pack(pady=10)
        progress = ttk.Progressbar(self.loading_window, length=300, mode='determinate')
        progress.pack(pady=10)

        def update_progress():
            for i in range(100):
                if self.loading_window and progress.winfo_exists():
                    progress['value'] += 1
                    self.loading_window.update_idletasks()
                    self.loading_window.after(int(duration * 10))

        threading.Thread(target=update_progress).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
