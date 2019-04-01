import tkinter as tk                # python 3
import vista as vs;
from functools import partial
import AdminBase as ab;
import CalculosDieta as cd;
from tkinter import *
from tkinter import ttk,font, messagebox;
from PIL import ImageTk, Image


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('500x500')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        self.frames = {}
        self.frames["menuPrincipal"] = menuPrincipal(parent=container, controller=self)
        self.frames["menuPrincipal"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["PageOne"] = PageOne(parent=container, controller=self)
        self.frames["PageOne"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["PageTwo"] = PageTwo(parent=container, controller=self)
        self.frames["PageTwo"].grid(row=0, column=0, sticky="nsew")
        
        '''
        for F in (menuPrincipal, PageOne, PageTwo, Salir):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
    '''
        self.show_frame("menuPrincipal")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class menuPrincipal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        self.bar = tk.Frame(self, relief=RIDGE, borderwidth=5)
        self.imgPath = './descarga.jpg'
        self.icon = ImageTk.PhotoImage(Image.open('./descarga.jpg'))
        self.icon_size = Label(self.bar)
        self.icon_size.configure(image=self.icon)
        button1 = tk.Button(self, text="Información de Usuario",
                            command=lambda: controller.show_frame("PageOne"),height = 2, width = 20,relief=GROOVE)
        button2 = tk.Button(self, text="Dieta diaria",
                            command=lambda: controller.show_frame("PageTwo"),height = 2, width = 20,relief=GROOVE)
        button3 = tk.Button(self, text="salir y gurdar",
                            command=guardar,height = 2, width = 20,relief=GROOVE)
        label.pack(side="top", fill="x", pady=10)
        self.icon_size.pack(side=LEFT)
        self.bar.pack(side=TOP)
        button1.pack()
        button2.pack()
        button3.pack();
def guardar():
    ab.guardarDatos(hojaAlimentos, hojaUsuarios, hojaPatologias)
    messagebox.showinfo("GUARDAR","Se ha guadado")

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("menuPrincipal"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("menuPrincipal"))
        button.pack()


if __name__ == "__main__":
        hojaAlimentos, hojaUsuarios, hojaPatologias = ab.cargarBaseDeDatos()
        mensajeError = "";
        login = tk.Tk();
        login.resizable(0,0)
        login.geometry('180x200')
        login.title("login")
        #iNICIALIZACIÓN DE FUENTES, SEPARADORES...
        fuente = font.Font(family="Helvetica",size=12, weight="bold")
        fuente2 = font.Font(family="Helvetica",size=7)
        #CUERPO
        lblMensaje = ttk.Label(login,text="",foreground="red",font=fuente2)
        lblU = ttk.Label(login,text="DNI", font=fuente)
        txtU = ttk.Entry(login,width=10)
        txtU.focus()
        lblP = ttk.Label(login,text="password",font=fuente)
        txtP = ttk.Entry(login,width=10, show="*")
        btnInit = ttk.Button(login, text="Inicio",command=partial(vs.cambio,txtU,txtP,login,lblU,lblMensaje))
        btnExit = ttk.Button(login, text="Salir",command=login.destroy)  
        #POSICIONAMIENTOOOO
        lblU.pack()
        txtU.focus()
        txtU.pack(fill=X)
        lblP.pack()
        txtP.pack(fill=X)   
        lblMensaje.pack();
        btnInit.pack(side=LEFT);
        btnExit.pack(side=RIGHT);
        login.mainloop(); 
        if(vs.getBandera()):
            app = SampleApp()
            app.mainloop()