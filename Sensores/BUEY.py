#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from struct import *

#Contiene la estructura del paquete BUEY para la confirmación de la recepción.
class BUEY:

	# Constructor
	def __init__(self, rand_id = 0, sensor_id = 0):
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

	def get_sensor_id(self):
		return self.__sensor_id

	def set_sensor_id(self, value):
		if not isinstance(value, int):
			raise TypeError("")
		self.__sensor_id = value

	def pack_byte_array(self):
		return pack('Bi', self.rand_id, self.sensor_id)

	def unpack_byte_array(self, byte_array):
		data = unpack('Bi', byte_array)

		self.rand_id = data[0]
		self.sensor_id = data[1]

	rand_id = property(get_rand_id, set_rand_id)
	sensor_id = property(get_sensor_id, set_sensor_id)