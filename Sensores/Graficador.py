#from Interfaz import Interfaz
from SensorId import SensorId
from Equipo import Equipo
from RelacionSensorIdTipo import RelacionSensorIdTipo
from Utilidades import Utilidades

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
import sysv_ipc
from struct import *

class Graficador:

	mq = None

	@classmethod
	def graficar(cls, sensor_id):

		try:
			cls.mq = sysv_ipc.MessageQueue(key = 3333, flags = 0, mode =int("0600", 8),max_message_size = 2048)
		except sysv_ipc.ExistentialError:
			print("La Interfaz no ha sido inicializada!")
			exit(0)

		datos = cls.obtener_datos(sensor_id)

		datos_interpretados = cls.interpretar_datos(sensor_id, datos)

		cls.plotear(sensor_id, datos_interpretados)

		return 0

	@classmethod
	def plotear(cls, sensor_id, data):

		names = list(data.keys())
		values = list(data.values())

		locator = mdates.DayLocator(bymonthday=[1, 15])
		formatter = mdates.DateFormatter('%b %d')

		fig, axs = plt.subplots(1, 2, figsize=(9, 3), sharey=True)
		#axs[0].bar(names, values)
		#axs.xaxis.set_major_locator(locator)
		#axs.xaxis.set_major_formatter(formatter)
		
		axs[0].scatter(names, values)
		axs[1].plot(names, values)
		axs[0].tick_params(axis='x', rotation=70)
		axs[1].tick_params(axis='x', rotation=70)
		fig.suptitle(sensor_id.group_id.name)

		return 0


	@classmethod
	def interpretar_datos(cls, sensor_id, datos):

		tipo_sensor = RelacionSensorIdTipo.ObtenerTipoSensorPorId(sensor_id)
		tamanno_datos = RelacionSensorIdTipo.ObtenerTamannoPorTipoSensor(tipo_sensor)

		if tamanno_datos == 4:
			datos_interpretados = cls.interpretar_datos_solo_fecha(datos)
		elif tamanno_datos == 5:
			datos_interpretados = cls.interpretar_datos_fecha_evento(datos)
		elif tamanno_datos == 8:
			datos_interpretados = cls.interpretar_datos_fecha_valor(datos)

		return datos_interpretados

	@classmethod
	def interpretar_datos_solo_fecha(cls, datos):
		datos_intermedios = [datos[i:i+4] for i in range(0, len(datos), 4)]

		datos_graficar = {}

		# Genera los pares para la graficación
		for dato in datos_intermedios:
			fecha_numero = int(unpack('I', dato)[0])

			fecha_texto = Utilidades.get_date(fecha_numero)

			punto = {fecha_texto : 1}

			datos_graficar.update(punto)

		return datos_graficar

	@classmethod
	def interpretar_datos_fecha_evento(cls, datos):
		datos_intermedios = [datos[i:i+5] for i in range(0, len(datos), 5)]

		datos_graficar = {}

		# Genera los pares para la graficación
		for dato in datos_intermedios:
			fecha_numero, valor = unpack('IB', dato)

			punto = {fecha_numero : valor}

			datos_graficar.update(punto)

		return datos_graficar

	@classmethod
	def interpretar_datos_fecha_valor(cls, datos):
		datos_intermedios = [datos[i:i+8] for i in range(0, len(datos), 8)]

		datos_graficar = {}

		# Genera los pares para la graficación
		for dato in datos_intermedios:
			fecha_numero, valor = unpack('If', dato)

			punto = {fecha_numero : valor}

			datos_graficar.update(punto)

		return datos_graficar

	@classmethod
	def obtener_datos(cls, sensor_id):
		sensor_id_bytes = pack('ssss', sensor_id.group_id.value, sensor_id.pos1, sensor_id.pos2, sensor_id.pos3)
		
		cls.mq.send(sensor_id_bytes, type = cls.READ)

		msg, tipo = cls.mq.receive(block = True, type = cls.DATOS_GRAFICADOR)

		with open("datos_graficador.bin", "rb") as f:
			sensor_data = f.read()

		datos = sensor_data

		#datos = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40'

		return datos

	@classmethod
	def iniciar_graficador(cls):
		try:
			sensor_id_param = sys.argv[1]

			e_id = Equipo(int(sensor_id_param.split(".")[0]))
			s_id = sensor_id_param.split(".")[1]

			sensor_id = SensorId([e_id, int(s_id[0]), int(s_id[1]), int(s_id[2])])

			cls.graficar(sensor_id)

		except KeyboardInterrupt:
			servidor.sock.close()
			print ("\nGraficador Finalizado...")


Graficador.iniciar_graficador()