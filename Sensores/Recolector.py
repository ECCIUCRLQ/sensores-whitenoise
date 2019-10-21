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

	MALLOC_MARAVILLOSO = 1
	DIR_LOGICA = 2
	WRITE = 3

	mq_Server = sysv_ipc.MessageQueue(2424, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
	mq_Interfaz = sysv_ipc.MessageQueue(3333, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
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
	def start(cls):
		carreta = CARRETA()
		try:
			while True:
				data, tipo = cls.mq_Server.receive()
				carreta.unpack_byte_array(data)
				sensor_id_value = carreta.sensor_id.get_single_value()

				data_extracted = cls.extract_data(carreta) # Extract data to be written in memory

				if sensor_id_value not in cls.log_dir:
					# Llamado por medio de la cola a Interfaz.malloc_maravilloso()
					cls.mq_Interfaz.send(pack("4sI", sensor_id_value, len(data_extracted)), block = True, type = cls.MALLOC_MARAVILLOSO) # Ejecuta Interfaz.malloc() en la interfaz
					cls.log_dir[sensor_id_value], tipo =  cls.mq_Interfaz.receive( block = True, type = cls.DIR_LOGICA)# Devuelve el resultado del Interfaz.Malloc()
					print("Nuevo Sensor Agregado: " + str(carreta.sensor_id) + ", Dir_Logica: " + str(int.from_bytes(cls.log_dir[sensor_id_value], "little")))
				
				cls.mq_Interfaz.send(pack("4s" + str(len(data_extracted)) + "s", cls.log_dir[sensor_id_value], data_extracted), block = True, type = cls.WRITE)
		except KeyboardInterrupt:
				print("\nRecolector Finalizado...")

Recolector.start()