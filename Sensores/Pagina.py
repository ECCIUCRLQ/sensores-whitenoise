

class Pagina:

	def __init__(self, nombre = "", frame = 0, nodo = 0):
		self.nombre = nombre
		self.frame = frame
		self.nodo = nodo

	def __repr__(self):
		return "Pagina: \n\tNombre -> %s \n\tNodo -> %s" % (self.nombre, self.nodo)

	def __str__(self):
		return "Pagina: \n\tNombre -> %s \n\tNodo -> %s" % (self.nombre, self.nodo)

	def get_nombre(self):
		return self.__nombre

	def set_nombre(self, value):
		if not isinstance(value, str):
			raise TypeError("El tipo esperado para nombre es string")
		self.__nombre =  value
