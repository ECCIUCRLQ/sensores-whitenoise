#coding utf-8

#from AdministradorMemoria import AdministradorMemoria

from struct import *


#print(AdministradorMemoria.malloc())

#print(AdministradorMemoria.malloc())

#print(AdministradorMemoria.malloc())

#print(AdministradorMemoria.malloc())

#print(AdministradorMemoria.malloc())

#print(AdministradorMemoria.malloc())

#s = "Prueba String"
#s = bytes(s, 'utf-8') 
#datosA = pack("I%ds" % (len(s),), len(s), s)

#for i in range(0, 10):
#	AdministradorMemoria.write("2x00000", datosA)


#ss = "Prueba String 2"
#ss = bytes(ss, 'utf-8') 
#datosB = pack("I", len(ss)) + ss

#for i in range(0, 10):
#	AdministradorMemoria.write("0x00000", datosB)
#	AdministradorMemoria.write("1x00000", datosB)
#	AdministradorMemoria.write("3x00000", datosB)
#	AdministradorMemoria.write("4x00000", datosB)
#	AdministradorMemoria.write("5x00000", datosB)

#print(AdministradorMemoria.read(2))

#print(AdministradorMemoria.read(0))
#print(AdministradorMemoria.read(1))
#print(AdministradorMemoria.read(3))
#print(AdministradorMemoria.read(4))
#print(AdministradorMemoria.read(5))

##sss = "Prueba String 3"
##sss = bytes(sss, 'utf-8') 
##datosC = pack("I", len(sss)) + sss

##AdministradorMemoria.write("3x00000", datosC)

##ssss = "Prueba String 4"
##ssss = bytes(ssss, 'utf-8') 
##datosD = pack("I", len(ssss)) + ssss

##AdministradorMemoria.write("1x00000", datosD)

##print(AdministradorMemoria.read(3))

##print(AdministradorMemoria.read(1))

##print(AdministradorMemoria.read(0))

#AdministradorMemoria.finalizar_memoria()

from Comunicacion import Comunicacion
from PaquetesHelper import PaquetesHelper
from TipoComunicacion import TipoComunicacion
from TipoOperacion import TipoOperacion

class Test():

	datos = b'\x00\x02P\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40'
	
	def Prueba(self, data):
		print(data)

	def RecibirDatos(self):
		com = Comunicacion()

		#com.recibir_paquete_tcp('127.0.0.1', 10000, self.Prueba)

		respuesta = com.enviar_paquete_tcp('192.168.86.180', 10000, self.datos)

		print(respuesta)

		#com.enviar_broadcast(15000, self.datos)

		#com.recibir_broadcast(10002, self.Prueba)

	def Desempaquetar(self):
		paquetes = PaquetesHelper()

		tipo_comunicacion = TipoComunicacion(0)
		tipo_operacion = TipoOperacion(0)
		tam = pack('I', 80)

		# | \x00 | \x02| P\x00\x00\x00 | \x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40
		datossss = b'\x00\x02P\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40'

		paquete = paquetes.desempaquetar(tipo_comunicacion, self.datos)

		datos_nuevos = paquetes.empaquetar(tipo_comunicacion, tipo_operacion, paquete)

		print(self.datos)

		print(datos_nuevos)



test = Test()



test.RecibirDatos()
