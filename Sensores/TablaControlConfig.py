#from SensorId import SensorId

class TablaControlConfig:
    #sensor_id manejarlo como 4bytes corridos mejor y no como una referencia a objeto
    def __init__(self, sensor_id = bytes(4), paginas = [], tamano_dato = 0):
        self.sensor_id = sensor_id
        self.paginas = paginas
        self.tamano_dato = tamano_dato

    def get_sensor_id(self):
        return self.sensor_id

    def get_paginas(self):
        return self.paginas

    def get_tamano_dato(self):
        return self.tamano_dato

    def set_sensor_id(self, sensor_id):
        self.sensor_id = sensor_id

    def set_paginas(self, paginas):
        self.paginas = paginas

    def set_tamano_dato(self, tamano_dato):
        self.tamano_dato = tamano_dato

    def pagina_actual(self):
        return max(self.paginas)

    def pagina_nueva(self, pagina):
        self.paginas.append(pagina)
