import time
import os
import signal

# Inicia Interfaz del Administrador de Memoria
Interfaz_pid = os.fork()
if Interfaz_pid == 0:
    os.execlp("python3.7", "python3.7", "/home/silvio/Desktop/U/PIRedesOperativos/Proyecto-pi/sensores-whitenoise/Sensores/Interfaz.py")

time.sleep(1)

# Inicia proceso Recolector
Recolector_pid = os.fork()
if Recolector_pid == 0:
    os.execlp("python3.7", "python3.7", "/home/silvio/Desktop/U/PIRedesOperativos/Proyecto-pi/sensores-whitenoise/Sensores/Recolector.py")

# Inicia proceso Graficador

Graficador_pid = os.fork()
if Graficador_pid == 0:
    os.execlp("gnome-terminal", "gnome-terminal", "-e" , "python3.7 GraficadorTest.py")

input()
os.kill(Recolector_pid, signal.SIGKILL)
print ("Recolector Finalizo")
os.kill(Interfaz_pid, signal.SIGKILL)
print ("Interfaz Finalizo")
#os.kill(Graficador_pid, signal.SIGHUP)
#print ("Graficador Finalizo")