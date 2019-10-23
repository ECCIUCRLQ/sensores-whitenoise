from SensorId import SensorId
from Equipo import Equipo
from Tipo import Tipo

class RelacionSensorIdTipo:

	@classmethod
	def ObtenerTipoSensorPorId(cls, sensor_id):
		tipo_sensor = 0

		if (sensor_id.group_id == Equipo.whitenoise and sensor_id.pos3 == 1):
		    return Tipo.movimiento.value

		if (sensor_id.group_id == Equipo.whitenoise and sensor_id.pos3 == 2):
		    return Tipo.big_sound.value

		if (sensor_id.group_id == Equipo.flamingo_black and sensor_id.pos3 == 1):
		    return Tipo.movimiento.value

		if (sensor_id.group_id == Equipo.flamingo_black and sensor_id.pos3 == 2):
		    return Tipo.fotoresistor.value

		if (sensor_id.group_id == Equipo.gisso and sensor_id.pos3 == 1):
		    return Tipo.movimiento.value

		if (sensor_id.group_id == Equipo.gisso and sensor_id.pos3 == 2):
		    return Tipo.shock.value

		if (sensor_id.group_id == Equipo.kof and sensor_id.pos3 == 1):
		    return Tipo.movimiento.value

		if (sensor_id.group_id == Equipo.kof and sensor_id.pos3 == 2):
		    return Tipo.touch.value

		if (sensor_id.group_id == Equipo.equipo_404 and sensor_id.pos3 == 1):
		    return Tipo.movimiento.value

		if (sensor_id.group_id == Equipo.equipo_404 and sensor_id.pos3 == 2):
		    return Tipo.humedad.value

		if (sensor_id.group_id == Equipo.equipo_404 and sensor_id.pos3 == 2):
		    return Tipo.temperatura.value

		if (sensor_id.group_id == Equipo.poffis and sensor_id.pos3 == 1):
		    return Tipo.movimiento.value

		if (sensor_id.group_id == Equipo.poffis and sensor_id.pos3 == 2):
		    return Tipo.ultrasonico.value

		if (sensor_id.group_id == Equipo.poffis and sensor_id.pos3 == 2):
		    return Tipo.big_sound_int.value

	@classmethod
	def ObtenerTamannoPorTipoSensor(cls, tipo_sensor):
		if tipo_sensor > 5:
			return 8
		else:
			if tipo_sensor == 3:
				return 5
			else:
				return 4
