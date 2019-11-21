class Paquete:
	def __init__(self, *args, **kwargs):
		self.operacion = None
		self.pagina_id = None
		self.mac = None
		self.filas1 = None
		self.filas2 = None
		self.dump1 = None
		self.dump2 = None
		self.ronda_id = None
		self.tamanno_pagina = None
		self.datos_pagina = None
		self.codigo_ok = None
		self.codigo_error = None
		self.tamanno_disponible = None

	def __str__(self):
		paquete = ""

		if self.operacion is not None:
			paquete += "Operacion: " + str(self.operacion) + " "

		if self.pagina_id is not None:
			paquete += "Pagina Id: " + str(self.pagina_id) + " "

		if self.mac is not None:
			paquete += "MAC: " + str(self.mac) + " "

		if self.filas1 is not None:
			paquete += "Cant Filas 1: " + str(self.filas1) + " "

		if self.filas2 is not None:
			paquete += "Cant Filas 2: " + str(self.filas2) + " "

		if self.dump1 is not None:
			paquete += "DUMP1: " + str(self.dump1) + " "
			
		if self.dump2 is not None:
			paquete += "DUMP2: " + str(self.dump2) + " "
			
		if self.ronda_id is not None:
			paquete += "Ronda ID: " + str(self.ronda_id) + " "
			
		if self.tamanno_pagina is not None:
			paquete += "Tamanno Pag: " + str(self.tamanno_pagina) + " "
			
		if self.datos_pagina is not None:
			paquete += "Pagina: " + str(self.datos_pagina) + " "
			
		if self.codigo_ok is not None:
			paquete += "Codigo Ok: " + str(self.codigo_ok) + " "
			
		if self.codigo_error is not None:
			paquete += "Codigo Error: " + str(self.codigo_error) + " "
			
		if self.tamanno_disponible is not None:
			paquete += "Espacio Disponible: " + str(self.tamanno_disponible) + " "

		return paquete

