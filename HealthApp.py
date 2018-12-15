# -*- coding: utf-8 -*-1
import numpy as np;
import AdminBase as ab;
import CalculosDieta as cd;
#Función que carga la base de datos.
datosAlimCliente = np.zeros(4)
listMacDiarios = np.zeros(4)
flagMenu = -1;
flagLogIn = False
#Vectores datos alimentos: calorias/grasas/garasas saturadas/hidratos/azucares/proteina
#Cargamos la hoja1 en la cual se encuentran los alimentos con sus macronutrientes.
hojaAlimentos, hojaUsuarios, hojaPatologias = ab.cargarBaseDeDatos()
#print(hojaAlimentos)
while ( flagLogIn == False):
    print("Introduzca su DNI:")
    user = int(input(">> "))
    print("Introduzca su contraseña:")
    pwd = int(input(">> "))
    #Indice de la fila del usuario
    n_FilaUser = ab.comprobarUsuario(user,pwd)
    if (n_FilaUser>-1):
        print("Bienvenido ", hojaUsuarios.iloc[ab.getFilaUsuario(user),1])
        flagLogIn = True
    else:
        print("Usuario o contraseña erroneos vuelva a intentarlo")
#Kcalorias que el usuario debe tomar al dia en base a su dieta
kcal_Por_Dia = cd.calculoTMB(hojaUsuarios.iloc[n_FilaUser,:])
listMacDiarios = np.array(cd.distribuciónDeMacronutrientes(kcal_Por_Dia,'normal'))
print(listMacDiarios)
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
       while (datosAlimCliente[0] != listMacDiarios[0]):
           for i in range(n_Opciones):
                print(i, " ",hojaAlimentos["Nombre"].iloc[i])
           opc = int(input("Introduzca la opción que desea desayunar"))
           hojaAlimentos.iloc[opc,8] =hojaAlimentos.iloc[opc,8] + 1
        #Rellenar datos.
           datosAlimCliente[0] = hojaAlimentos.iloc[opc,1] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos.iloc[opc,2] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos.iloc[opc,4] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos.iloc[opc,5] + datosAlimCliente[3]
           print(datosAlimCliente)
           hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])

ab.guardarDatos (hojaAlimentos,hojaUsuarios,hojaPatologias)
print("Ya puede cerrar el sistema, hasta pronto:)")