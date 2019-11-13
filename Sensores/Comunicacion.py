#coding=utf-8

import socket
import time

class Comunicacion:

	BUFFER_SIZE = 1024

	def __init__(self, *args, **kwargs):
		return super().__init__(*args, **kwargs)

	def enviar_paquete_tcp(self, tcp_ip, tcp_port, message):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
		s.connect((tcp_ip, tcp_port))
		s.send(message)
		data = s.recv(self.BUFFER_SIZE)
		s.close()

	def recibir_paquete_tcp(self, tcp_ip, tcp_port, metodo):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
		s.bind((tcp_ip, tcp_port))
		s.listen()
		metodo("HOOOLA")
		conn, addr = s.accept()
		
		while True:
			data = conn.recv(self.BUFFER_SIZE)
			if not data: break

			
			conn.send(data)  # echo
		
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

	def enviar_broadcast(self, broadcast_port, message):
		server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		# Timeout para no bloquear el socket mientras se envia el broadcast
		server.settimeout(0.2)
		server.bind(("", 44444)) # TODO: Revisar este puerto
		while True:
			server.sendto(message, ('<broadcast>', broadcast_port))
			time.sleep(1)

	def recibir_broadcast(self, broadcast_port, metodo):
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		client.bind(("", broadcast_port))
		while True:
			data, addr = client.recvfrom(self.BUFFER_SIZE)
			# Aqui hacer algo con los datos
			metodo(data)
