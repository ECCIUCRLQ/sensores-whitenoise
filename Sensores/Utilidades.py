import time

def fecha():
	t = int(time.time())
	return t
	
print(time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(fecha())))