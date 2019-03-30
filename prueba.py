#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk,font
import AdminBase as ab;
import CalculosDieta as cd;
# Gestor de geometría (pack)

class diseño():
    def __init__(self):
        self.login = Tk()
        self.login.geometry('150x170')
        self.login.title("login")
        #iNICIALIZACIÓN DE FUENTES, SEPARADORES...
        self.fuente = font.Font(family="Helvetica",size=12, weight="bold")
        
        #CUERPO
        self.lblU = ttk.Label(self.login,text="DNI", font=self.fuente)
        self.txtU = ttk.Entry(self.login,width=10)
        self.lblP = ttk.Label(self.login,text="password",font=self.fuente)
        self.txtP = ttk.Entry(self.login,width=10, show="*")
        self.btnInit = ttk.Button(self.login, text="Inicio",command=self.cambio)
        self.btnExit = ttk.Button(self.login, text="Salir",command=self.login.destroy)
        
        #POSICIONAMIENTOOOO
        self.lblU.pack()
        self.txtU.focus()
        self.txtU.pack(fill=X)
        self.lblP.pack()
        self.txtP.pack(fill=X)       
        self.btnInit.pack(side=LEFT);
        self.btnExit.pack(side=RIGHT);
        self.login.mainloop();
    def cambio(self):
        if(int(ab.comprobarUsuario(int(self.txtU.get()),str(self.txtP.get()))) > -1):
            
            print(self.txtU.get())
            print(self.txtP.get())
        else:
            print(int(ab.comprobarUsuario(int(self.txtU.get()),str(self.txtP.get()))))
            self.lblU.configure(fg="red")

def main():
    mi_app = diseño();
    return 0;
if __name__ == '__main__':
    main()