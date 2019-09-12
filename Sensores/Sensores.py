from CARRETA import CARRETA
from BUEY import BUEY
from Cliente import Cliente
from Servidor import Servidor
import Utilidades
import random

def main():
	opcion = 0
	while not (opcion == 1 or opcion == 2):
		opcion = int(input("Para enviar: 1 \nPara recibir: 2\n"))

	if opcion == 1:
		carreta = CARRETA()
		carreta.date = Utilidades.getUnixTime()
		carreta.sensor_id = 123
		carreta.rand_id = random.getrandbits(8)
		carreta.type = 2

		print(carreta)

		ba = carreta.pack_byte_array()

		ab = carreta.unpack_byte_array(ba)

		cliente = Cliente()

		cliente.enviar_paquete(carreta)

	elif opcion == 2:
		Servidor.recibir()

main()
