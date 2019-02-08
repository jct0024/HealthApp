# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:50:40 2018

@author: Jesus
"""
"""
Calcula el número de calorias que el usuario ha de gastar en base a:
   altura, peso, edad,sexo, actividad realizada y sus objetivos(bjar,subir o mantener peso)
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
    #Por ultimo, el TBM son las calorias que el usuario gasta al dia aproximadas,
    #si quiere subir y bajar el restamos o sumamos el resto de calorias
    if(usuario[10]=='subir'):
        TMB=TMB+500;
    elif(usuario[6]=='bajar'):
        TMB=TMB-500
    return TMB
def distribuciónDeMacronutrientes(kcal,tipoDieta):
    if (tipoDieta == 'normal'):
        '''
        En una dieta normal la distribución es:
            Hidratos = 50%
            Proteinas = 25%
            Grasas = 25%
        Por esta razon dividimos entre 2 a los hidratos y luego otra vez entre 4 para trasnformar las kcal en gramos
        hacemos lo mismo con las proteinas y las grasas, solo que las grasas son 8 kcal/gramo, es decir 4 * 8 = 32.
        '''
        hidratos = kcal/8 #En gramos todo
        proteinas = kcal/16
        grasas = kcal/32
        listMacDiarios = [kcal,hidratos,proteinas,grasas]
        return listMacDiarios
    '''
    Retocar para que la grasa sea menos o mayor según sea necesario, esto queda pendiente de estudio, para 
    saber cual seria la distribución correcta.
    '''
    if (tipoDieta == 'baja en grasa'):
        hidratos = kcal/8 #En gramos todo
        proteinas = kcal/16
        grasas = kcal/32
        listMacDiarios = [kcal,hidratos,proteinas,grasas]
    else:
        return None;
'''
Crear Función que te devuelva en diferentes arrays, las kcal, 
y gramos de comida correspondientes al desayuno, almuerzo, comida, merienda y cena
'''
def repartoDeKcal (kcalDiaria):
    desayuno = kcalDiaria*0.23;
    almuerzo = kcalDiaria*0.10;
    comida = kcalDiaria*0.37;
    merienda = kcalDiaria*0.10;
    cena = kcalDiaria*0.20;
    kcalDesAlmComMerCen = [desayuno,almuerzo,comida,merienda,cena];
    return kcalDesAlmComMerCen;
'''
Serie de metodos que te devuelve verdadero o falso según si es el tipo de comida que se espera o no
'''
def esDesayuno(tipoComida):
    if tipoComida==31 or tipoComida==26:
        return True;
    return False;
    