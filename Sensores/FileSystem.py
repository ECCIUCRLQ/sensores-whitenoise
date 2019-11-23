import socket
from struct import *
import time

class FileSystem:

    FILENAME = "prueba.bin"
    IND_DATOS = 0
    IND_METAS = 0

    @classmethod
    def writeData(cls, page_id, size, data):
        # Guarda el contenido de todo el archivo en un byte array
        f = open(cls.FILENAME, "rb")
        contenido = bytearray(f.read())
        f.close()

        # Agrega las fechas a los datos
        datos = pack('>'+str(size)+'sII', data, int(time.time()), int(time.time()))
        #print("Datos: ")
        #print(datos)

        # Arma la estructura de los metadatos que se van a guardar
        metadatos = pack('>III', page_id, size, cls.IND_DATOS-len(datos))

        # Se guardan los datos y metadatos en el bytearray
        contenido[cls.IND_METAS:cls.IND_METAS+12] = metadatos
        contenido[cls.IND_DATOS-size-8:cls.IND_DATOS] = datos

        # Se escribe el bytearray en el archivo
        f = open(cls.FILENAME, "wb")
        f.write(contenido)
        f.close()

        cls.IND_METAS += 12
        cls.IND_DATOS -= len(datos)
        print(contenido)

        return (cls.IND_DATOS-cls.IND_METAS)-12

    @classmethod
    def readData(cls, id):
        f = open(cls.FILENAME, "rb")
        contenido = bytearray(f.read())
        f.close()
        datos = bytearray()
        i = 0
        while i < cls.IND_METAS:
            current = int.from_bytes(contenido[i:i+4], "big")
            if(current == id):
                size = int.from_bytes(contenido[i+4:i+8], "big")
                dir = int.from_bytes(contenido[i+8:i+12], "big")
                datos = (contenido[dir:dir+size])
                contenido[dir+size:dir+size+4] = pack('I', int(time.time()))
                break
            i += 12
        return datos

    @classmethod
    def start(cls, size):
        # Llena el archivo con bytes en cero para reservar todo el espacio
        f = open("prueba.bin", "wb+")
        f.write(bytearray(size))
        f.close()

        cls.IND_METAS = 0
        cls.IND_DATOS = size

        # Hacer broadcast para ver cual nodo me recibe

        while True:
            # Recibir paquete de operacion
            op = int(input("Digite la operación: "))

            if op == 0:
                id = int(input("Digite el id: "))
                datos = input("Digite los datos: ").encode()
                print("Espacio disponible: ")
                espacio = cls.writeData(id, len(datos), datos)
                print(espacio)
            if op == 1:
                id = int(input("Digite el id: "))
                print(cls.readData(id).decode("utf-8"))
            if op > 1:
                break

FileSystem.start(1000)
