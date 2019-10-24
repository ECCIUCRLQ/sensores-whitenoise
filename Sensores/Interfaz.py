from AdministradorMemoria import AdministradorMemoria
from TablaControlConfig import TablaControlConfig
import sysv_ipc
import os
import sys
import signal
import threading
from struct import *

class Interfaz:

    PAGE_SIZE = 80
    PIPE_MAX_SIZE = 4096
    MALLOC_MARAVILLOSO = 1
    DIR_LOGICA = 2
    WRITE = 3
    READ = 4
    DATOS_GRAFICADOR = 5
    tabla_control = []
    tabla_offset = []

    pipe = 0

    try:
        mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREX, int("0600", 8), 2048)
    except:
        mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
        mq.remove()
        mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREX, int("0600", 8), 2048)

    @classmethod
    def guardar(cls, dirLog, message):
        offset = cls.tabla_offset[dirLog]
        if offset >= cls.PAGE_SIZE-1:
            paginaNueva = AdministradorMemoria.malloc()
            cls.tabla_control[dirLog].paginas.append(paginaNueva)
            offset = '0'
            cls.tabla_offset[dirLog] = 0
        dirFisica = str(max(cls.tabla_control[dirLog].paginas))
        direccion = dirFisica.zfill(5) + 'x' + str(offset).zfill(5)
        AdministradorMemoria.write(direccion, message)
        cls.tabla_offset[dirLog] += cls.tabla_control[dirLog].tamano_dato
        #print(AdministradorMemoria.read(max(cls.tabla_control[dirLog].paginas)))

    @classmethod
    def leer(cls, sensor_id):
        print("Paginas referenciadas\n")
        index = -1
        for i in range(0, len(cls.tabla_control)):
            if cls.tabla_control[i].sensor_id == sensor_id:
                index = i
        if index == -1:
            paginas_raw = bytes(1)
            print("Ninguna")
            return paginas_raw

        mem_principal = "MemoriaPrincipal: "
        mem_secundaria = "MemoriaSecundaria: "

        for pagina in cls.tabla_control[index].paginas:
            obj_pagina = AdministradorMemoria.tabla_paginas[pagina]

            if obj_pagina.frame >= 0:
                mem_principal += obj_pagina.nombre + " "
            else:
                mem_secundaria += obj_pagina.nombre + " "

        paginas_raw = bytearray()
        for pagina in cls.tabla_control[index].paginas:
            paginas_raw += AdministradorMemoria.read(pagina)
            #print(AdministradorMemoria.tabla_paginas)

        print(mem_principal)
        print(mem_secundaria)
        return  paginas_raw

    @classmethod
    def malloc_maravilloso(cls, sensor_id, tamano_dato):
        pagina = AdministradorMemoria.malloc()
        cls.tabla_control.append(TablaControlConfig(sensor_id, [pagina], tamano_dato))
        cls.tabla_offset.append(0)
        return (len(cls.tabla_control) - 1)

    @classmethod
    def start(cls):
        print("Interfaz Inicializada!")
        try:
            while True:
                try:
                    msg, tipo = cls.mq.receive()
                except sysv_ipc.Error:
                    exit(0)
                if tipo == cls.MALLOC_MARAVILLOSO:
                    print("Malloc!")
                    sensor_id, tamano_dato  = unpack('4sI', msg)
                    dir_logica = cls.malloc_maravilloso(sensor_id, tamano_dato)
                    cls.mq.send(pack('I', dir_logica), block = True, type = cls.DIR_LOGICA)

                if tipo == cls.WRITE:
                    dir_logica, data = unpack('I' + str(len(msg) - 4) + 's', msg)
                    print("\nWrite en la página " + max(cls.tabla_control[dir_logica].paginas) + " en offset " + cls.tabla_offset[dir_logica])
                    cls.guardar(dir_logica, data)

                if tipo == cls.READ:
                    id_grupo, id_sensor = unpack('s3s', msg)
                    print("Leyendo datos de: ID grupo: " + str(int.from_bytes(id_grupo, "little")) + " ID sensor: " + str(int.from_bytes(id_sensor, "little")))
                    paginas_raw = cls.leer(msg)
                    with open("datos_graficador.bin", "wb") as f:
                        f.write(paginas_raw)
                    cls.mq.send(bytes(1), type = cls.DATOS_GRAFICADOR)

        except KeyboardInterrupt:
            cls.mq.remove()
            #TODO: finalizar administrador de memoria
            print("\nInterfaz Finalizada...")

Interfaz.start()
