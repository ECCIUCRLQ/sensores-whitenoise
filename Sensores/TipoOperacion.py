import enum

class TipoOperacion(enum.Enum):
	Guardar_QuieroSer = 0
	Pedir_SoyActiva = 1
	Ok_KeepAlive = 2
	Enviar = 3
	Error = 4
	EstoyAqui = 5