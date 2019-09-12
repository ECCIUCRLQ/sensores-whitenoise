import time

class Utilidades:

	@classmethod
	def get_unix_time(cls):
		t = int(time.time())
		return t

	@classmethod
	def get_date(cls, t):
		return time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(t))
