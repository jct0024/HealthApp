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
from PIL import ImageTk, Image
bandera = False;
usr = 0;
contraseña = "";
'''
Funcion que te comprueba que el usuario y contraseña son correctos Y te cambia de pantalla 
en caso de que el inicio de sesión haya sido satisfactorio.
Parametros:
    usuaio - Usuario que intenta iniciar sesión
    passwd - Contraseña insertada por el usuario
    login - Pantalla principal en la que nos encontramos.
    lblMensjae - Etiqueta del mensaje de error.
'''
def cambio(usuario,passwd,login,lblMensaje): 
    try:
        if(usuario.get() != '' and passwd.get() != ''):
            if(ab.comprobarUsuario(int(usuario.get()),str(passwd.get())) > -1):        
                global bandera 
                global usr
                global contraseña;
                usr =int(usuario.get())
                contraseña = str(passwd.get())
                bandera = True;
                login.destroy();
            else:
                lblMensaje.config(text="ERROR:usuario o contraseña incorrectos")
    except ValueError:
        blMensaje.config(text="ERROR INESPERADO")
'''
Funcion que te devuelve el estado de la bandera
para hacer mas adelante la comprobación, si se ha conectado el usuario exitosamente te bare las caracteristicas del programa
sino se cierra completamente
'''       
def getBandera():
    return bandera;
'''
Función que devuelve el usuario y contraseña actual.
'''
def getUsuario():
    return usr,contraseña;
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
Función que actualiza la barra de progesión y la tiñe según el umbra
'''
def actualizarBarra(menuDeHoy,alimento,barProgTotal,datosAlimCliente,listMacDiarios,style):
    n=0;
    calidad = 0;
    for i in menuDeHoy:
        if (i != ""):
            n+=1;
    if not (n == 0):
        calidad = datosAlimCliente[4]/n
    else:
        calidad=0;
    if(calidad<=1.5):      
        style.configure("green.Horizontal.TProgressbar", background='lime green')         
        barProgTotal.config(style="green.Horizontal.TProgressbar")
    elif(calidad>1.5 and calidad<=2.4):
        style.configure("yellowgreen.Horizontal.TProgressbar", background='lawn green')
        barProgTotal.config(style="yellowgreen.Horizontal.TProgressbar")
    elif(calidad>2.4 and calidad<=3.4):
        style.configure("yellow.Horizontal.TProgressbar", background='gold')
        barProgTotal.config(style="yellow.Horizontal.TProgressbar")
    elif(calidad>3.4 and calidad<4.4):
        style.configure("orange.Horizontal.TProgressbar", background='orange')
        barProgTotal.config(style="orange.Horizontal.TProgressbar")
    elif(calidad>4.4 and calidad<4.8):
        style.configure("yellow.Horizontal.TProgressbar", background='orange red')
        barProgTotal.config(style="yellow.Horizontal.TProgressbar")
    else:
        style.configure("red.Horizontal.TProgressbar", background='red')
        barProgTotal.config(style="red.Horizontal.TProgressbar")
    barProgTotal['value'] = int((100*calidad)/5);

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

def refrescar(selfi,tipoComida, container,listaFiltrada,umb,comida,hojaAlimentos, dictBotones,n_opciones,btnSelect,btnRefresh,etiquetaInfor,listDistribuciónKcal,datosAlimCliente,kcal_Por_Dia,listMacDiarios,menuDeHoy,barProgTotal,banderaSelect,style):
    for cont in range(0,n_opciones):
        fila=ab.getFilaAlimento(listaFiltrada["Nombre"].iloc[cont],hojaAlimentos);
        hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
    #Aumentamos el umbral    
    umbral =umb+0.4;
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
    comida = cd.OrdMinimaDiferencia(comida,listDistribuciónKcal,"desayuno",datosAlimCliente,kcal_Por_Dia,listMacDiarios)
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
    cal = CalidadNumberToString(listaFiltrada["Calidad"].iloc[i])
    texto = "Nombre: "+str(listaFiltrada["Nombre"].iloc[i])+" \nCalorias: "+str(listaFiltrada["Calorias"].iloc[i])+"\nGrasa: "+str(listaFiltrada["Grasa"].iloc[i])+" (Saturadas: "+str(listaFiltrada["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(listaFiltrada["Hidratos"].iloc[i])+"(Azucares"+str(listaFiltrada["Azucares"].iloc[i])+")\nProteina "+str(listaFiltrada["Proteina"].iloc[i])+"\nCalidad: "+cal
    etiquetaComida.config(text=texto);
'''
Función que recoge el valor númerico de la calidad calculado por el algoritmo nutriscore y te
devuelve la letra correspondiente a dicha calidad
'''
def CalidadNumberToString(calidad):
    cal=""
    calid = calidad;
    if(calid == 1):
        cal= 'A'
    elif(calid ==2):
        cal= 'B'
    elif(calid ==3):
        cal= 'C'
    elif(calid ==4):
        cal= 'D'
    elif(calid ==5):
        cal= 'E' 
    return cal;
'''
Función que sirve de transacción para que al pulsar el botón haga dos funciones y asi mantener la funcionalidad
'''
def seleccionarYActualizarResto(loc,tipoComida,arrrayBoton,btnSel,selected,banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,listaComida,barProgTotal,listMacDiarios,style,umbral):
    #Recogemos el boton refrescar concreto pues solo necesitamos pasar uno por parametro 
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
    
    #Cambiamos los contenedores de las 5 comidas
    loc.lblDesTotal.config(text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]))
    loc.lblAlmTotal.config(text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]))
    loc.lblComTotal.config(text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]))
    loc.lblMerTotal.config(text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]))
    loc.lblCenTotal.config(text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]))
    #Actualizamos el dato de las kcalorias que llevo comidas
    loc.LblLoQueLlevoDes.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoAlm.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoCom.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoMer.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    loc.LblLoQueLlevoCen.config(text="Llevo Comido: "+str(datosAlimCliente[0])+" Kcal")
    umbral=1;
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
    comida = cd.OrdMinimaDiferencia(comida,listDistribuciónKcal,"desayuno",datosAlimCliente,kcal_Por_Dia,listMacDiarios)
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
'''
Función que representa el gráfico en patanlla.
Recibe como parametros:
    selfi - Todas las variables locales de la clase
    x - Eje x en formato de fecha
    y - Eje y con el valor de la calidad
    badera- Valor que indica que tipo de gráfico es.
