import socket
import sys

from CARRETA import CARRETA
from BUEY import BUEY

class Cliente:

	def enviar_paquete(self, carreta_enviar):

		# Crea el socket UDP
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Timeout un segundo
		sock.settimeout(1)

		server_address = ('localhost', 10000)

		# Archivo para guardar los datos generados por el sensor
		file = open("DatosCliente.txt", "a")

		try:
			file.write("%s\n\n" % carreta_enviar.__str__())

			paquete_confirmado = False
			dato_enviar = carreta_enviar.pack_byte_array()

			random_id_ultimo_pkt_enviado = carreta_enviar.rand_id
			buey_recibido = BUEY()

			while not paquete_confirmado:
				
				# Envia los datos
				sock.sendto(dato_enviar, server_address)
				
				try:
					# Recibe un paquete BUEY
					dato_recibido, server = sock.recvfrom(4096)
					buey_recibido.unpack_byte_array(dato_recibido)
					print(buey_recibido)
					
					print("Conflicto: Random id de ultimo paquete enviado %s \n" % random_id_ultimo_pkt_enviado)
					print("Random id de buey recibido %s" % buey_recibido.rand_id)

					if random_id_ultimo_pkt_enviado == buey_recibido.rand_id:
						paquete_confirmado = True
						
					
				except socket.timeout:
					print ("Timeout")

			print(buey_recibido)
		finally:
			file.close()
			sock.close()