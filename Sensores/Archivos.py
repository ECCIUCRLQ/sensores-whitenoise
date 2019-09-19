
class Archivos:

	datos_sensores = "datos_sensores.txt"
	datos_cliente = "datos_cliente.bytes"

	@classmethod
	def leer_linea(cls):
		primera_linea = ""

		with open(cls.datos_sensores, "w+") as archivo:
			primera_linea = archivo.readline()

		return primera_linea

	@classmethod
	def quitar_linea(cls):
		with open(cls.datos_sensores, 'r+') as archivo_entrada:
			linea = archivo_entrada.read().splitlines(True)
		with open(cls.datos_sensores, 'w+') as archivo_salida:
			archivo_salida.writelines(linea[1:])

	@classmethod
	def adjuntar_linea(cls, datos):
		with open(cls.datos_sensores, "a+") as archivo:
			archivo.write(datos)

	@classmethod
	def leer_bytes(cls):
		return 0

	@classmethod
	def quitar_bytes(cls):
		return 0

	@classmethod
	def adjuntar_bytes(cls):
		return 0