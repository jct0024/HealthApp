# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:36:25 2018

@author: Jesus
"""
import pandas as pd;
import datetime
import CalculosDieta as cd
from tkinter import messagebox
def cargarBaseDeDatos():
    #Cargamos la base de datos
    #doc = wx.Book("BaseDeDatosDeAlimentos.xlsx")
    doc = pd.ExcelFile("BaseDeDatosDeAlimentos.xlsx")
    docU = pd.ExcelFile("BaseDeDatosUsuarios.xlsx")
    #print(doc.sheetnames) #Si añadimos hojas a la base de datos, podremos saber la información.
    #Seleccionamos la hoja de excell que contendrá dicha información-

    hojaAl = pd.read_excel(doc,'Alimentos')
    hojaUs = pd.read_excel(docU,'Usuarios')
    hojaPa = pd.read_excel(doc,'Patologias')
    archivo = open('config.txt','r')
    config = str(archivo.read()).split(':')
    archivo.close()
    
    return hojaAl,hojaUs,hojaPa,config;
def cargarBaseAlimentos():
    doc = pd.ExcelFile("BaseDeDatosDeAlimentos.xlsx")
    hojaAl = pd.read_excel(doc,'Alimentos')
    hojaPa = pd.read_excel(doc,'Patologias')
    return hojaAl,hojaPa;
'''
Función que carga el historial del usuario para futuros calculosy gráficas para ello necesita solo la id del usuario,se 
criba y se devuelve para ser almacenado.
'''

def cargarHistorial(usr):
    hist = pd.ExcelFile("Historial.xlsx");
    hojaHisAl = pd.read_excel(hist, 'UsrAl')
    hojaHisAl = hojaHisAl.loc[hojaHisAl.Usuario == usr]
    
    return(hojaHisAl)
'''
Modificamos el array 'menuDeHoy' con la información de hoy si es que hay
'''
def cargaHistorialHoy(hojaHisAl,menuDeHoy,datosAlimCliente,hojaAlimentos):
    hoy = str(datetime.date.today())
    if(hoy in list(hojaHisAl.Fecha)):
       diaEntero=hojaHisAl.loc[hojaHisAl.Fecha == hoy]
       if not (diaEntero.iloc[0].isnull().loc['Desayuno']):
           menuDeHoy[0] = str(diaEntero.iloc[0].loc['Desayuno'])
           fila = getFilaAlimento(menuDeHoy[0],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Almuerzo']):
           menuDeHoy[1] = str(diaEntero.iloc[0].loc['Almuerzo'])
           fila = getFilaAlimento(menuDeHoy[0],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Comida']):
           menuDeHoy[2] = str(diaEntero.iloc[0].loc['Comida'])
           fila = getFilaAlimento(menuDeHoy[0],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Merienda']):
           menuDeHoy[3] = str(diaEntero.iloc[0].loc['Merienda'])
           fila = getFilaAlimento(menuDeHoy[0],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Cena']):
           menuDeHoy[4] = str(diaEntero.iloc[0].loc['Cena'])    
           fila = getFilaAlimento(menuDeHoy[0],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
def comprobarUsuario(userId,passwd):
    a,u,p,c = cargarBaseDeDatos();
    indice=-1;
    bandera =True;
    if ((u.iloc[:,0]==userId).any()):
        for i in u.iloc[:,0]:
            indice+=1
            if(i == userId):
                if(str(passwd) == str(u.iloc[indice,3])):
                    bandera = False;
                    return indice;
    if(bandera):
        indice = -1;            
    return indice;
def getFilaPatologia(patologiaID,p):
    indice=0;
    for i in p.iloc[:,0]:
        if(i == patologiaID):
            break;
        indice+=1;
    return indice;
def getFilaUsuario(userId,u):
    indice=0;
    for i in u.iloc[:,0]:
        if(i == userId):
            break;
        indice+=1;
    return indice;
def getFilaAlimento(nombre,a):
    indice=0;
    for i,alimento in a.iterrows():
        if(alimento["Nombre"] == nombre):
            break;
        indice+=1;
    return i;    
def guardaTodo(usr, menuDeHoy, historial,hojaAlimentos, hojaUsuarios, hojaPatologias,config):
    guardarHistorial (usr, menuDeHoy, historial)
    guardarUsuario(hojaUsuarios)
    guardarDatos (hojaAlimentos, hojaPatologias)

    
    messagebox.showinfo("Ya se ha guardado","Datos guardados ya puede cerrar el programa")
def guardarUsuario(hojaUsuarios):
    writer = pd.ExcelWriter("BaseDeDatosUsuarios.xlsx")
    hojaUsuarios.to_excel(writer,'Usuarios',index=False)
    writer.save();
def guardarHistorial (usr, menuDeHoy, historial):
    fech = str(datetime.date.today())
    h = historial.loc[historial.Fecha == fech]
    hoy = pd.DataFrame({"Fecha":[fech],
                    "Usuario":[usr],
                    "Desayuno":[menuDeHoy[0]],
                    "Almuerzo":[menuDeHoy[1]],
                    "Comida":[menuDeHoy[2]],
                    "Merienda":[menuDeHoy[3]],
                    "Cena":[menuDeHoy[4]]})
    if(usr in list(h.Usuario)):
        lala = historial.index[(historial.Fecha == fech) & (historial.Usuario == usr)]
        historial.iloc[lala] = hoy
    else:
        historial=historial.append(hoy)    
    writer = pd.ExcelWriter("Historial.xlsx")
    historial.to_excel(writer,'UsrAl',index=False)
    writer.save();
#Guarda los datos en la hoja que se le pasa como argumento
def guardarDatos (hojaAlimentos, hojaPatologias):
    writer = pd.ExcelWriter("BaseDeDatosDeAlimentos.xlsx")
    hojaAlimentos.to_excel(writer,'Alimentos',index=False)
    hojaPatologias.to_excel(writer,'Patologias',index=False)
    writer.save();
def ComproYAlmacenamientoUsuario(hojaUsuarios,selfi,controller):
    fila = getFilaUsuario(selfi.user,hojaUsuarios)
    if(len(selfi.entry_Nom.get()) ==0 or len(selfi.entry_Ape.get()) == 0 or len(selfi.entry_Eda.get()) == 0 or len(selfi.entry_Alt.get()) == 0 or len(selfi.entry_Pes.get()) == 0 or selfi.var.get() == 0 or selfi.varTipo.get() == 0 or selfi.varAct.get() == 0):
        selfi.label_Error.config(text="ERROR: Algun dato erroneo, comprueba todo")
    else:
        try:
            int(selfi.entry_Eda.get())
            int(selfi.entry_Pes.get())
            int(selfi.entry_Alt.get())
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
        guardarUsuario(hojaUsuarios)
        messagebox.showinfo("Datos actualizados","Datos actualizados correctamente, veras los cambios al reiniciar el programa")
        controller.show_frame("InfoUsuario")
'''
Función que te comprueba que los datos son correctos e inserta un nuevo menu a la base de datos
Carga el actual estado de la base de datos, además de la lista de la cual esta haciendo uso el usuario, añade el nuevo alimento a ambas, asi cuando
guarda el alimento, lo hace solo sobre ese cambio y no tiene que guardar todo su progreso, y cuando quiere guardar todo su progreso el alimento esta ya almacenado
en la lista, lo cual evita que se sobreescriba y se borren los avances.
'''
def ComrproYAlmacenamientoAlimento(hojaAlimentos,selfi,controller):
    print(selfi.varDes.get())
    alimentos, patologias = cargarBaseAlimentos()
    if(len(selfi.entry_Nom.get()) ==0 or len(selfi.entry_kcal.get()) == 0 or len(selfi.entry_gras.get()) == 0 or len(selfi.entry_sat.get()) == 0 or len(selfi.entry_Hid.get()) == 0 or len(selfi.entry_Azuc.get()) == 0 or len(selfi.entry_Pro.get()) == 0 or selfi.varAct.get() == 0):
        selfi.label_Error.config(text="ERROR: Algun dato erroneo, comprueba todo")
    elif(selfi.varDes.get() == 0 and selfi.varAlm.get() == 0 and selfi.varCom.get() == 0 and selfi.varMer.get() == 0 and selfi.varCen.get() == 0 ):
        selfi.label_Error.config(text="ERROR: Seleccione que tipo de comida es")
    else:
        try:
            int(selfi.entry_kcal.get())
            int(selfi.entry_gras.get())
            int(selfi.entry_sat.get())
            int(selfi.entry_Hid.get())
            int(selfi.entry_Azuc.get())
            int(selfi.entry_Pro.get())
            selfi.label_Error.config(text="")
        except ValueError:
            selfi.label_Error.config(text="ERROR: Inserte un valor numerico válido")
        tipo =cd.stringTipoToNumber(selfi.varDes.get(),selfi.varAlm.get(),selfi.varCom.get(),selfi.varMer.get(),selfi.varCen.get());
        print('holi')        
        nuevaFila= pd.DataFrame({'Nombre':[selfi.entry_Nom.get()],
                                 'Calorias': [selfi.entry_kcal.get()],
                                 'Grasa': [selfi.entry_gras.get()], 
                                 'Saturadas':[selfi.entry_sat.get()],
                                 'Hidratos':[selfi.entry_Hid.get()],
                                 'Azucares':[selfi.entry_Azuc.get()],
                                 'Proteina':[selfi.entry_Pro.get()],
                                 'Tipo': [tipo],
                                 'LRE':[0],
                                 'Calidad': [selfi.varAct.get()]})
        hojaAlimentos = hojaAlimentos.append(nuevaFila)
        alimentos = alimentos.append(nuevaFila)
        print(alimentos)
        #Guardamos la 'imagen' de la base de datos sin retoques, solo con la nueva linea
        guardarDatos(alimentos,patologias)
        messagebox.showinfo("Datos actualizados","Datos actualizados correctamente, veras los cambios al reiniciar el programa")