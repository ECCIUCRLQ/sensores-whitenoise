import socket
import sys
import time

from CARRETA import CARRETA
from BUEY import BUEY

class Servidor:

	@classmethod
	def recibir(cls):

		# Crea el socket UDP.
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Configura el puerto y la direccion donde estaran esperando datos.
		server_address = ('', 10001)
		sock.bind(server_address)

		# Archivo para guardar los datos que recibe
		file = open("DatosServidor.txt", "a")

		# Se asegura que la conexión con el cliente aún está abierta
		connected = True

		ultimo_random_id_recibido = -1

		while connected:

			# Recibe los datos (data) y la direccion desde donde se enviaron (address)
			dato_recibido, address = sock.recvfrom(4096)

			# Convierte los datos en un paquete CARRETA para generar un paquete BUEY
			carreta_recibida = CARRETA()
			carreta_recibida.unpack_byte_array(dato_recibido)


			# Cierra la conexión si en el paquete CARRETA viene la señal end_connection
			#if carreta_recibida.type == 2:
			#	connected = False

			actual_random_id_recibido = carreta_recibida.rand_id

			# Control de duplicación de paquetes.
			if ultimo_random_id_recibido != actual_random_id_recibido:

				# Escribe el dato recibido en el archivo
				print("Paquete con rid = %s escrito en el archivo." % carreta_recibida.rand_id)
				file.write("%s\n\n" % carreta_recibida.__str__())
				ultimo_random_id_recibido = actual_random_id_recibido
				
			else:
				print("Paquete con rid = %s descartado." % carreta_recibida.rand_id)
				
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