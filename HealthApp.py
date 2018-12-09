# -*- coding: utf-8 -*-
import pandas as pd;
import numpy as np;
#Función que te devuelve la hoja de información de 
#la base de datos, la cual se pasa como parametros.
def cargarBaseDeDatos(hoja):
    #Cargamos la base de datos
    #doc = op.load_workbook("BaseDeDatosDeAlimentos.xlsx");  
    doc = pd.ExcelFile("BaseDeDatosDeAlimentos.xlsx")
    #print(doc.sheetnames) #Si añadimos hojas a la base de datos, podremos saber la información.
    #Seleccionamos la hoja de excell que contendrá dicha información-
    hojaExcell = pd.read_excel(doc,hoja)
    return hojaExcell;

def guardarDatos (hoja):
    writer = pd.ExcelWriter("BaseDeDatosDeAlimentos.xlsx")
    hojaAlimentos.to_excel(writer,hoja)
    writer.save();
 a = -1;   
while (a !=0):
   #Hacer todo lo del menu , opciones apra el cliente y demas
   a=0;
#Vectores datos alimentos: calorias/grasas/garasas saturadas/hidratos/azucares/proteina
datosAlimCliente = np.zeros(6)
datosAlimTotal = np.zeros(6)
#Cargamos la hoja1 en la cual se encuentran los alimentos con sus macronutrientes.
hojaAlimentos = cargarBaseDeDatos('Hoja1')
hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
n_Opciones = 3;
#Escoger entre opciones el desayuno de hoy:
while (datosAlimCliente[0] != datosAlimTotal):
    for i in range(n_Opciones):
        print(i, " ",hojaAlimentos["Nombre"].iloc[i])
        opc = int(input("Introduzca la opción que desea desayunar"))
        hojaAlimentos.iloc[opc,8] =hojaAlimentos.iloc[opc,8] + 1

    #Rellenar datos.
    for i in range(datosAlimTotal.size):
        datosAlimCliente[i] = hojaAlimentos.iloc[opc,i+1] + datosAlimCliente[i]
    print(datosAlimCliente)
    hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
guardarDatos ('Hoja1')
print(hojaAlimentos)
PRUEBA = str(1101);
total=0;
for p in PRUEBA:
    total=int(p)+total
    print(total)