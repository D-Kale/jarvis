import platform
import psutil
import socket
import os

def getsysteminfo():
    return {
        "Sistema Operativo": platform.system(),
        "Versión del SO": platform.version(),
        "Arquitectura": platform.architecture()[0],
        "Procesador": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "CPU Threads": psutil.cpu_count(logical=True),
        "Memoria Total (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "Memoria Disponible (GB)": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "Dirección IP": socket.gethostbyname(socket.gethostname()),
        "Nombre del Host": socket.gethostname(),
        "Usuario Actual": os.getlogin()
    }
