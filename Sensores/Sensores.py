#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from CARRETA import CARRETA
from BUEY import BUEY
#from Cliente import Cliente
#from Servidor import Servidor
from Utilidades import Utilidades
from SensorId import SensorId
#from Sensor import Sensor
from Tipo import Tipo
from Equipo import Equipo
import random
import time

def main():
	opcion = 0
	while not (opcion == 1 or opcion == 2):
		opcion = int(input("Para enviar: 1 \nPara recibir: 2\n"))
		
	pin_movimiento = 23 #PIR 23
	pin_big_sound = 17 

	if opcion == 1:

   #         #cliente = Cliente()
   #         carretas = []

   #         sensor_id_movimiento = SensorId([1,0,0,1])
   #         sensor_id_big_sound = SensorId([1,0,0,2])

   #         sensor_movimiento = Sensor(sensor_id_movimiento, Tipo.movimiento, pin_movimiento)
   #         sensor_big_sound = Sensor(sensor_id_big_sound, Tipo.big_sound, pin_big_sound)

   #         sensor_movimiento.start_sensor()
   #         sensor_big_sound.start_sensor()

   #         try:
   #             while True:
   #                     time.sleep(100)
   #         except KeyboardInterrupt:
   #                 print ("Sensores Recepcion Finalizado...")

		utilidades = Utilidades() 

		carreta = CARRETA()
		carreta.sensor_id = SensorId([Equipo.whitenoise,0,0,1])
		carreta.date = utilidades.get_unix_time()
		carreta.rand_id = random.getrandbits(8)
		carreta.type = Tipo.movimiento
        #carretas.append(carreta)
		print(carreta)

		ba = carreta.pack_byte_array()

		ncarreta = CARRETA()

		ncarreta.unpack_byte_array(ba)

		buey = BUEY()
		buey.sensor_id = SensorId([Equipo.flamingo_black, 0, 0, 1])

		bab = buey.pack_byte_array();

		nbuey = BUEY()
		nbuey.unpack_byte_array(bab);

		print(buey)

        #while len(carretas) > 0:
                #carreta = carretas.pop()
                #cliente.enviar_paquete(carreta)
	elif opcion == 2:
		Servidor.recibir()

main()
