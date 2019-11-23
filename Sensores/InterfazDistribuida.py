from TipoOperacion import TipoOperacion
from TipoComunicacion import TipoComunicacion
from Paquete import Paquete
from PaquetesHelper import PaquetesHelper
from Comunicacion import Comunicacion

from threading import Thread, Event
from threading import Lock
from time import sleep

from struct import *

from uuid import getnode as get_mac

import socket

class TablaPaginas:
	def __init__(self):
		self.tabla_paginas = []
		self.filas = 0

	def __str__(self):
		return str(self.tabla_paginas)

	def to_raw(self):
		raw_table = bytearray()
		for fila in range(0, self.filas):
			raw_table += pack('=BB', self.tabla_paginas[fila][0], self.tabla_paginas[fila][1])
		return raw_table

	def append(self, par):  # Recibe una lista de la forma [paginaId, NodoId]
		self.filas += 1
		self.tabla_paginas.append(par)

	def actualizar(self, filas_cambios, datos_tabla): # Los cambios de esta tabla solamente son adiciones de paginas.
		for fila in range(0, filas_cambios):
			self.tabla_paginas.append([datos_tabla[fila * 2], datos_tabla[fila * 2 + 1]])
			self.filas += 1
	
	def get_filas(self):
		return self.filas

class TablaNodos:
	def __init__(self):
		self.tabla_nodos = []
		self.filas = 0
	def __str__(self):
		return str(self.tabla_nodos)
	
	def to_raw(self):
		raw_table = bytearray()
		for fila in range(0, self.filas):
			raw_table += self.tripleta_to_raw(self.tabla_nodos[fila])
		return raw_table

	def tripleta_to_raw(self, tripleta):
		return pack('B', tripleta[0]) + socket.inet_aton(tripleta[1]) + pack('I', tripleta[2])

	def append(self, tripleta):
		self.filas += 1
		self.tabla_nodos.append(tripleta)
	
	def actualizar(self, filas_cambios, datos_tabla):
		for fila in range(0, filas_cambios):
			nodo_id = unpack("B", datos_tabla[fila * 9: fila * 9 + 1])[0]
			ip = socket.inet_ntoa(datos_tabla[fila * 9 + 1 : fila * 9 + 5])
			espacio_disponible = unpack("I", datos_tabla[fila * 9 + 5: fila * 9 + 9])[0]
			# print("nodo_id: " + str(nodo_id) + " ip: " + ip + " espacio_disponible: " + str(espacio_disponible))
			if self.nodo_agregado(nodo_id):
				print("Nodo " + str(nodo_id) + " espacio actualizado")
				self.set_espacio_disponible_nodo(nodo_id, espacio_disponible)
			else:
				print("Nodo " + str(nodo_id) + " agregado")
				self.append([nodo_id, ip, espacio_disponible])
	
	def nodo_agregado(self, nodo_id):
		for fila in range(0, self.filas):
			if(self.tabla_nodos[fila][0] == nodo_id):
				return True
		return False

	def set_espacio_disponible_nodo(self, nodo_id, espacio_disponible):
		for fila in range(0, self.filas):
			if(self.tabla_nodos[fila][0] == nodo_id):
				self.tabla_nodos[fila][2] = espacio_disponible

