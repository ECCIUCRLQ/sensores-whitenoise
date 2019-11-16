from TipoOperacion import TipoOperacion
from TipoComunicacion import TipoComunicacion
from Paquete import Paquete
from PaquetesHelper import PaquetesHelper
from Comunicacion import Comunicacion

from threading import Thread, Event
from threading import Lock
from time import sleep


class InterfazDistribuida:

	tabla_nodos = []

	event = Event()

	def __init__(self, *args, **kwargs):
		return super().__init__(*args, **kwargs)

	def RecibirComunicacionesTCP(self, tabla_nodos):

		com = Comunicacion()

		while True:
			if self.event.is_set():
				break

			com.recibir_paquete_tcp('10.1.137.79', 10000, self.AnalizarPaqueteTCP)


	def RecibirComunicacionesBroadcast(self, tabla_nodos):

		com = Comunicacion()

		com.recibir_broadcast(1000, self.AnalizarPaqueteBC)

		return 0

	def AnalizarPaqueteTCP(self, data):

		paquete_helper = PaquetesHelper()

		paquete = paquete_helper.desempaquetar(TipoComunicacion.MLID, data)

		paquete.operacion = TipoOperacion.Ok.value
		paquete.ok = paquete.pagina_id

		respuesta = paquete_helper.empaquetar(TipoComunicacion.MLID, TipoOperacion.Ok, paquete)


		print(data)
		print(respuesta)

		return respuesta

	def AnalizarPaqueteBC(self, data):

		return 0

	def IniciarInterfazDistribuida(self):
		
		#Inicio la interfaz distribuida

		# Averiguo quien es la ID Activa, o me autoproclamo si es necesario

		# En caso de que sea la activa inicio las tareas de escucha

		hilo_tcp = Thread(target=self.RecibirComunicacionesTCP, args=(self.tabla_nodos, ))
		hilo_bc = Thread(target=self.RecibirComunicacionesBroadcast, args=(self.tabla_nodos, ))

		hilo_tcp.start()
		#hilo_bc.start()

		while True:
			try:
				sleep(1)
			except KeyboardInterrupt:
				self.event.set()
				break
		
		hilo_tcp.join()
		hilo_bc.join()
