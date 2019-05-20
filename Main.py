import tkinter as tk                # python 3
import vista as vs;
from functools import partial
import AdminBase as ab;
import CalculosDieta as cd;
from tkinter import *
from tkinter import ttk,font, messagebox;
from PIL import ImageTk, Image
import numpy as np;
import os
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
        usr,pws =vs.getUsuario();
        histUA = ab.cargarHistorial(usr)
        ab.cargaHistorialHoy(histUA,menuDeHoy,datosAlimCliente,hojaAlimentos)
        menu = Menu(self)
        subMenuArchivo = Menu(menu)
        subMenuArchivo.add_command(label="Manual",command=self.pdf)
        subMenuArchivo.add_separator()
        subMenuArchivo.add_command(label="Guardar",command=guardar)
        subMenuArchivo.add_command(label="G-Hist",command=partial(ab.guardarHistorial,usr,menuDeHoy,histUA))
        menu.add_cascade(label='Archivo',menu=subMenuArchivo)
        self.config(menu=menu)
        self.frames = {}
        self.frames["menuPrincipal"] = menuPrincipal(parent=container, controller=self)
        self.frames["menuPrincipal"].grid(row=0, column=0, sticky="nsew")
        self.frames["menuPrincipal"].config(bg=fondoGeneral)
        
        self.frames["InfoUsuario"] = InfoUsuario(parent=container, controller=self)
        self.frames["InfoUsuario"].grid(row=0, column=0, sticky="nsew")
        self.frames["InfoUsuario"].config(bg=fondoGeneral)
        
        self.frames["editarInforUsuario"] = editarInforUsuario(parent=container, controller=self)
        self.frames["editarInforUsuario"].grid(row=0, column=0, sticky="nsew")
        self.frames["editarInforUsuario"].config(bg=fondoGeneral)
        
        self.frames["Historial"] = Historial(parent=container, controller=self)
        self.frames["Historial"].grid(row=0, column=0, sticky="nsew")
        self.frames["Historial"].config(bg=fondoGeneral)
        
        self.frames["histSemanal"] = histSemanal(parent=container, controller=self)
        self.frames["histSemanal"].grid(row=0, column=0, sticky="nsew")
        self.frames["histSemanal"].config(bg=fondoGeneral)
        
        self.frames["MostrarDieta"] = MostrarDieta(parent=container, controller=self)
        self.frames["MostrarDieta"].grid(row=0, column=0, sticky="nsew")
        self.frames["MostrarDieta"].config(bg=fondoGeneral)
        
        
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
        
        
        
        label = tk.Label(self, text="This is the start page", font=controller.title_font,bg=fondoGeneral)
        self.bar = tk.Frame(self, relief=RIDGE, borderwidth=5)
        self.imgPath = './descarga.jpg'
        self.icon = ImageTk.PhotoImage(Image.open('./descarga.jpg'))
        self.icon_size = Label(self.bar)
        self.icon_size.configure(image=self.icon)
        button1 = tk.Button(self, text="Información de Usuario",
                            command=lambda: controller.show_frame("InfoUsuario"),height = 2, width = 20,relief=GROOVE,bg=colorDetalles)
        button2 = tk.Button(self, text="Dieta diaria",
                            command=lambda: controller.show_frame("MostrarDieta"),height = 2, width = 20,relief=GROOVE,bg=colorDetalles)
        button3 = tk.Button(self, text="Historial",
                            command=lambda: controller.show_frame("Historial"),height = 2, width = 20,relief=GROOVE,bg=colorDetalles)
        label.pack(side="top", fill="x", pady=10)
        self.icon_size.pack(side=LEFT)
        self.bar.pack(side=TOP)
        button1.pack()
        button2.pack()
        button3.pack();
def guardar():
    ab.guardarDatos(hojaAlimentos, hojaUsuarios, hojaPatologias)
    messagebox.showinfo("GUARDAR","Se ha guadado")
class Historial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        usr,pws =vs.getUsuario();
        histUA = ab.cargarHistorial(usr)
        label = tk.Label(self, text="Historial", font=controller.title_font,bg=fondoGeneral)
        label.pack(side="top", fill="x", pady=10)
        self.history=tk.Frame(self,bg=fondoGeneral)
        self.frameBotones = tk.Frame(self.history,bg=fondoGeneral)
        self.grafo = tk.Frame(self.history,bg=fondoGeneral)
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        self.lin, = a.plot([],[],'r-')
        self.canvas = FigureCanvasTkAgg(f,self.grafo)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        btnGrafo = tk.Button(self.frameBotones,text='Mostrar',command=partial(vs.gráfico,self,[0,1,2,3],[0,1,4,9]),relief=GROOVE)
        btnGrafo2 = tk.Button(self.frameBotones,text='Otro',command=partial(vs.gráfico,self,[0,1,2,3],[3,2,1,0]),relief=GROOVE)
        self.history.pack()
        self.frameBotones.pack(side=LEFT)
        self.grafo.pack(side=tk.RIGHT)
        
        #Volver al iniciao
        button = tk.Button(self.frameBotones, text="Volver al inicio",command=lambda: controller.show_frame("menuPrincipal"),relief=GROOVE)
        button2 = tk.Button(self.frameBotones, text="Semana ingerida",command=lambda: controller.show_frame("histSemanal"),relief=GROOVE)
        btnGrafo.pack(fill=X)
        btnGrafo2.pack(fill=X)
        button2.pack(side=BOTTOM,fill=X)
        button.pack(side=BOTTOM,fill=X)
