from Frame import Frame
from MLID import MLID
from Pagina import Pagina

from Comunicacion import Comunicacion
from Paquete import Paquete
from PaquetesHelper import PaquetesHelper
from TipoComunicacion import TipoComunicacion
from TipoOperacion import TipoOperacion

from operator import attrgetter

import datetime
import os
import shutil

class AdministradorMemoria:

	tamanno_memoria_principal = 4
	memoria_inicializada = False
	tabla_paginas = []
	tabla_ID = []
	memoria_principal = []
	ruta_ID_uno = "192.168.86.198"

	@classmethod
	def write(cls, direccion_fisica, dato):

		# Descomponer 'direccion_fisica' para obtener pagina y offset.
		pagina_id = int(direccion_fisica.split('x')[0])

		# Localizar pagina en la tabla de paginas.
		pagina = cls.tabla_paginas[pagina_id]

		# Si la pagina esta en memoria principal obtiene el frame y le hace un append de 'dato'
		# en la seccion de datos.
		if pagina.frame >= 0:
			frame = cls.memoria_principal[pagina.frame]
			frame.datos.append(dato)
			frame.fecha_ultimo_acceso = datetime.datetime.now()

		# Si la pagina está en memoria secundaria localiza un frame libre,
		# obtiene la pagina desde un archivo y lo carga a memoria.
		else:
			# Obtiene un espacio en memoria principal
			frame_libre = cls.obtener_frame_memoria_principal(False)

			# Obtiene los datos que haya en memoria secundaria
			datos_memoria_secundaria = cls.obtener_datos_ID(pagina.nombre, pagina.ID)

			# Le adjunta los datos y lo deja en memoria principal
			datos_memoria_secundaria.append(dato)

			frame = cls.memoria_principal[frame_libre]

			frame.datos.extend(datos_memoria_secundaria)
			frame.fecha_ultimo_acceso = datetime.datetime.now()

			# Actualiza la tabla de paginas
			pagina.frame = frame_libre
			pagina.ID = 0

	@classmethod
	def read(cls, pagina_id):

		datos = []
		# Localiza la pagina en la tabla de paginas.
		pagina = cls.tabla_paginas[pagina_id]

		# Si esta en memoria principal obtiene la seccion de datos y la retorna
		if pagina.frame >= 0:
			frame = cls.memoria_principal[pagina.frame]
			frame.fecha_ultimo_acceso = datetime.datetime.now()

			datos = frame.datos

		# Si esta en memoria secundaria localiza un frame libre y carga la pagina a memoria
		# principal y la retorna.
		else:
			# Obtiene un espacio en memoria principal
			frame_libre = cls.obtener_frame_memoria_principal(True)

			# Obtiene los datos que haya en memoria secundaria
			datos_memoria_secundaria = cls.obtener_datos_ID(pagina.nombre, pagina.ID)

			frame = cls.memoria_principal[frame_libre]

			frame.datos.extend(datos_memoria_secundaria)
			frame.fecha_ultimo_acceso = datetime.datetime.now()

			# Actualiza la tabla de paginas
			#pagina.frame = frame_libre ###################### YA NO HAY QUE ACTUALIZAR EL FRAME PORQUE SIGUEN ESTANDO EN UN NM#############################
			#pagina.ID = 0 ###################### YA NO HAY QUE ACTUALIZAR EL FRAME PORQUE SIGUEN ESTANDO EN UN NM#############################

			datos = datos_memoria_secundaria

		# Si no hay frame libre tiene que mover la pagina con la escritura mas antigua
		# a memoria secundaria y cargar ahí la pagina solicitada.
		datos_raw = bytearray().join(datos)
		
		return datos_raw

	@classmethod
	def malloc(cls):
		# Si no se ha inicializado la memoria inicia el proceso que lo hace.
		if cls.memoria_inicializada == False:
			cls.inicializar_memoria()

		# Le asigna una pagina de memoria
		return cls.asignar_pagina_memoria()

	@classmethod
	def inicializar_memoria(cls):
		# Inicializa la memoria principal con todos los frames disponibles.
		cls.memoria_principal = [Frame() for i in range(cls.tamanno_memoria_principal)]

		for index, frame in enumerate(cls.memoria_principal):
			if index % 2 != 0:
				frame.solo_lectura = True

		# Comprueba si existe el directorio de memoria, si existe lo elimina. Crea uno nuevo
		if os.path.exists(cls.ruta_ID_uno):
			cls.finalizar_memoria()

		os.makedirs(cls.ruta_ID_uno)
		# Agrega el MLID por defecto a la tabla de IDs.
		cls.tabla_ID.append(MLID(1, cls.ruta_ID_uno))

		# Pone la bandera de que la memoria fue inicializada.
		cls.memoria_inicializada = True

	@classmethod
	def finalizar_memoria(cls):
		# Borra la carpeta de memoria secundaria y todo su contenido.
		shutil.rmtree(cls.ruta_ID_uno)

	@classmethod
	def asignar_pagina_memoria(cls):
		# Localiza el siguiente numero de pagina que le corresponde
		siguiente = len(cls.tabla_paginas)

		# Le da un sitio en memoria principal
		frame = cls.obtener_frame_memoria_principal(False)
		print("frame: " + str(frame))
		nueva_pagina = Pagina('Pag' + str(siguiente), frame, 0)

		cls.tabla_paginas.append(nueva_pagina)

		return siguiente

	@classmethod
	def obtener_frame_memoria_principal(cls, es_lectura = False):
		
		frame_disponible = -1

		# Busca el primer frame de memoria disponible
		for index, frame in enumerate(cls.memoria_principal):
			if (frame.disponible == True and frame.solo_lectura == es_lectura):
				
				frame_disponible = index

				frame.disponible = False
				frame.fecha_ultimo_acceso = datetime.datetime.now()
				break

		# Si no lo encuentra libera uno pasando los datos a memoria secundaria
		if frame_disponible < 0:
			# Localiza el frame con el ultimo acceso mas antiguo y lo mueve a memoria secundaria
			frame_antiguo = min(cls.memoria_principal,key=attrgetter('fecha_ultimo_acceso'))

			# Obtiene el indice en la memoria principal del frame a mover a memoria secundaria
			frame_indice = cls.memoria_principal.index(frame_antiguo)

			# Mueve los datos a memoria secundaria si es una operacion de escritura
			if es_lectura == False:
				cls.mover_frame_memoria_secundaria(frame_indice, frame_antiguo.datos)

			# Limpia los datos en la seccion de data
			frame_antiguo.datos = []
			frame_antiguo.disponible = False
			frame_antiguo.fecha_ultimo_acceso = datetime.datetime.now()

			# Asigna el indice a devolver
			frame_disponible = frame_indice

		return frame_disponible

	@classmethod
	def mover_frame_memoria_secundaria(cls, frame_indice, data):

		# Busca en la tabla de paginas la pagina que tenga el 'frame_indice' para hacer el cambio de datos
		for index, pagina in enumerate(cls.tabla_paginas):
			if pagina.frame == frame_indice:
				pagina.frame = -1
				pagina.ID = cls.guardar_datos_ID(pagina.nombre, data)
				break
		return 0

	@classmethod
	def guardar_datos_ID(cls, nombre_pagina, data):
		# Obtiene la ID que le corresponda (en esta etapa solo hay una ID y en esta parte realmente es una interfaz distribuida)
		ID = cls.obtener_ID_disponible()

		# Ahora la ID tiene la IP de la Interfaz Distribuida. Solo hay que 
		# generar un paquete y enviarlo

		paquete = Paquete()
		paquete.operacion = TipoOperacion.Guardar_QuieroSer.value
		paquete.pagina_id = nombre_pagina
		paquete.tamanno_pagina = len(data)
		paquete.datos_pagina = data

		paq_helper = PaquetesHelper()
		buffer = paq_helper.empaquetar(TipoComunicacion.MLID, TipoOperacion.Guardar_QuieroSer, paquete)

		com = Comunicacion()
		respuesta = com.enviar_paquete_tcp(com.IP_MLID, com.PUERTO_TCP_NMMLID, buffer) # TODO: Esperar OK de respuesta

		print(respuesta)

		return ID.id

	@classmethod
	def obtener_datos_ID(cls, nombre_pagina, ID_id):
		#print("Leyendo de memoria secundaria página: " + str(nombre_pagina))
		# Obtiene la ID que le corresponda (en esta etapa solo hay una ID)
		ID = cls.obtener_ID_correspondiente(ID_id)

		# Ahora la ID trae la ip donde está la interfaz distribuida
		# y envia una solicitud para recibir la página

		paquete_pedir = Paquete()
		paquete_pedir.operacion = TipoOperacion.Pedir_SoyActiva.value
		paquete_pedir.pagina_id = nombre_pagina

		paquete_helper = PaquetesHelper()
		buffer = paquete_helper.empaquetar(TipoComunicacion.MLID, TipoOperacion.Pedir_SoyActiva, paquete_pedir)

		com = Comunicacion()
		respuesta = com.enviar_paquete_tcp(com.IP_MLID, com.PUERTO_TCP_NMMLID, buffer)

		paq_helper = PaquetesHelper()
		paquete_respuesta = paq_helper.desempaquetar(TipoComunicacion.MLID, respuesta)

		return paquete_respuesta.datos_pagina

	@classmethod
	def obtener_ID_disponible(cls):
		# Metodo para obtener la ID que se debe utilizar para guardar en memoria secundaria
		# en este etapa solo devuelve la unica ID que existe
		return cls.tabla_ID[0]

	@classmethod
	def obtener_ID_correspondiente(cls, ID_id):
		# Obtiene la ID que le corresponde a una página
		ID_utilizado = None

		for ID in cls.tabla_ID:
			if ID.id == ID_id:
				ID_utilizado = ID

		return ID_utilizado