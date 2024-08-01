# Iperf3 GUI

Este proyecto es una interfaz gráfica (GUI) para realizar pruebas de velocidad de red utilizando `iperf3`. La GUI permite configurar el servidor, ejecutar pruebas de subida y bajada, y visualizar los resultados en gráficos.

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
    - [Clonación del Repositorio](#clonación-del-repositorio)
    - [Instalación de Dependencias](#instalación-de-dependencias)
    - [Instalación de iperf3](#instalación-de-iperf3)
        - [En Linux](#en-linux)
        - [En Windows](#en-windows)
3. [Configuración del Servidor iperf3](#configuración-del-servidor-iperf3)
    - [En Linux](#en-linux-1)
    - [En Windows](#en-windows-1)
4. [Uso del Aplicativo](#uso-del-aplicativo)
    - [Instrucciones de Uso](#instrucciones-de-uso)
5. [Agradecimientos](#agradecimientos)

## Requisitos

- Python 3.7 o superior
- iperf3

## Instalación

### Clonación del Repositorio

```sh
git clone https://github.com/tu_usuario/iperf3-gui.git
cd iperf3-gui

### Instalación de Dependencias

pip install -r requirements.txt

### Instalación de iperf3

## En Linux

## 1. Actualiza los repositorios:

sudo apt-get update

## 2. Instala iperf3:

sudo apt-get install iperf3
```
## En Windows

Descarga iperf3 desde [aquí](https://iperf.fr/).

Extrae el contenido del archivo descargado en una carpeta, por ejemplo, C:\iperf3.

### Configuración del Servidor iperf3

## En Linux

Para iniciar el servidor de iperf3 en Linux, ejecuta el siguiente comando en la terminal:

```iperf3 -s ```

### En Windows

1. Para iniciar el servidor de iperf3 en Windows:

Abre una ventana de CMD.

2. Navega a la carpeta donde está **iperf3.exe**, por ejemplo:

```cd C:\iperf3```

3. Ejecuta el siguiente comando:

```iperf3.exe -s```

### Uso del Aplicativo

1. Asegúrate de que el servidor de iperf3 esté corriendo en el equipo o servidor que va a recibir las pruebas.

2. Inicia la aplicación GUI:

3. En la interfaz de usuario:

* Introduce la IP del servidor que está escuchando en el campo Server IP.
* Especifica el tiempo deseado para tu prueba en el campo Tiempo de prueba (s).
* Haz clic en el botón Iniciar Prueba para comenzar.

4. Los resultados de las pruebas se mostrarán en el gráfico de la GUI.


### Instrucciones de Uso

Para más detalles sobre cómo utilizar el aplicativo, puedes acceder a las instrucciones directamente desde la GUI haciendo clic en el botón Instrucciones.

## Instrucciones de Uso desde la GUI

Para utilizar el aplicativo:

1. Preparación:

* Asegúrate de tener un equipo o servidor corriendo **iperf3 -s**. Esto se hace por el CMD en el equipo que escucha.

2. Configuración:

* Corre el programa en el equipo que oye.
* Introduce la IP del servidor que está escuchando en el campo Server IP.
* Especifica el tiempo deseado para tu prueba en el campo Tiempo de prueba (s).

3. Ejecutar Prueba:

* Haz clic en el botón Iniciar Prueba para comenzar.

**Nota: Puedes encontrar iperf3.exe en la carpeta iperf3 o descargarlo desde Internet.**

### Agradecimientos

Este proyecto se basa en iperf3, una herramienta de pruebas de red. Puedes encontrar más información sobre iperf3 en su sitio oficial.
