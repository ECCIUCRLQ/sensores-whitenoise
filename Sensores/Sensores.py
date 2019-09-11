from CARRETA import CARRETA
from BUEY import BUEY
from Cliente import Cliente

def main():
	print("Hola")

	carreta = CARRETA()
	carreta.date = 12;

	ba = carreta.pack_byte_array()

	ab = carreta.unpack_byte_array(ba);

	cliente = Cliente()

	cliente.enviar_paquete(carreta)

	print(ba)

	print(ab)

main()