'''
def gráfico(selfi,x,y,bandera):
    numero=[]
    i=0
    for index in x:
        numero.append(i)
        i+=1
    #selfi.lin.set_xticks(np.range(len(x)),x)
    selfi.lin.set_data(numero,y)
    ax = selfi.canvas.figure.axes[0]
    if(bandera==0):
        ax.set_title("DESAYUNO")
    elif(bandera==1):
        ax.set_title("ALMUERZO")
    elif(bandera==2):
        ax.set_title("COMIDA")
    elif(bandera==3):
        ax.set_title("MERIENDA")
    elif(bandera==4):
        ax.set_title("CENA")
    else:
        ax.set_title("Media del día")
    #Ponemos las etiquetas
    ax.set_xlabel("Dias")
    ax.set_ylabel("Calidad")
    #Cambiamos el valor númerico por el de la fecha
    ax.set_xticks(numero)
    ax.set_xticklabels(x)
    #Implantamos los máximos y minimos
    ax.set_xlim(min(numero),max(numero))
    ax.set_ylim(0.7,5) 
    #Se dibuja en pantalla-
    selfi.canvas.draw()
'''
Función que carga y almacena el nuevo estilo seleccionado para la aplicación.
Parametros:
    idEstilo = Id del estilo a almacenar
'''  
def estiloTotal(idEstilo):
    if(idEstilo == 0):
        config=['powder blue','spring green']
    elif(idEstilo == 1):
        config=['thistle1','MediumPurple']
    file = open('Dat/config.txt','w')
    texto = config[0]+":"+config[1]
    file.write(texto)
    file.close()
    messagebox.showinfo("!Todo correcto¡","Veras el nuevo diseño cuando reinicie el programa")
'''
Función que muestra por pantalla el formulario para crear un nuevo usuario.
Parametros:
    hojaUsuarios - Array de la base de datos de los usuarios.
    hojaPatologias - Array de la base de datos de las patologias.
