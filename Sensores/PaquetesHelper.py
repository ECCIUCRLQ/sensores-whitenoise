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
			TipoComunicacion.IDNM: self.procesar_operacion_desempaquetar_IDNM,
			TipoComunicacion.NMID: self.procesar_operacion_desempaquetar_NMID
		}
		
		procesador_comunicacion = switcher.get(tipo_comunicacion, lambda: "Comunicacion No Valida")
		
		return procesador_comunicacion(datos)

	def obtener_metodo_empaquetar_tipo_comunicacion(self, tipo_comunicacion, tipo_operacion, paquete):
		switcher = {
			TipoComunicacion.MLID: self.procesar_operacion_empaquetar_MLID,
			TipoComunicacion.IDID: self.procesar_operacion_empaquetar_IDID,
			TipoComunicacion.IDNM: self.procesar_operacion_empaquetar_IDNM,
			TipoComunicacion.NMID: self.procesar_operacion_empaquetar_NMID
		}
		
		procesador_comunicacion = switcher.get(tipo_comunicacion, lambda: "Comunicacion No Valida")
		
		return procesador_comunicacion(tipo_operacion, paquete)

	def procesar_operacion_desempaquetar_MLID(self, datos):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Guardar_QuieroSer: self.procesar_operacion_desempaquetar_MLID_Guardar,
			TipoOperacion.Pedir_SoyActiva: self.procesar_operacion_desempaquetar_MLID_pedir,
			TipoOperacion.Enviar: self.procesar_operacion_desempaquetar_MLID_recibir,
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_desempaquetar_MLID_ok,
			TipoOperacion.Error: self.procesar_operacion_desempaquetar_MLID_error
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de MLID No Valida")

		return procesador_operacion(datos)

	def procesar_operacion_empaquetar_MLID(self, tipo_operacion, paquete):

		switcher = {
			TipoOperacion.Guardar_QuieroSer: self.procesar_operacion_empaquetar_MLID_Guardar,
			TipoOperacion.Pedir_SoyActiva: self.procesar_operacion_empaquetar_MLID_pedir,
			TipoOperacion.Enviar: self.procesar_operacion_empaquetar_MLID_recibir,
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_empaquetar_MLID_ok,
			TipoOperacion.Error: self.procesar_operacion_empaquetar_MLID_error
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de MLID No Valida")

		return procesador_operacion(paquete)

	

	def procesar_operacion_desempaquetar_IDID(self, datos):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Guardar_QuieroSer: self.procesar_operacion_desempaquetar_IDID_QuieroSer,
			TipoOperacion.Pedir_SoyActiva: self.procesar_operacion_desempaquetar_IDID_SoyActiva,
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_desempaquetar_IDID_KeepAlive,
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de IDID No Valida")

		return procesador_operacion(datos)

	def procesar_operacion_empaquetar_IDID(self, tipo_operacion, paquete):

		switcher = {
			TipoOperacion.Guardar_QuieroSer: self.procesar_operacion_empaquetar_IDID_QuieroSer,
			TipoOperacion.Pedir_SoyActiva: self.procesar_operacion_empaquetar_IDID_SoyActiva,
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_empaquetar_IDID_KeepAlive,
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de IDID No Valida")

		return procesador_operacion(paquete)

	def procesar_operacion_desempaquetar_IDNM(self, datos):

		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Guardar_QuieroSer: self.procesar_operacion_desempaquetar_IDNM_Guardar,
			TipoOperacion.Pedir_SoyActiva: self.procesar_operacion_desempaquetar_IDNM_pedir,
			TipoOperacion.Enviar: self.procesar_operacion_desempaquetar_IDNM_recibir,
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_desempaquetar_IDNM_ok,
			TipoOperacion.Error: self.procesar_operacion_desempaquetar_IDNM_error,
			TipoOperacion.EstoyAqui: self.procesar_operacion_desempaquetar_IDNM_estoyaqui
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de IDNM No Valida")

		return procesador_operacion(datos)

	def procesar_operacion_empaquetar_IDNM(self, tipo_operacion, paquete):

		switcher = {
			TipoOperacion.Guardar_QuieroSer: self.procesar_operacion_empaquetar_IDNM_Guardar,
			TipoOperacion.Pedir_SoyActiva: self.procesar_operacion_empaquetar_IDNM_pedir,
			TipoOperacion.Enviar: self.procesar_operacion_empaquetar_IDNM_recibir,
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_empaquetar_IDNM_ok,
			TipoOperacion.Error: self.procesar_operacion_empaquetar_IDNM_error,
			TipoOperacion.EstoyAqui: self.procesar_operacion_empaquetar_IDNM_estoyaqui
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de IDNM No Valida")

		return procesador_operacion(paquete)

	def procesar_operacion_desempaquetar_NMID(self, datos):
		# Primero verifica que tipo de operacion es.
		tipo_operacion = self.obtener_tipo_operacion(datos);

		switcher = {
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_desempaquetar_NMID_ok
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de NMID No Valida")

		return procesador_operacion(datos)

	def procesar_operacion_empaquetar_NMID(self, tipo_operacion, paquete):
		switcher = {
			TipoOperacion.Ok_KeepAlive: self.procesar_operacion_empaquetar_NMID_ok
		}

		procesador_operacion = switcher.get(tipo_operacion, lambda: "Operacion de NMID No Valida")

		return procesador_operacion(paquete)

	# OPERACIONES DE DESEMPAQUETAR

	#MLID

	def procesar_operacion_desempaquetar_MLID_Guardar(self, datos):
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

		return paquete

	def procesar_operacion_desempaquetar_MLID_recibir(self, datos):
		# Recibe una pagina desde memoria distribuida a memoria local
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + DatosPagina(n Bytes)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id = unpack('B', datos[1:2])[0]
		paquete.datos_pagina = datos[2:tam]

		return paquete

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

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.codigo_error = unpack('B', datos[1:2])[0]

		return paquete

	# IDNM

	def procesar_operacion_desempaquetar_IDNM_Guardar(self, datos):
		# Guarda una pagina desde memoria local a memoria distribuida
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + TamanoPagina(4 Bytes) + DatosPagina(TamanoPagina Bytes)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id = unpack('B', datos[1:2])[0]
		paquete.tamanno_pagina = unpack('I', datos[2:6])[0]
		paquete.datos_pagina = datos[6:(6 + paquete.tamanno_pagina)]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_pedir(self, datos):
		# Obtiene una pagina de memoria desde la interfaz distribuida.
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id= unpack('B', datos[1:2])[0]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_recibir(self, datos):
		# Recibe una pagina desde memoria distribuida a memoria local
		# Formato: CodigoOperacion(1 Byte) + PaginaId(1 Byte) + DatosPagina(n Bytes)
		tam = len(datos)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id = unpack('B', datos[1:2])[0]
		paquete.datos_pagina = datos[2:tam]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_ok(self, datos):
		# Envia un codigo de ok????
		# Formato: CodigoOperacion(1 Byte)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_error(self, datos):
		# Envia un codigo de error????
		# Formato: CodigoOperacion(1 Byte) + Codigo_Error(1 Byte)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.codigo_error = unpack('B', datos[1:2])[0]

		return paquete

	def procesar_operacion_desempaquetar_IDNM_estoyaqui(self, datos):
		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.tamanno_disponible = unpack('I', datos[1:5])[0]

		return paquete

	#NMID
	def procesar_operacion_desempaquetar_NMID_ok(self, datos):
		# Envia un codigo de ok????
		# Formato: CodigoOperacion(1 Byte)

		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.pagina_id = unpack('B', datos[1:2])[0]
		paquete.tamanno_disponible = unpack('I', datos[2:6])[0]

		return paquete

	#IDID

	def procesar_operacion_desempaquetar_IDID_QuieroSer(self, datos):
		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.mac = datos[1:7]
		paquete.ronda_id = unpack('B', datos[7:8])[0]
		
		return paquete

	def procesar_operacion_desempaquetar_IDID_SoyActiva(self, datos):
		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.filas1 = unpack('B', datos[1:2])[0]
		paquete.filas2 = unpack('B', datos[2:3])[0]
		paquete.dump1 = datos[3: 3 + paquete.filas1 * 2]
		paquete.dump2 = datos[3 + paquete.filas1 * 2: 3 + paquete.filas1 * 2 + paquete.filas2 * 9]

		return paquete
	
	def procesar_operacion_desempaquetar_IDID_KeepAlive(self, datos):
		paquete = Paquete()
		paquete.operacion = unpack('B', datos[0:1])[0]
		paquete.filas1 = unpack('B', datos[1:2])[0]
		paquete.filas2 = unpack('B', datos[2:3])[0]
		paquete.dump1 = datos[3: 3 + paquete.filas1 * 2]
		paquete.dump2 = datos[3 + paquete.filas1 * 2: 3 + paquete.filas1 * 2 + paquete.filas2 * 9]

	# OPERACIONES DE EMPAQUETAR

	# MLID

	def procesar_operacion_empaquetar_MLID_Guardar(self, paquete):
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

	def procesar_operacion_empaquetar_IDNM_Guardar(self, paquete):
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
		
		datos = pack('=B', paquete.operacion)

		return datos

	def procesar_operacion_empaquetar_IDNM_error(self, paquete):
		
		datos = pack('=BB', paquete.operacion, paquete.pagina_id)

		return datos

	def procesar_operacion_empaquetar_IDNM_estoyaqui(self, paquete):
		datos = pack('=BI', paquete.operacion, paquete.tamanno_disponible)

		return datos

	# NMID
	def procesar_operacion_empaquetar_NMID_ok(self, paquete):
		
		datos = pack('=BBI', paquete.operacion, paquete.pagina_id, paquete.tamanno_disponible)

		return datos
	
	# IDID

	def procesar_operacion_empaquetar_IDID_QuieroSer(self, paquete):

		datos = pack('=B', paquete.operacion)
		datos += paquete.mac
		datos += pack('=B', paquete.ronda)

		return datos

	def procesar_operacion_empaquetar_IDID_SoyActiva(self, paquete):
		datos = pack('=BBB' , paquete.operacion, paquete.filas1, paquete.filas2)
		datos += paquete.dump1 + paquete.dump2

		return datos

	def procesar_operacion_empaquetar_IDID_KeepAlive(self, paquete):
		datos = pack('=BBB' , paquete.operacion, paquete.filas1, paquete.filas2)
		datos += paquete.dump1 + paquete.dump2

		return datos