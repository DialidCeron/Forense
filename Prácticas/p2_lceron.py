#!/usr/bin/python3
#Lezly Dialid Ceron Rodriguez

#Modo de ejecucion: ./p2_lceron.py
"""
Práctica 02 - Programa particiones

Desarrollar un programa que permita particionar (la escritura debe realizarse a nivel de bytes)

•Debe soportar al menos 5 tipos diferentes de sistema de archivos

•Similar a fdisk (opción 'n' y permitir definir el tamaño (K,M,G))

•Solamente se pide crear las particiones

•Leer el dispositivo o archivo con fdisk al concluir para comprobar el funcionamiento del programa
"""

from datetime import datetime
import struct

def newPartition(type, size, dev, part):
	little_endian = struct.pack("<I", size)
	with open(dev, "wb") as disk:
		disk.seek(446+part,0)
		disk.write(bytes([0x00]))

		disk.seek(450+part,0)
		disk.write(type)

		disk.seek(447+part,0)
		disk.write(bytes([0x20]))
		disk.seek(448+part,0)
		disk.write(bytes([0x20]))
		disk.seek(449+part,0)
		disk.write(bytes([0x20]))
		disk.seek(451+part,0)
		disk.write(bytes([0x20]))
		disk.seek(452+part,0)
		disk.write(bytes([0x20]))
		disk.seek(453+part,0)
		disk.write(bytes([0x20]))
		disk.seek(454+part,0)
		disk.write(bytes([0x20]))
		disk.seek(455+part,0)
		disk.write(bytes([0x20]))
		disk.seek(456+part,0)
		disk.write(bytes([0x20]))
		disk.seek(457+part,0)
		disk.write(bytes([0x20]))

		disk.seek(458+part,0)
		disk.write(bytes([little_endian[0]]))
		disk.seek(459+part,0)
		disk.write(bytes([little_endian[1]]))
		disk.seek(460+part,0)
		disk.write(bytes([little_endian[2]]))
		disk.seek(461+part,0)
		disk.write(bytes([little_endian[3]]))

		disk.seek(510,0)
		disk.write(bytes([0x55]))
		disk.seek(511,0)
		disk.write(bytes([0xaa]))

		print("Particion creada exitosamente")
def defineType():
	type = b"\x00"
	print("1. Windows\n2. Linux\n3. Linux swap/Solaris\n4. FAT16\n5. Extendida")
	tmp = input("Selecciona el tipo de particion a crear: ")
	if(tmp is "1"):
		type = b"\x07"
	elif(tmp is "2"):
		type = b"\x83"
	elif(tmp is "3"):
		type = b"\x82"
	elif(tmp is "4"):
		type = b"\x06"
	elif(tmp is "5"):
		type = b"\x05"
	else:
		defineType()
	return type

def defineSize():
	tmp = input("Ingresa el tamaño de la particion a crear Ejemplo 100K(K,G,M): ")
	if ("K" in tmp[-1]):
		return int(tmp[:-1])*2
	elif ("M" in tmp[-1]):
		return int(tmp[:-1])*2048
	elif ("G" in tmp[-1]):
		return int(tmp[:-1])*2097152
	else:
		return 0

def defineDevice():
 	dev=input("Introduce el dispositivo a particionar: ")
 	path="/dev/"
 	if dev.startswith(path):
 		path = dev
 		return path
 	else:
 		path=path+dev
 		return path

def numberPartition():
	number=input("Introduce el id de particion en disco(1-4): ")
	part=0
	if (number is "1"):
		part=0
	elif (number is "2"):
		part=16
	elif (number is "3"):
		part=32
	elif (number is "4"):
		part=48
	else:
		numberPartition()
	return part

if __name__ == "__main__":
	print("-" *50)
	print("Bienvenido al creador de particiones")   
	print("Hora de ejecucion: "+str(datetime.now()))
	print("-" *50)
	type=defineType()
	size=defineSize()
	device=defineDevice()
	number=numberPartition()
	newPartition(type, size, device, number)