'''
def registrarse(hojaUsuarios,hojaPatologias):
    #login.destroy()
    
    registro = tk.Tk();
    registro.resizable(0,0)
    registro.geometry('700x350')
    registro.title("Registro")
    #lista = np.aray(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),:])
    label = tk.Label(registro, text="Rellene los datos")    
    label.pack()
    containerDNI = tk.Frame(registro)
    containerNOM = tk.Frame(registro)
    containerAPE = tk.Frame(registro)
    containerPWD = tk.Frame(registro)
    containerSEX = tk.Frame(registro)
    containerEDA = tk.Frame(registro)
    containerALT = tk.Frame(registro)
    containerPES = tk.Frame(registro)
    containerACT = tk.Frame(registro)
    containerPAT = tk.Frame(registro)
    containerTIP = tk.Frame(registro)
    containerBut = tk.Frame(registro)
    containerERR = tk.Frame(registro)
    containerDNI.pack(fill=tk.X)
    containerNOM.pack(fill=tk.X)
    containerAPE.pack(fill=tk.X)
    containerPWD.pack(fill=tk.X)
    containerSEX.pack(fill=tk.X)
    containerEDA.pack(fill=tk.X)
    containerALT.pack(fill=tk.X)
    containerPES.pack(fill=tk.X)
    containerACT.pack(fill=tk.X)
    containerPAT.pack(fill=tk.X)
    containerTIP.pack(fill=tk.X)
    containerBut.pack(fill=tk.X)
    containerERR.pack(fill=tk.BOTH)
    label_Dni = tk.Label(containerDNI, text="DNI",width=20,font=("bold", 10))
    label_Dni.pack(side=tk.LEFT)
    
    entry_Dni = tk.Entry(containerDNI)
    entry_Dni.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    label_Pwd = tk.Label(containerPWD, text="Contraseña",width=20,font=("bold", 10))
    label_Pwd.pack(side=tk.LEFT)
    
    entry_Pwd = tk.Entry(containerPWD)
    entry_Pwd.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    label_Nom = tk.Label(containerNOM, text="Nombre",width=20,font=("bold", 10))
    label_Nom.pack(side=tk.LEFT)
    
    entry_Nom = tk.Entry(containerNOM)
    entry_Nom.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    
    label_Ape = tk.Label(containerAPE, text="Apellido",width=20,font=("bold", 10))
    label_Ape.pack(side=tk.LEFT)       
    
    entry_Ape = tk.Entry(containerAPE)
    entry_Ape.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    label_Eda = tk.Label(containerEDA, text="Edad (Años)",width=20,font=("bold", 10))
    label_Eda.pack(side=tk.LEFT)    
    
    entry_Eda = tk.Entry(containerEDA)
    entry_Eda.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    label_Alt = tk.Label(containerALT, text="Altura (cm)",width=20,font=("bold", 10))
    label_Alt.pack(side=tk.LEFT)      
    
    entry_Alt = tk.Entry(containerALT)
    entry_Alt.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    label_Pes = tk.Label(containerPES, text="Peso (Kg)",width=20,font=("bold", 10))
    label_Pes.pack(side=tk.LEFT)      
    
    entry_Pes = tk.Entry(containerPES)
    entry_Pes.pack(expand=1,fill=tk.BOTH,side=tk.LEFT)
    
    label_3 = tk.Label(containerSEX, text="Sexo:",width=20,font=("bold", 10))
    label_3.pack(side=tk.LEFT)
    varSex = tk.StringVar(registro)
    tk.Radiobutton(containerSEX, text="Hombre",padx = 5, variable=varSex, value='H').pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerSEX, text="Mujer",padx = 20, variable=varSex, value='M').pack(expand=1,side=tk.LEFT,fill=tk.Y)
    
    label_Act = tk.Label(containerACT, text="Actividad: ",width=20,font=("bold", 10))
    label_Act.pack(side=tk.LEFT)
    varAct2 = tk.IntVar(registro)
    tk.Radiobutton(containerACT, text="1 ",padx = 10,value=1, variable=varAct2).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerACT, text="2 ",padx = 10,value=2, variable=varAct2).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerACT, text="3 ",padx = 10,value=3, variable=varAct2).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerACT, text="4 ",padx = 10,value=4, variable=varAct2).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerACT, text="5 ",padx = 10,value=5, variable=varAct2).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    
    label_3 = tk.Label(containerTIP, text="Tipo",width=20,font=("bold", 10))
    label_3.pack(side=tk.LEFT)
    varTipDiet = tk.IntVar(registro)
    tk.Radiobutton(containerTIP, text="bajar",padx = 5, variable=varTipDiet, value=1).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerTIP, text="mantener",padx = 20, variable=varTipDiet, value=2).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    tk.Radiobutton(containerTIP, text="subir",padx = 20, variable=varTipDiet, value=3).pack(expand=1,side=tk.LEFT,fill=tk.Y)
    listPatologias=list(hojaPatologias.iloc[:,1])
    label_Pat =  tk.Label(containerPAT, text="Patología: ",width=20,font=("bold", 10))
    label_Pat.pack(side=tk.LEFT)
    
    patologia=tk.StringVar()
    patologia.set(listPatologias[0])
    droplist=tk.OptionMenu(containerPAT,patologia, *listPatologias)
    droplist.config(width=90, font=('Helvetica', 12), relief=tk.GROOVE)
     
    droplist.pack(side=tk.LEFT)

    label_Err = tk.Label(containerERR, text="",width=20,font=("bold", 10),foreground="red")
    
    buttonEnviar = tk.Button(containerBut, text='Aceptar y Guardar',command=partial(ab.NuevoUsuario,registro,hojaUsuarios,entry_Dni, entry_Nom,entry_Ape,entry_Pwd, varSex,entry_Eda,entry_Alt,entry_Pes,varAct2, varTipDiet,label_Err,patologia, hojaPatologias),relief=tk.GROOVE)
    buttonEnviar.pack(fill=tk.X)
    button = tk.Button(containerBut, text="Cancelar",command=lambda:registro.destroy(),relief=tk.GROOVE)
    button.pack(fill=tk.X)
    label_Err.pack()
    registro.mainloop(); 
'''
Función que muestra la información (Nutrientes, Histograma, calidad, etcétera) de la nueva información a añadir.
Parametros: 
    hojaAlimentos - Array que contiene la base de datos alimentos
    selfi - Variable que contiene las variables locales de la clase que invoca la función.
    colorDetalles - Color de los detalles de la nueva página.
    colorFondo - Color del fondo de la nueva página
