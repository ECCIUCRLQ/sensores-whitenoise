import socket
from struct import *
import time
import socket
from Comunicacion import Comunicacion
from TipoComunicacion import TipoComunicacion
from TipoOperacion import TipoOperacion
from Paquete import Paquete
from PaquetesHelper import PaquetesHelper

from threading import Thread, Event

class FileSystem:

    FILENAME = "volume.bin"
    IND_DATOS = 0
    IND_METAS = 0
    keep_trying_bc = True
    hostname = socket.gethostname()
    nodo_ip = ""

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

        paquete_helper = PaquetesHelper()
        paquete = Paquete()
        paquete.operacion = TipoOperacion.Ok_KeepAlive.value
        paquete.pagina_id = page_id
        paquete.tamanno_disponible = ((cls.IND_DATOS - cls.IND_METAS) - 12)

        buffer = paquete_helper.empaquetar(TipoComunicacion.NMID, TipoOperacion.Ok_KeepAlive, paquete)

        return buffer

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
        
        paquete_helper = PaquetesHelper()
        paquete_enviar = Paquete()
        paquete_enviar.operacion = TipoOperacion.Enviar.value
        paquete_enviar.pagina_id = id
        paquete_enviar.datos_pagina = datos

        buffer = paquete_helper.empaquetar(TipoComunicacion.IDNM, TipoOperacion.Enviar, paquete_enviar)

        return buffer

    @classmethod
    def anunciarse_broadcast(cls, keep_trying_bc):
        com = Comunicacion()
        paquete_estoy_aqui = Paquete()
        paquete_helper = PaquetesHelper()

        paquete_estoy_aqui.operacion = TipoOperacion.EstoyAqui.value
        paquete_estoy_aqui.tamanno_disponible = (cls.IND_DATOS - cls.IND_METAS) - 12
        
        paquete_estoy_aqui_raw = paquete_helper.empaquetar(TipoComunicacion.IDNM, TipoOperacion.EstoyAqui, paquete_estoy_aqui)

        while cls.keep_trying_bc:
            print("Anunciadome desde: ", cls.nodo_ip)
            com.enviar_broadcast(cls.nodo_ip, com.PUERTO_BC_NMID, 1, paquete_estoy_aqui_raw)
            time.sleep(1)

    
    @classmethod
    def analizar_paquete_TCP(cls, data):
        paquete_helper = PaquetesHelper()

        paquete = paquete_helper.desempaquetar(TipoComunicacion.IDNM, data)

        tipo_operacion = TipoOperacion(paquete.operacion)

        if tipo_operacion == TipoOperacion.Guardar_QuieroSer:
            print("Se recibio pagina para guardar")
            respuesta = cls.writeData(paquete.pagina_id, paquete.tamanno_pagina, paquete.datos_pagina)
        elif tipo_operacion == TipoOperacion.Pedir_SoyActiva:
            print("Se recibio peticion de pagina")
            respuesta = cls.readData(paquete.pagina_id)
        elif tipo_operacion == TipoOperacion.Ok_KeepAlive:
            cls.keep_trying_bc = False
            respuesta = b'\x00'

        print(paquete)
        print("Enviando respuesta", str(respuesta))


        return respuesta

    @classmethod
    def start(cls, size, nodo_ip):
        # Llena el archivo con bytes en cero para reservar todo el espacio
        f = open(cls.FILENAME, "wb+")
        f.write(bytearray(size))
        f.close()

        cls.IND_METAS = 0
        cls.IND_DATOS = size
        cls.nodo_ip = nodo_ip

        # Hacer broadcast para ver cual nodo me recibe
        hilo_bc = Thread(target = cls.anunciarse_broadcast, args = (cls.keep_trying_bc, ))
        hilo_bc.start()

        com = Comunicacion()
        while True:
            # Recibir paquete de operacion
            com.recibir_paquete_tcp(cls.nodo_ip, com.PUERTO_TCP_IDNM, cls.analizar_paquete_TCP)
            
            # op = int(input("Digite la operación: "))

            # if op == 0:
            #     id = int(input("Digite el id: "))
            #     datos = input("Digite los datos: ").encode()
            #     print("Espacio disponible: ")
            #     espacio = cls.writeData(id, len(datos), datos)
            #     print(espacio)

            # if op == 1:
            #     id = int(input("Digite el id: "))
            #     print(cls.readData(id).decode("utf-8"))
            
            # if op > 1:
            #     break


FileSystem.start(1000, "192.168.86.203")