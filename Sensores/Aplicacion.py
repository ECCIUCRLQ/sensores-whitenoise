import time
import sys
import random
import sysv_ipc
from CARRETA import CARRETA
from BUEY import BUEY
from Utilidades import Utilidades
from SensorId import SensorId
from Archivos import Archivos

class Aplicacion:

	def __init__(self):
		self.mq = sysv_ipc.MessageQueue(2424, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)
	def start(self):
		try:
			while True:
				message, type = self.mq.receive()
				carreta = CARRETA()
				carreta.unpack_byte_array(message)
				Archivos.adjuntar_linea(carreta.__str__())
				print(carreta)
		except KeyboardInterrupt:
				print ("\nAplicacion Finalizada...")

app = Aplicacion()
app.start()
