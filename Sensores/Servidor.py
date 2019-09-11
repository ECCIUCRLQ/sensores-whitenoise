import socket
import sys

from CARRETA import CARRETA
from BUEY import BUEY

class Servidor:

	@classmethod
	def recibir():

		# Crea el socket UDP.
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Configura el puerto y la direccion donde estaran esperando datos.
		server_address = ('localhost', 5050)
		sock.bind(server_address)

		while True:
			# Recibe los datos (data) y la direccion desde donde se enviaron (address)
			dato_recibido, address = sock.recvfrom(4096)

			# Convierte los datos en un paquete CARRETA para generar un paquete BUEY
			carreta_recibida = CARRETA()
			carreta_recibida.unpack_byte_array(dato_recibido)

			buey_confirmacion = BUEY()
			buey_confirmacion.rand_id = carreta_recibida.rand_id
			buey_confirmacion.sensor_id = carreta_recibida.sensor_id

			buey_enviar = buey_confirmacion.pack_byte_array();

			if buey_enviar:
				sent = sock.sendto(buey_enviar, address)

		return