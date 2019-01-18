# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:36:25 2018

@author: Jesus
"""
import pandas as pd;
def cargarBaseDeDatos():
    #Cargamos la base de datos
    #doc = op.load_workbook("BaseDeDatosDeAlimentos.xlsx");  
    doc = pd.ExcelFile("BaseDeDatosDeAlimentos.xlsx")
    #print(doc.sheetnames) #Si añadimos hojas a la base de datos, podremos saber la información.
    #Seleccionamos la hoja de excell que contendrá dicha información-
    hojaAl = pd.read_excel(doc,'Alimentos')
    hojaUs = pd.read_excel(doc,'Usuarios')
    hojaPa = pd.read_excel(doc,'Patologias')
    return hojaAl,hojaUs,hojaPa;

def comprobarUsuario(userId,passwd):
    a,u,p = cargarBaseDeDatos();
    indice=-1;
    if ((u.iloc[:,0]==userId).any()):
        for i in u.iloc[:,0]:
            indice+=1
            if(i == userId):
                if(passwd == u.iloc[indice,3]):
                    return indice;
            
    return indice;
def getFilaPatologia(patologiaID):
    a,u,p = cargarBaseDeDatos();
    indice=0;
    for i in p.iloc[:,0]:
        if(i == patologiaID):
            break;
        indice+=1;
    return indice;
def getFilaUsuario(userId):
    a,u,p = cargarBaseDeDatos();
    indice=0;
    for i in u.iloc[:,0]:
        if(i == userId):
            break;
        indice+=1;
    return indice;
#Guarda los datos en la hoja que se le pasa como argumento
def guardarDatos (hojaAlimentos, hojaUsuarios, hojaPatologias):
    writer = pd.ExcelWriter("BaseDeDatosDeAlimentos.xlsx")
    hojaAlimentos.to_excel(writer,'Alimentos')
    hojaUsuarios.to_excel(writer,'Usuarios')
    hojaPatologias.to_excel(writer,'Patologias')
    writer.save();