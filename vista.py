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
        menuDeHoy[indince] = str(hojaAlimentos["Nombre"].loc[fila])
        #Creamos el % de lo que hemos comido sobre la barra de progreso.
        actualizarBarra(menuDeHoy,hojaAlimentos.loc[fila],barProgTotal,datosAlimCliente,listMacDiarios,style)
        #barProgTotal['value'] = int((100*datosAlimCliente[0])/listMacDiarios[0]);
        #Desabilitamos los botones
        for i in arrrayBoton.values():
            i['state']='disable'
        btnSel.config(text="Editar")
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
    elif(calidad>1.5 and calidad<=2):
        style.configure("yellowgreen.Horizontal.TProgressbar", background='yellow green')
        barProgTotal.config(style="yellowgreen.Horizontal.TProgressbar")
    elif(calidad>2 and calidad<=2.5):
        style.configure("yellow.Horizontal.TProgressbar", background='yellow')
        barProgTotal.config(style="yellow.Horizontal.TProgressbar")
    elif(calidad>2.5 and calidad<3):
        style.configure("orange.Horizontal.TProgressbar", background='orange')
        barProgTotal.config(style="orange.Horizontal.TProgressbar")
    elif(calidad>3 and calidad<3.6):
        style.configure("yellow.Horizontal.TProgressbar", background='orange red')
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

def refrescar(selfi,tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect,style):
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
    #Configuramos los values
    i=0;
    for k in dictBotones.keys():
        boton = dictBotones[k];
        nombre=str(i)+") "+str(listaFiltrada["Nombre"].iloc[i])+" ("+ str(listaFiltrada["Calorias"].iloc[i])+"Kcal)"
        boton.config(text=nombre,command=partial(MostrarInfo,i,listaFiltrada, etiquetaInfor))
        i=i+1;

    #Hacemos una llamada recursiva al propio procedimiento
    btnSelect.config(command=partial(seleccionarYActualizarResto,selfi,tipoComida,dictBotones,btnSelect,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaFiltrada,barProgTotal,listMacDiarios,style,umbral))
    btnRefresh.config(command=partial(refrescar,selfi,tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect,style))
 
