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
	
	def obtener_nodo_id(self, pg_id):
		for fila in range(0, self.filas):
			if self.tabla_paginas[fila][0] == pg_id:
				return self.tabla_paginas[fila][1]
		return -1

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

	def obtener_nodo_disponible(self, tamanno_pagina):
		for fila in range(0, self.filas):
			if(self.tabla_nodos[fila][2] >= tamanno_pagina):
				return self.tabla_nodos[fila][0], self.tabla_nodos[fila][1]
		return -1, -1
	
	def obtener_nodo_ip(self, nodo_id):
		for fila in range(0, self.filas):
			if self.tabla_nodos[fila][0] == nodo_id:
				return self.tabla_nodos[fila][1]
		return -1

	def append(self, tripleta):
		self.filas += 1
		self.tabla_nodos.append(tripleta)
		print("Nodo Agregado: " + str(tripleta))
	
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
		self.tabla_paginas = TablaPaginas()
		self.tabla_nodos = TablaNodos()
		self.ronda = 0
		self.event = Event()
		self.ip_pata_nmid = ""
		self.soy_activa = False
		self.existe_activa = False
		self.timeout_campeonato_termino = False
		self.timeout_keep_alive_termino = False

		return super().__init__(*args, **kwargs)

	def recibir_comunicaciones_TCP(self, tabla_nodos):
			com = Comunicacion()

			while True:
				if self.soy_activa:
					if self.event.is_set():
						break

					com.recibir_paquete_tcp(com.IP_MLID, com.PUERTO_TCP_NMMLID, self.analizar_datos_TCP)


	def iniciar_comunicacion_IDID(self, tabla_nodos):
		
		com = Comunicacion()
		
		while True:

			# Iniciar con un quiero ser
			self.enviar_quiero_ser()
			
			# Iniciar timer
			timer_campeonato = Thread(target=self.iniciar_timer_campeonato, args=(3, self.timeout_campeonato_termino,))
			timer_campeonato.start()

			while self.timeout_campeonato_termino == False and self.existe_activa == False:
				# Espero otros quiero ser o un soy activa
				com.recibir_broadcast(self.ip_pata_nmid, com.PUERTO_BC_IDID, self.analizar_paquete_BC_IDID)

			if self.soy_activa == False and self.existe_activa == False:
				#Me declaro activa
				self.soy_activa = True
				self.ronda = 3
				
			if self.soy_activa():
				keep_alive = Thread(target=self.enviar_keep_alive(), args=())

				keep_alive.start()

			timer_keep_alive = Thread(target=self.iniciar_timer_keep_alive, args=(4, self.timeout_campeonato_termino,))
			timer_keep_alive.start()
			
			while True:
				com.recibir_broadcast(self.ip_pata_nmid, com.PUERTO_BC_IDID, self.analizar_paquete_BC_IDID)

				if self.timeout_keep_alive_termino == True and self.soy_activa == False:
					break

				
	def enviar_keep_alive(self):
		com = Comunicacion()

		paquete = Paquete()

		paquete.operacion = TipoOperacion.Ok_KeepAlive.value
		paquete.filas1 = 0
		paquete.filas2 = 0

		paquetes_helper = Paquetes_Helper()

		buffer = paquetes_helper.empaquetar(TipoComunicacion.IDID, TipoTipoOperacion.Ok_KeepAlive, paquete)

		while True:
			com.enviar_broadcast(self.ip_pata_nmid, com.PUERTO_BC_IDID, None, buffer)
			sleep(2)

	def iniciar_timer_campeonato(self, tiempo, timeout_campeonato_termino):
		sleep(tiempo)
		self.timeout_campeonato_termino = True

	def iniciar_timer_keep_alive(self, tiempo, timeout_campeonato_termino):
		sleep(tiempo)
		self.timeout_keep_alive_termino = True
		

	def enviar_quiero_ser(self):
		com = Comunicacion()

		paquete_quiero_ser = Paquete()

		paquete_quiero_ser.operacion = TipoOperacion.Guardar_QuieroSer.value
		paquete_quiero_ser.mac = self.obtener_mac_address()
		paquete_quiero_ser.ronda = self.ronda

		paquete_helper = PaquetesHelper()

		buffer = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Guardar_QuieroSer, paquete_quiero_ser)

		com.enviar_broadcast(self.ip_pata_nmid, com.PUERTO_BC_IDID, None, buffer)

	def recibir_comunicaciones_broadcast_NMID(self, tabla_nodos):
			com = Comunicacion()

			while True:
				if self.soy_activa:
					com.recibir_broadcast(self.ip_pata_nmid, com.PUERTO_BC_NMID, self.analizar_paquete_BC_NMID)

	def analizar_datos_TCP(self, data):

		paquete_helper = PaquetesHelper()

		paquete = paquete_helper.desempaquetar(TipoComunicacion.MLID, data)

		tipo_operacion = TipoOperacion(paquete.operacion)

		if tipo_operacion == TipoOperacion.Guardar_QuieroSer:
			print("Se recibio pagina para guardar")
			respuesta = self.GuardarEnNM(paquete)
		elif tipo_operacion == TipoOperacion.Pedir_SoyActiva:
			print("Se recibio peticion de pagina")
			respuesta = self.PedirEnNM(paquete)

		print(paquete)
		print("Enviando respuesta", str(respuesta))

		
		return respuesta

	def GuardarEnNM(self, paquete):

		paquete_helper = PaquetesHelper()

		buffer = paquete_helper.empaquetar(TipoComunicacion.IDNM, TipoOperacion.Guardar_QuieroSer, paquete)

		nodo_id, nodo_ip = self.tabla_nodos.obtener_nodo_disponible(paquete.tamanno_pagina)

		self.tabla_paginas.append([paquete.pagina_id, nodo_id])

		com = Comunicacion()

		respuesta = com.enviar_paquete_tcp(nodo_ip, com.PUERTO_TCP_IDNM, buffer)
		
		# respuesta trae espacio disponible, cambiar paquete para solo enviar OK

		paquete_respuesta = paquete_helper.desempaquetar(TipoComunicacion.NMID, respuesta)

		self.tabla_nodos.set_espacio_disponible_nodo(nodo_id, paquete_respuesta.tamanno_disponible)

		# enviar broadcast de ID ID Keep Alive con Actualización
		paquete_bc = Paquete()
		paquete_bc.operacion = TipoOperacion.Ok_KeepAlive.value
		paquete_bc.filas1 = 1
		paquete_bc.filas2 = 1
		paquete_bc.dump1 = pack("=BB", paquete.pagina_id, nodo_id)
		paquete_bc.dump2 = self.tabla_nodos.tripleta_to_raw([nodo_id, nodo_ip, paquete_respuesta.tamanno_disponible])

		buffer_bc = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Ok_KeepAlive, paquete_bc)

		com.enviar_broadcast(self.ip_pata_nmid, com.PUERTO_BC_IDID, None, buffer_bc)

		# Crea respuesta para ML con un OK
		paquete_ok = Paquete()
		paquete_ok.operacion = TipoOperacion.Ok_KeepAlive.value
		paquete_ok.pagina_id = paquete.pagina_id

		respuesta_ok = paquete_helper.empaquetar(TipoComunicacion.MLID, TipoOperacion.Ok_KeepAlive, paquete_ok)

		return respuesta_ok

	def PedirEnNM(self, paquete):

		paquete_helper = PaquetesHelper()

		buffer = paquete_helper.empaquetar(TipoComunicacion.IDNM, TipoOperacion.Pedir_SoyActiva, paquete)

		# Obtengo el nodo y la dirección donde está almacenada la página
		nodo_id = self.tabla_paginas.obtener_nodo_id(paquete.pagina_id)
		nodo_ip = self.tabla_nodos.obtener_nodo_ip(nodo_id)

		com = Comunicacion()

		# Envio el paquete para pedir la pagina al Nodo de Memoria
		respuesta = com.enviar_paquete_tcp(nodo_ip, com.PUERTO_TCP_IDNM, buffer)

		# En la respuesta está la pagina con los datos, no es necesario empaquetar y desempaquetar ya que la estructura del paquete es la misma en NM y ML

		return respuesta

	def analizar_paquete_BC_IDID(self, data, addr):

		paquete_helper = PaquetesHelper()

		paquete = paquete_helper.desempaquetar(TipoComunicacion.IDID, data)

		tipo_operacion = TipoOperacion(paquete.operacion)

		if tipo_operacion ==  TipoOperacion.Pedir_SoyActiva:
			#Actualizar mis tablas

			#Cambiar a que existe activa
			self.existe_activa = True

		elif tipo_operacion == TipoOperacion.Guardar_QuieroSer:
			if self.soy_activa:
				self.responder_a_quiero_ser()
			else:
				pass

		elif tipo_operacion == TipoOperacion.Ok_KeepAlive:
			self.analizar_keep_alive(paquete)

		print(paquete)

	def analizar_keep_alive(self, paquete):
		return 0


	def responder_a_quiero_ser(self):
		# enviar broadcast de ID ID Keep Alive con toda la información
		paquete_bc = Paquete()
		paquete_bc.operacion = TipoOperacion.Ok_KeepAlive.value
		paquete_bc.filas1 = self.tabla_paginas.filas
		paquete_bc.filas2 = self.tabla_nodos.filas
		paquete_bc.dump1 = self.tabla_paginas.to_raw()
		paquete_bc.dump2 = self.tabla_nodos.to_raw()

		buffer_bc = paquete_helper.empaquetar(TipoComunicacion.IDID, TipoOperacion.Ok_KeepAlive, paquete_bc)

		com.enviar_broadcast(self.ip_pata_nmid, com.PUERTO_BC_IDID, None, buffer_bc)

	def analizar_paquete_BC_NMID(self, data, addr):
		paquete_helper = PaquetesHelper()
		paquete = paquete_helper.desempaquetar(TipoComunicacion.IDNM, data)
		
		tipo_operacion = TipoOperacion(paquete.operacion)

		if tipo_operacion == TipoOperacion.EstoyAqui:
			com = Comunicacion()
			paquete_ok = Paquete()
			paquete_ok.operacion = TipoOperacion.Ok_KeepAlive.value
			
			paquete_ok_raw = paquete_helper.empaquetar(TipoComunicacion.IDNM, TipoOperacion.Ok_KeepAlive, paquete_ok)
			com.enviar_paquete_tcp(addr[0], com.PUERTO_TCP_IDNM, paquete_ok_raw)

			self.tabla_nodos.append([self.tabla_nodos.filas, addr[0], paquete.tamanno_disponible])
			
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

		return mac_array

	def IniciarInterfazDistribuida(self, ip_pata_nmid):
		
		# Inicio la interfaz distribuida
		self.ip_pata_nmid = ip_pata_nmid

		# Iniciar campeonato

		hilo_bc_IDID = Thread(target=self.iniciar_comunicacion_IDID, args=(self.tabla_nodos,))
		hilo_bc_IDID.start()
		
		hilo_bc_NMID = Thread(target=self.recibir_comunicaciones_broadcast_NMID, args=(self.tabla_nodos,))
		hilo_tcp = Thread(target=self.recibir_comunicaciones_TCP, args=(self.tabla_nodos,))

		hilo_bc_NMID.start()
		hilo_tcp.start()

		hilo_tcp.join()
		hilo_bc_IDID.join()
		hilo_bc_NMID.join()

	

interfaz_distribuida = InterfazDistribuida()


interfaz_distribuida.IniciarInterfazDistribuida("192.168.86.203")
#interfaz_distribuida.test()