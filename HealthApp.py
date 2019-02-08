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
#Cargamos las hojas donde se encuentran las diferentes bases de datos.
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
#Lista en la cual se encuentran los macronutrientes que el usuario ha de comer en kcal, hidratos, proteina y grasas
if (hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(user),9])),2] == 'normal' or hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(user),9])),2] == 'baja azucares'):    
    listMacDiarios = np.array(cd.distribuciónDeMacronutrientes(kcal_Por_Dia,'normal'))
    print('hola')
#Distribución en Kcal en desayuno, almuerzo, comido, merienda y cena.
listDistribuciónKcal = np.array(cd.repartoDeKcal(listMacDiarios[0]))
#Sacamos las patologias que tiene el usuario.
if(hojaUsuarios.iloc[int(ab.getFilaUsuario(user)),9]>0 and hojaUsuarios.iloc[int(ab.getFilaUsuario(user)),9]<9999):
    datosPatologias = np.array(hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(user),9])),:])
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
       #Mientras las kcal que el cliente lleva, no supere las del desayuno, seguir preguntando.
       while (datosAlimCliente[0] <= listDistribuciónKcal[0]):
           print()
           i=0
           #Variable que lleva un "puntero" de las opciones que nos muestra sobre la base de datos
           #para mas tarde poder elegir una opción
           localizadorDeAli=0;
           while i<3:
               if(cd.esDesayuno(int(hojaAlimentos["Tipo"].iloc[localizadorDeAli]))):
                   print(i, " ",hojaAlimentos["Nombre"].iloc[localizadorDeAli])
                   if i == 0:
                       al1= localizadorDeAli;
                   elif i == 1:
                       al2=localizadorDeAli;
                   elif i== 2:
                       al3 = localizadorDeAli
                   i=i+1;
               localizadorDeAli = localizadorDeAli+1;
           opc = int(input("Introduzca la opción que desea desayunar"))
           if opc == 0:
               hojaAlimentos.iloc[al1,8] =hojaAlimentos.iloc[al1,8] + 1
           elif opc == 1:
               hojaAlimentos.iloc[al2,8] =hojaAlimentos.iloc[al2,8] + 1
           elif opc== 2:
               hojaAlimentos.iloc[al3,8] =hojaAlimentos.iloc[al3,8] + 1
           
        #Rellenar datos.
           datosAlimCliente[0] = hojaAlimentos.iloc[opc,1] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos.iloc[opc,2] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos.iloc[opc,4] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos.iloc[opc,6] + datosAlimCliente[3]
           print("Lo que llevamos comido", datosAlimCliente[0])
           print("objetivo: ", listDistribuciónKcal[0])
           hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])

ab.guardarDatos (hojaAlimentos,hojaUsuarios,hojaPatologias)
print("Ya puede cerrar el sistema, hasta pronto:)")