'''
Muestra la información del checkButton seleccionado
Params: i Indice de la comida en la lista filtrada
Params: tipo Tipo de comida para saber cual es el tipo de desayuno a criptar
'''
def MostrarInfo(i,listaFiltrada,etiquetaComida):
    texto = "Nombre: "+str(listaFiltrada["Nombre"].iloc[i])+" \nCalorias: "+str(listaFiltrada["Calorias"].iloc[i])+"\nGrasa: "+str(listaFiltrada["Grasa"].iloc[i])+" (Saturadas: "+str(listaFiltrada["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(listaFiltrada["Hidratos"].iloc[i])+"(Azucares"+str(listaFiltrada["Azucares"].iloc[i])+")\nProteina "+str(listaFiltrada["Proteina"].iloc[i])+"\nCalidad: "+str(listaFiltrada["Calidad"].iloc[i])
    etiquetaComida.config(text=texto);
'''
Función que sirve de transacción para que al pulsar el botón haga dos funciones y asi mantener la funcionalidad
'''
def seleccionarYActualizarResto(loc,tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios,style,umbral):
    #Llamamos a la función seleccionar
    seleccionar(tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios,style)       
    #Cadena de texto que muestra el menu de hoy
    textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
    #Cambiamos los contenedores de las 5 comidas
    loc.lblDesTotal.config(text=textoTotal)
    loc.lblAlmTotal.config(text=textoTotal)
    loc.lblComTotal.config(text=textoTotal)
    loc.lblMerTotal.config(text=textoTotal)
    loc.lblCenTotal.config(text=textoTotal)
    #Actualizamos el dato de las kcalorias que llevo comidas
    loc.LblLoQueLlevoDes.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoAlm.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoCom.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoMer.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoCen.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    if(tipoComida!="desayuno"):
        if(banderaSelect[0]== False):
            Actualizar(loc,"desayuno",loc.cont_opciones_Des2,loc.filtDesayuno,umbral, loc.desayuno,hojaAlimentos,loc.botonesDes,loc.n_opciones,loc.btnSelDes,loc.btnRefrDes,loc.label_Informacion_comida,loc.listDistribuciónKcal[0],datosAlimCliente,loc.kcal_Por_Dia,loc.listMacDiarios,menuDeHoy,loc.barProgTotal,loc.banderaSelect,loc.style)
    if(tipoComida != "almuerzo"):    
        if(banderaSelect[1]== False):
            #Refrescamos almuerzo
            Actualizar(loc,"almuerzo",loc.cont_opciones_Alm,loc.filtAlmuerzo,umbral, loc.almuerzo,hojaAlimentos,loc.botonesAl,loc.n_opciones,loc.btnSelAlm,loc.btnRefrAlm,loc.label_Informacion_Alm,loc.listDistribuciónKcal[1],datosAlimCliente,loc.kcal_Por_Dia,loc.listMacDiarios,menuDeHoy,loc.barProgTotal,loc.banderaSelect,loc.style)
    if(tipoComida != "comida"):    
        if(banderaSelect[2]== False):
            #Refrescamos comida
            Actualizar(loc,"comida",loc.cont_opciones_Com,loc.filtComida,umbral, loc.comida,hojaAlimentos,loc.botonesCom,loc.n_opciones,loc.btnSelCom,loc.btnRefrCom,loc.label_Informacion_Com,loc.listDistribuciónKcal[2],datosAlimCliente,loc.kcal_Por_Dia,loc.listMacDiarios,menuDeHoy,loc.barProgTotal,loc.banderaSelect,loc.style)
    if(tipoComida != "merienda"):  
        if(banderaSelect[3]== False):
            #Refrescamos merienda
            Actualizar(loc,"merienda",loc.cont_opciones_Mer,loc.filtMerienda,umbral, loc.merienda,hojaAlimentos,loc.botonesMer,loc.n_opciones,loc.btnSelMer,loc.btnRefrMer,loc.label_Informacion_Mer,loc.listDistribuciónKcal[3],datosAlimCliente,loc.kcal_Por_Dia,loc.listMacDiarios,menuDeHoy,loc.barProgTotal,loc.banderaSelect,loc.style)
    if(tipoComida != "cena"):  
        if(banderaSelect[4]== False):
            #Refrescamos cena
            Actualizar(loc,"cena",loc.cont_opciones_Cen,loc.filtCena,umbral, loc.cena,hojaAlimentos,loc.botonesCen,loc.n_opciones,loc.btnSelCen,loc.btnRefrCen,loc.label_Informacion_Cen,loc.listDistribuciónKcal[4],datosAlimCliente,loc.kcal_Por_Dia,loc.listMacDiarios,menuDeHoy,loc.barProgTotal,loc.banderaSelect,loc.style)
'''
Función que refresca la información y aumenta el umbral para que puedas comer "peor"
te destruye la actual ventana y te la vuelve a crear de cero para refrescar.
POR HACER
hay que cambiar la lista de filtrar para que te cargue los nuevos valores.
'''

def Actualizar(selfi,tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect,style):
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
    i=0;
    for k in dictBotones.keys():
        boton = dictBotones[k];
        nombre=str(i)+") "+str(listaFiltrada["Nombre"].iloc[i])+" ("+ str(listaFiltrada["Calorias"].iloc[i])+"Kcal)"
        boton.config(text=str(nombre),command=partial(MostrarInfo,i,listaFiltrada, etiquetaInfor))
        i=i+1;
    btnSelect.config(command=partial(seleccionarYActualizarResto,selfi,tipoComida,dictBotones,btnSelect,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaFiltrada,barProgTotal,listMacDiarios,style,umbral))
    btnRefresh.config(command=partial(refrescar,selfi,tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect,style))
                