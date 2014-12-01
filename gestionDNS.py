#!/usr/bin/env python
# -*- coding: utf-8 -*-

#By: Tedezed
#Python 2.7
#Gestion DNS para bind9 en debian
#OJO! cambia las rutas: ruta y ruta2 por las tuyas ;)
#OJO! ejecutame como ROOT
#EJECUCION DESDE TERMINAL //EJEMPLOS:
#python gestionDNS.py -b inma     => Borra inma del DNS
#python gestionDNS.py -a -dir inma 192.168.2.2 		=> Añade inma con la IP al DNS
#python gestionDNS.py -a -alias correo  inma			=> Añade el alias correo a inma en el DNS
#

import re
import sys
import commands

#Metodo para añadir
def addnoob(ruta,metodo,param1,param2):
	f = open (ruta, "a")
	f.write(param1 + "		IN	" + metodo + "	" + param2 + "\n")
	f.close()

#Metdo para borrar
def delnoob(ruta,re_ex):
	directo = open(ruta,"r")
	list_directo = directo.readlines()
	contador = 0
	list_id_list = []
	for x in list_directo:
		ex_1 = re_ex
		parametro_encontrado = re.findall(ex_1, x)
		if parametro_encontrado != []:
			list_id_list.append(contador)
		contador += 1
	contador = 0
	for x in list_id_list:
		x_final = x-contador
		del list_directo[x_final]
		contador += 1
		final = ''
	try:
		for x in list_directo:
			final = final + x
			f = open (ruta, "w")
			f.write(final)
			f.close()
		print "Parametro encontrado y borrado."
	except:
		print "ERROR-0001: No se encontro el parametro para eliminar."
		final = ''
	print ".................................."
	directo.close()

#Cambia las rutas por las tuyas
ruta = "/etc/bind/db.iesgn.org"
ruta2 = "/etc/bind/db.172.22.2"

#Ejecucion
if len(sys.argv) == 1:
	print "Porfavor introduce alguna opcion. (T__+)"
else:
	parametro = sys.argv[1]
	#Metodo -a para aniadir
	if parametro == "-a":
		#Nuevo nombre de maquina
		if sys.argv[2] == "-dir":
			param1 = sys.argv[3]
			param2 = sys.argv[4]
			metodo = "A"
			addnoob(ruta,metodo,param1,param2)
			metodo = "PTR"
			ip_list = param2.split(".")
			param1 = param1 + '.'
			addnoob(ruta2,metodo,ip_list[3],param1)

		#Nuevo alias de maquina
		if sys.argv[2] == "-alias":
			param1 = sys.argv[3]
			param2 = sys.argv[4]
			metodo = "CNAME"
			addnoob(ruta,metodo,param1,param2)
		print "Configuracion DNS modificada. BIND9"
		print "Reinizando Bind9"
		comando = commands.getoutput("service bind9 restart")
		print comando

	#Metodo -b para borrar
	elif parametro == "-b":
		parametro = sys.argv[2]
		print "Zona Directa:"
		ex_para_del = "^" + parametro
		delnoob(ruta,ex_para_del)
		print "Zona Inversa:"
		ex_para_del = parametro + ".$"
		delnoob(ruta2,ex_para_del)
