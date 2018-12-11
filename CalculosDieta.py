# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:50:40 2018

@author: Jesus
"""
"""
Calcula el número de calorias que el usuario ha de gastar en base a:
   altura, peso, edad,sexo, actividad realizada y sus objetivs(bjar,subir o mantener peso)
"""
def calculoTMB(usuario):
    #Formula para calcular la tasa de metabolismo basal
    TMB = (10*usuario[7])+(6.25*usuario[6])-(5*usuario[5])
    #Difrencia entre mujery ho,bre
    if(usuario[4] == 'H'):
        TMB=TMB+5
    else:
        TMB=TMB-161
    #Calculamos el TBM en base a la actividad que haga el usuario
    if(usuario[8]==0):
        TMB = TMB*1.2;
    elif(usuario[8]==1):
        TMB = TMB*1.375;
    elif(usuario[8]==2):
        TMB = TMB*1.55;
    elif(usuario[8]==3):
        TMB = TMB*1.725;
    elif(usuario[8]==4):
        TMB = TMB*1.9;
    else:
        TMB = "ERROR"
    print(usuario[10])
    #Por ultimo, el TBM son las calorias que el usuario gasta al dia aproximadas,
    #si quiere subir y bajar el restamos o sumamos el resto de calorias
    if(usuario[10]=='subir'):
        TMB=TMB+500;
    elif(usuario[6]=='bajar'):
        TMB=TMB-500
    print(TMB)
    return TMB