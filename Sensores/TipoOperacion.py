import enum

class TipoOperacion(enum.Enum):
	Guardar = 0
	Pedir = 1
	Recibir = 2
	Error = 3
