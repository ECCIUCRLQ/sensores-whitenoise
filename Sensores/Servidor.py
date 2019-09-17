#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
import sys
import time
from CARRETA import CARRETA
from BUEY import BUEY

class Servidor:

	def __init__(self, ip_adress, port_number): #Podria recibir el path del archivo de donde lee
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.my_address = (ip_adress, port_number)
		self.client_address = 0

	def recibir(self):
		connected = True

		rid_ultima_carreta_procesada = -1

		while connected:

			# Recibe los datos (data) y la direccion desde donde se enviaron (address)
			dato_recibido, self.client_address = self.sock.recvfrom(4096)
			# Convierte los datos en un paquete CARRETA para generar un paquete BUEY
			carreta_recibida = CARRETA()
			carreta_recibida.unpack_byte_array(dato_recibido)

			# Cierra la conexión si en el paquete CARRETA viene la señal end_connection
			#if carreta_recibida.type == 2:
			#	connected = False
			# Resuelve la ambiguedad ACk perdido (duplicación de paquetes).Figura 5.9b, Página 275, Libro León García.
			if rid_ultima_carreta_procesada != carreta_recibida.rand_id:

				# Escribe el dato recibido en el archivo
				print("SERVIDOR - Rid carreta = %s escrito en el archivo." % carreta_recibida.rand_id)
				#file.write("%s\n\n" % carreta_recibida.__str__())
				rid_ultima_carreta_procesada = carreta_recibida.rand_id
				
			else:
				print("SERVIDOR - La carreta con rid = %s, ya fue recibida anteriormente." % carreta_recibida.rand_id)
				
			buey_confirmacion = BUEY()
			buey_confirmacion.rand_id = carreta_recibida.rand_id
			buey_confirmacion.sensor_id = carreta_recibida.sensor_id

			datos_enviar = buey_confirmacion.pack_byte_array()

			if datos_enviar:
				self.sock.sendto(datos_enviar, self.client_address)
				
		self.sock.close()
		print("Socket closed due to 'end_connection' signal, server no longer listening")
		return

def iniciar_servidor():
	servidor = Servidor(sys.argv[1], (int)(sys.argv[2]));
	servidor.sock.bind(servidor.my_address)
	servidor.recibir()

iniciar_servidor()
