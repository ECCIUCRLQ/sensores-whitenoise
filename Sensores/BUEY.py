from struct import *
from SensorId import SensorId

#Contiene la estructura del paquete BUEY para la confirmaci�n de la recepci�n.
class BUEY:

	# Constructor
	def __init__(self, rand_id = 0, sensor_id = SensorId()):
		self.rand_id = rand_id
		self.sensor_id = sensor_id

	def __repr__(self):
	   return "BUEY()"

	def __str__(self):
	   return "Paquete BUEY: \n\trand_id -> %s \n\tsensor_id -> %s" % (self.rand_id, self.sensor_id)

	def get_rand_id(self):
		return self.__rand_id

	def set_rand_id(self, value):
		if not isinstance(value, int):
			raise TypeError("")
		self.__rand_id = value

	def pack_byte_array(self):
		return pack('BBBBB', self.rand_id, self.sensor_id.group_id, self.sensor_id.pos1, self.sensor_id.pos2, self.sensor_id.pos3)

	def unpack_byte_array(self, byte_array):
		data = unpack('BBBBB', byte_array)

		self.rand_id = data[0]
		self.sensor_id = SensorId([datos[1], datos[2], datos[3], datos[4]])

	rand_id = property(get_rand_id, set_rand_id)
	sensor_id = SensorId()