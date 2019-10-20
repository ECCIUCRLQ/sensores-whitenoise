from AdministradorMemoria import AdministradorMemoria

from struct import *


print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

print(AdministradorMemoria.malloc())

s = "Prueba String"
s = bytes(s, 'utf-8') 
datosA = pack("I%ds" % (len(s),), len(s), s)

AdministradorMemoria.write("2x00000", datosA)

ss = "Prueba String 2"
ss = bytes(ss, 'utf-8') 
datosB = pack("I", len(ss)) + ss

AdministradorMemoria.write("0x00000", datosB)

print(AdministradorMemoria.read(2))

print(AdministradorMemoria.read(1))

sss = "Prueba String 3"
sss = bytes(sss, 'utf-8') 
datosC = pack("I", len(sss)) + sss

AdministradorMemoria.write("3x00000", datosC)

ssss = "Prueba String 4"
ssss = bytes(ssss, 'utf-8') 
datosD = pack("I", len(ssss)) + ssss

AdministradorMemoria.write("1x00000", datosD)

print(AdministradorMemoria.read(3))

print(AdministradorMemoria.read(1))

print(AdministradorMemoria.read(0))