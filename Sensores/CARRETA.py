#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from struct import *
from SensorId import SensorId
from Utilidades import Utilidades
from Equipo import Equipo
from Tipo import Tipo

# Contiene la estructura del paquete CARRETA para el envío de información.
class CARRETA:

	# Constructor
	def __init__(self, rand_id = 0, date = 0, sensor_id = SensorId(), type = Tipo.keep_alive, data = 0):
		self.rand_id = rand_id
		self.date = date
		self.sensor_id = sensor_id
		self.type = type
		self.data = data

	def __repr__(self):
		return "CARRETA()"

	def __str__(self):
		utilidades = Utilidades()
		return "Paquete CARRETA: \n\trand_id -> %s \n\tdate -> %s \n\t%s \n\ttype -> %s (%s) \n\tdata -> %s\n\n" % (self.rand_id, utilidades.get_date(self.date), self.sensor_id, self.type.name, self.type.value, self.data)

	def get_rand_id(self):
		return self.__rand_id

	def set_rand_id(self, value):
		if (value < 0 or value > 255):
			raise TypeError("El valor para rand_id esta fuera del rango permitido.")
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
		if not isinstance(value, SensorId):
			raise TypeError("El tipo esperado para sensor_id es SensorId")
		self.__sensor_id =  value

	def get_type(self):
		return self.__type

	def set_type(self, value):
		if not isinstance(value, Tipo):
			raise TypeError("El tipo debe ser un enumerado Tipo")
		self.__type = value

	def get_data(self):
		return self.__data

	def set_data(self, value):
		self.__data = value

	def pack_byte_array(self):
		return pack('BIBBBBBf', self.rand_id, self.date, self.sensor_id.group_id.value, self.sensor_id.pos1, self.sensor_id.pos2, self.sensor_id.pos3, self.type.value, self.data)

	def unpack_byte_array(self, byte_array):
		datos = unpack('BIBBBBBf', byte_array)

		self.rand_id = datos[0]
		self.date = datos[1]
		self.sensor_id = SensorId([Equipo(datos[2]), datos[3], datos[4], datos[5]])
		self.type = Tipo(datos[6])
		self.data = datos[7]

	def to_string(self):
		return "%s;%s;%s;%s;%s;%s;%s;%s" % (self.rand_id, self.date, self.sensor_id.group_id.value, self.sensor_id.pos1, self.sensor_id.pos2, self.sensor_id.pos3, self.type.value, self.data)

	def from_string(self, linea):
		return 0

	rand_id = property(get_rand_id, set_rand_id)
	date = property(get_date, set_date)
	sensor_id = property(get_sensor_id, set_sensor_id)
	type = property(get_type, set_type)
	data = property(get_data, set_data)
