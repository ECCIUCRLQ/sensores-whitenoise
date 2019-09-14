#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
import sys

from CARRETA import CARRETA
from BUEY import BUEY

HOST = 'localhost'
PORT = 10002

class Cliente:

	def enviar_paquete(self, carreta_enviar):

		# Crea el socket UDP.
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Un segundo de timeout.
		sock.settimeout(1)

		server_address = (HOST, PORT)

		# Archivo para guardar los datos generados por el sensor.
		file = open("DatosCliente.txt", "a")

		try:
			file.write("%s\n\n" % carreta_enviar.__str__())

			haya_confirmado_buey = False
			dato_enviar = carreta_enviar.pack_byte_array()

			rid_carreta_enviada = carreta_enviar.rand_id
			buey_recibido = BUEY()
			
			# Resuelve la ambiguedad de ACK no numerado(pérdida de paquetes). Figura 5.10, Página 275, Libro León García.
			# Reenvía el paquete carreta hasta que reciba la confirmación por parte de un paquete buey.
			while not haya_confirmado_buey:
				
				# Envia los datos.
				sock.sendto(dato_enviar, server_address)
				
				try:
					# Recibe un paquete BUEY.
					dato_recibido, server = sock.recvfrom(4096)
					buey_recibido.unpack_byte_array(dato_recibido)
					rid_buey_recibido = buey_recibido.rand_id
					print(buey_recibido)	

					if rid_carreta_enviada == rid_buey_recibido:
						haya_confirmado_buey = True
					else:
						print("CLIENTE -  Error: Rid carreta = %s, Rid buey = %s.\n" % (rid_carreta_enviada, rid_buey_recibido))
						
				except socket.timeout: 
					print ("CLIENTE - Buey no recibido en el intervalo definido, reenviando carreta con Rid = %s.\n" % rid_carreta_enviada)
		finally:
			file.close()
			sock.close()