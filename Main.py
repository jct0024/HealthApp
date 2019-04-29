import tkinter as tk                # python 3
import vista as vs;
from functools import partial
import AdminBase as ab;
import CalculosDieta as cd;
from tkinter import *
from tkinter import ttk,font, messagebox;
from PIL import ImageTk, Image
import numpy as np;
import datetime
import os
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        print(datetime.date.today())
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('500x500')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        menu = Menu(self)
        subMenuArchivo = Menu(menu)
        subMenuArchivo.add_command(label="Manual",command=self.pdf)
        subMenuArchivo.add_separator()
        subMenuArchivo.add_command(label="Guardar",command=guardar)
        menu.add_cascade(label='Archivo',menu=subMenuArchivo)
        self.config(menu=menu)
        self.frames = {}
        self.frames["menuPrincipal"] = menuPrincipal(parent=container, controller=self)
        self.frames["menuPrincipal"].grid(row=0, column=0, sticky="nsew")
        self.frames["menuPrincipal"].config(bg="powder blue")
        self.frames["InfoUsuario"] = InfoUsuario(parent=container, controller=self)
        self.frames["InfoUsuario"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["MostrarDieta"] = MostrarDieta(parent=container, controller=self)
        self.frames["MostrarDieta"].grid(row=0, column=0, sticky="nsew")
        self.frames["MostrarDieta"].config(bg="powder blue")
        self.show_frame("menuPrincipal")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    '''
    Funcion que muestra el Manual del pdf
    Posible evolución, que se pase el pdf como parametro y se pueda mostrat cualquier manual.
    '''
    def pdf(self):
        os.system('ejemplo.pdf')
    def guardar():
        ab.guardarDatos(hojaAlimentos, hojaUsuarios, hojaPatologias)
        messagebox.showinfo("GUARDAR","Se ha guadado")
 
        
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
                            command=lambda: controller.show_frame("InfoUsuario"),height = 2, width = 20,relief=GROOVE,bg="spring green")
        button2 = tk.Button(self, text="Dieta diaria",
                            command=lambda: controller.show_frame("MostrarDieta"),height = 2, width = 20,relief=GROOVE,bg="spring green")
        button3 = tk.Button(self, text="Guardar",
                            command=guardar,height = 2, width = 20,relief=GROOVE,bg="spring green")
        label.pack(side="top", fill="x", pady=10)
        self.icon_size.pack(side=LEFT)
        self.bar.pack(side=TOP)
        button1.pack()
        button2.pack()
        button3.pack();
    def refresh(self):
        self.update_idletasks
def guardar():
    ab.guardarDatos(hojaAlimentos, hojaUsuarios, hojaPatologias)
    messagebox.showinfo("GUARDAR","Se ha guadado")

class InfoUsuario(tk.Frame):
    def __init__(self, parent, controller):
        self.user,self.pwd = vs.getUsuario()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #lista = np.aray(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),:])
        self.c = 0;
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        for i in hojaUsuarios.iloc[int(ab.getFilaUsuario(self.user,hojaUsuarios)),:]:
            if(str(hojaUsuarios.columns.values[self.c]) == "patologia"):
                self.texto = str(hojaUsuarios.columns.values[self.c])+ ": "+str(hojaPatologias.iloc[i,1])
            elif(str(hojaUsuarios.columns.values[self.c]) == "password"):
                self.texto = str(hojaUsuarios.columns.values[self.c])+ ": *******"
            else:
                self.texto = str(hojaUsuarios.columns.values[self.c])+ ": "+str(i)
            self.labelInfo = tk.Label(self, text=self.texto)
            self.labelInfo.pack(anchor=tk.W)
            self.c+=1;
        btnEditar = tk.Button(self, text="Editar información",height = 2, width = 20,relief=GROOVE)
        btnEditar.pack();
        button = tk.Button(self, text="Volver al inicio",command=lambda: controller.show_frame("menuPrincipal"),relief=GROOVE)
        button.pack(side=BOTTOM)


