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

class ServidorTest:

	mq = sysv_ipc.MessageQueue(2424, sysv_ipc.IPC_CREAT, int("0600", 8), 2048)

	@classmethod
	def sendToQueue(cls):
		carreta = CARRETA(2, 0, SensorId([Equipo((int)(sys.argv[1])), 0, 0, 0]), Tipo((int)(sys.argv[2])), 0)
		while True:
			cls.mq.send(carreta.pack_byte_array())
			time.sleep(1)

	@classmethod
	def start(cls):
		try:
			cls.sendToQueue()
		except KeyboardInterrupt:
			print ("\nServidorTest Finalizado...")

#ServidorTest.mq.remove()
ServidorTest.start()