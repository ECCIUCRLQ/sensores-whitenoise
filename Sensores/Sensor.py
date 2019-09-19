
import RPi.GPIO as GPIO
import sys
import time
import sysv_ipc
from threading import Thread

from CARRETA import CARRETA
from SensorId import SensorId
from Tipo import Tipo
from Utilidades import Utilidades

class Sensor:

	def __init__(self, sensor_id = SensorId(), tipo = Tipo.keep_alive, pin = 0):
		self.sensor_id = sensor_id
		self.tipo = tipo
		self.pin = pin
		self.mq = sysv_ipc.MessageQueue(2525, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)

		self.ka = Thread(target=self.keep_alive, args=())

		# Configuracion GPIO
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN)

	def __repr__(self):
		return "Sensor()"

	def __str__(self):
		return "Sensor: \n\tSensor Id -> %s \n\tTipo -> %s \n\tPin -> %s" % (self.sensor_id, self.tipo, self.pin)

	def evento(self, canal):
		#Falta archivo para persistencia.
		pre_paquete = CARRETA(0, Utilidades.get_unix_time(), self.sensor_id, self.tipo, 1)
		print(pre_paquete)
		self.mq.send(pre_paquete.pack_byte_array())
		
	def start_sensor(self):
		# Agrega el evento.
		GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=300)
		GPIO.add_event_callback(self.pin, self.evento)
		print("Iniciando el sensor %s de tipo %s" % (self.sensor_id, self.tipo))

		#Inicia el keep alive
		
		self.ka.start()

	def keep_alive(self):
		while(True):
			pre_paquete = CARRETA(0, Utilidades.get_unix_time(), self.sensor_id, Tipo.keep_alive, 0)
			self.mq.send(pre_paquete.pack_byte_array())
			time.sleep(60)

	def get_sensor_id(self):
		return self.__sensor_id

	def set_sensor_id(self, value):
		if not isinstance(value, SensorId):
			raise TypeError("El tipo esperado para sensor_id es SensorId")
		self.__sensor_id =  value

	def get_tipo(self):
		return self.__tipo

	def set_tipo(self, value):
		self.__tipo = value

	def get_pin(self):
		return self.__pin

	def set_pin(self, value):
		self.__pin = value

	sensor_id = property(get_sensor_id, set_sensor_id)
	tipo = property(get_tipo, set_tipo)
	pin = property(get_pin, set_pin)