class histSemanal(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        usr,pws =vs.getUsuario();
        histUA = ab.cargarHistorial(usr)
        label = tk.Label(self, text="Historial", font=controller.title_font,bg=fondoGeneral)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Volver al inicio",command=lambda: controller.show_frame("Historial"),relief=GROOVE)
        button.pack()
class InfoUsuario(tk.Frame):
    def __init__(self, parent, controller):
        self.user,self.pwd = vs.getUsuario()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #lista = np.aray(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),:])
        self.c = 0;
        label = tk.Label(self, text="Información del usuario", font=controller.title_font,bg=fondoGeneral)
        label.pack(side="top", fill="x", pady=10)
        arrayLabelInfo={}
        for i in hojaUsuarios.iloc[int(ab.getFilaUsuario(self.user,hojaUsuarios)),:]:
            if(str(hojaUsuarios.columns.values[self.c]) == "patologia"):
                self.texto = str(hojaUsuarios.columns.values[self.c])+ ": "+str(hojaPatologias.iloc[i,1])
            elif(str(hojaUsuarios.columns.values[self.c]) == "password"):
                self.texto = str(hojaUsuarios.columns.values[self.c])+ ": *******"
            else:
                self.texto = str(hojaUsuarios.columns.values[self.c])+ ": "+str(i)
            nombre="inf"+str(self.c)
            self.labelInfo = tk.Label(self, text=self.texto,bg=fondoGeneral)
            arrayLabelInfo[nombre]=self.labelInfo
            self.labelInfo.pack(anchor=tk.W)
            self.c+=1;
        btnEditar = tk.Button(self, text="Editar información",height = 2, width = 20,command=lambda: controller.show_frame("editarInforUsuario"),relief=GROOVE)
        button = tk.Button(self, text="Volver al inicio",command=lambda: controller.show_frame("menuPrincipal"),relief=GROOVE)
        btnEditar.pack();
        
        button.pack(side=BOTTOM)

class editarInforUsuario(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.user,self.pwd = vs.getUsuario()
            self.controller = controller
            #lista = np.aray(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),:])
            self.c = 0;
            
            label = tk.Label(self, text="Editando información", font=controller.title_font,bg=fondoGeneral)    
            label.grid(column=0,row=0)
            
            label_Nom = Label(self, text="Nombre",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Nom.grid(column=0,row=1)
            
            self.entry_Nom = Entry(self,bg=fondoGeneral)
            self.entry_Nom.grid(column=1,row=1)
            
            label_Ape = Label(self, text="Apellidos",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Ape.grid(column=0,row=2)
            
            self.entry_Ape = Entry(self,bg=fondoGeneral)
            self.entry_Ape.grid(column=1,row=2)
            
            label_Eda = Label(self, text="Edad",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Eda.grid(column=0,row=3)         
            
            self.entry_Eda = Entry(self,bg=fondoGeneral)
            self.entry_Eda.grid(column=1,row=3)
            
            label_Alt = Label(self, text="Altura",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Alt.grid(column=0,row=4)       
            
            self.entry_Alt = Entry(self,bg=fondoGeneral)
            self.entry_Alt.grid(column=1,row=4)
            
            label_Pes = Label(self, text="Peso",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Pes.grid(column=0,row=5)       
            
            self.entry_Pes = Entry(self,bg=fondoGeneral)
            self.entry_Pes.grid(column=1,row=5)
            
            label_3 = Label(self, text="Sexo:",width=20,font=("bold", 10),bg=fondoGeneral)
            label_3.grid(column=0,row=6)
            self.var = IntVar()
            Radiobutton(self, text="Hombre",padx = 5, variable=self.var, value=1,bg=fondoGeneral).grid(column=0,row=7)
            Radiobutton(self, text="Mujer",padx = 20, variable=self.var, value=2,bg=fondoGeneral).grid(column=1,row=7)
            
            label_Act = Label(self, text="Actividad: ",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Act.grid(column=0,row=8)
            self.varAct = IntVar()
            Radiobutton(self, text="1 ",padx = 10, variable=self.varAct, value=1,bg=fondoGeneral).grid(column=0,row=9)
            Radiobutton(self, text="2 ",padx = 10, variable=self.varAct, value=2,bg=fondoGeneral).grid(column=1,row=9)
            Radiobutton(self, text="3 ",padx = 10, variable=self.varAct, value=3,bg=fondoGeneral).grid(column=0,row=10)
            Radiobutton(self, text="4 ",padx = 10, variable=self.varAct, value=4,bg=fondoGeneral).grid(column=1,row=10)
            
            label_3 = Label(self, text="Tipo",width=20,font=("bold", 10),bg=fondoGeneral)
            label_3.grid(column=0,row=11)
            self.varTipo = IntVar()
            Radiobutton(self, text="bajar",padx = 5, variable=self.varTipo, value=1,bg=fondoGeneral).grid(column=0,row=12)
            Radiobutton(self, text="mantener",padx = 20, variable=self.varTipo, value=2,bg=fondoGeneral).grid(column=1,row=12)
            Radiobutton(self, text="subir",padx = 20, variable=self.varTipo, value=3,bg=fondoGeneral).grid(column=2,row=12)
            '''
            label_4 = Label(self, text="country",width=20,font=("bold", 10))
            label_4.grid(column=0,row=13)
            
            list1 = ['Canada','India','UK','Nepal','Iceland','South Africa'];
            c=StringVar()
            droplist=OptionMenu(self,c, *list1)
            droplist.config(width=15)
            c.set('select your country') 
            droplist.grid(column=0,row=14)
            
            label_4 = Label(self, text="Programming",width=20,font=("bold", 10))
            label_4.place(x=85,y=330)
            var1 = IntVar()
            Checkbutton(self, text="java", variable=var1).place(x=235,y=330)
            var2 = IntVar()
            Checkbutton(self, text="python", variable=var2).place(x=290,y=330)
            '''
            a = Button(self, text='Submit',command=partial(self.value,self)).grid(column=0,row=15)
            print(a)
            button = tk.Button(self, text="Volver al inicio",command=lambda: controller.show_frame("InfoUsuario"),relief=GROOVE)
            button.grid(column=0,row=16)
            
            self.label_Error = Label(self, text="",width=20,font=("bold", 10),bg=fondoGeneral,foreground="red")
            self.label_Error.grid(column=0,row=17)
        def value(self,selfi):
            fila = ab.getFilaUsuario(selfi.user,hojaUsuarios)
            print(hojaUsuarios.loc[fila])
            print(selfi.varTipo.get())
            if(len(selfi.entry_Nom.get()) ==0 or len(selfi.entry_Ape.get()) == 0 or len(selfi.entry_Eda.get()) == 0 or len(selfi.entry_Alt.get()) == 0 or len(selfi.entry_Pes.get()) == 0):
                selfi.label_Error.config(text="ERROR: Algun dato erroneo, comprueba todo")
            else:
                hojaUsuarios['nombre'].loc[fila] = selfi.entry_Nom.get()
                hojaUsuarios['apellido'].loc[fila] = selfi.entry_Ape.get()
                if(selfi.var.get() == 1):
                    hojaUsuarios['sexo'] .loc[fila]= 'H'
                else:
                    hojaUsuarios['sexo'].loc[fila] = 'M'
                hojaUsuarios['edad'].loc[fila] = selfi.entry_Eda.get()
                hojaUsuarios['altura'].loc[fila] = selfi.entry_Alt.get()
                hojaUsuarios['peso'].loc[fila] = selfi.entry_Pes.get()
                hojaUsuarios['actividad'].loc[fila] = selfi.varAct.get()
                if(selfi.varTipo.get() == 1):
                    hojaUsuarios['tipo'].loc[fila] = "bajar"
                elif(selfi.varTipo.get() == 2):
                    hojaUsuarios['tipo'].loc[fila] = "mantener"
                else:
                    hojaUsuarios['tipo'].loc[fila] = "subir"
            print(hojaUsuarios.iloc[fila])

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
        self.style = ttk.Style()
        self.style.theme_use('clam')
        tk.Frame.__init__(self, parent)   
        self.controller = controller
        self.tab_control = ttk.Notebook(self)
        self.tabDesayuno = tk.Frame(self.tab_control,bg=fondoGeneral);
        self.tabAlmuerzo = tk.Frame(self.tab_control,bg=fondoGeneral);
        self.tabComida = tk.Frame(self.tab_control,bg=fondoGeneral);
        self.tabMerienda = tk.Frame(self.tab_control,bg=fondoGeneral);
        self.tabCena = tk.Frame(self.tab_control,bg=fondoGeneral);
        self.tab_control.add(self.tabDesayuno, text='Desayuno')
        self.tab_control.add(self.tabAlmuerzo, text='Almuerzo')
        self.tab_control.add(self.tabComida, text='Comida')
        self.tab_control.add(self.tabMerienda, text='Merienda')
        self.tab_control.add(self.tabCena, text='Cena')
        #NO BORRAAARR, DE MOMENTO NO LO NECESITAMOS, PERO ASI SE CAMBIARÍA EL COLOR DE LA BARRA.
        
        self.n_opciones = 3;
        self.style.configure("black.Horizontal.TProgressbar", background='green')
        #self.style.configure("black.Horizontal.TProgressbar", background='orange')
        
        self.barProgTotal = ttk.Progressbar(self,length=150,style='black.Horizontal.TProgressbar')
        self.barProgTotal['value'] = (100*datosAlimCliente[0])/self.listMacDiarios[0];
        vs.actualizarBarra(menuDeHoy,'alimento',self.barProgTotal,datosAlimCliente,self.listMacDiarios,self.style)
        self.banderaSelect = vs.crearArrayBandera(menuDeHoy)
        print(self.banderaSelect)
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
        self.label = tk.Label(self.tabDesayuno, text="-DESAYUNO-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        selected = IntVar()
        i=0;
        umbral=2
        self.desayuno = self.desayuno.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.desayuno = cd.OrdMinimaDiferencia(self.desayuno,self.listDistribuciónKcal[0],"desayuno",datosAlimCliente,self.kcal_Por_Dia)
        self.filtDesayuno = self.desayuno.loc[self.desayuno["Calidad"] <= umbral]
        self.filtDesayuno = self.filtDesayuno.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabDesayuno,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal // Objetivo Desayuno: "+str(self.listDistribuciónKcal[0]),bg=fondoGeneral)
        self.objetivo.pack()
        self.cont_comida_inf = tk.Frame(self.tabDesayuno,bg=fondoGeneral);
        self.cont_opciones_Des2 =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_comida = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_comida.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        self.LblLoQueLlevoDes = tk.Label(self.tabDesayuno, text="Llevo Comido: "+str(datosAlimCliente[0]),bg=fondoGeneral)
        self.LblLoQueLlevoDes.pack();
        self.botonesDes = {};
        while(i<self.n_opciones):
            nombre=str(i)+") "+str(self.filtDesayuno["Nombre"].iloc[i])+" ("+ str(self.filtDesayuno["Calorias"].iloc[i])+"Kcal)"
            self.rad1 = tk.Radiobutton(self.cont_opciones_Des2,text=str(nombre), value=i, variable=selected, command=partial(vs.MostrarInfo,i,self.filtDesayuno, self.label_Informacion_comida),bg=fondoGeneral)
            if(self.banderaSelect[0]):
                self.rad1['state']='disable' #DESABILITAMOS LOS BOTONES SI YA HEMOS ESCOGIFO.
            self.rad1.pack(anchor=tk.W)
            nomb = "botonD"+str(i)
            self.botonesDes[nomb]=self.rad1
            i=i+1;
        self.cont_opciones_Des2.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        self.btnRefrDes = tk.Button(self.tabDesayuno, text="Refrescar")
        if(self.banderaSelect[0]): 
            self.btnSelDes = tk.Button(self.tabDesayuno, text="Editar")
            self.btnRefrDes['state']='disable'
        else:
            self.btnSelDes = tk.Button(self.tabDesayuno, text="Seleccionar")
        self.btnSelDes.config( command=partial(vs.seleccionarYActualizarResto,self,"desayuno",self.botonesDes,self.btnSelDes,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtDesayuno,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        
        self.btnRefrDes.config(command=partial(vs.refrescar,self,"desayuno",self.cont_opciones_Des2,self.filtDesayuno,umbral,self.desayuno,hojaAlimentos,self.botonesDes,self.n_opciones,self.btnSelDes,self.btnRefrDes, self.label_Informacion_comida,self.listDistribuciónKcal[0],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        self.btnSelDes.pack(fill=X)
        self.btnRefrDes.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblDesTotal = tk.Label(self.tabDesayuno,text=textoTotal,bg=fondoGeneral)
        self.lblDesTotal.pack(anchor=tk.W)
    def AlmuerzoF(self):
        self.label = tk.Label(self.tabAlmuerzo, text="-ALMUERZO-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabAlmuerzo,bg=fondoGeneral);
        self.cont_opciones_Alm =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Alm = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Alm.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.almuerzo = self.almuerzo.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.almuerzo = cd.OrdMinimaDiferencia(self.almuerzo,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia)
        self.filtAlmuerzo = self.almuerzo.loc[self.almuerzo["Calidad"] <= umbral]
        self.filtAlmuerzo = self.filtAlmuerzo.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabAlmuerzo,text="Objetivo tital: "+str(self.listMacDiarios[0])+" Kcal // Objetivo Almuerzo: "+str(self.listDistribuciónKcal[1]),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoAlm = tk.Label(self.tabAlmuerzo, text="Llevo Comido: "+str(datosAlimCliente[0]),bg=fondoGeneral)
        self.LblLoQueLlevoAlm.pack();
        self.botonesAl=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtAlmuerzo["Nombre"].iloc[i])+" ("+ str(self.filtAlmuerzo["Calorias"].iloc[i])+"Kcal)"
            self.rad2 = tk.Radiobutton(self.cont_opciones_Alm,text=str(nombre), value=i, variable=selected, command=partial(vs.MostrarInfo,i,self.filtAlmuerzo, self.label_Informacion_Alm),bg=fondoGeneral)
            self.rad2.pack(anchor=tk.W)
            if(self.banderaSelect[1]):
                self.rad2['state']='disable' #DESABILITAMOS LOS BOTONES SI YA HEMOS ESCOGIFO.
            nomb = "botonA"+str(i)
            self.botonesAl[nomb]=self.rad2
            i=i+1;
        self.cont_opciones_Alm.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        self.btnRefrAlm = tk.Button(self.tabAlmuerzo, text="Refrescar")
        if(self.banderaSelect[1]):
            self.btnRefrAlm['state']='disable'
            self.btnSelAlm = tk.Button(self.tabAlmuerzo, text="Editar")
        else:
            self.btnSelAlm = tk.Button(self.tabAlmuerzo, text="Seleccionar")
        self.btnSelAlm.config(command=partial(vs.seleccionarYActualizarResto,self,"almuerzo",self.botonesAl,self.btnSelAlm,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtAlmuerzo,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        
        
        self.btnRefrAlm.config(command=partial(vs.refrescar,self,"almuerzo",self.cont_opciones_Alm,self.filtAlmuerzo,umbral,self.almuerzo,hojaAlimentos,self.botonesAl,self.n_opciones,self.btnSelAlm,self.btnRefrAlm, self.label_Informacion_Alm,self.listDistribuciónKcal[1],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        self.btnSelAlm.pack(fill=X)
        self.btnRefrAlm.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblAlmTotal = tk.Label(self.tabAlmuerzo,text=textoTotal,bg=fondoGeneral)
        self.lblAlmTotal.pack(anchor=tk.W)
    def ComidaF(self):
        
        self.label = tk.Label(self.tabComida, text="-COMIDA-", font=self.controller.title_font)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabComida,bg=fondoGeneral);
        self.cont_opciones_Com =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Com = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Com.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.comida = self.comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.comida = cd.OrdMinimaDiferencia(self.comida,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia)
        self.filtComida = self.comida.loc[self.comida["Calidad"] <= umbral]
        self.filtComida = self.filtComida.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabComida,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal // Objetivo Comida: "+str(self.listDistribuciónKcal[2]),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoCom = tk.Label(self.tabComida, text="Llevo Comido: "+str(datosAlimCliente[0]),bg=fondoGeneral)
        self.LblLoQueLlevoCom.pack()
        self.botonesCom=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtComida["Nombre"].iloc[i])+" ("+ str(self.filtComida["Calorias"].iloc[i])+"Kcal)"
            self.radCom = tk.Radiobutton(self.cont_opciones_Com,text=str(nombre), value=i, variable=selected, command=partial(vs.MostrarInfo,i,self.filtComida, self.label_Informacion_Com),bg=fondoGeneral)
            self.radCom.pack(anchor=tk.W)
            if(self.banderaSelect[2]):
                self.radCom['state']='disable' #DESABILITAMOS LOS BOTONES SI YA HEMOS ESCOGIFO.
            nomb = "botonCo"+str(i)
            self.botonesCom[nomb]=self.radCom
            i=i+1;
        self.cont_opciones_Com.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        self.btnRefrCom = tk.Button(self.tabComida, text="Refrescar")
        if(self.banderaSelect[2]):
            self.btnRefrCom['state']='disable'
            self.btnSelCom = tk.Button(self.tabComida, text="Editar")
        else:
            self.btnSelCom = tk.Button(self.tabComida, text="Seleccionar")
        cont = self.btnSelCom.config(command=partial(vs.seleccionarYActualizarResto,self,"comida",self.botonesCom,self.btnSelCom,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        #self.barProgTotal['value'] = int((100*datosAlimCliente[0])/self.listMacDiarios[0]);
        self.btnRefrCom = tk.Button(self.tabComida, text="Refrescar")
        self.btnRefrCom.config(command=partial(vs.refrescar,self,"comida",self.cont_opciones_Com,self.filtComida,umbral,self.comida,hojaAlimentos,self.botonesCom,self.n_opciones,self.btnSelCom,self.btnRefrCom, self.label_Informacion_Com,self.listDistribuciónKcal[2],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        
        self.btnSelCom.pack(fill=X)
        self.btnRefrCom.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblComTotal = tk.Label(self.tabComida,text=textoTotal,bg=fondoGeneral)
        self.lblComTotal.pack(anchor=tk.W)
    def MeriendaF(self):
        self.label = tk.Label(self.tabMerienda, text="-MERIENDA-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabMerienda,bg=fondoGeneral);
        self.cont_opciones_Mer =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Mer = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Mer.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.merienda = self.merienda.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.merienda = cd.OrdMinimaDiferencia(self.merienda,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia)
        self.filtMerienda = self.merienda.loc[self.merienda["Calidad"] <= umbral]
        self.filtMerienda = self.filtMerienda.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabMerienda,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal // Objetivo Merienda: "+str(self.listDistribuciónKcal[3]),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoMer = tk.Label(self.tabMerienda, text="Llevo Comido: "+str(datosAlimCliente[0]),bg=fondoGeneral)
        self.LblLoQueLlevoMer.pack()
        self.botonesMer=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtMerienda["Nombre"].iloc[i])+" ("+ str(self.filtMerienda["Calorias"].iloc[i])+"Kcal)"
            self.radMer = tk.Radiobutton(self.cont_opciones_Mer,text=str(nombre), value=i, variable=selected, command=partial(vs.MostrarInfo,i,self.filtMerienda, self.label_Informacion_Mer),bg=fondoGeneral)
            self.radMer.pack(anchor=tk.W)
            if(self.banderaSelect[3]):
                self.radMer['state']='disable' #DESABILITAMOS LOS BOTONES SI YA HEMOS ESCOGIFO.
            nomb = "botonM"+str(i)
            self.botonesMer[nomb]=self.radMer
            i=i+1;
        self.cont_opciones_Mer.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        self.btnRefrMer = tk.Button(self.tabMerienda, text="Refrescar")
        
        if(self.banderaSelect[3]):
            self.btnRefrMer['state']='disable'
            self.btnSelMer = tk.Button(self.tabMerienda, text="Editar")
        else:
            self.btnSelMer = tk.Button(self.tabMerienda, text="Seleccionar")
        self.btnSelMer.config(command=partial(vs.seleccionarYActualizarResto,self,"merienda",self.botonesMer,self.btnSelMer,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        self.btnRefrMer = tk.Button(self.tabMerienda, text="Refrescar")
        self.btnRefrMer.config(command=partial(vs.refrescar,self,"merienda",self.cont_opciones_Mer,self.filtMerienda,umbral,self.merienda,hojaAlimentos,self.botonesMer,self.n_opciones,self.btnSelMer,self.btnRefrMer, self.label_Informacion_Mer,self.listDistribuciónKcal[3],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        
        self.btnSelMer.pack(fill=X)
        self.btnRefrMer.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblMerTotal = tk.Label(self.tabMerienda,text=textoTotal,bg=fondoGeneral)
        self.lblMerTotal.pack(anchor=tk.W)
    def CenaF(self):
        self.label = tk.Label(self.tabCena, text="-CENA-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=2
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabCena,bg=fondoGeneral);
        self.cont_opciones_Cen =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Cen = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Cen.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.cena = self.cena.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.cena = cd.OrdMinimaDiferencia(self.cena,self.listDistribuciónKcal[1],"cena",datosAlimCliente,self.kcal_Por_Dia)
        self.filtCena = self.cena.loc[self.cena["Calidad"] <= umbral]
        self.filtCena = self.filtCena.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabCena,text="Objetivo: "+str(self.listMacDiarios[0])+" Kcal // Objetivo Cena: "+str(self.listDistribuciónKcal[4]),bg=fondoGeneral)
        self.LblLoQueLlevoCen = tk.Label(self.tabCena, text="Llevo Comido: "+str(datosAlimCliente[0]),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoCen.pack()
        self.botonesCen=  dict()
        while i<3:
            nombre=str(i)+") "+str(self.filtCena["Nombre"].iloc[i])+" ("+ str(self.filtCena["Calorias"].iloc[i])+"Kcal)"
            self.radCen = tk.Radiobutton(self.cont_opciones_Cen,text=str(nombre), value=i, variable=selected, command=partial(vs.MostrarInfo,i,self.filtCena, self.label_Informacion_Cen),bg=fondoGeneral)
            self.radCen.pack(anchor=tk.W)
            if(self.banderaSelect[4]):
                self.radCen['state']='disable' #DESABILITAMOS LOS BOTONES SI YA HEMOS ESCOGIFO.
            nomb = "botonC"+str(i)
            self.botonesCen[nomb]=self.radCen
            i=i+1;
        self.cont_opciones_Cen.pack(side=LEFT)
        self.cont_inf_eleccion.pack(side=LEFT)
        self.cont_comida_inf.pack()
        self.btnRefrCen = tk.Button(self.tabCena, text="Refrescar")
        if(self.banderaSelect[4]):
            self.btnRefrCen['state']='disable'
            self.btnSelCen = tk.Button(self.tabCena, text="Editar")  
        else:
            self.btnSelCen = tk.Button(self.tabCena, text="Seleccionar")
        self.btnSelCen.config(command=partial(vs.seleccionarYActualizarResto,self,"cena",self.botonesCen,self.btnSelCen,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        self.btnRefrCen = tk.Button(self.tabCena, text="Refrescar")
        self.btnRefrCen.config(command=partial(vs.refrescar,self,"cena",self.cont_opciones_Cen,self.filtCena,umbral,self.cena,hojaAlimentos,self.botonesCen,self.n_opciones,self.btnSelCen,self.btnRefrCen, self.label_Informacion_Cen,self.listDistribuciónKcal[4],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        
        self.btnSelCen.pack(fill=X)
        self.btnRefrCen.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblCenTotal = tk.Label(self.tabCena,text=textoTotal,bg=fondoGeneral)
        self.lblCenTotal.pack(anchor=tk.W)

if __name__ == "__main__":
        #Variable que almacena lo que lleva comido el cliente en cuanto a datos
        datosAlimCliente = np.zeros(5)
        #Array que guarda lo que ha comido hoy el cliente
        fondoGeneral='powder blue'
        colorDetalles="spring green"
        menuDeHoy = ["","","","",""]
        #Variable que almacena lo que tiene que comer
        listMacDiarios = np.zeros(4)
        totalKcalComidas=0;
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