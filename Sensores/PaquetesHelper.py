#coding=utf-8


from struct import *

from TipoComunicacion import TipoComunicacion
from TipoOperacion import TipoOperacion
from Paquete import Paquete

class PaquetesHelper:
	def __init__(self, *args, **kwargs):
		return super().__init__(*args, **kwargs)

	def empaquetar(self, tipo_comunicacion, tipo_operacion, paquete):

		resultado = self.obtener_metodo_empaquetar_tipo_comunicacion(tipo_comunicacion, tipo_operacion, paquete)

		return resultado

	def desempaquetar(self, tipo_comunicacion, datos):

		resultado = self.obtener_metodo_desempaquetar_tipo_comunicacion(tipo_comunicacion, datos)

		return resultado

	def obtener_tipo_operacion(self, datos):
		tipo = datos[0]

		tipo_operacion = TipoOperacion(tipo)

		return tipo_operacion

	def obtener_metodo_desempaquetar_tipo_comunicacion(self, tipo_comunicacion, datos):
		switcher = {
			TipoComunicacion.MLID: self.procesar_operacion_desempaquetar_MLID,
			TipoComunicacion.IDID: self.procesar_operacion_desempaquetar_IDID,
			TipoComunicacion.IDNM: self.procesar_operacion_desempaquetar_IDNM
		}
		
		procesador_comunicacion = switcher.get(tipo_comunicacion, lambda: "Comunicacion No Valida")
		
		return procesador_comunicacion(datos)

	def obtener_metodo_empaquetar_tipo_comunicacion(self, tipo_comunicacion, tipo_operacion, paquete):
		switcher = {
			TipoComunicacion.MLID: self.procesar_operacion_empaquetar_MLID,
			TipoComunicacion.IDID: self.procesar_operacion_empaquetar_IDID,
			TipoComunicacion.IDNM: self.procesar_operacion_empaquetar_IDNM
		}
		
		procesador_comunicacion = switcher.get(tipo_comunicacion, lambda: "Comunicacion No Valida")
		
		return procesador_comunicacion(tipo_operacion, paquete)

	def procesar_operacion_desempaquetar_MLID(self, datos):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Guardar: self.procesar_operacion_desempaquetar_MLID_guardar,
			TipoOperacion.Pedir: self.procesar_operacion_desempaquetar_MLID_pedir,
			TipoOperacion.Recibir: self.procesar_operacion_desempaquetar_MLID_recibir,
			TipoOperacion.Ok: self.procesar_operacion_desempaquetar_MLID_ok,
			TipoOperacion.Error: self.procesar_operacion_desempaquetar_MLID_error
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de MLID No Valida")

		return procesador_operacion(datos)

	def procesar_operacion_empaquetar_MLID(self, tipo_operacion, paquete):

		switcher = {
			TipoOperacion.Guardar: self.procesar_operacion_empaquetar_MLID_guardar,
			TipoOperacion.Pedir: self.procesar_operacion_empaquetar_MLID_pedir,
			TipoOperacion.Recibir: self.procesar_operacion_empaquetar_MLID_recibir,
			TipoOperacion.Ok: self.procesar_operacion_empaquetar_MLID_ok,
			TipoOperacion.Error: self.procesar_operacion_empaquetar_MLID_error
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de MLID No Valida")

		return procesador_operacion(paquete)

	

	def procesar_operacion_desempaquetar_IDID(self, datos):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		return 0

	def procesar_operacion_empaquetar_IDID(self, tipo_operacion, paquete):

		return 0

	def procesar_operacion_desempaquetar_IDNM(self, datos):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Guardar: self.procesar_operacion_desempaquetar_IDNM_Guardar,
			TipoOperacion.Pedir: self.procesar_operacion_desempaquetar_IDNM_pedir,
			TipoOperacion.Recibir: self.procesar_operacion_desempaquetar_IDNM_recibir,
			TipoOperacion.Error: self.procesar_operacion_desempaquetar_IDNM_ok,
			TipoOperacion.Error: self.procesar_operacion_desempaquetar_IDNM_error
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de IDNM No Valida")

		return procesador_operacion(datos)

	def procesar_operacion_empaquetar_IDNM(self, tipo_operacion, paquete):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Guardar: self.procesar_operacion_empaquetar_IDNM_Guardar,
			TipoOperacion.Pedir: self.procesar_operacion_empaquetar_IDNM_pedir,
			TipoOperacion.Recibir: self.procesar_operacion_empaquetar_IDNM_recibir,
			TipoOperacion.Error: self.procesar_operacion_empaquetar_IDNM_ok,
			TipoOperacion.Error: self.procesar_operacion_empaquetar_IDNM_error
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de IDNM No Valida")

		return procesador_operacion(datos)

	# OPERACIONES DE DESEMPAQUETAR

	#MLID

	def procesar_operacion_desempaquetar_MLID_guardar(self, datos):
		# Guarda una pagina desde memoria local a memoria distribuida
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + TamanoPagina(4 Bytes) + DatosPagina(TamanoPagina Bytes)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id = unpack('B', datos[1:2])[0]
		paquete.tamanno_pagina = unpack('I', datos[2:6])[0]
		paquete.datos_pagina = datos[6:(6 + paquete.tamanno_pagina)]

		return paquete

	def procesar_operacion_desempaquetar_MLID_pedir(self, datos):
		# Obtiene una pagina de memoria desde la interfaz distribuida.
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id= unpack('B', datos[1:2])[0]

		return 0

	def procesar_operacion_desempaquetar_MLID_recibir(self, datos):
		# Recibe una pagina desde memoria distribuida a memoria local
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + DatosPagina(n Bytes)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id= unpack('B', datos[1:2])[0]
		paquete.datos_pagina = datos[2:tam]

		return 0

	def procesar_operacion_desempaquetar_MLID_ok(self, datos):
		# Envia un codigo de ok????
		# Formato: CodigoOperacion(1 Byte) + Codigo_Ok(1 Byte)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.codigo_ok = unpack('B', datos[1:2])[0]

		return paquete

	def procesar_operacion_desempaquetar_MLID_error(self, datos):
		# Envia un codigo de error????
		# Formato: CodigoOperacion(1 Byte) + Codigo_Error(1 Byte)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.codigo_error= unpack('B', datos[1:2])[0]

		return paquete

	# IDNM

	def procesar_operacion_desempaquetar_IDNM_guardar(self, datos):
		# Guarda una pagina desde memoria local a memoria distribuida
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + TamanoPagina(4 Bytes) + DatosPagina(TamanoPagina Bytes)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id = unpack('B', datos[1:2])[0]
		paquete.tamanno_pagina = unpack('I', datos[2:6])[0]
		paquete.datos_pagina = datos[6:(6 + paquete.tamanno_pagina)]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_pedir(self, datos):
		# Obtiene una pagina de memoria desde la interfaz distribuida.
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id= unpack('B', datos[1:2])[0]

		return 0

	def procesar_operacion_desempaquetar_IDNM_recibir(self, datos):
		# Recibe una pagina desde memoria distribuida a memoria local
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + DatosPagina(n Bytes)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id= unpack('B', datos[1:2])[0]
		paquete.datos_pagina = datos[2:tam]

		return 0

	def procesar_operacion_desempaquetar_IDNM_ok(self, datos):
		# Envia un codigo de ok????
		# Formato: CodigoOperacion(1 Byte) + Codigo_Ok(1 Byte)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.codigo_ok = unpack('B', datos[1:2])[0]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_error(self, datos):
		# Envia un codigo de error????
		# Formato: CodigoOperacion(1 Byte) + Codigo_Error(1 Byte)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.codigo_error= unpack('B', datos[1:2])[0]

		return paquete



	# OPERACIONES DE EMPAQUETAR

	# MLID

	def procesar_operacion_empaquetar_MLID_guardar(self, paquete):
		# Guarda una pagina desde memoria local a memoria distribuida
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + TamanoPagina(4 Bytes) + DatosPagina(TamanoPagina Bytes)

		datos = pack('=BBI', paquete.operacion, paquete.pagina_id, paquete.tamanno_pagina)
		datos = datos + paquete.datos_pagina

		return datos

	def procesar_operacion_empaquetar_MLID_pedir(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos

	def procesar_operacion_empaquetar_MLID_recibir(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)
		datos = datos + paquete.datos_pagina

		return datos

	def procesar_operacion_empaquetar_MLID_ok(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos

	def procesar_operacion_empaquetar_MLID_error(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos


	# IDNM

	def procesar_operacion_empaquetar_IDNM_guardar(self, paquete):
		# Guarda una pagina desde memoria local a memoria distribuida
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + TamanoPagina(4 Bytes) + DatosPagina(TamanoPagina Bytes)

		datos = pack('=BBI', paquete.operacion, paquete.pagina_id, paquete.tamanno_pagina)
		datos = datos + paquete.datos_pagina

		return datos

	def procesar_operacion_empaquetar_IDNM_pedir(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos

	def procesar_operacion_empaquetar_IDNM_recibir(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)
		datos = datos + paquete.datos_pagina

		return datos

	def procesar_operacion_empaquetar_IDNM_ok(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos

	def procesar_operacion_empaquetar_IDNM_error(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos