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
		carreta = CARRETA()
		carreta.date = utilidades.get_unix_time()
		carreta.sensor_id = 123
		carreta.rand_id = random.getrandbits(8)
		carreta.type = 2

		carreta2 = CARRETA()
		carreta2.date = utilidades.get_unix_time()
		carreta2.sensor_id = 345
		carreta2.rand_id = random.getrandbits(8)
		carreta2.type = 2

		print(carreta)

		ba = carreta.pack_byte_array()

		ab = carreta.unpack_byte_array(ba)

		cliente = Cliente()

		cliente.enviar_paquete(carreta)
		cliente.enviar_paquete(carreta2)

	elif opcion == 2:
		Servidor.recibir()

main()