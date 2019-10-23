from AdministradorMemoria import AdministradorMemoria
from TablaControlConfig import TablaControlConfig
import sysv_ipc
import os
import signal
import threading
from struct import *

class Interfaz:

    PAGE_SIZE = 80
    PIPE_MAX_SIZE = 16000
    MALLOC_MARAVILLOSO = 1
    DIR_LOGICA = 2
    WRITE = 3
    READ = 4
    tabla_control = []
    tabla_offset = []

    try:
        mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREX, int("0600", 8), 2048)
    except:
        mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
        mq.remove()
        mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREX, int("0600", 8), 2048)
    pipe = 0

    @classmethod
    def init(cls):
        FIFO_PATH = "interfaz_graficador"
        if not os.path.exists(FIFO_PATH):
            os.mkfifo(FIFO_PATH)
        cls.pipe = os.open(FIFO_PATH, os.O_WRONLY)

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
    def leer(cls, dirLog):
        paginas_raw = bytearray()
        for pagina in cls.tabla_control[dirLog].paginas:
            paginas_raw += AdministradorMemoria.read(pagina)
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
                    print("Write!")
                    dir_logica, data = unpack('I' + str(len(msg) - 4) + 's', msg)
                    cls.guardar(dir_logica, data)
                if tipo == cls.READ:
                    print("Read!")
                    print(len(AdministradorMemoria.read(0)))
                    if len(AdministradorMemoria.read(0)) != 0 :
                        os.write(cls.pipe, bytes(1))
                    else:
                        os.write(cls.pipe, bytes(1))

        except KeyboardInterrupt:
            cls.mq.remove()
            #TODO: finalizar administrador de memoria
            print("\nInterfaz Finalizada...")

Interfaz.init()
Interfaz.start()
# interfaz_thread = threading.Thread(target=Interfaz.listen_recolector)
# interfaz_thread.start()
