from AdministradorMemoria import AdministradorMemoria
from TablaControlConfig import TablaControlConfig
#from SensorId import SensorId
import sysv_ipc
from struct import *

class Interfaz:

    PAGE_SIZE = 76800
    MALLOC_MARAVILLOSO = 1
    DIR_LOGICA = 2

    tabla_control = []
    tabla_offset = []
    mq = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)

    @classmethod
    def guardar(cls, dirLog, message):
        offset = str(cls.tabla_offset[dirLog])
        if offset >= cls.PAGE_SIZE-1:
            paginaNueva = AdministradorMemoria.malloc(tamano_dato)
            tabla_control[dirLog].paginas.append(paginaNueva)
            offset = '0'
            cls.tabla_offset[dirLog] = 0
        dirFisica = str(max(tabla_control[dirLog].paginas))
        direccion = dirFisica.zfill(5) + 'x' + offset.zfill(5)
        AdministradorMemoria.write(direccion, message)
        cls.tabla_offset[dirLog] += cls.tabla_control[dirLog].tamano_dato

    @classmethod
    def leer(cls, dirLog):
        datos = []
        for pagina in cls.tabla_control[dirLog].paginas:
            datos.append(AdministradorMemoria.read(paginas))
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
                if tipo == cls.MALLOC_MARAVILLOSO:
                    print("Malloc!")
                    sensor_id, tamano_dato  = unpack('4sI', msg)
                    dir_logica = cls.malloc_maravilloso(sensor_id, tamano_dato)
                    cls.mq.send(pack('I', dir_logica), block = True, type = cls.DIR_LOGICA)
        except KeyboardInterrupt:
            print ("\nRecolector Finalizado...")

Interfaz.start()