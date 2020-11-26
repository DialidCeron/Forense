#!/usr/bin/python3
"""
Desarrollar un programa que permita recuperar archivos (EXE,ZIP, PNG, JPG, JPEG, otro (elegido por el alumno))
    Archivo de configuración
    Ejecutar por línea de comandos
"""
#Lezly Dialid Ceron Rodriguez
#Modo de ejecucion: ./p3_lceron.py archivo_raw

import struct
import re
import sys
import binascii

def file_to_hex(path):
    """
    Funcion que abre un archivo y convierte su contenido a valor hexadecimal
    Recibe: Ruta del archivo a leer
    Retorna: Lista del contenido en hexadecimal
    """
    file = open(path,'rb') 
    list_hex = [] 
    while True: 
        hexa = struct.unpack('B',file.read(1))[0]
        if not hexa: 
            break 
        list_hex.append(hex(hexa)) 
    return list_hex

def size(string):
    """
    Funcion que convierte una cadena a su correspondiente en bytes.
    Recibe: string con la cadena a convertir
    Retorna: Entero que es la cantidad en bytes.
    """
    match = re.search("(^[0-9]*)([MBK])$", string)
    if match:
        if (match.group(2) == 'K'):
            size = int(match.group(1)) * 1024
        if (match.group(2) == 'M'):
            size = int(match.group(1)) * 1048576
        if (match.group(2) == 'B'):
            size = int(match.group(1))
    return size

def file_conf():
    """
    Funcion que lee el archivo de configuracion y almacena sus valores en un diccionario
    Retorna: Diccionario de configuracion
    """
    config = open("conf.txt",'r')
    lines = config.readlines() 
    config_dicc={}
    for line in lines: 
        match = re.search("^#", line)
        if not match:
            split = line.split(" ")
            config_dicc[split[0]]=[size(split[3]),split[1],split[2]]
    return config_dicc


def create_files():
    """
    Funcion que crea los archivos recuperados
    """
    if len(sys.argv)< 2:
        print("Sintaxis incorrecta")
        print("Sintaxis: ./p3_lceron.py archivo_raw")
        exit()

    recovered_files=[]    
    file = sys.argv[1]
    read_bin=file_to_hex(file)
    config=file_conf()

    for x in config:
        aux=""
        tmp=(config[x][1]).split("0x")[1]
        length=len(tmp)
        if length==4:
            for j in range(0,len(read_bin)-1):
                aux=read_bin[j].split("0x")[1]+read_bin[j+1].split("0x")[1]
                if config[x][1].split("0x")[1]==aux:
                    recovered_files.append([x,j])
        elif length==8:
            for j in range(0,len(read_bin)-3):
                aux=read_bin[j].split("0x")[1]+read_bin[j+1].split("0x")[1]+read_bin[j+2].split("0x")[1]+read_bin[j+3].split("0x")[1]
                if config[x][1].split("0x")[1]==aux:
                    recovered_files.append([x,j])
    i=0
    for x in recovered_files:
        aux=""
        count=0
        for j in range(x[1],len(read_bin)-1):
            if count==config[x[0]][0]:
                break
            aux=aux+read_bin[j].split("0x")[1]
            count+=1
        binary_string = binascii.unhexlify(aux)
        file_r="recuperado"+str(i)+"."+x[0].lower()
        with open(file_r, mode='wb') as file_r:
            file_r.write(binary_string)
        i+=1

if __name__ == '__main__':
    create_files()