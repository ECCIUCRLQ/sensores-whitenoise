from Frame import Frame
from Nodo import Nodo
from Pagina import Pagina

from operator import attrgetter

import datetime
import os
import shutil

class AdministradorMemoria:

	tamanno_memoria_principal = 4
	memoria_inicializada = False
	tabla_paginas = []
	tabla_nodos = []
	memoria_principal = []
	ruta_nodo_uno = "memoria/"

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
			frame_libre = cls.obtener_frame_memoria_principal()

			# Obtiene los datos que haya en memoria secundaria
			datos_memoria_secundaria = cls.obtener_datos_nodo(pagina.nombre, pagina.nodo)

			# Le adjunta los datos y lo deja en memoria principal
			datos_memoria_secundaria.append(dato)

			frame = cls.memoria_principal[frame_libre]

			frame.datos.extend(datos_memoria_secundaria)
			frame.fecha_ultimo_acceso = datetime.datetime.now()

			# Actualiza la tabla de paginas
			pagina.frame = frame_libre
			pagina.nodo = 0

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
			frame_libre = cls.obtener_frame_memoria_principal()

			# Obtiene los datos que haya en memoria secundaria
			datos_memoria_secundaria = cls.obtener_datos_nodo(pagina.nombre, pagina.nodo)

			frame = cls.memoria_principal[frame_libre]

			frame.datos.extend(datos_memoria_secundaria)
			frame.fecha_ultimo_acceso = datetime.datetime.now()

			# Actualiza la tabla de paginas
			pagina.frame = frame_libre
			pagina.nodo = 0

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

		# Comprueba si existe el directorio de memoria, si existe lo elimina. Crea uno nuevo
		if os.path.exists(cls.ruta_nodo_uno):
			cls.finalizar_memoria()

		os.makedirs(cls.ruta_nodo_uno)
		# Agrega el nodo por defecto a la tabla de nodos.
		cls.tabla_nodos.append(Nodo(1, cls.ruta_nodo_uno))

		# Pone la bandera de que la memoria fue inicializada.
		cls.memoria_inicializada = True

	@classmethod
	def finalizar_memoria(cls):
		# Borra la carpeta de memoria secundaria y todo su contenido.
		shutil.rmtree(cls.ruta_nodo_uno)

	@classmethod
	def asignar_pagina_memoria(cls):
		# Localiza el siguiente numero de pagina que le corresponde
		siguiente = len(cls.tabla_paginas)

		# Le da un sitio en memoria principal
		frame = cls.obtener_frame_memoria_principal()

		nueva_pagina = Pagina('Pag' + str(siguiente), frame, 0)

		cls.tabla_paginas.append(nueva_pagina)

		return siguiente

	@classmethod
	def obtener_frame_memoria_principal(cls):
		
		frame_disponible = -1

		# Busca el primer frame de memoria disponible
		for index, frame in enumerate(cls.memoria_principal):
			if frame.disponible == True:
				
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

			# Mueve los datos a memoria secundaria
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
				pagina.nodo = cls.guardar_datos_nodo(pagina.nombre, data)
				break
		return 0

	@classmethod
	def guardar_datos_nodo(cls, nombre_pagina, data):
		# Obtiene el nodo que le corresponda (en esta etapa solo hay un nodo)
		nodo = cls.obtener_nodo_disponible()

		# Crea o abre el archivo de datos para guardar los datos
		filename = nodo.localizacion + nombre_pagina + ".bin"

		with open(filename, "wb") as f:
			for dato in data:
				#print("dato: " + str(dato) + "pagina: " + nombre_pagina)
				f.write(dato)

		return nodo.id

	@classmethod
	def obtener_datos_nodo(cls, nombre_pagina, nodo_id):
		print("Leyendo de memoria secundaria página: " + str(nombre_pagina))
		# Obtiene el nodo que le corresponda (en esta etapa solo hay un nodo)
		nodo = cls.obtener_nodo_correspondiente(nodo_id)

		# Crea o abre el archivo de datos para guardar los datos
		filename = nodo.localizacion + nombre_pagina + ".bin"

		datos = []
		# Obtiene los datos del archivo
		with open(filename, "rb") as f:
			datos.append(f.read())

		# Borra el archivo
		os.remove(filename)
		print("Archivo: " + filename + " borrado")

		return datos

	@classmethod
	def obtener_nodo_disponible(cls):
		# Metodo para obtener el nodo que se debe utilizar para guardar en memoria secundaria
		# en este etapa solo devuelve el unico nodo que existe
		return cls.tabla_nodos[0]

	@classmethod
	def obtener_nodo_correspondiente(cls, nodo_id):
		# Obtiene el nodo que le corresponde a una página
		nodo_utilizado = None

		for nodo in cls.tabla_nodos:
			if nodo.id == nodo_id:
				nodo_utilizado = nodo

		return nodo_utilizado