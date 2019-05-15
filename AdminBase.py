# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:36:25 2018

@author: Jesus
"""
import pandas as pd;
import win32com.client;
import xlwings as wx;
import datetime
def cargarBaseDeDatos():
    #Cargamos la base de datos
    #doc = wx.Book("BaseDeDatosDeAlimentos.xlsx")
    doc = pd.ExcelFile("BaseDeDatosDeAlimentos.xlsx")
    #print(doc.sheetnames) #Si añadimos hojas a la base de datos, podremos saber la información.
    #Seleccionamos la hoja de excell que contendrá dicha información-

    hojaAl = pd.read_excel(doc,'Alimentos')
    hojaUs = pd.read_excel(doc,'Usuarios')
    hojaPa = pd.read_excel(doc,'Patologias')

    return hojaAl,hojaUs,hojaPa;
def cargarHistorial():
    hist = pd.ExcelFile("Historial.xlsx");
    hojaHisAl = pd.read_excel(hist, 'UsrAl')
    return(hojaHisAl)
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
        print(historial)
        lala = historial.index[(historial.Fecha == fech) & (historial.Usuario == usr)]
        historial.iloc[lala] = hoy
        print(historial)
    else:
        historial=historial.append(hoy)    
    writer = pd.ExcelWriter("Historial.xlsx")
    historial.to_excel(writer,'UsrAl')
    writer.save();
#Guarda los datos en la hoja que se le pasa como argumento
def guardarDatos (hojaAlimentos, hojaUsuarios, hojaPatologias):
    writer = pd.ExcelWriter("BaseDeDatosDeAlimentos.xlsx")
    hojaAlimentos.to_excel(writer,'Alimentos')
    hojaUsuarios.to_excel(writer,'Usuarios')
    hojaPatologias.to_excel(writer,'Patologias')
    writer.save();