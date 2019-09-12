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
    		return "\n\tgroup -> %s \n\tsensor_id -> %s %s %s" % (Sensor_Id.group_id, Sensor_Id.pos1, Sensor_Id.pos2, Sensor_Id.pos3)

	def set_group_id(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.__group_id = x

	def get_group_id(self):
		return self.group_id

	def set_pos1(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.pos1 = x

	def get_pos1(self):
		return self.pos1

	def set_pos2(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.pos2 = x

	def get_pos2(self):
		return self.pos2

	def set_pos3(self, x):
		if (x < 0 or x > 255):
			raise TypeError("Value esta fuera del rango")
		self.pos3 = x

	def get_pos3(self):
		return self.pos3

	group_id = property(get_group_id, set_group_id)
	pos1 = property(get_pos1, set_pos1)
	pos2 = property(get_pos2, set_pos2)
	pos3 = property(get_pos3, set_pos3)

