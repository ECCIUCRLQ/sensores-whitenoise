#!/usr/bin/env python
import socket
import sys
import time
import sysv_ipc
import random
from CARRETA import CARRETA
from BUEY import BUEY
from Utilidades import Utilidades
from SensorId import SensorId


class Cliente:

	def __init__(self, ip_adress, port_number): #Podria recibir el path del archivo de donde lee
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_address = (ip_adress, port_number)
		self.frecuencia = 1
		self.mq = sysv_ipc.MessageQueue(2525, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)

	def enviar_paquete(self, carreta_enviar):
		dato_enviar = carreta_enviar.pack_byte_array()
		self.sock.sendto(dato_enviar, self.server_address)

	def recibir_paquete(self):
		dato_recibido, server = self.sock.recvfrom(4096)
		buey_recibido = BUEY()
		buey_recibido.unpack_byte_array(dato_recibido)
		return buey_recibido

	def send_recv_loop(self):
		# Resuelve la ambiguedad de ACK no numerado(perdida de paquetes). Figura 5.10, Pagina 275, Libro Leon Garcia.
		# Reenvia el paquete carreta hasta que reciba la confirmacion por parte de un paquete buey.
		message, type = self.mq.receive()
		carreta = CARRETA()
		carreta.unpack_byte_array(message)
		carreta.rand_id = random.getrandbits(8)
		# Envia datos todo el tiempo!
		while True:
			# Envia los datos.
			self.enviar_paquete(carreta)
			try:
				# Recibe un paquete BUEY
				buey = 	self.recibir_paquete()
				if carreta.rand_id == buey.rand_id:
					print("CLIENTE - Buey de confirmacion recibido para la carreta con rid = %s" % (carreta.rand_id))
					message, type = self.mq.receive()
					carreta = CARRETA()
					carreta.unpack_byte_array(message)
					carreta.rand_id = random.getrandbits(8)
				else:
					print("CLIENTE -  Error: Rid carreta = %s, Rid buey = %s.\n" % (carreta.rand_id, buey.rand_id))
			except socket.timeout:
				print("CLIENTE - Buey no recibido en el intervalo definido, reenviando carreta con Rid = %s.\n" % carreta.rand_id)
			time.sleep(self.frecuencia)

def iniciar_cliente():
	# Se crea un cliente que se conecta al socket(address) indicado por linea de comandos
	cliente = Cliente(sys.argv[1], (int)(sys.argv[2]))
	cliente.sock.settimeout(1)
	cliente.send_recv_loop()

iniciar_cliente()
