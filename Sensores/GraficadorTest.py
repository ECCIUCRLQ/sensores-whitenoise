import sysv_ipc
import time
import os

class GraficadorTest:

    READ = 4
    PIPE_MAX_SIZE = 16000
    
    try:
        mq = sysv_ipc.MessageQueue(key = 3333, flags = 0, mode =int("0600", 8),max_message_size = 2048)
    except sysv_ipc.ExistentialError:
        print("La Interfaz no ha sido inicializada!")
        exit(0)

    pipe = os.open("interfaz_graficador", os.O_RDONLY)
    @classmethod
    def start(cls):
        try:
            while(True):
                cls.mq.send(bytes(1), type = cls.READ)
                data = os.read(cls.pipe, cls.PIPE_MAX_SIZE)
                print(len(data))
                time.sleep(3)
        except KeyboardInterrupt:
            print("\nGraficador Finalizada...")

GraficadorTest.start()