class InterfazDistribuida:
	
	def __init__(self, *args, **kwargs):
		self.ip_red_ml = '127.0.0.1'
		self.ip_red_nodos_id = '192.168.1.1'
		self.tabla_paginas = TablaPaginas()
		self.tabla_nodos = TablaNodos()
		self.ronda = 0
		self.event = Event()

		return super().__init__(*args, **kwargs)

	def recibir_comunicaciones_TCP(self, tabla_nodos):

		com = Comunicacion()

		while True:
			if self.event.is_set():
				break

			com.recibir_paquete_tcp(com.IP_MLID, com.PUERTO_TCP_NMMLID, self.analizar_datos_TCP)


	def recibir_comunicaciones_broadcast_IDID(self, tabla_nodos):

		com = Comunicacion()

		com.recibir_broadcast(com.PUERTO_BC_IDID, self.analizar_paquete_BC_IDID)

		return 0

	def analizar_datos_TCP(self, data):

		paquete_helper = PaquetesHelper()

		paquete = paquete_helper.desempaquetar(TipoComunicacion.MLID, data)

		paquete.operacion = TipoOperacion.Ok_KeepAlive.value
		paquete.ok = paquete.pagina_id

		respuesta = paquete_helper.empaquetar(TipoComunicacion.MLID, TipoOperacion.Ok_KeepAlive, paquete)


		print(paquete)
		print(respuesta)

		return respuesta

	def analizar_paquete_BC_IDID(self, data):

		paquete_helper = PaquetesHelper()

		paquete = paquete_helper.desempaquetar(TipoComunicacion.IDID, data)

		print(paquete)

	def enviar_bc_quiero_ser(self):

		paquete_helper = PaquetesHelper()

		paquete = Paquete()

		paquete.operacion = TipoOperacion.Guardar_QuieroSer.value
		paquete.mac = self.obtener_mac_address()
		paquete.ronda = self.ronda

		quiero_ser = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Guardar_QuieroSer, paquete)

		com = Comunicacion()

		com.enviar_broadcast(com.PUERTO_BC_IDID, 1, quiero_ser)

	def obtener_mac_address(self):
		mac = get_mac()

		mac_array = mac.to_bytes(6, 'little')

		return 0

	def IniciarInterfazDistribuida(self):
		
		# Inicio la interfaz distribuida

		# Iniciar campeonato

		hilo_bc = Thread(target=self.recibir_comunicaciones_broadcast_IDID, args=(self.tabla_nodos,))
		# Llamado a metodo activa

		hilo_tcp = Thread(target=self.recibir_comunicaciones_TCP, args=(self.tabla_nodos, ))

		# Llamado a metodo de pasiva
		hilo_tcp.start()
		hilo_bc.start()

		while True:
			try:
				sleep(1)
			except KeyboardInterrupt:
				self.event.set()
				break
		
		hilo_tcp.join()
		hilo_bc.join()

	def test(self):
		# pg_id = 1
		# node_id = 7
		# node_ip = 15
		# espacio_disponible = 75

	
		# #self.tabla_paginas.append([pg_id, node_id])
		# print (self.tabla_paginas.tabla_paginas)
		# # tabla_nodos = []
		# # tabla_nodos.append((node_id, node_ip ,espacio_disponible ))
		paquete_helper = PaquetesHelper()

		# paquete_enviar = Paquete()

		# paquete_enviar.operacion = TipoOperacion.Pedir_SoyActiva.value
		# paquete_enviar.filas1 = self.tabla_paginas.filas
		# paquete_enviar.filas2 = 1
		# paquete_enviar.dump1 = self.tabla_paginas.to_raw()
		# paquete_enviar.dump2 = pack('=BII', node_id, node_ip, espacio_disponible)
		
		# # paquete_enviar.operacion = TipoOperacion.Guardar_QuieroSer.value
		# # paquete_enviar.mac = b'\x01\x02\x03\x04\x05\x06'
		# # paquete_enviar.ronda_id = 0

		# paquete_raw = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Pedir_SoyActiva, paquete_enviar)
		
		# print (paquete_raw)

		# paquete_recibir = paquete_helper.desempaquetar(TipoComunicacion.IDID, paquete_raw)

		# self.tabla_paginas.actualizar(paquete_recibir.filas1, paquete_recibir.dump1)
		# print (self.tabla_paginas.tabla_paginas)
		
		self.tabla_nodos.append([7, '192.168.1.1', 70])
		print(self.tabla_nodos)
		raw_table = self.tabla_nodos.to_raw()
		
		paquete_enviar = Paquete()
		paquete_enviar.operacion = TipoOperacion.Pedir_SoyActiva.value
		paquete_enviar.filas1 = self.tabla_paginas.filas
		paquete_enviar.filas2 = self.tabla_nodos.filas
		paquete_enviar.dump1 = self.tabla_paginas.to_raw()
		paquete_enviar.dump2 = self.tabla_nodos.to_raw()

		paquete_raw = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Pedir_SoyActiva, paquete_enviar)
		paquete_recibir = paquete_helper.desempaquetar(TipoComunicacion.IDID, paquete_raw)

		print(paquete_recibir)


		#self.tabla_nodos.actualizar(paquete_recibir.filas2, paquete_recibir.dump2)

		print(self.tabla_nodos)
		
interfaz_distribuida = InterfazDistribuida()
interfaz_distribuida.IniciarInterfazDistribuida()
#interfaz_distribuida.test()