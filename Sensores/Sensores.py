#!/usr/bin/env python
from SensorId import SensorId
from Tipo import Tipo
from Equipo import Equipo
from Sensor import Sensor
import time

def main():
		
	pin_movimiento = 23 #PIR 23
	pin_big_sound = 17 

	sensor_id_movimiento = SensorId([Equipo.whitenoise,0,0,1])
	sensor_id_big_sound = SensorId([Equipo.whitenoise,0,0,2])

	sensor_movimiento = Sensor(sensor_id_movimiento, Tipo.movimiento, pin_movimiento)
	sensor_big_sound = Sensor(sensor_id_big_sound, Tipo.big_sound, pin_big_sound)

	sensor_movimiento.start_sensor()
	sensor_big_sound.start_sensor()

	try:
	    while True:
	        time.sleep(100)
	except KeyboardInterrupt:
	    print ("Sensores Recepcion Finalizado...")

main()
