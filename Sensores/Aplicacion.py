import time
import sys
import random
import sysv_ipc
from CARRETA import CARRETA
from BUEY import BUEY
from Utilidades import Utilidades
from SensorId import SensorId

class Aplicacion:

	def __init__(self): #Podria recibir el path del archivo de donde lee
		self.mq = sysv_ipc.MessageQueue(2424, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
	def start(self):
		while True:
			message, type = self.mq.receive()
			carreta = CARRETA()
			carreta.unpack_byte_array(message)
			print(carreta)

app = Aplicacion()
app.start()