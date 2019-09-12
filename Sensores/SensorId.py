class SensorId:

	# Constructor
	def __init__(self, valores = [0,0,0,0]):
		self.group_id = valores[0]
		self.pos1 = valores[1]
		self.pos2 = valores[2]
		self.pos3 = valores[3]

	def __repr__(self):
		return "SensorId()"

	def __str__(self):
		return "\n\tgroup -> %s \n\tsensor_id -> %s %s %s" % (self.group_id, self.pos1, self.pos2, self.pos3)

	def set_group_id(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.__group_id = x

	def get_group_id(self):
		return self.__group_id

	def set_pos1(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.__pos1 = x

	def get_pos1(self):
		return self.__pos1

	def set_pos2(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.__pos2 = x

	def get_pos2(self):
		return self.__pos2

	def set_pos3(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.__pos3 = x

	def get_pos3(self):
		return self.__pos3

	group_id = property(get_group_id, set_group_id)
	pos1 = property(get_pos1, set_pos1)
	pos2 = property(get_pos2, set_pos2)
	pos3 = property(get_pos3, set_pos3)

