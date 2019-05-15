# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:19:30 2019

@author: Jesus
"""
import pandas as pd
from cryptography.fernet import Fernet
import win32com.client
import csv
import sys
def storeKey(key):
    file = open('key.key','wb')
    file.write(key)
    file.close()
def carga():
    file = open('key.key','rb')
    key = file.read();
    file.close();
    return key;
#key = Fernet.generate_key()
with open('key.encrypt','rb') as f:
    data = f.read()
'''
key=b'YJSBYAeQ5L3TuDvObBqH-Yw5yFSQTO6EIjxVX77thP8='
fernet = Fernet(key)
des = fernet.decrypt(data)
print(des)
'''
inputfile = r'\\BaseDeDatosDeAlimentos2.xlsx'
xlApp = win32com.client.Dispatch("Excel.Application")
xlwb = xlApp.Workbooks.Open(inputfile,Password='1234')
print(xlwb)