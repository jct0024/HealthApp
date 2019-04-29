# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 12:51:31 2019

@author: Jesus
"""

from tkinter import *
from tkinter import ttk,font
import AdminBase as ab;
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
def seleccionar(tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios):
    #Comprobamos si el bton esta en modo editar o seleccionar
    indince = indiceCom(tipoComida)
    if not(banderaSelect[indince]):
        opc=selected.get()
        fila=ab.getFilaAlimento(listaComida["Nombre"].iloc[opc],hojaAlimentos);
        hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
        #Rellenar datos.
        datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
        datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
        datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
        datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
        #Añadimos el desayuno a la opción de que llevamos comido
        menuDeHoy[indince] = hojaAlimentos["Nombre"].loc[fila]
        #Creamos el % de lo que hemos comido sobre la barra de progreso.
        barProgTotal['value'] = int((100*datosAlimCliente[0])/listMacDiarios[0]);
        #Desabilitamos los botones
        for i in arrrayBoton.values():
            i['state']='disable'
        btnSel.config(text="Editar")
        banderaSelect[indince]=True
    else:
        menuDeHoy[indince]=None
        for i in arrrayBoton.values():
            i['state']='enable'
        btnSel.config(text="Seleccionar")
        banderaSelect[indince]=False
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