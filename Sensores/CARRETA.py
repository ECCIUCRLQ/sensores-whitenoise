from struct import *
from Utilidades import Utilidades

#Contiene la estructura del paquete CARRETA para el env�o de informaci�n.
class CARRETA:

	# Constructor
	def __init__(self, rand_id = 0, date = 0, sensor_id = 0, type = 0, data = 0):
		self.rand_id = rand_id
		self.date = date
		self.sensor_id = sensor_id
		self.type = type
		self.data = data

	def __repr__(self):
		return "CARRETA()"

	def __str__(self):
		utilidades = Utilidades()
		return "Paquete CARRETA: \n\trand_id -> %s \n\tdate -> %s \n\tsensor_id -> %s \n\ttype -> %s \n\tdata -> %s" % (self.rand_id, utilidades.get_date(self.date), self.sensor_id, self.type, self.data)

	def get_rand_id(self):
		return self.__rand_id

	def set_rand_id(self, value):
		if not isinstance(value, int):
			raise TypeError("El tipo esperado para rand_id es un numero entero")
		self.__rand_id = value

	def get_date(self):
		return self.__date

	def set_date(self, value):
		if not isinstance(value, int):
			raise TypeError("El tipo esperado para date es un numero entero")
		self.__date = value

	def get_sensor_id(self):
		return self.__sensor_id

	def set_sensor_id(self, value):
		if not isinstance(value, int):
			raise TypeError("")
		self.__sensor_id = value

	def get_type(self):
		return self.__type

	def set_type(self, value):
		if not isinstance(value, int):
			raise TypeError("")
		self.__type = value

	def get_data(self):
		return self.__data

	def set_data(self, value):
		self.__data = value

	def pack_byte_array(self):
		return pack('BiiHf', self.rand_id, self.date, self.sensor_id, self.type, self.data)

	def unpack_byte_array(self, byte_array):
		datos = unpack('BiiHf', byte_array)

		self.rand_id = datos[0]
		self.date = datos[1]
		self.sensor_id = datos[2]
		self.type = datos[3]
		self.data = datos[4]

	rand_id = property(get_rand_id, set_rand_id)
	date = property(get_date, set_date)
	sensor_id = property(get_sensor_id, set_sensor_id)
	type = property(get_type, set_type)
	data = property(get_data, set_data)
