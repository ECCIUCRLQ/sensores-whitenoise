
class Nodo:

	def __init__(self, id = 0, localizacion = ""):
		self.id = id
		self.localizacion = localizacion

	def __repr__(self):
		return "Nodo()"

	def __str__(self):
		return "Nodo: \n\tId -> %s \n\tLocalizacion -> %s" % (self.id, self.localizacion)

	def get_id(self):
		return self.__id

	def set_id(self, value):
		if not isinstance(value, int):
			raise TypeError("El tipo esperado para nodo id es entero")
		self.__id =  value

	def get_localizacion(self):
		return self.__localizacion

	def set_localizacion(self, value):
		if not isinstance(value, str):
			raise TypeError("El tipo esperado para nodo localizacion es string")
		self.__localizacion =  value

	id = property(get_id, set_id)
	localizacion = property(get_localizacion, set_localizacion)
