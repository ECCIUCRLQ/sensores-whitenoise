from AdministradorMemoria import AdministradorMemoria
from TablaControlConfig import TablaControlConfig
from SensorId import SensorId

class Intefaz:
    tabla_control = []
    tabla_offset = []
    PAGE_SIZE = 76800

    @classmethod
    def guardar(cls, dirLog, message):
        offset = str(cls.tabla_offset[dirLog])
        if offset >= PAGE_SIZE-1:
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
        pagina = AdministradorMemoria.malloc(tamano_dato)
        cls.tabla_control.append(new TablaControlConfig(sensor_id, [paginas], tamano_dato))
        cls.tabla_offset.append(0)
        return len(tabla_control)-1
