

class Pagina:

	def __init__(self, nombre = "", frame = 0, ID = 0):
		self.nombre = nombre
		self.frame = frame
		self.ID = ID

	def __repr__(self):
		return "Pagina: \n\tNombre -> %s \n\tID -> %s" % (self.nombre, self.ID)

	def __str__(self):
		return "Pagina: \n\tNombre -> %s \n\tID -> %s" % (self.nombre, self.ID)

	def get_nombre(self):
		return self.__nombre

	def set_nombre(self, value):
		if not isinstance(value, str):
			raise TypeError("El tipo esperado para nombre es string")
		self.__nombre =  value
