#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from struct import *
from SensorId import SensorId
from Equipo import Equipo

#Contiene la estructura del paquete BUEY para la confirmación de la recepción.
class BUEY:

	# Constructor
	def __init__(self, rand_id = 0, sensor_id = SensorId()):
		self.rand_id = rand_id
		self.sensor_id = sensor_id

	def __repr__(self):
	   return "BUEY()"

	def __str__(self):
	   return "Paquete BUEY: \n\trand_id -> %s \n\t%s" % (self.rand_id, self.sensor_id)

	def get_rand_id(self):
		return self.__rand_id

	def set_rand_id(self, value):
		if (value < 0 or value > 255):
			raise TypeError("El valor para rand_id esta fuera del rango permitido.")
		self.__rand_id = value

	def get_sensor_id(self):
		return self.__sensor_id

	def set_sensor_id(self, value):
		if not isinstance(value, SensorId):
			raise TypeError("El tipo esperado para sensor_id es SensorId")
		self.__sensor_id =  value

	def pack_byte_array(self):
		return pack('BBBBB', self.rand_id, self.sensor_id.group_id.value, self.sensor_id.pos1, self.sensor_id.pos2, self.sensor_id.pos3)

	def unpack_byte_array(self, byte_array):
		data = unpack('BBBBB', byte_array)

		self.rand_id = data[0]
		self.sensor_id = SensorId([Equipo(data[1]), data[2], data[3], data[4]])

	rand_id = property(get_rand_id, set_rand_id)
	sensor_id = property(get_sensor_id, set_sensor_id)
