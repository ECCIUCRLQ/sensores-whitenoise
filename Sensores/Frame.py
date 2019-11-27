import datetime

class Frame:

	def __init__(self, disponible = True, datos = [], fecha = datetime.datetime.now(), solo_lectura = False):
		self.disponible = disponible
		self.datos = bytearray()
		self.fecha_ultimo_acceso = fecha
		self.solo_lectura = False

	def get_disponible(self):
		return self.__disponible

	def set_disponible(self, value):
		self.__disponible =  value

	def get_datos(self):
		return self.__datos

	def set_datos(self, value):
		self.__datos =  value

	def get_fecha_ultimo_acceso(self):
		return self.__fecha_ultimo_acceso

	def set_fecha_ultimo_acceso(self, value):
		self.__fecha_ultimo_acceso =  value

	def get_solo_lectura(self):
		return self.__solo_lectura

	def set_solo_lectura(self, value):
		self.__solo_lectura =  value


	disponible = property(get_disponible, set_disponible)
	datos = property(get_datos, set_datos)
	fecha_ultimo_acceso = property(get_fecha_ultimo_acceso, set_fecha_ultimo_acceso)
	solo_lectura = property(get_solo_lectura, set_solo_lectura)