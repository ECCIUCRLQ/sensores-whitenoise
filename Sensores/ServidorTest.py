#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import random
import sysv_ipc
from SensorId import SensorId
from Tipo import Tipo
from Equipo import Equipo
from CARRETA import CARRETA
from BUEY import BUEY
from Utilidades import Utilidades

class ServidorTest:

	mq = sysv_ipc.MessageQueue(2424, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)

	@classmethod
	def sendToQueue(cls):
		while True:
			carreta = CARRETA(2, Utilidades.get_unix_time(), SensorId([Equipo(5), 0, 0, 2]), Tipo(2), random.randint(15, 50))
			cls.mq.send(carreta.pack_byte_array())
			time.sleep(0.5)

	@classmethod
	def start(cls):
		try:
			cls.sendToQueue()
		except KeyboardInterrupt:
			print ("\nServidorTest Finalizado...")

#ServidorTest.mq.remove()
ServidorTest.start()