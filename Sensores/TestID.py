from InterfazDistribuida import InterfazDistribuida
from uuid import getnode as get_mac



class TestID:
    def Prueba(self):
        mac = get_mac()
        mac_array = mac.to_bytes(6, 'little')
        #id = InterfazDistribuida()
        print(mac)
        #id.IniciarInterfazDistribuida()

test = TestID()

test.Prueba()
