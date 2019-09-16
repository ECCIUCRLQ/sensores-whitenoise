
import RPi.GPIO as GPIO
from SensorId import SensorId
from Tipo import Tipo

class Sensor:

	def __init__(self, sensor_id = SensorId(), tipo = Tipo.keep_alive, pin = 0):
		self.sensor_id = sensor_id
		self.tipo = tipo
		self.pin = pin

		# Configuracion GPIO
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN)

		# Agrega el evento.
		GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=300)
		GPIO.add_event_callback(self.pin, self.callback)

	def callback(self):
		if GPIO.input(self.pin):
		    print("Hay un evento")

		return 0

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


