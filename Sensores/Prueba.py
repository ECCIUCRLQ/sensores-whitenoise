from Utilidades import Utilidades
from CARRETA import CARRETA
from SensorId import SensorId
from Tipo import Tipo
from Equipo import Equipo
import random
import time
import sys
import sysv_ipc

def main():
    mq = sysv_ipc.MessageQueue(2525, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
    try:
        while True:
            c = sys.stdin.read(1)
            if c != '\n':
                if c == '' or int(c) > 9:
                    c = '0'
                pre_paquete = CARRETA(0, Utilidades.get_unix_time(), SensorId([Equipo.whitenoise,0,0,1]), Tipo(int(c)), 1)
                print(pre_paquete)
                mq.send(pre_paquete.pack_byte_array())
    except KeyboardInterrupt:
        print("\nPrueba finalizada...")

main()
