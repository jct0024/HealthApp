# -*- coding: utf-8 -*-
import openpyxl as op;
import numpy as np;
doc = op.load_workbook("BaseDeDatosDeAlimentos.xlsx");
#print(doc.sheetnames)
hoja1 = doc['Hoja1'];
nFila=-1;
mAlimentos = np.empty((6,8), dtype=object);
for alimentos in hoja1:
    nFila =nFila+1
    if (nFila!=0):
        i = 0;
        for inf in alimentos:
            if (i==0):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==1):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==2):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==3):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==4):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==5):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==6):
                mAlimentos[nFila-1,i]=inf.value;
            elif (i==7):
                mAlimentos[nFila-1,i]=inf.value;
            i=i+1
    
print (mAlimentos)