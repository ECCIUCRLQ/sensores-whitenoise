#coding=utf-8

import socket
import time

class Comunicacion:

	BUFFER_SIZE = 1024
	
	PUERTO_BC_NMID = 5000
	PUERTO_BC_IDID = 6666
	PUERTO_TCP_IDNM = 3114
	PUERTO_TCP_NMMLID = 2000

	IP_MLID = "192.168.86.198"
	
	def __init__(self, *args, **kwargs):
		return super().__init__(*args, **kwargs)

	def enviar_paquete_tcp(self, tcp_ip, tcp_port_to, message):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP

		s.connect((tcp_ip, tcp_port_to))
		s.send(message)
		data = s.recv(self.BUFFER_SIZE)
		s.close()

		return data

	def recibir_paquete_tcp(self, tcp_ip, tcp_port, metodo):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((tcp_ip, tcp_port))
		s.listen()
		
		conn, addr = s.accept()

		t = s.getsockname()

		print("Se recibio un paquete desde: ", addr)

		data = conn.recv(self.BUFFER_SIZE)

		if data != None:
			respuesta = metodo(data)
			conn.send(respuesta)  # echo
		
		conn.close()

	def enviar_paquete_udp(self, udp_ip, udp_port, message):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		sock.sendto(message, (udp_ip, udp_port))

	def recibir_paquete_udp(self, udp_ip, udp_port, metodo):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		sock.bind((udp_ip, udp_port))

		while True:
			data, addr = sock.recvfrom(self.BUFFER_SIZE)
			metodo(data)

	def enviar_broadcast(self, broadcast_ip, broadcast_port, timeout, message):
		server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

		# Timeout para no bloquear el socket mientras se envia el broadcast
		if timeout != None:
			server.settimeout(timeout)

		server.bind((broadcast_ip, 44444)) # TODO: Revisar este puerto
		server.sendto(message, ('<broadcast>', broadcast_port))

	def recibir_broadcast(self, broadcast_ip, broadcast_port, metodo):
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		client.bind((broadcast_ip, broadcast_port))

		client.setblocking(0)

		try:
			data, addr = client.recvfrom(self.BUFFER_SIZE)
			# Aqui hacer algo con los datos
			metodo(data,addr)
		except socket.error:
			pass

		client.close()

	def recibir_broadcast_ciclo(self, broadcast_ip, broadcast_port, metodo):
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		client.bind((broadcast_ip, broadcast_port))

		while True:
			data, addr = client.recvfrom(self.BUFFER_SIZE)
			# Aqui hacer algo con los datos
			metodo(data,addr)
