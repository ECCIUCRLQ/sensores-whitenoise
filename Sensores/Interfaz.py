from AdministradorMemoria import AdministradorMemoria
from TablaControlConfig import TablaControlConfig
#from SensorId import SensorId
import sysv_ipc
from struct import *

class Interfaz:

    PAGE_SIZE = 76800
    MALLOC_MARAVILLOSO = 1
    DIR_LOGICA = 2
    WRITE = 3

    tabla_control = []
    tabla_offset = []
    mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)

    @classmethod
    def guardar(cls, dirLog, message):
        offset = cls.tabla_offset[dirLog]
        if offset >= cls.PAGE_SIZE-1:
            paginaNueva = AdministradorMemoria.malloc(tamano_dato)
            cls.tabla_control[dirLog].paginas.append(paginaNueva)
            offset = '0'
            cls.tabla_offset[dirLog] = 0
        dirFisica = str(max(cls.tabla_control[dirLog].paginas))
        direccion = dirFisica.zfill(5) + 'x' + str(offset).zfill(5)
        AdministradorMemoria.write(direccion, message)
        cls.tabla_offset[dirLog] += cls.tabla_control[dirLog].tamano_dato
        print(AdministradorMemoria.read(max(cls.tabla_control[dirLog].paginas)))

    @classmethod
    def leer(cls, dirLog):
        datos = []
        for pagina in cls.tabla_control[dirLog].paginas:
            datos.append(AdministradorMemoria.read(pagina))
        return datos

    @classmethod
    def malloc_maravilloso(cls, sensor_id, tamano_dato):
        pagina = AdministradorMemoria.malloc()
        cls.tabla_control.append(TablaControlConfig(sensor_id, [pagina], tamano_dato))
        cls.tabla_offset.append(0)
        return (len(cls.tabla_control) - 1)

    @classmethod
    def start(cls):
        try:
            while True:
                msg, tipo = cls.mq.receive()
                print("tipo: " + str(tipo))
                if tipo == cls.MALLOC_MARAVILLOSO:
                    print("Malloc!")
                    sensor_id, tamano_dato  = unpack('4sI', msg)
                    dir_logica = cls.malloc_maravilloso(sensor_id, tamano_dato)
                    cls.mq.send(pack('I', dir_logica), block = True, type = cls.DIR_LOGICA)
                
                if tipo == cls.WRITE:
                    print("Write!")
                    dir_logica, data = unpack('I' + str(len(msg) - 4) + 's', msg)
                    cls.guardar(dir_logica, data)

        except KeyboardInterrupt:
            print("\nRecolector Finalizado...")

Interfaz.start()