class MostrarDieta(tk.Frame):
    global user;
    global pwd;
    global datosAlimCliente;
    global listMacDiarios;
    global totalKcalComidas;
    def __init__(self, parent, controller):
        self.codigo()
        '''
        Parte gráfica
        '''
        tk.Frame.__init__(self, parent)   
        self.controller = controller
        self.tab_control = ttk.Notebook(self)
        self.tabDesayuno = ttk.Frame(self.tab_control);
        self.tabAlmuerzo = ttk.Frame(self.tab_control);
        self.tabComida = ttk.Frame(self.tab_control);
        self.tabMerienda = ttk.Frame(self.tab_control);
        self.tabCena = ttk.Frame(self.tab_control);
        self.tab_control.add(self.tabDesayuno, text='Desayuno')
        self.tab_control.add(self.tabAlmuerzo, text='Almuerzo')
        self.tab_control.add(self.tabComida, text='Comida')
        self.tab_control.add(self.tabMerienda, text='Merienda')
        self.tab_control.add(self.tabCena, text='Cena')
        #NO BORRAAARR, DE MOMENTO NO LO NECESITAMOS, PERO ASI SE CAMBIARÍA EL COLOR DE LA BARRA.
        '''
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("black.Horizontal.TProgressbar", background='red')
        self.style.configure("black.Horizontal.TProgressbar", background='orange')
        '''
        self.barProgTotal = ttk.Progressbar(self,length=150,style='black.Horizontal.TProgressbar')
        self.barProgTotal['value'] = (100*datosAlimCliente[0])/self.listMacDiarios[0];

        self.banderaSelect = [False,False,False,False,False]
        ####-COMIDAS-####
        self.desayunoF()
        self.AlmuerzoF()
        self.ComidaF()
        self.MeriendaF()
        self.CenaF()
        self.tab_control.pack(expand=1, fill='both')

        ###-Comun todas comidas-######
        self.barProgTotal.pack(side=RIGHT)
        self.button = tk.Button(self, text="Volver al inicio", command=lambda: self.controller.show_frame("menuPrincipal"),relief=GROOVE)
        self.button.pack(side=LEFT)

        '''
        Aqui metemos la carga inicial de datos.
        '''
    def codigo(self):
        self.user,self.pwd = vs.getUsuario();
        #Indice de la fila del usuario
        self.n_FilaUser = ab.comprobarUsuario(self.user,self.pwd);
        #Kcalorias que el usuario debe tomar al dia en base a su dieta
        self.kcal_Por_Dia = cd.calculoTMB(hojaUsuarios.iloc[self.n_FilaUser,:])
        if (hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(self.user,hojaUsuarios),9],hojaPatologias)),2] == 'normal' or hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(self.user,hojaUsuarios),9],hojaPatologias)),2] == 'bajo azucares'):    
            #Lista en la cual se encuentran los macronutrientes que el usuario ha de comer en kcal, hidratos, proteina y grasas
            self.listMacDiarios = np.array(cd.distribuciónDeMacronutrientes(self.kcal_Por_Dia,'normal'))
        #Distribución en Kcal en desayuno, almuerzo, comido, merienda y cena.
        self.listDistribuciónKcal = np.array(cd.repartoDeKcal(self.listMacDiarios[0]))
        #Sacamos las patologias que tiene el usuario.
        if(hojaUsuarios.iloc[int(ab.getFilaUsuario(self.user,hojaUsuarios)),9]>0 and hojaUsuarios.iloc[int(ab.getFilaUsuario(self.user,hojaUsuarios)),9]<9999):
            self.datosPatologias = np.array(hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(self.user,hojaUsuarios),9],hojaPatologias)),:])
        #CARGAMOS las 5 comidas
        self.desayuno,self.almuerzo,self.comida,self.merienda,self.cena = cd.listasPorTipo(hojaAlimentos);  
    '''
    Serie de funciones que lo que hace es según la comida en la que estemos (Desayuno, almuerzo...)
    Primero te ordena la lsita de la forma mas conveniente para el tipo de comida de manera simple por el macronutriente para
    conseguir una mayor precision, luego te filtra la lista, quitandote aquellos alimentos que no cumplan el umbral de calidad para la consulta
    actual, te muestra cual es tu objetivo total y lo que llevas, crea los botones en base al número de opciones que quieras que te aparezcan
    Según eliges una opción a la derecha te indica su información
    '''
    def desayunoF(self):
        self.opc=-1;
        self.label = tk.Label(self.tabDesayuno, text="-DESAYUNO-", font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        selected = IntVar()
        i=0;
        umbral=2
        self.desayuno = self.desayuno.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.desayuno = cd.OrdMinimaDiferencia(self.desayuno,self.listDistribuciónKcal[0],"desayuno",datosAlimCliente,self.kcal_Por_Dia)
        self.filtDesayuno = self.desayuno.loc[self.desayuno["Calidad"] <= umbral]
        self.filtDesayuno = self.filtDesayuno.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabDesayuno,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal")
        self.objetivo.pack()
        self.cont_comida_inf = tk.Frame(self.tabDesayuno);
        self.cont_opciones_Des =tk.Frame(self.cont_comida_inf)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf)
        self.label_Informacion_comida = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN")
        self.label_Informacion_comida.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        
        botones = {};
        while(i<n_opciones):
            nombre=str(i)+") "+str(self.filtDesayuno["Nombre"].iloc[i])+" ("+ str(self.filtDesayuno["Calorias"].iloc[i])+"Kcal)"
            self.rad1 = ttk.Radiobutton(self.cont_opciones_Des,text=str(nombre), value=i, variable=selected, command=partial(self.MostrarInfo,i,"desayuno"))
            #rad1['state']='disable' #DESABILITAMOS LOS BOTONES.
            self.rad1.pack(anchor=tk.W)
            nomb = "boton"+str(i)
            botones[nomb]=self.rad1
            i=i+1;
        self.cont_opciones_Des.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        btnSel = tk.Button(self.tabDesayuno, text="Seleccionar")
        btnSel.config( command=partial(vs.seleccionar,"desayuno",botones,btnSel,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtDesayuno,self.barProgTotal,self.listMacDiarios))
        self.btnRefr = tk.Button(self.tabDesayuno, text="Refrescar", command=partial(self.refresh,"desayuno"))
        btnSel.pack(fill=X)
        self.btnRefr.pack(fill=X)

    def AlmuerzoF(self):
        self.label = tk.Label(self.tabAlmuerzo, text="-ALMUERZO-", font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabAlmuerzo);
        self.cont_opciones_Des =tk.Frame(self.cont_comida_inf)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf)
        self.label_Informacion_Alm = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN")
        self.label_Informacion_Alm.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.almuerzo = self.almuerzo.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.almuerzo = cd.OrdMinimaDiferencia(self.almuerzo,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia)
        self.filtAlmuerzo = self.almuerzo.loc[self.almuerzo["Calidad"] <= umbral]
        self.filtAlmuerzo = self.filtAlmuerzo.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabAlmuerzo,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal")
        self.objetivo.pack()
        botonesAl=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtAlmuerzo["Nombre"].iloc[i])+" ("+ str(self.filtAlmuerzo["Calorias"].iloc[i])+"Kcal)"
            self.rad2 = ttk.Radiobutton(self.cont_opciones_Des,text=str(nombre), value=i, variable=selected, command=partial(self.MostrarInfo,i,"almuerzo"))
            self.rad2.pack(anchor=tk.W)
            nomb = "botonA"+str(i)
            botonesAl[nomb]=self.rad2
            i=i+1;
        self.cont_opciones_Des.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        btnSel = tk.Button(self.tabAlmuerzo, text="Seleccionar")
        btnSel.config(command=partial(vs.seleccionar,"almuerzo",botonesAl,btnSel,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtAlmuerzo,self.barProgTotal,self.listMacDiarios))
        
        self.btnRefr = tk.Button(self.tabAlmuerzo, text="Refrescar", command=partial(self.refresh,"desayuno"))
        btnSel.pack(fill=X)
        self.btnRefr.pack(fill=X)
    def ComidaF(self):
        self.label = tk.Label(self.tabComida, text="-COMIDA-", font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabComida);
        self.cont_opciones_Des =tk.Frame(self.cont_comida_inf)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf)
        self.label_Informacion_Com = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN")
        self.label_Informacion_Com.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.comida = self.comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.comida = cd.OrdMinimaDiferencia(self.comida,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia)
        self.filtComida = self.comida.loc[self.comida["Calidad"] <= umbral]
        self.filtComida = self.filtComida.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabComida,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal")
        self.objetivo.pack()
        botonesCom=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtComida["Nombre"].iloc[i])+" ("+ str(self.filtComida["Calorias"].iloc[i])+"Kcal)"
            self.radCom = ttk.Radiobutton(self.cont_opciones_Des,text=str(nombre), value=i, variable=selected, command=partial(self.MostrarInfo,i,"comida"))
            self.radCom.pack(anchor=tk.W)
            nomb = "botonA"+str(i)
            botonesCom[nomb]=self.radCom
            i=i+1;
        self.cont_opciones_Des.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        btnSel = tk.Button(self.tabComida, text="Seleccionar")
        cont = btnSel.config(command=partial(vs.seleccionar,"comida",botonesCom,btnSel,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios))
        #self.barProgTotal['value'] = int((100*datosAlimCliente[0])/self.listMacDiarios[0]);
        self.btnRefr = tk.Button(self.tabComida, text="Refrescar", command=partial(self.refresh,"desayuno"))
        btnSel.pack(fill=X)
        self.btnRefr.pack(fill=X)
    def MeriendaF(self):
        self.label = tk.Label(self.tabMerienda, text="-MERIENDA-", font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabMerienda);
        self.cont_opciones_Des =tk.Frame(self.cont_comida_inf)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf)
        self.label_Informacion_Mer = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN")
        self.label_Informacion_Mer.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.merienda = self.merienda.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.merienda = cd.OrdMinimaDiferencia(self.merienda,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia)
        self.filtMerienda = self.merienda.loc[self.merienda["Calidad"] <= umbral]
        self.filtMerienda = self.filtMerienda.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabMerienda,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal")
        self.objetivo.pack()
        botonesMer=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtMerienda["Nombre"].iloc[i])+" ("+ str(self.filtMerienda["Calorias"].iloc[i])+"Kcal)"
            self.radMer = ttk.Radiobutton(self.cont_opciones_Des,text=str(nombre), value=i, variable=selected, command=partial(self.MostrarInfo,i,"merienda"))
            self.radMer.pack(anchor=tk.W)
            nomb = "botonA"+str(i)
            botonesMer[nomb]=self.radMer
            i=i+1;
        self.cont_opciones_Des.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        btnSel = tk.Button(self.tabMerienda, text="Seleccionar")
        btnSel.config(command=partial(vs.seleccionar,"merienda",botonesMer,btnSel,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios))
        self.btnRefr = tk.Button(self.tabMerienda, text="Refrescar", command=partial(self.refresh,"merienda"))
        btnSel.pack(fill=X)
        self.btnRefr.pack(fill=X)
    def CenaF(self):
        self.label = tk.Label(self.tabCena, text="-CENA-", font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabCena);
        self.cont_opciones_Des =tk.Frame(self.cont_comida_inf)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf)
        self.label_Informacion_Cen = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN")
        self.label_Informacion_Cen.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.cena = self.cena.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.cena = cd.OrdMinimaDiferencia(self.cena,self.listDistribuciónKcal[1],"cena",datosAlimCliente,self.kcal_Por_Dia)
        self.filtCena = self.cena.loc[self.cena["Calidad"] <= umbral]
        self.filtCena = self.filtCena.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabCena,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal")
        self.objetivo.pack()
        botonesCen=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtCena["Nombre"].iloc[i])+" ("+ str(self.filtCena["Calorias"].iloc[i])+"Kcal)"
            self.radCen = ttk.Radiobutton(self.cont_opciones_Des,text=str(nombre), value=i, variable=selected, command=partial(self.MostrarInfo,i,"cena"))
            self.radCen.pack(anchor=tk.W)
            nomb = "botonA"+str(i)
            botonesCen[nomb]=self.radCen
            i=i+1;
        self.cont_opciones_Des.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        btnSel = tk.Button(self.tabCena, text="Seleccionar")
        btnSel.config(command=partial(vs.seleccionar,"cena",botonesCen,btnSel,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios))
        self.btnRefr = tk.Button(self.tabCena, text="Refrescar", command=partial(self.refresh,"cena"))
        btnSel.pack(fill=X)
        self.btnRefr.pack(fill=X)

    '''
    Muestra la información del checkButton seleccionado
    Params: i Indice de la comida en la lista filtrada
    Params: tipo Tipo de comida para saber cual es el tipo de desayuno a criptar
    '''
    def MostrarInfo(self,i,tipo):
        if(tipo == "desayuno"):
            texto = "Nombre: "+str(self.filtDesayuno["Nombre"].iloc[i])+" \nCalorias: "+str(self.filtDesayuno["Calorias"].iloc[i])+"\nGrasa: "+str(self.filtDesayuno["Grasa"].iloc[i])+" (Saturadas: "+str(self.filtDesayuno["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(self.filtDesayuno["Hidratos"].iloc[i])+"(Azucares"+str(self.filtDesayuno["Azucares"].iloc[i])+")\nProteina "+str(self.filtDesayuno["Proteina"].iloc[i])+"\nCalidad: "+str(self.filtDesayuno["Calidad"].iloc[i])
            self.label_Informacion_comida.config(text=texto);
        elif(tipo=="almuerzo"):
            texto = "Nombre: "+str(self.filtAlmuerzo["Nombre"].iloc[i])+" \nCalorias: "+str(self.filtAlmuerzo["Calorias"].iloc[i])+"\nGrasa: "+str(self.filtAlmuerzo["Grasa"].iloc[i])+" (Saturadas: "+str(self.filtAlmuerzo["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(self.filtAlmuerzo["Hidratos"].iloc[i])+"(Azucares"+str(self.filtAlmuerzo["Azucares"].iloc[i])+")\nProteina "+str(self.filtAlmuerzo["Proteina"].iloc[i])+"\nCalidad: "+str(self.filtAlmuerzo["Calidad"].iloc[i])
            self.label_Informacion_Alm.config(text=texto);
        elif(tipo=="comida"):
            texto = "Nombre: "+str(self.filtComida["Nombre"].iloc[i])+" \nCalorias: "+str(self.filtComida["Calorias"].iloc[i])+"\nGrasa: "+str(self.filtComida["Grasa"].iloc[i])+" (Saturadas: "+str(self.filtComida["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(self.filtComida["Hidratos"].iloc[i])+"(Azucares"+str(self.filtComida["Azucares"].iloc[i])+")\nProteina "+str(self.filtComida["Proteina"].iloc[i])+"\nCalidad: "+str(self.filtComida["Calidad"].iloc[i])
            self.label_Informacion_Com.config(text=texto);
        elif(tipo=="merienda"):
            texto = "Nombre: "+str(self.filtMerienda["Nombre"].iloc[i])+" \nCalorias: "+str(self.filtMerienda["Calorias"].iloc[i])+"\nGrasa: "+str(self.filtMerienda["Grasa"].iloc[i])+" (Saturadas: "+str(self.filtMerienda["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(self.filtMerienda["Hidratos"].iloc[i])+"(Azucares"+str(self.filtMerienda["Azucares"].iloc[i])+")\nProteina "+str(self.filtMerienda["Proteina"].iloc[i])+"\nCalidad: "+str(self.filtMerienda["Calidad"].iloc[i])
            self.label_Informacion_Mer.config(text=texto);
        elif(tipo=="cena"):
            texto = "Nombre: "+str(self.filtCena["Nombre"].iloc[i])+" \nCalorias: "+str(self.filtCena["Calorias"].iloc[i])+"\nGrasa: "+str(self.filtCena["Grasa"].iloc[i])+" (Saturadas: "+str(self.filtCena["Saturadas"].iloc[i])+")"+"\nHidratos: "+str(self.filtCena["Hidratos"].iloc[i])+"(Azucares"+str(self.filtCena["Azucares"].iloc[i])+")\nProteina "+str(self.filtCena["Proteina"].iloc[i])+"\nCalidad: "+str(self.filtCena["Calidad"].iloc[i])
            self.label_Informacion_Cen.config(text=texto);
    def refresh(self, tipoCom):
        if(tipoCom == "desayuno"):
           fila=ab.getFilaAlimento(self.filtDesayuno["Nombre"].iloc[0],hojaAlimentos);
           hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;  
           fila=ab.getFilaAlimento(self.filtDesayuno["Nombre"].iloc[1],hojaAlimentos);
           hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1;
           fila=ab.getFilaAlimento(self.filtDesayuno["Nombre"].iloc[2],hojaAlimentos);
           hojaAlimentos["LRE"].loc[fila] =hojaAlimentos["LRE"].loc[fila] + 1; 
           self.desayuno["LRE"].iloc[2] = self.desayuno["LRE"].iloc[2]+1
           self.desayuno["LRE"].iloc[0] = self.desayuno["LRE"].iloc[0]+1
           self.desayuno["LRE"].iloc[1] = self.desayuno["LRE"].iloc[1]+1
        self.tab_control.update
if __name__ == "__main__":
        #Variable que almacena lo que lleva comido el cliente en cuanto a datos
        datosAlimCliente = np.zeros(4)
        #Array que guarda lo que ha comido hoy el cliente
        menuDeHoy = np.empty(5, dtype = str)
        #Variable que almacena lo que tiene que comer
        listMacDiarios = np.zeros(4)
        totalKcalComidas=0;
        n_opciones = 3;
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