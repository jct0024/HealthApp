# -*- coding: utf-8 -*-
import pandas as pd;
#Función que te devuelve la hoja de información de 
#la base de datos.
def cargarBaseDeDatos(hoja):
    #Cargamos la base de datos
    #doc = op.load_workbook("BaseDeDatosDeAlimentos.xlsx");  
    doc = pd.ExcelFile("BaseDeDatosDeAlimentos.xlsx")
    #print(doc.sheetnames) #Si añadimos hojas a la base de datos, podremos saber la información.
    #Seleccionamos la hoja de excell que contendrá dicha información-
    hojaExcell = pd.read_excel(doc,hoja)
    return hojaExcell;

#Cargamos la hoja1 en la cual se encuentran los alimentos con sus macronutrientes.
hojaAlimentos = cargarBaseDeDatos('Hoja1')
hojaAlimentos = hojaAlimentos.sort_values(by=['LRE']).sort_values(by=['Proteina'],ascending=False)
n_Opciones = 3;
for i in range(n_Opciones):
    print(i, " ",hojaAlimentos["Nombre"].loc[i])
opc = int(input("Introduzca la opción que desea desayunar"))
hojaAlimentos.loc[opc,'LRE'] = 1
hojaAlimentos = hojaAlimentos.sort_values(by=['Proteina'],ascending=False).sort_values(by=['LRE'])
writer = pd.ExcelWriter("BaseDeDatosDeAlimentos.xlsx")
hojaAlimentos.to_excel(writer,'Hoja1')
writer.save();
print(hojaAlimentos)