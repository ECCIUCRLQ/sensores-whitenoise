from InterfazDistribuida import InterfazDistribuida
from uuid import getnode as get_mac
import socket

import netifaces as ni


class TestID:
    def Prueba(self):
        mac = get_mac()
        mac_array = mac.to_bytes(6, 'little')
        #id = InterfazDistribuida()
        print(mac)
        #id.IniciarInterfazDistribuida()

	def PruebaIP(self):

		ip = socket.gethostbyname(socket.gethostname())

		print(ip)

test = TestID()

test.PruebaIP()
