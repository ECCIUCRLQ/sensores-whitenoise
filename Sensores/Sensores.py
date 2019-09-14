#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from CARRETA import CARRETA
from BUEY import BUEY
from Cliente import Cliente
from Servidor import Servidor
from Utilidades import Utilidades
import random

def main():
	opcion = 0
	while not (opcion == 1 or opcion == 2):
		opcion = int(input("Para enviar: 1 \nPara recibir: 2\n"))

	if opcion == 1:

		utilidades = Utilidades()	
		cliente = Cliente()
		carretas = []

		for i in range(10):
			carreta = CARRETA()
			carreta.sensor_id = 123
			carreta.date = utilidades.get_unix_time()
			carreta.rand_id = random.getrandbits(8)
			carreta.type = 5
			carretas.append(carreta)
			print(carreta)
   
		while len(carretas) > 0:
			carreta = carretas.pop()
			cliente.enviar_paquete(carreta)
	elif opcion == 2:
		Servidor.recibir()

main()