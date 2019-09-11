import socket
import sys

from CARRETA import CARRETA
from BUEY import BUEY

class Cliente:

	def enviar_paquete(self, carreta_enviar):

		# Crea el socket UDP
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = ('localhost', 10000)

		try:
			dato_enviar = carreta_enviar.pack_byte_array()
			
			# Envia los datos
			sent = sock.sendto(dato_enviar, server_address)

			# Recibe un paquete BUEY
			dato_recibido, server = sock.recvfrom(4096)

			buey_recibido = BUEY()
			buey_recibido.unpack_byte_array(dato_recibido)

			print(buey_recibido)

		finally:
			sock.close()