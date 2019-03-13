#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font
import getpass

# Gestor de geometría (pack)

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("Acceso")
        # Cambia el formato de la fuente actual a negrita para
        # resaltar las dos etiquetas que acompañan a las cajas
        # de entrada. (Para este cambio se ha importado el  
        # módulo 'font' al comienzo del programa):
        
        fuente = font.Font(weight='bold')
        
        # Define las etiquetas que acompañan a las cajas de
        # entrada y asigna el formato de fuente anterior: 
                               
        self.etiq1 = ttk.Label(self.raiz, text="Usuario:", 
                               font=fuente)
        self.etiq2 = ttk.Label(self.raiz, text="Contraseña:", 
                               font=fuente)
        
        # Declara dos variables de tipo cadena para contener
        # el usuario y la contraseña: 
        
        self.usuario = StringVar()
        self.clave = StringVar()



        self.ctext1 = ttk.Entry(self.raiz, 
                                textvariable=self.usuario, 
                                width=30)
        self.ctext2 = ttk.Entry(self.raiz, 
                                textvariable=self.clave, 
                                width=30, show="*")
        self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)
        

        self.boton1 = ttk.Button(self.raiz, text="Aceptar", 
                                 command=self.aceptar)
        self.boton2 = ttk.Button(self.raiz, text="Cancelar", 
                                 command=self.raiz.destroy)
                                 
                        
        self.etiq1.pack(side=TOP, fill=BOTH, expand=True, 
                        padx=5, pady=5)
        self.ctext1.pack(side=TOP, fill=X, expand=True, 
                         padx=5, pady=5)
        self.etiq2.pack(side=TOP, fill=BOTH, expand=True, 
                        padx=5, pady=5)
        self.ctext2.pack(side=TOP, fill=X, expand=True, 
                         padx=5, pady=5)
        self.separ1.pack(side=TOP, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        self.boton1.pack(side=LEFT, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        self.boton2.pack(side=RIGHT, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        
        # Cuando se inicia el programa se asigna el foco
        # a la caja de entrada de la contraseña para que se
        # pueda empezar a escribir directamente:
                
        self.ctext2.focus_set()
        
        self.raiz.mainloop()
    
    # El método 'aceptar' se emplea para validar la 
    # contraseña introducida. Será llamado cuando se 
    # presione el botón 'Aceptar'. Si la contraseña
    # coincide con la cadena 'tkinter' se imprimirá
    # el mensaje 'Acceso permitido' y los valores 
    # aceptados. En caso contrario, se mostrará el
    # mensaje 'Acceso denegado' y el foco volverá al
    # mismo lugar.
    
    def aceptar(self):
        print("Acceso permitido")
        print("Usuario:   ", self.ctext1.get())
        print("Contraseña:", self.ctext2.get())

        self.ventana2 = Tk()
        self.hola = ttk.Label(self.ventana2, text="holiiiii")
        self.hola.pack(side=TOP,fill=BOTH,expand=True)
        self.ctext2.focus_set()
        self.ventana2.mainloop()
def main():
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()