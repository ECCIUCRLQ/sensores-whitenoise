import enum

class TipoOperacion(enum.Enum):
	Guardar = 0
	Pedir = 1
	Recibir = 2
	Ok = 3
	Error = 4
