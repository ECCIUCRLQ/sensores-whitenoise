from CARRETA import CARRETA
from BUEY import BUEY
from Cliente import Cliente
from Servidor import Servidor
from Utilidades import Utilidades
from SensorId import SensorId
import random

def main():
	opcion = 0
	while not (opcion == 1 or opcion == 2):
		opcion = int(input("Para enviar: 1 \nPara recibir: 2\n"))

	if opcion == 1:
		utilidades = Utilidades()
		carreta = CARRETA()
		carreta.date = utilidades.get_unix_time()
		carreta.sensor_id = SensorId([1,0,0,1])
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
