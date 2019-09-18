
import RPi.GPIO as GPIO
import sys
import time
import sysv_ipc

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

		# Configuracion GPIO
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN)
        
	def __repr__(self):
		return "Sensor()"

	def __str__(self):
		return "Sensor: \n\tSensor Id -> %s \n\tTipo -> %s \n\tPin -> %s" % (self.sensor_id.__str__(), self.tipo, self.pin)

	def evento(self, canal):
		#Falta archivo para persistencia.
		pre_paquete = CARRETA(0, Utilidades.get_unix_time(), self.sensor_id, self.tipo.value, 1)
		print(pre_paquete)
		self.mq.send(pre_paquete.pack_byte_array())
		
	def start_sensor(self):
		# Agrega el evento.
		GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=300)
		GPIO.add_event_callback(self.pin, self.evento)
		print("Iniciando el sensor %s de tipo %s" % (self.sensor_id, self.tipo))

	def get_tipo(self):
		return self.__tipo

	def set_tipo(self, value):
		self.__tipo = value

	def get_pin(self):
		return self.__pin

	def set_pin(self, value):
		self.__pin = value

	tipo = property(get_tipo, set_tipo)
	pin = property(get_pin, set_pin)


