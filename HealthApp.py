# -*- coding: utf-8 -*-1
import numpy as np;
import AdminBase as ab
#Función que carga la base de datos.
datosAlimCliente = np.zeros(6)
datosAlimTotal = np.zeros(6)
flagMenu = -1;
flagLogIn = False
#Vectores datos alimentos: calorias/grasas/garasas saturadas/hidratos/azucares/proteina
#Cargamos la hoja1 en la cual se encuentran los alimentos con sus macronutrientes.
hojaAlimentos, hojaUsuarios, hojaPatologias = ab.cargarBaseDeDatos()
#print(hojaAlimentos)
while ( flagLogIn == False):
    user = int(input("Introduzca el DNI"))
    pwd = int(input("Introduzca la contraseña"))
    if (ab.comprobarUsuario(user,pwd)):
        print("Bienvenido ", hojaUsuarios.iloc[ab.getFilaUsuario(user),1])
        flagLogIn = True
    else:
        print("Usuario o contraseña erroneos vuelva a intentarlo")
while (flagMenu !=0):
   #Hacer todo lo del menu , opciones para el cliente y demas
   print('1: Mostrar datos del usuario' )
   print('2: Mostrar dieta de hoy')
   print('0: Salir del programa')
   flagMenu = int(input("Introduzca la opción que desea hacer hoy"))
   if (flagMenu==1):
       #Datos del usuario.
       break;
   elif (flagMenu ==2):
       hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
       n_Opciones = 3;
       #Escoger entre opciones el desayuno de hoy:
       while (datosAlimCliente[0] != datosAlimTotal[0]):
           for i in range(n_Opciones):
                print(i, " ",hojaAlimentos["Nombre"].iloc[i])
                opc = int(input("Introduzca la opción que desea desayunar"))
                hojaAlimentos.iloc[opc,8] =hojaAlimentos.iloc[opc,8] + 1
        #Rellenar datos.
       for i in range(datosAlimTotal.size):
          datosAlimCliente[i] = hojaAlimentos.iloc[opc,i+1] + datosAlimCliente[i]
          print(datosAlimCliente)
          hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])

ab.guardarDatos (hojaAlimentos,hojaUsuarios,hojaPatologias)
print("Ya puede cerrar el sistema, hasta pronto:)")