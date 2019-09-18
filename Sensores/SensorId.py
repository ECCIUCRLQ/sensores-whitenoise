from Equipo import Equipo
class SensorId:

	# Constructor
	def __init__(self, valores = [Equipo.whitenoise,0,0,0]):
		self.group_id = valores[0]
		self.pos1 = valores[1]
		self.pos2 = valores[2]
		self.pos3 = valores[3]

	def __repr__(self):
		return "SensorId()"

	def __str__(self):
		return "grupo -> %s (%s) id -> %s %s %s" % (self.group_id.name, self.group_id.value, self.pos1, self.pos2, self.pos3)

	def set_group_id(self, value):
		if not isinstance(value, Equipo):
			raise TypeError("El tipo esperado para group_id es Equipo")
		self.__group_id = value

	def get_group_id(self):
		return self.__group_id

	def set_pos1(self, value):
		if (value < 0 or value > 255):
			raise TypeError("El valor para pos1 esta fuera del rango permitido.")
		self.__pos1 = value

	def get_pos1(self):
		return self.__pos1

	def set_pos2(self, value):
		if (value < 0 or value > 255):
			raise TypeError("El valor para pos2 esta fuera del rango permitido.")
		self.__pos2 = value

	def get_pos2(self):
		return self.__pos2

	def set_pos3(self, value):
		if (value < 0 or value > 255):
			raise TypeError("El valor para pos3 esta fuera del rango permitido.")
		self.__pos3 = value

	def get_pos3(self):
		return self.__pos3

	group_id = property(get_group_id, set_group_id)
	pos1 = property(get_pos1, set_pos1)
	pos2 = property(get_pos2, set_pos2)
	pos3 = property(get_pos3, set_pos3)
