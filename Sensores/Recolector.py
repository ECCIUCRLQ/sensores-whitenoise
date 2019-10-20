import time
import sys
import random
import sysv_ipc
from struct import *
from Tipo import Tipo
from CARRETA import CARRETA
from Utilidades import Utilidades
from SensorId import SensorId

class Recolector:

	mq = sysv_ipc.MessageQueue(2424, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
	log_dir = dict()

	@classmethod
	def extract_data(cls, carreta):
		date = carreta.get_date()
		type_value = carreta.get_type().value
		if type_value > 5:
			return pack('If', date, carreta.get_data())
		else:
			if type_value == 3:
				return pack('IB', date, int(carreta.get_data()))
			else:
				return pack('I', date)

	@classmethod
	def malloc_maravilloso(cls, sendor_id_value, tamano_dato): # Simula el malloc_maravilloso de la interfaz
		return 1

	@classmethod
	def start(cls):
		carreta = CARRETA()
		try:
			while True:
				data, type = cls.mq.receive()
				carreta.unpack_byte_array(data)
				sensor_id_value = carreta.sensor_id.get_single_value()

				if sensor_id_value not in cls.log_dir:
					cls.log_dir[sensor_id_value] = cls.malloc_maravilloso(sensor_id_value, 4)
					print("Nuevo Sensor Agregado: " + str(carreta.sensor_id))
				data_extracted = cls.extract_data(carreta) # Extract data to be written in memory
				# Interfaz.write(sensor_id_value, data_extracted)
		except KeyboardInterrupt:
				print ("\nRecolector Finalizado...")

Recolector.start()