import socket
import sys
import time

from CARRETA import CARRETA
from BUEY import BUEY

HOST = ''
PORT = 10000

class Servidor:

	@classmethod
	def recibir(cls):

		# Crea el socket UDP.
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Configura el puerto y la direccion donde estaran esperando datos.
		server_address = (HOST, PORT)
		sock.bind(server_address)

		# Archivo para guardar los datos que recibe.
		file = open("DatosServidor.txt", "a")

		# Se asegura que la conexión con el cliente aún está abierta.
		connected = True

		rid_ultima_carreta_procesada = -1

		while connected:

			# Recibe los datos (data) y la direccion desde donde se enviaron (address)
			dato_recibido, address = sock.recvfrom(4096)

			# Convierte los datos en un paquete CARRETA para generar un paquete BUEY
			carreta_recibida = CARRETA()
			carreta_recibida.unpack_byte_array(dato_recibido)

			# Cierra la conexión si en el paquete CARRETA viene la señal end_connection
			if carreta_recibida.type == 2:
				connected = False

			rid_carreta_recibda = carreta_recibida.rand_id

			# Resuelve la ambiguedad ACk perdido (duplicación de paquetes).Figura 5.9b, Página 275, Libro León García.
			if rid_ultima_carreta_procesada != rid_carreta_recibda:

				# Escribe el dato recibido en el archivo
				print("Rid carreta = %s escrito en el archivo." % carreta_recibida.rand_id)
				file.write("%s\n\n" % carreta_recibida.__str__())
				rid_ultima_carreta_procesada = rid_carreta_recibda
				
			else:
				print("La carreta con rid = %s, ya fue recibida anteriormente." % carreta_recibida.rand_id)
				
			buey_confirmacion = BUEY()
			buey_confirmacion.rand_id = carreta_recibida.rand_id
			buey_confirmacion.sensor_id = carreta_recibida.sensor_id

			buey_enviar = buey_confirmacion.pack_byte_array()

			if buey_enviar:
				time.sleep(5)
				sent = sock.sendto(buey_enviar, address)
				
		sock.close()
		print("Socket closed due to 'end_connection' signal, server no longer listening")
		file.close()
		print("Data file is closed")
		return