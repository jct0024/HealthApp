#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk,font
import vista as vs;
from functools import partial
import AdminBase as ab;
import CalculosDieta as cd;
hojaAlimentos, hojaUsuarios, hojaPatologias = ab.cargarBaseDeDatos()
login = Tk();
login.geometry('150x170')
login.title("login")
#iNICIALIZACIÓN DE FUENTES, SEPARADORES...
fuente = font.Font(family="Helvetica",size=12, weight="bold")
  
#CUERPO
lblU = ttk.Label(login,text="DNI", font=fuente)
txtU = ttk.Entry(login,width=10)
lblP = ttk.Label(login,text="password",font=fuente)
txtP = ttk.Entry(login,width=10, show="*")
btnInit = ttk.Button(login, text="Inicio",command=partial(vs.cambio,txtU,txtP,login,lblU))
btnExit = ttk.Button(login, text="Salir",command=login.destroy)  
#POSICIONAMIENTOOOO

usuario = txtU.get()
passwd = txtP.get()

lblU.pack()
txtU.focus()
txtU.pack(fill=X)
lblP.pack()
txtP.pack(fill=X)       
btnInit.pack(side=LEFT);
btnExit.pack(side=RIGHT); 
login.mainloop(); 

if(vs.getBandera()):
    principal = Tk();
    principal.geometry('500x500')
    principal.title("HealthApp")
    usr,pwd = vs.getUsuario()
    print(u,p)
    bienv = ttk.Label(principal,text="BIENVENIDO"+hojaUsuarios.iloc[ab.getFilaUsuario(usr,hojaUsuarios),1])
    login.mainloop(); 