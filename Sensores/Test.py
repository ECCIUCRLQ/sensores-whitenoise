from AdministradorMemoria import AdministradorMemoria

from struct import *


print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

AdministradorMemoria.write("2x00000", b"A")

AdministradorMemoria.write("0x00000", b"B")

print(AdministradorMemoria.read(2))

print(AdministradorMemoria.read(1))

AdministradorMemoria.write("3x00000", b"C")

AdministradorMemoria.write("1x00000", b"D")