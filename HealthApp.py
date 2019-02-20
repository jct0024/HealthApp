# -*- coding: utf-8 -*-1
import numpy as np;
import AdminBase as ab;
import CalculosDieta as cd;
#Variable que almacena lo que lleva comido el cliente
datosAlimCliente = np.zeros(4)
#Variable que almacena lo que tiene que comer
listMacDiarios = np.zeros(4)
flagMenu = -1;
flagLogIn = False
n_Opciones = 3;
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
        print("Bienvenido ", hojaUsuarios.iloc[ab.getFilaUsuario(user,hojaUsuarios),1])
        flagLogIn = True
    else:
        print("Usuario o contraseña erroneos vuelva a intentarlo")
#Kcalorias que el usuario debe tomar al dia en base a su dieta
kcal_Por_Dia = cd.calculoTMB(hojaUsuarios.iloc[n_FilaUser,:])

if (hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(user,hojaUsuarios),9],hojaPatologias)),2] == 'normal' or hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(user,hojaUsuarios),9],hojaPatologias)),2] == 'bajo azucares'):    
    #Lista en la cual se encuentran los macronutrientes que el usuario ha de comer en kcal, hidratos, proteina y grasas
    listMacDiarios = np.array(cd.distribuciónDeMacronutrientes(kcal_Por_Dia,'normal'))
#Distribución en Kcal en desayuno, almuerzo, comido, merienda y cena.
listDistribuciónKcal = np.array(cd.repartoDeKcal(listMacDiarios[0]))
#Sacamos las patologias que tiene el usuario.
if(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),9]>0 and hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),9]<9999):
    datosPatologias = np.array(hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(user,hojaUsuarios),9],hojaPatologias)),:])
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
 
       '''
       ayuda
       '''
       #hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
       desayuno,almuerzo,comida,merienda,cena = cd.listasPorTipo(hojaAlimentos);       
       opc = -1;
       '''
       MEJORAAAAAAAAAAAAAAAAAA
       Umbral es una variable de calidad que va aumentando cada vez que da una vuelta
       Hay que hacer un control de errores, de tal manera que si no hay 3 opciones de umbra 1 (ejemplo), la tercera opción sea de umbral 2
       '''
       #DESAYUNO
       umbral=1
       while (opc==-1 or opc ==3):

           i=0
           umbral = umbral+1;
           desayuno = desayuno.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
           desayuno = cd.OrdMinimaDiferencia(desayuno,listDistribuciónKcal[0])
           filtDesayuno = desayuno.loc[desayuno["Calidad"] <= umbral]
           filtDesayuno = filtDesayuno.sort_values(by=["LRE"])
           while i<n_Opciones:
               print(i, " ",filtDesayuno["Nombre"].iloc[i], " (",filtDesayuno["Calorias"].iloc[i],"Kcal)")
               i=i+1;
           print("3   Refresh")
           opc = int(input("Introduzca la opción que desea desayunar"))
           #Si la opcion es refresh, añadimos a todos un punto al LRE, para que a la siguiente vuelta no aparezcan de nuevo.
           if (opc == 3):
               fila=ab.getFilaAlimento(filtDesayuno["Nombre"].iloc[0],hojaAlimentos);
               hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;  
               fila=ab.getFilaAlimento(filtDesayuno["Nombre"].iloc[1],hojaAlimentos);
               hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;
               fila=ab.getFilaAlimento(filtDesayuno["Nombre"].iloc[2],hojaAlimentos);
               hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
               desayuno["LRE"].iloc[2] = desayuno["LRE"].iloc[2]+1
               desayuno["LRE"].iloc[0] = desayuno["LRE"].iloc[0]+1
               desayuno["LRE"].iloc[1] = desayuno["LRE"].iloc[1]+1
      #Sumamos 1 al LRE, esto indica que lo hemos comido recientemente.
       fila=ab.getFilaAlimento(filtDesayuno["Nombre"].iloc[opc],hojaAlimentos);
       hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;      
        #Rellenar datos.
       datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
       datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
       datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
       datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
       print("Lo que llevamos comido", datosAlimCliente[0])
       print("objetivo: ", listMacDiarios[0])
       #hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
       #ALMUERZO
       umbral=2
       opc = -1;
       while (opc==-1 or opc ==3):
           i=0
           print(almuerzo)
           umbral = umbral+1;
           almuerzo = almuerzo.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
           almuerzo = cd.OrdMinimaDiferencia(almuerzo,listDistribuciónKcal[0])
           filtAlmuerzo = almuerzo.loc[almuerzo["Calidad"] <= umbral]
           filtAlmuerzo = filtAlmuerzo.sort_values(by=["LRE"])
           while i<n_Opciones:
               print(i, " ",filtAlmuerzo["Nombre"].iloc[i], " (",filtAlmuerzo["Calorias"].iloc[i],"Kcal)")
               i=i+1;
           print("3   Refresh")
           opc = int(input("Introduzca la opción que desea desayunar"))
           #Si la opcion es refresh, añadimos a todos un punto al LRE, para que a la siguiente vuelta no aparezcan de nuevo.
           if (opc == 3):
               fila=ab.getFilaAlimento(filtAlmuerzo["Nombre"].iloc[0],hojaAlimentos);
               hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;  
               fila=ab.getFilaAlimento(filtAlmuerzo["Nombre"].iloc[1],hojaAlimentos);
               hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;
               fila=ab.getFilaAlimento(filtAlmuerzo["Nombre"].iloc[2],hojaAlimentos);
               hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
               almuerzo["LRE"].iloc[2] = almuerzo["LRE"].iloc[2]+1
               almuerzo["LRE"].iloc[0] = almuerzo["LRE"].iloc[0]+1
               almuerzo["LRE"].iloc[1] = almuerzo["LRE"].iloc[1]+1
      #Sumamos 1 al LRE, esto indica que lo hemos comido recientemente.
       fila=ab.getFilaAlimento(filtAlmuerzo["Nombre"].iloc[opc],hojaAlimentos);
       hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;      
        #Rellenar datos.
       datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
       datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
       datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
       datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
       print("Lo que llevamos comido", datosAlimCliente[0])
       print("objetivo: ", listMacDiarios[0]+listMacDiarios[1])
       #hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
       
       
       
print("Guardando...")
hojaAlimentos.sort_index(inplace=True);
ab.guardarDatos (hojaAlimentos,hojaUsuarios,hojaPatologias)
print("Ya puede cerrar el sistema, hasta pronto:)")