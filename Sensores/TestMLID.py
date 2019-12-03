
from AdministradorMemoria import AdministradorMemoria

datos = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x40'


AdministradorMemoria.inicializar_memoria()

pagina_id = AdministradorMemoria.malloc()

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)


datos = AdministradorMemoria.read(0)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

datos = AdministradorMemoria.read(1)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

datos = AdministradorMemoria.read(2)

datos = AdministradorMemoria.read(3)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)





pagina_id = AdministradorMemoria.malloc()

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

datos = AdministradorMemoria.read(0)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

datos = AdministradorMemoria.read(1)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)

datos = AdministradorMemoria.read(2)

datos = AdministradorMemoria.read(3)

for i in range(0, 79):
	AdministradorMemoria.write(str(pagina_id) + "x00", b'\x01')

pagina_id = AdministradorMemoria.malloc(pagina_id)




#AdministradorMemoria.guardar_datos_ID(1, datos)

#print(AdministradorMemoria.obtener_datos_ID(1, 1))

#print(AdministradorMemoria.obtener_datos_ID(2, 1))

#print(AdministradorMemoria.obtener_datos_ID(3, 1))

#print(AdministradorMemoria.obtener_datos_ID(4, 1))

#print(AdministradorMemoria.obtener_datos_ID(5, 1))