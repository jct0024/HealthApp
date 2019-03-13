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
    desayuno = kcalDiaria*0.2475;
    almuerzo = kcalDiaria*0.135;
    comida = kcalDiaria*0.305;
    merienda = kcalDiaria*0.115;
    cena = kcalDiaria*0.1975;
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
MEJOOOOOORAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Hay que hacer los calculos según sea: Desayuno, almuerzo... 
y sacar de ahí las kcal en carb, proteina y grasas
para sacar la diferencia de las tres con lo que deberiamos llevar, y hacer una media de la diferencia.
ESTA MAAAAAL HAY QUE CORREGIRLO
'''
def OrdMinimaDiferencia(listComida,objetivo,tipoComida,dat,kcaldiarias):
    dif=0;
    listComida.loc[:,"dif"]=0;
    if(tipoComida == "desayuno"):
      #Es el tanto por ciento correspondiente a cada macronutriente en base al objetivo de la comida
      # Se calcula = %pesoMacronutrienteSobreKcalDiarias*100/%pesodelacomidadelmomentocar
      graDeber = kcaldiarias*0.0375
      carDeber = kcaldiarias*0.15
      protDeber = kcaldiarias*0.06
      #deber = objetivo
      carb = objetivo*0.606060
      gra = objetivo*0.15
      prot = objetivo*0.2424
    #PENDIENTE DE CALCULAR EL RESTO DE COMIDAS EMPEZANDO POR AQUI
    elif(tipoComida == "almuerzo"):
      graDeber = kcaldiarias*0.015+kcaldiarias*0.0375
      carDeber = kcaldiarias*0.1+kcaldiarias*0.15
      protDeber = kcaldiarias*0.02+kcaldiarias*0.06
      #deber = objetivo+kcaldiarias*0.135
      carb = objetivo*0.74074074
      gra = objetivo*0.111111
      prot = objetivo*0.14814814
    elif(tipoComida == "comida"):
      graDeber = kcaldiarias*0.075+kcaldiarias*0.015+kcaldiarias*0.0375
      carDeber = kcaldiarias*0.145+kcaldiarias*0.1+kcaldiarias*0.15
      protDeber = kcaldiarias*0.085+kcaldiarias*0.02+kcaldiarias*0.06
      #deber = objetivo+kcaldiarias*0.135+kcaldiarias*0.305
      carb = objetivo*0.4754098
      gra = objetivo*0.245901
      prot = objetivo*0.2786885
    elif(tipoComida == "merienda"):
      graDeber = kcaldiarias*0.045+kcaldiarias*0.075+kcaldiarias*0.015+kcaldiarias*0.0375
      carDeber = kcaldiarias*0.45+kcaldiarias*0.145+kcaldiarias*0.1+kcaldiarias*0.15
      protDeber = kcaldiarias*0.025+kcaldiarias*0.085+kcaldiarias*0.02+kcaldiarias*0.06
      #deber = objetivo+kcaldiarias*0.135+kcaldiarias*0.305+kcaldiarias*0.115
      carb = objetivo*0.39130434
      gra = objetivo*0.39130434
      prot = objetivo*0.2173913043
    else:
      graDeber = kcaldiarias*0.0875+kcaldiarias*0.045+kcaldiarias*0.075+kcaldiarias*0.015+kcaldiarias*0.0375
      carDeber = kcaldiarias*0.05+kcaldiarias*0.45+kcaldiarias*0.145+kcaldiarias*0.1+kcaldiarias*0.15
      protDeber = kcaldiarias*0.06+kcaldiarias*0.025+kcaldiarias*0.085+kcaldiarias*0.02+kcaldiarias*0.06
      #deber = objetivo+kcaldiarias*0.135+kcaldiarias*0.305+kcaldiarias*0.115+kcaldiarias*0.1975
      carb = objetivo*0.2531645570
      gra = objetivo*0.4430379747
      prot = objetivo*0.3037974684
    for i,comida in listComida.iterrows():        
        dif = formulDif(dat,carb,prot,gra,comida,objetivo,carDeber,graDeber,protDeber)
        #dif = abs(objetivo-int(comida["Calorias"]))
        listComida["dif"].loc[i]=dif
    listComida = listComida.sort_values(by=['dif'],ascending=False)
    return listComida;

def formulDif(loQueLlevo,carb,prot,gras,comida,deboComida,carDeber,graDeber,protDeber):
    #print("carb que deberia llevar: ",carDeber, "//Lo que llevo: ",loQueLlevo[2])
    #print("resta carb que debería comer vslo que como", (carb-(comida["Hidratos"]*4)))
    #print("kcal deberia vs calorias llevo", (deboComida-(comida["Calorias"])))
    if ((carDeber-loQueLlevo[1]*4) >= 0 ):
        comidaCarb = (carDeber-loQueLlevo[2]*4)/(carb-(comida["Hidratos"]*4)+(deboComida-(comida["Calorias"])))
    else:
        comidaCarb=0;
    if ((protDeber-loQueLlevo[2]*4) >= 0 ):
        comidaPro = (carDeber-loQueLlevo[3]*4)/(prot-(comida["Proteina"]*4)+(deboComida-(comida["Calorias"])))
    else:
        comidaPro=0;
    if ((graDeber-loQueLlevo[3]*8)>= 0 ):
        comidaGra = (carDeber-loQueLlevo[1]*8)/(gras-(comida["Grasa"]*8)+(deboComida-(comida["Calorias"])))
    else:
        comidaGra=0;
    return (comidaCarb+comidaPro+comidaGra)/3
'''
Funcion que te reparte lo sobrante entre las comidas que quedan
POSIBLE MEJORA: Que te reparta de manera proporcional a la importancia de la comida
es decir si sobran 40 kcal en el desayuno, que no se repartan equitativamente sino que la comida
tenga 15 y el almuerzo 5 (por ejemplo)
'''
def repartoKcalSobrantes(kcal,listakcalcomidas, comida):
    cont=0;
    if(comida == "desayuno"):
        cont = (int(listakcalcomidas[0])-int(kcal))/4;
        listakcalcomidas[1] = listakcalcomidas[1] + cont
        listakcalcomidas[2] = listakcalcomidas[2] + cont
        listakcalcomidas[3] = listakcalcomidas[3] + cont
        listakcalcomidas[4] = listakcalcomidas[4] + cont
    elif (comida == "almuerzo"):
        cont = (int(listakcalcomidas[1])-int(kcal))/3;
        listakcalcomidas[2] = listakcalcomidas[2] + cont
        listakcalcomidas[3] = listakcalcomidas[3] + cont
        listakcalcomidas[4] = listakcalcomidas[4] + cont
    elif(comida == "comida"):
        cont = (int(listakcalcomidas[2])-int(kcal))/2
        listakcalcomidas[3] = listakcalcomidas[3] + cont
        listakcalcomidas[4] = listakcalcomidas[4] + cont
    elif(comida == "merienda"):
        cont = (int(listakcalcomidas[3])-int(kcal))
        listakcalcomidas[4] = listakcalcomidas[4] + cont       
    return listakcalcomidas
        