#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
import time
import sys
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

	def enviar_paquete(self, carreta_enviar):
		dato_enviar = carreta_enviar.pack_byte_array()
		self.sock.sendto(dato_enviar, self.server_address)

	def recibir_paquete(self):
		dato_recibido, server = self.sock.recvfrom(4096)
		buey_recibido = BUEY()
		buey_recibido.unpack_byte_array(dato_recibido)
		print(buey_recibido)
		return buey_recibido

	def send_recv_loop(self):
		# Resuelve la ambiguedad de ACK no numerado(pérdida de paquetes). Figura 5.10, Página 275, Libro León García.
		# Reenvía el paquete carreta hasta que reciba la confirmación por parte de un paquete buey.
		# ToDo: Carreta se crea con datos del archivo si hay datos si no se queda esperando
		carreta = CARRETA(random.getrandbits(8), Utilidades.get_unix_time(), SensorId([1,0,0,1]), 2, 0)
		
		# Envia datos todo el tiempo!
		while True:
			# Envia los datos.
			self.enviar_paquete(carreta)
			try:
				# Recibe un paquete BUEY
				buey = 	self.recibir_paquete()
				if carreta.rand_id == buey.rand_id:
					# ToDo: Carreta se crea con datos del archivo si hay datos si no se queda esperando
					carreta = CARRETA(random.getrandbits(8), Utilidades.get_unix_time(), SensorId([1,0,0,1]), 2, 0)
				else:
					print("CLIENTE -  Error: Rid carreta = %s, Rid buey = %s.\n" % (carreta.rand_id, buey.rand_id))	
			except socket.timeout:
				print("CLIENTE - Buey no recibido en el intervalo definido, reenviando carreta con Rid = %s.\n" % carreta.rand_id)
			time.sleep(self.frecuencia)

def iniciar_cliente():
	# Se crea un cliente que se conecta al socket(address) indicado por linea de comandos
	cliente = Cliente(sys.argv[1], (int)(sys.argv[2]))
	cliente.sock.settimeout(3)
	cliente.send_recv_loop()

iniciar_cliente()