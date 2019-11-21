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

class TablaPaginas:
	def __init__(self):
		self.tabla_paginas = []
		self.filas = 0

	def append(self, par):
		self.filas += 1
		self.tabla_paginas.append(par)

	def actualizar(self, filas_nuevas, datos_tabla):
		for fila in range(0, filas_nuevas):
			self.tabla_paginas.append([datos_tabla[fila * 2], datos_tabla[fila * 2 + 1]])
			self.filas += 1
	
	def get_filas(self):
		return self.filas

	def to_raw(self):
		raw_table = bytearray()
		print(self.filas)
		for fila in range(0, self.filas):
			raw_table += pack('=BB', self.tabla_paginas[fila][0], self.tabla_paginas[fila][1])

		return raw_table

class InterfazDistribuida:

	tabla_nodos = []

	#event = Event()
	def __init__(self, *args, **kwargs):
		self.tabla_paginas = TablaPaginas()
		self.tabla_nodos = []
		self.ronda = 0

		return super().__init__(*args, **kwargs)

	def RecibirComunicacionesTCP(self, tabla_nodos):

		com = Comunicacion()

		#while True:
		#	if self.event.is_set():
		#		break

		com.recibir_paquete_tcp('10.1.137.79', com.PUERTO_TCP_NMMLID, self.AnalizarPaqueteTCP)


	def recibir_comunicaciones_broadcast_IDID(self, tabla_nodos):

		com = Comunicacion()

		com.recibir_broadcast(com.PUERTO_BC_IDID, self.analizar_paquete_BC_IDID)

		return 0

	def AnalizarPaqueteTCP(self, data):

		paquete_helper = PaquetesHelper()

		paquete = paquete_helper.desempaquetar(TipoComunicacion.MLID, data)

		paquete.operacion = TipoOperacion.Ok_KeepAlive.value
		paquete.ok = paquete.pagina_id

		respuesta = paquete_helper.empaquetar(TipoComunicacion.MLID, TipoOperacion.Ok_KeepAlive, paquete)


		print(data)
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

		hilo_tcp = Thread(target=self.RecibirComunicacionesTCP, args=(self.tabla_nodos, ))

		# Llamado a metodo de pasiva
		#hilo_tcp.start()
		hilo_bc.start()

		while True:
			try:
				sleep(1)
			except KeyboardInterrupt:
				#self.event.set()
				break
		
		hilo_tcp.join()
		hilo_bc.join()

	def test(self):
		pg_id = 1
		node_id = 7
		node_ip = 15
		espacio_disponible = 75

	
		#self.tabla_paginas.append([pg_id, node_id])
		print (self.tabla_paginas.tabla_paginas)
		# tabla_nodos = []
		# tabla_nodos.append((node_id, node_ip ,espacio_disponible ))
		paquete_helper = PaquetesHelper()

		paquete_enviar = Paquete()

		paquete_enviar.operacion = TipoOperacion.Pedir_SoyActiva.value
		paquete_enviar.filas1 = self.tabla_paginas.filas
		paquete_enviar.filas2 = 1
		paquete_enviar.dump1 = self.tabla_paginas.to_raw()
		paquete_enviar.dump2 = pack('=BII', node_id, node_ip, espacio_disponible)
		
		# paquete_enviar.operacion = TipoOperacion.Guardar_QuieroSer.value
		# paquete_enviar.mac = b'\x01\x02\x03\x04\x05\x06'
		# paquete_enviar.ronda_id = 0

		paquete_raw = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Pedir_SoyActiva, paquete_enviar)
		
		print (paquete_raw)

		paquete_recibir = paquete_helper.desempaquetar(TipoComunicacion.IDID, paquete_raw)

		self.tabla_paginas.actualizar(paquete_recibir.filas1, paquete_recibir.dump1)
		print (self.tabla_paginas.tabla_paginas)
		
interfaz_distribuida = InterfazDistribuida()
interfaz_distribuida.IniciarInterfazDistribuida()
#interfaz_distribuida.test()