'''
def InformacionNuevaComida(hojaAlimentos, selfi,colorDetalles,colorFondo):
    try:
        nombre, kcalTotal,grasasTotal, saturadasTotal,hidratosTotal, fibraTotal,azucarTotal,proteinasTotal,sodioTotal,tipo, arrayCalidad, error = cd.AñadirMenuCalculos(selfi)
    except:
        error=True;
    if not (error):
        info = tk.Tk();
        info.resizable(0,0)
        info.geometry('700x500')
        info.title("Información")
        #Contenedores dentro del registro
        containerGen = tk.Frame(info)
        containerGen.pack(fill=tk.X)
        containerBut = tk.Frame(info)
        containerBut.pack(fill=tk.X)

        #HISTOGRAMA DE CALIDAD
        f = Figure(figsize=(5,4))
        
        
        p = f.gca()
        p.hist(arrayCalidad,bins=[1,2,3,4,5,6],histtype='barstacked',label="CALIDAD")

        canvas = FigureCanvasTkAgg(f, master=containerGen)
        canvas.draw();
        canvas.get_tk_widget().pack(side=tk.LEFT)
        ax = canvas.figure.axes[0]
        ax.set_xlabel("Calidad")
        ax.set_ylabel("Nº Alimentos")
        #Contenedores dentro del contenedor General
        containerNom = tk.Frame(containerGen)
        containerNom.pack(fill=tk.X)
        containerKcal = tk.Frame(containerGen)
        containerKcal.pack(fill=tk.X)
        containerGra = tk.Frame(containerGen)
        containerGra.pack(fill=tk.X)
        containerSat = tk.Frame(containerGen)
        containerSat.pack(fill=tk.X)
        containerHid = tk.Frame(containerGen)
        containerHid.pack(fill=tk.X)
        containerFib = tk.Frame(containerGen)
        containerFib.pack(fill=tk.X)
        containerAzu = tk.Frame(containerGen)
        containerAzu.pack(fill=tk.X)
        containerPro = tk.Frame(containerGen)
        containerPro.pack(fill=tk.X)
        containerSod= tk.Frame(containerGen)
        containerSod.pack(fill=tk.X)
        containerTip = tk.Frame(containerGen)
        containerTip.pack(fill=tk.X)
        containerCal = tk.Frame(containerGen)
        containerCal.pack(fill=tk.X)
        containerIMG = tk.Frame(containerGen)
        containerIMG.pack(fill=tk.X)
        
        labelNom= tk.Label(containerNom, text="NOMBRE: "+nombre,bg=colorFondo)
        labelNom.pack(side=tk.LEFT)
        
        labelKcal= tk.Label(containerKcal, text="KCALORIAS: "+str(round(kcalTotal,2)),bg=colorFondo)
        labelKcal.pack(side=tk.LEFT)
        
        labelGra= tk.Label(containerGra, text="GRASAS: "+str(round(grasasTotal,2)),bg=colorFondo)
        labelGra.pack(side=tk.LEFT)
        
        labelSat= tk.Label(containerSat, text="SATURADAS: "+str(round(saturadasTotal,2)),bg=colorFondo)
        labelSat.pack(side=tk.LEFT)
        
        labelHid= tk.Label(containerHid, text="HIDRATOS: "+str(round(hidratosTotal,2)),bg=colorFondo)
        labelHid.pack(side=tk.LEFT)
        
        labelFib= tk.Label(containerFib, text="FIBRA: "+str(round(fibraTotal,2)),bg=colorFondo)
        labelFib.pack(side=tk.LEFT)
        
        labelAzu= tk.Label(containerAzu, text="AZUCAR: "+str(round(azucarTotal,2)),bg=colorFondo)
        labelAzu.pack(side=tk.LEFT)
        
        labelPro= tk.Label(containerPro, text="PROTEINA: "+str(round(proteinasTotal,2)),bg=colorFondo)
        labelPro.pack(side=tk.LEFT)
        
        labelSod= tk.Label(containerSod, text="SODIO: "+str(round(sodioTotal,2)),bg=colorFondo)
        labelSod.pack(side=tk.LEFT)
        
        labelTipo= tk.Label(containerTip, text="TIPO: xxx",bg=colorFondo)
        labelTipo.pack(side=tk.LEFT)
        resultado=[0,0,0,0,0]
        for i in arrayCalidad:
            resultado[i-1]+=1
        cal = CalidadNumberToString(resultado.index(max(resultado))+1)
        
        labelCal= tk.Label(containerCal, text="Calidad: "+str(cal),bg=colorFondo)
        labelCal.pack(side=tk.LEFT)

        imgPath ='assets/'+str(cal)+'.PNG'
        icon = ImageTk.PhotoImage(Image.open(imgPath), master=containerIMG)
        icon_size = tk.Label(containerIMG)
        icon_size.configure(image=icon)
        icon_size.pack(side=tk.LEFT)

        #ab.ComrproYAlmacenamientoAlimento(hojaAlimentos,nombre, kcalTotal,grasasTotal, saturadasTotal,hidratosTotal, fibraTotal,azucarTotal,proteinasTotal,sodioTotal,tipo, calidad)
        buttonEnviar = tk.Button(containerBut, text='Guardar',command=partial(ab.ComrproYAlmacenamientoAlimento,hojaAlimentos, nombre, kcalTotal,grasasTotal, saturadasTotal, hidratosTotal, fibraTotal , azucarTotal, proteinasTotal, sodioTotal,tipo ,cal),bg=colorDetalles,relief=tk.GROOVE)
        buttonEnviar.pack(fill=tk.X)
        
        button = tk.Button(containerBut, text="Cancelar",command=lambda:info.destroy(),bg=colorDetalles,relief=tk.GROOVE)
        button.pack(fill=tk.X)
        info.mainloop(); 