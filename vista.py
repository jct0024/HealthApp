# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 12:51:31 2019

@author: Jesus
"""

import tkinter as tk;
from tkinter import ttk
import AdminBase as ab;
from functools import partial;
import CalculosDieta as cd
import Main as m;
bandera = False;
usr = 0;
contraseña = "";
'''
Funcion que te comprueba que el usuario y contraseña son correctos
'''
def cambio(usuario,passwd,login,lblU,lblMensaje): 
    if(usuario.get() != '' or passwd.get() != ''):
        if(ab.comprobarUsuario(int(usuario.get()),str(passwd.get())) > -1):        
            global bandera 
            global usr
            global contraseña;
            usr =int(usuario.get())
            contraseña = str(passwd.get())
            bandera = True;
            login.destroy();
        else:
            #lblU.config(foreground='red')
            lblMensaje.config(text="ERROR:usuario o contraseña incorrectos")
'''
Funcion que te devuelve el estado de la bandera
parahacer mas adelante la comprobación, si se ha conectado el usuario exitosamente te bare las caracteristicas del programa
sino se cierra completamente
'''       
def getBandera():
    return bandera;
def getUsuario():
    return usr,contraseña;
def show_frame(frames, page_name):
    '''Show a frame for the given page name'''
    frame = frames[page_name]
    frame.tkraise()
'''
Funcion que te recoge como parametros, el tipo de comida que es, los checkButton sobre los que tiene que actuar
y el btnSel, que es el boton seleccionar que ha de editar.
Una vez seleccionado, te suma a lo que llevas hoy, lo propio de la comida que has seleccionado, y si deseleccionas la comida,
para elegir otra cosa te lo resta
'''
def seleccionar(tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios,style):
    #Comprobamos si el bton esta en modo editar o seleccionar
    indince = indiceCom(tipoComida)
    if not(banderaSelect[indince]):
        opc=selected.get()
        #Sacamos la fila del alimento, o lo que es lo mismo sus datos.
        fila=ab.getFilaAlimento(listaComida["Nombre"].iloc[opc],hojaAlimentos);
        #Aumentamos el LRE del alimento en cuestión
        hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
        #Rellenar datos.
        datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
        datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
        datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
        datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
        datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        #Añadimos el desayuno a la opción de que llevamos comido
        menuDeHoy[indince] = hojaAlimentos["Nombre"].loc[fila]
        #Creamos el % de lo que hemos comido sobre la barra de progreso.
        actualizarBarra(menuDeHoy,hojaAlimentos.loc[fila],barProgTotal,datosAlimCliente,listMacDiarios,style)
        #barProgTotal['value'] = int((100*datosAlimCliente[0])/listMacDiarios[0]);
        #Desabilitamos los botones
        for i in arrrayBoton.values():
            i['state']='disable'
        btnSel.config(text="Editar")
        print(menuDeHoy)
        #Cambiamos de valor a la variable
        banderaSelect[indince]=True
    else:
        opc=selected.get()
        #Sacamos la fila del alimento, o lo que es lo mismo sus datos.
        fila=ab.getFilaAlimento(listaComida["Nombre"].iloc[opc],hojaAlimentos);
        #Aumentamos el LRE del alimento en cuestión
        hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] -1; 
        datosAlimCliente[0] -= hojaAlimentos["Calorias"].loc[fila] 
        datosAlimCliente[1] -= hojaAlimentos["Grasa"].loc[fila] 
        datosAlimCliente[2] -= hojaAlimentos["Hidratos"].loc[fila] 
        datosAlimCliente[3] -= hojaAlimentos["Proteina"].loc[fila]
        #Restamos el % en la barra
        actualizarBarra(menuDeHoy,hojaAlimentos.loc[fila],barProgTotal,datosAlimCliente,listMacDiarios,style)
        menuDeHoy[indince]=""
        for i in arrrayBoton.values():
            i['state']='enable'
        btnSel.config(text="Seleccionar")
        banderaSelect[indince]=False
'''
Función que actualiza la brra de progesión y la tiñe según el umbra
'''
def actualizarBarra(menuDeHoy,alimento,barProgTotal,datosAlimCliente,listMacDiarios,style):
    n=0;
    for i in menuDeHoy:
        if (i != ""):
            n+=1;
    calidad = datosAlimCliente[4]/n
    print(calidad)
    if(calidad<=1.5):      
        style.configure("green.Horizontal.TProgressbar", background='green')         
        barProgTotal.config(style="green.Horizontal.TProgressbar")
    elif(calidad>1.5 or calidad<=3.5):
        style.configure("yellow.Horizontal.TProgressbar", background='yellow')
        barProgTotal.config(style="yellow.Horizontal.TProgressbar")
    else:
        style.configure("red.Horizontal.TProgressbar", background='red')
        barProgTotal.config(style="red.Horizontal.TProgressbar")
    barProgTotal['value'] = int((100*datosAlimCliente[0])/listMacDiarios[0]);

'''
Función Simple que te coge el tipo de comida en forma de string y te devuelve el indice correspondiente a esa comida
'''
def indiceCom(tipoComida):
    if(tipoComida=="desayuno"):
        return 0;
    elif(tipoComida=="almuerzo"):
        return 1;
    elif(tipoComida=="comida"):
        return 2;
    elif(tipoComida=="merienda"):
        return 3;
    elif(tipoComida=="cena"):
        return 4;
'''
Función que edita la información del usuario y guarda los datos.
'''
def editarInf(dictLabelsInfoUsuario,containerPack):
    #Inicilizamos las opciones cerradas
    sexo = ["H","M"]
    actividad = [0,1,2,3,4]
    tipo=["bajar", "mantener","subir"]
    for key in dictLabelsInfoUsuario.keys():
        l = dictLabelsInfoUsuario[key]
        l.destroy()
    txtNombre = ttk.Label(containerPack,text="prueba")
    txtNombre.pack()
'''
Función que refresca la información y aumenta el umbral para que puedas comer "peor"
te destruye la actual ventana y te la vuelve a crear de cero para refrescar.
POR HACER
hay que cambiar la lista de filtrar para que te cargue los nuevos valores.
'''

def refrescar(tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect):
    for cont in range(0,n_opciones):
        fila=ab.getFilaAlimento(listaFiltrada["Nombre"].iloc[cont],hojaAlimentos);
        hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
    #Aumentamos el umbral    
    umbral +=1;
    selected = tk.IntVar()
    #Según la comida que estemos trabajando, se recalcula con el nuevo LRE, se carga y se vueve a ordenar
    if(tipoComida=="desayuno"):
        comida,_,_,_,_ = cd.listasPorTipo(hojaAlimentos);
        comida = comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
    elif(tipoComida=="almuerzo"):
        _,comida,_,_,_ = cd.listasPorTipo(hojaAlimentos);
        comida = comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
    elif(tipoComida=="comida"):
        _,_,comida,_,_ = cd.listasPorTipo(hojaAlimentos);
        comida = comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Hidratos'],ascending=False).sort_values(by=['Proteina'],ascending=False)
    elif(tipoComida=="merienda"):
        _,_,_,comida,_ = cd.listasPorTipo(hojaAlimentos);
        comida = comida.sort_values(by=['Hidratos'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Grasa'],ascending=False)
    elif(tipoComida=="cena"):
        _,_,_,_,comida = cd.listasPorTipo(hojaAlimentos);
        comida = comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
    comida = comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
    comida = cd.OrdMinimaDiferencia(comida,listDistribuciónKcal,"desayuno",datosAlimCliente,kcal_Por_Dia)
    #Sustituimos la listaFiltrada con los nuevos valores.
    listaFiltrada = comida.loc[comida["Calidad"] <= umbral]
    listaFiltrada = listaFiltrada.sort_values(by=["LRE"])
    #Borramos las opciones viejas
    for k in dictBotones.keys():
        boton = dictBotones[k];
        boton.destroy()
    #Vaciamos el array
    dictBotones={}
    i=0;
    #Añadimos un nuevo array
    while(i<n_opciones):
        nombre=str(i)+") "+str(listaFiltrada["Nombre"].iloc[i])+" ("+ str(listaFiltrada["Calorias"].iloc[i])+"Kcal)"
        rad1 = ttk.Radiobutton(container,text=str(nombre), value=i,variable=selected,command=partial(MostrarInfo,i,listaFiltrada, etiquetaInfor))
        #rad1['state']='disable' #DESABILITAMOS LOS BOTONES.
        rad1.pack(anchor=tk.W)
        nomb = "boton"+str(i)
        dictBotones[nomb]=rad1
        i=i+1;
    #Hacemos una llamada recursiva al propio procedimiento
    #tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios
    btnSelect.config(command=partial(seleccionar,tipoComida,dictBotones,btnSelect,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaFiltrada,barProgTotal,listMacDiarios))
    btnRefresh.config(command=partial(refrescar,tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios))
'''
Muestra la información del checkButton seleccionado
Params: i Indice de la comida en la lista filtrada
Params: tipo Tipo de comida para saber cual es el tipo de desayuno a criptar
'''
def MostrarInfo(i,listaFiltrada,etiquetaComida):
    texto = "Nombre: "+str(listaFiltrada["Nombre"].iloc[i])+" \nCalorias: "+str(listaFiltrada["Calorias"].iloc[i])+"\nGrasa: "+str(listaFiltrada["Grasa"].iloc[i])+" (Saturadas: "+str(listaFiltrada["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(listaFiltrada["Hidratos"].iloc[i])+"(Azucares"+str(listaFiltrada["Azucares"].iloc[i])+")\nProteina "+str(listaFiltrada["Proteina"].iloc[i])+"\nCalidad: "+str(listaFiltrada["Calidad"].iloc[i])
    etiquetaComida.config(text=texto);
