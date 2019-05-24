# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 12:51:31 2019

@author: Jesus
"""

import tkinter as tk;
from tkinter import  messagebox
import AdminBase as ab;
from functools import partial;
import CalculosDieta as cd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
def seleccionar(tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios,style,btnRefresh):
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
        btnRefresh['state']='disable'
        #Cambiamos de valor a la variable
        banderaSelect[indince]=True
    else:
        #Sacamos la fila del alimento, o lo que es lo mismo sus datos.
        if(tipoComida == 'desayuno'):
            fila = ab.getFilaAlimento(menuDeHoy[0],hojaAlimentos)
        if(tipoComida == 'almuerzo'):
            fila = ab.getFilaAlimento(menuDeHoy[1],hojaAlimentos)
        if(tipoComida == 'comida'):
            fila = ab.getFilaAlimento(menuDeHoy[2],hojaAlimentos)
        if(tipoComida == 'merienda'):
            fila = ab.getFilaAlimento(menuDeHoy[3],hojaAlimentos)
        if(tipoComida == 'cena'):
            fila = ab.getFilaAlimento(menuDeHoy[4],hojaAlimentos)
        print('###################################################################################')
        print(hojaAlimentos["Nombre"].loc[fila])
        #Aumentamos el LRE del alimento en cuestión
        hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] -1; 
        datosAlimCliente[0] -= hojaAlimentos["Calorias"].loc[fila] 
        datosAlimCliente[1] -= hojaAlimentos["Grasa"].loc[fila] 
        datosAlimCliente[2] -= hojaAlimentos["Hidratos"].loc[fila] 
        datosAlimCliente[3] -= hojaAlimentos["Proteina"].loc[fila]
        datosAlimCliente[4] -= hojaAlimentos["Calidad"].loc[fila]
        #Restamos el % en la barra
        actualizarBarra(menuDeHoy,hojaAlimentos.loc[fila],barProgTotal,datosAlimCliente,listMacDiarios,style)
        menuDeHoy[indince]=""
        for i in arrrayBoton.values():
            i['state']='normal'
        btnSel.config(text="Seleccionar")
        btnRefresh['state']='normal'
        banderaSelect[indince]=False
'''
Función que actualiza la brra de progesión y la tiñe según el umbra
'''
def actualizarBarra(menuDeHoy,alimento,barProgTotal,datosAlimCliente,listMacDiarios,style):
    n=0;
    calidad = 0;
    for i in menuDeHoy:
        if (i != ""):
            n+=1;
    calidad = datosAlimCliente[4]/n
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
        boton.config(text=nombre,command=partial(MostrarInfo,i,listaFiltrada, etiquetaInfor),value=i, variable=selected)
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
    if(tipoComida == "desayuno"):
        btnRefresh = loc.btnRefrDes;
    if(tipoComida == "almuerzo"):
        btnRefresh = loc.btnRefrAlm;
    if(tipoComida == "comida"):
        btnRefresh = loc.btnRefrCom;
    if(tipoComida == "merienda"):
        btnRefresh = loc.btnRefrMer;
    if(tipoComida == "cena"):
        btnRefresh = loc.btnRefrCen;
    seleccionar(tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios,style,btnRefresh)       
    
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
        boton.config(text=str(nombre),command=partial(MostrarInfo,i,listaFiltrada, etiquetaInfor),value=i, variable=selected)
        i=i+1;
    btnSelect.config(command=partial(seleccionarYActualizarResto,selfi,tipoComida,dictBotones,btnSelect,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaFiltrada,barProgTotal,listMacDiarios,style,umbral))
    btnRefresh.config(command=partial(refrescar,selfi,tipoComida, container,listaFiltrada,umbral,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect,style))
'''
Función que inicializa el array bandera qu se usará para activar o desactivar los radiobutton
de las selecciones de la comida. Coge como parametros el menu diario y haca las comprobaiones.
'''
def crearArrayBandera(menuDeHoy):
    banderaSelect = [False, False, False, False, False]
    for i in range(len(menuDeHoy)):
        if menuDeHoy[i] != "":
            banderaSelect[i]= True;
    return banderaSelect
def gráfico(selfi,x,y):
    selfi.lin.set_data(x,y)
    ax = selfi.canvas.figure.axes[0]
    ax.set_xlim(min(x),max(x))
    ax.set_ylim(0.7,4) 
    selfi.canvas.draw()
def value(hojaUsuarios,selfi,controller):
    fila = ab.getFilaUsuario(selfi.user,hojaUsuarios)
    if(len(selfi.entry_Nom.get()) ==0 or len(selfi.entry_Ape.get()) == 0 or len(selfi.entry_Eda.get()) == 0 or len(selfi.entry_Alt.get()) == 0 or len(selfi.entry_Pes.get()) == 0 or selfi.var.get() == 0 or selfi.varTipo.get() == 0 or selfi.varAct.get() == 0):
        selfi.label_Error.config(text="ERROR: Algun dato erroneo, comprueba todo")
    else:
        try:
            print(int(selfi.entry_Eda.get()))
            print(int(selfi.entry_Pes.get()))
            print(int(selfi.entry_Alt.get()))
            selfi.label_Error.config(text="")
        except ValueError:
            selfi.label_Error.config(text="ERROR: Algun dato erroneo, comprueba todo")
            
       
        hojaUsuarios['nombre'].loc[fila] = selfi.entry_Nom.get()
        hojaUsuarios['apellido'].loc[fila] = selfi.entry_Ape.get()
        if(selfi.var.get() == 1):
            hojaUsuarios['sexo'] .loc[fila]= 'H'
        else:
            hojaUsuarios['sexo'].loc[fila] = 'M'
        hojaUsuarios['edad'].loc[fila] = int(selfi.entry_Eda.get())
        hojaUsuarios['altura'].loc[fila] = int(selfi.entry_Alt.get())
        hojaUsuarios['peso'].loc[fila] = int(selfi.entry_Pes.get())
        hojaUsuarios['actividad'].loc[fila] = selfi.varAct.get()
        if(selfi.varTipo.get() == 1):
            hojaUsuarios['tipo'].loc[fila] = "bajar"
        elif(selfi.varTipo.get() == 2):
            hojaUsuarios['tipo'].loc[fila] = "mantener"
        else:
            hojaUsuarios['tipo'].loc[fila] = "subir"
        ab.guardarUsuario(hojaUsuarios)
        messagebox.showinfo("Datos actualizados","Datos actualizados correctamente, veras los cambios al reiniciar el programa")
def estiloTotal(idEstilo):
    if(idEstilo == 0):
        config=['powder blue','spring green']
    elif(idEstilo == 1):
        config=['thistle1','MediumPurple']
    file = open('config.txt','w')
    texto = config[0]+":"+config[1]
    file.write(texto)
    file.close()
    messagebox.showinfo("!Todo correcto¡","Veras el nuevo diseño cuando reinicie el programa")