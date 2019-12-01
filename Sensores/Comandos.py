import os
import getpass
import socket
import time
from struct import *

class Comandos:

    FILENAME = "/home/redes/sensores-whitenoise/Sensores/volume.bin"

    @classmethod
    def ls(cls, opciones):
        f = open(cls.FILENAME, "rb")
        contenido = bytearray(f.read())
        f.close()
        ind_metas = int.from_bytes(contenido[0:4], "big")
        if ind_metas == 8:
            print("No hay datos registrados en este volumen")
        else:
            print("ID Página  " + "Fecha y Hora de Creación  Fecha y Hora de Acceso  Tamaño de Página  " + "Dirección".ljust(10))
            i = 8
            while i < ind_metas:
                id = int.from_bytes(contenido[i:i+4], "big")
                size = int.from_bytes(contenido[i+4:i+8], "big")
                dir = int.from_bytes(contenido[i+8:i+12], "big")
                fa = int.from_bytes(contenido[dir+size:dir+size+4], "big")
                fc = int.from_bytes(contenido[dir+size+4:dir+size+8], "big")
                linea = ""
                linea += str(id).ljust(11)
                linea += time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(fc)).ljust(26)
                linea += time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(fa)).ljust(24)
                linea += str(size).ljust(18)
                linea += str(dir).ljust(10)
                print(linea)
                i += 12

    @classmethod
    def escuchar_comando(cls):
        hostname = socket.gethostname()
        path = os.getcwd()
        username = username = getpass.getuser()
        try:
            while True:
                comando = input(username+"@"+hostname+":"+path+"/Volume$ ").split()
                if len(comando) > 0:
                    if comando[0].lower() == "ls":
                        cls.ls(comando[1:])
                    else:
                        print("Comando no disponible")
        except KeyboardInterrupt:
            print("\nLínea de comandos finalizada...")

Comandos.escuchar_comando()
