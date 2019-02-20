# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:50:40 2018

@author: Jesus
"""
import pandas as pd;
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
Función que crea 5 listas con los alimentos que son desayunos, almuerzos, comidas, meriendas o cena respectivamente
RECORDATORIO: un alimento puede pertenecer perfectamente a varios grupos de comida a la vez.
'''
def listasPorTipo(listaDeAlimentos):
    desayuno = pd.DataFrame();
    almuerzo = pd.DataFrame();
    comida = pd.DataFrame();
    comida2  = pd.DataFrame();
    merienda = pd.DataFrame();
    cena = pd.DataFrame();
    for indice, comida in listaDeAlimentos.iterrows():
        if(int(comida["Tipo"])==31):
            desayuno = desayuno.append(listaDeAlimentos.loc[indice]);
            almuerzo = almuerzo.append(listaDeAlimentos.loc[indice]);
            comida2 = comida2.append(listaDeAlimentos.loc[indice]);
            merienda = merienda.append(listaDeAlimentos.loc[indice]);
            cena = cena.append(listaDeAlimentos.loc[indice]);
        elif(int(comida["Tipo"])==26):
            desayuno = desayuno.append(listaDeAlimentos.loc[indice]);
            almuerzo = almuerzo.append(listaDeAlimentos.loc[indice]);
            merienda = merienda.append(listaDeAlimentos.loc[indice]);
        elif(int(comida["Tipo"])==5):
            comida2 = comida2.append(listaDeAlimentos.loc[indice]);
            cena = cena.append(listaDeAlimentos.loc[indice]);
        elif(int(comida["Tipo"])==15):
            almuerzo = almuerzo.append(listaDeAlimentos.loc[indice]);
            comida2 = comida2.append(listaDeAlimentos.loc[indice]);
            merienda = merienda.append(listaDeAlimentos.loc[indice]);
            cena = cena.append(listaDeAlimentos.loc[indice]);
    return desayuno, almuerzo, comida2, merienda, cena;
'''
Ordena la comida en base a la minima diferencia entre lo que debo comer y el 
objetivo que tengo para esta comida especifica
'''
def OrdMinimaDiferencia(listComida,objetivo):
    dif=0;
    listComida.loc[:,"dif"]=0;
    for i,comida in listComida.iterrows():
        dif = abs(objetivo-int(comida["Calorias"]))
        listComida["dif"].loc[i]=dif
    listComida = listComida.sort_values(by=['dif'])
    return listComida;