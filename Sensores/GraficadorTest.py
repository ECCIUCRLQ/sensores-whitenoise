import sysv_ipc
import time
import os
from struct import *

class GraficadorTest:

    READ = 4
    DATOS_GRAFICADOR = 5
    PIPE_MAX_SIZE = 4096

    try:
        mq = sysv_ipc.MessageQueue(key = 3333, flags = 0, mode =int("0600", 8),max_message_size = 2048)
    except sysv_ipc.ExistentialError:
        print("La Interfaz no ha sido inicializada!")
        exit(0)

    @classmethod
    def start(cls):
        try:
            while(True):
                id_grupo = bytes([int(input("Inserte ID grupo: "))])
                id_sensor = bytes([int(input("Inserte ID sensor: "))])
                cls.mq.send(pack('ssss', id_grupo, b'\x00', b'\x00',id_sensor), type = cls.READ)
                #cls.mq.send(pack('ssss', b'\x01', b'\x00', b'\x00',b'\x01'), type = cls.READ)
                msg, tipo = cls.mq.receive(block = True, type = cls.DATOS_GRAFICADOR)
                with open("datos_graficador.bin", "rb") as f:
                    sensor_data = f.read()
                print(sensor_data)

        except KeyboardInterrupt:
            print("\nGraficador Finalizado...")

GraficadorTest.start()