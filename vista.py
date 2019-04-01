# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 12:51:31 2019

@author: Jesus
"""

from tkinter import *
from tkinter import ttk,font
import AdminBase as ab;
bandera = False;
usr = 0;
contraseña = "";
def cambio(usuario,passwd,login,lblU,lblMensaje): 
    if(usuario.get() != '' or passwd.get() != ''):
        if(ab.comprobarUsuario(int(usuario.get()),str(passwd.get())) > -1):        
            global bandera 
            global usr
            global contraseña;
            usr =int(usuario.get())
            contraseña = str(passwd.get())
            bandera = True;
            login.destroy();
        else:
            #lblU.config(foreground='red')
            lblMensaje.config(text="ERROR:usuario o contraseña incorrectos")
        
def getBandera():
    return bandera;
def getUsuario():
    return usr,contraseña;
def show_frame(frames, page_name):
    '''Show a frame for the given page name'''
    frame = frames[page_name]
    frame.tkraise()