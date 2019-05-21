# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:36:25 2018

@author: Jesus
"""
import pandas as pd;
import datetime
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

    return hojaAl,hojaUs,hojaPa;
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
    a,u,p = cargarBaseDeDatos();
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
def guardaTodo(usr, menuDeHoy, historial,hojaAlimentos, hojaUsuarios, hojaPatologias):
    guardarHistorial (usr, menuDeHoy, historial)
    guardarUsuario(hojaUsuarios)
    guardarDatos (hojaAlimentos, hojaUsuarios, hojaPatologias)
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
def guardarDatos (hojaAlimentos, hojaUsuarios, hojaPatologias):
    writer = pd.ExcelWriter("BaseDeDatosDeAlimentos.xlsx")
    hojaAlimentos.to_excel(writer,'Alimentos',index=False)
    hojaPatologias.to_excel(writer,'Patologias',index=False)
    writer.save();