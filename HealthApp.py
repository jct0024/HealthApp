import tkinter as tk                # python 3
import vista as vs;
from functools import partial
import AdminBase as ab;
import CalculosDieta as cd;
from tkinter import *
from tkinter import ttk,font
from PIL import ImageTk, Image
import numpy as np;
import os
import matplotlib
import webbrowser
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
class HealthApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("HealthApp")
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('800x500')
        self.minsize(800,500)
        self.iconbitmap('assets/logo.ico')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        usr,pws =vs.getUsuario();
        self.histUA,self.historialTotal = ab.cargarHistorial(usr)
        ab.cargaHistorialHoy(self.histUA,menuDeHoy,datosAlimCliente,hojaAlimentos)
        menu = Menu(self)
        subMenuArchivo = Menu(menu)
        subMenuEstilo = Menu(menu)
        subMenuArchivo.add_command(label="Manual",command=self.pdf)
        config = [fondoGeneral,colorDetalles]
        subMenuArchivo.add_command(label="Guardar",command=partial(ab.guardaTodo,usr,menuDeHoy, self.historialTotal ,hojaAlimentos, hojaUsuarios, hojaPatologias,config))
        subMenuArchivo.add_separator()
        subMenuArchivo.add_command(label="Salir",command= lambda: self.destroy())
        menu.add_cascade(label='Archivo',menu=subMenuArchivo)
        ###################################################################
        subMenuEstilo.add_command(label="Azul/Verde",command=partial(vs.estiloTotal,0))
        subMenuEstilo.add_command(label="Blanco/Morado",command=partial(vs.estiloTotal,1))
        menu.add_cascade(label='Estilos',menu=subMenuEstilo)
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
        
        self.frames["addComida"] = addComida(parent=container, controller=self)
        self.frames["addComida"].grid(row=0, column=0, sticky="nsew")
        self.frames["addComida"].config(bg=fondoGeneral)
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
        os.system('assets\Manual.pdf')
 
        
class menuPrincipal(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        
        label = tk.Label(self, text="Página principal", font=controller.title_font,bg=fondoGeneral)
        self.bar = tk.Frame(self, relief=RIDGE, borderwidth=5)
        self.imgPath = 'assets/logo.png'
        imagen = Image.open(self.imgPath)
        imagen = imagen.resize((250, 250), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(imagen)
        self.icon_size = Label(self.bar,bg=fondoGeneral)
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
class Historial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        usr,pws =vs.getUsuario();
        self.histUA = self.controller.histUA

        label = tk.Label(self, text="Historial", font=controller.title_font,bg=fondoGeneral)
        label.pack(side="top", fill="x", pady=10)
        self.history=tk.Frame(self,bg=fondoGeneral)
        self.frameBotones = tk.Frame(self.history,bg=fondoGeneral)
        self.grafo = tk.Frame(self.history,bg=fondoGeneral)
        f = Figure(figsize=(5,5), dpi=100)
        self.a = f.add_subplot(111)
        self.lin, = self.a.plot([],[],'r-')
        self.canvas = FigureCanvasTkAgg(f,self.grafo)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        btnGrafoTotal = tk.Button(self.frameBotones,text='Grafico total mensual',command=partial(cd.graficoTotal,self,hojaAlimentos),relief=GROOVE,bg=colorDetalles)
        btnGrafoDes = tk.Button(self.frameBotones,text='Gráfico desayuno',command=partial(cd.graficoMejoraComida,self,hojaAlimentos,0),relief=GROOVE,bg=colorDetalles)
        btnGrafoAlm = tk.Button(self.frameBotones,text='Gráfico almuerzo',command=partial(cd.graficoMejoraComida,self,hojaAlimentos,1),relief=GROOVE,bg=colorDetalles)
        btnGrafoCom = tk.Button(self.frameBotones,text='Gráfico comida',command=partial(cd.graficoMejoraComida,self,hojaAlimentos,2),relief=GROOVE,bg=colorDetalles)
        btnGrafoMer = tk.Button(self.frameBotones,text='Gráfico merienda',command=partial(cd.graficoMejoraComida,self,hojaAlimentos,3),relief=GROOVE,bg=colorDetalles)
        btnGrafoCen = tk.Button(self.frameBotones,text='Gráfico cena',command=partial(cd.graficoMejoraComida,self,hojaAlimentos,4),relief=GROOVE,bg=colorDetalles)
        self.history.pack()
        self.frameBotones.pack(side=LEFT)
        self.grafo.pack(side=tk.RIGHT)
        
        buttonSemana = tk.Button(self.frameBotones, text="Ultimos 7 Días",command=lambda: controller.show_frame("histSemanal"),relief=GROOVE,bg=colorDetalles)
        #Volver al iniciao
        buttonComeBack = tk.Button(self.frameBotones, text="Volver al inicio",command=lambda: controller.show_frame("menuPrincipal"),relief=GROOVE,bg=colorDetalles)
        
        btnGrafoTotal.pack(fill=X)
        btnGrafoDes.pack(fill=X)
        btnGrafoAlm.pack(fill=X)
        btnGrafoCom.pack(fill=X)
        btnGrafoMer.pack(fill=X)
        btnGrafoCen.pack(fill=X)
        buttonSemana.pack(fill=X)
        buttonComeBack.pack(fill=X)
'''
Clase encargada de mostrarte por pantalla la infroamción relativa al usuario a la ultima semana.
'''
class histSemanal(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Historial", font=controller.title_font,bg=fondoGeneral)
        label.pack(side="top", fill="x", pady=10)
        usr,pws =vs.getUsuario();
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = RIGHT, fill = Y)
        mylist = tk.Listbox(self, yscrollcommand = scrollbar.set)
        histUA = self.controller.histUA
        for index,dias in histUA.iterrows():
            if(index == 7):
                break;
            mylist.insert(END,'--Fecha: '+dias['Fecha']+'--','\n\tDesayuno: '+str(dias['Desayuno']),'\n\tAlmuerzo: '+str(dias['Almuerzo']),'\n\tComida: '+str(dias['Comida']),'\n\tMerienda: '+str(dias['Merienda']),'\n\tCena: '+str(dias['Cena']))
        mylist.pack(fill=BOTH)
        scrollbar.config( command = mylist.yview )
        button = tk.Button(self, text="Volver al inicio",command=lambda: controller.show_frame("Historial"),relief=GROOVE,bg=colorDetalles)
        button.pack()
class InfoUsuario(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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
        btnEditar = tk.Button(self, text="Editar información",height = 2, width = 20,command=lambda: controller.show_frame("editarInforUsuario"),relief=GROOVE,bg=colorDetalles)
        button = tk.Button(self, text="Volver al inicio",command=lambda: controller.show_frame("menuPrincipal"),relief=GROOVE,bg=colorDetalles)
        btnEditar.pack();
        
        button.pack(side=BOTTOM)



class editarInforUsuario(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = Label(self, text="Editando información", font=controller.title_font,bg=fondoGeneral)    
            label.pack()
            containerNOM = tk.Frame(self,bg=fondoGeneral)
            containerAPE = tk.Frame(self,bg=fondoGeneral)
            containerSEX = tk.Frame(self,bg=fondoGeneral)
            containerEDA = tk.Frame(self,bg=fondoGeneral)
            containerALT = tk.Frame(self,bg=fondoGeneral)
            containerPES = tk.Frame(self,bg=fondoGeneral)
            containerACT = tk.Frame(self,bg=fondoGeneral)
            containerPAT = tk.Frame(self,bg=fondoGeneral)
            containerTIP = tk.Frame(self,bg=fondoGeneral)
            containerBut = tk.Frame(self,bg=fondoGeneral)
            containerERR = tk.Frame(self,bg=fondoGeneral)
            containerNOM.pack(fill=X)
            containerAPE.pack(fill=X)
            containerSEX.pack(fill=X)
            containerEDA.pack(fill=X)
            containerALT.pack(fill=X)
            containerPES.pack(fill=X)
            containerACT.pack(fill=X)
            containerPAT.pack(fill=X)
            containerTIP.pack(fill=X)
            containerBut.pack(fill=X)
            containerERR.pack(fill=X)
            self.user,self.pwd = vs.getUsuario()
            self.controller = controller
            #lista = np.aray(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),:])
            self.c = 0;
            
            
            
            label_Nom = Label(containerNOM, text="Nombre",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Nom.pack(side=LEFT)
            
            self.entry_Nom = Entry(containerNOM,bg=fondoGeneral)
            self.entry_Nom.pack(expand=1,side=LEFT,fill=BOTH)
            
            label_Ape = Label(containerAPE, text="Apellidos",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Ape.pack(side=LEFT)
            
            self.entry_Ape = Entry(containerAPE,bg=fondoGeneral)
            self.entry_Ape.pack(expand=1,side=LEFT,fill=BOTH)
            
            label_Eda = Label(containerEDA, text="Edad (Años)",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Eda.pack(side=LEFT)       
            
            self.entry_Eda = Entry(containerEDA,bg=fondoGeneral)
            self.entry_Eda.pack(expand=1,side=LEFT,fill=BOTH)
            
            label_Alt = Label(containerALT, text="Altura (Cm)",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Alt.pack(side=LEFT)      
            
            self.entry_Alt = Entry(containerALT,bg=fondoGeneral)
            self.entry_Alt.pack(expand=1,side=LEFT,fill=BOTH)
            
            label_Pes = Label(containerPES, text="Peso (Kg)",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Pes.pack(side=LEFT)     
            
            self.entry_Pes = Entry(containerPES,bg=fondoGeneral)
            self.entry_Pes.pack(expand=1,side=LEFT,fill=BOTH)
            
            label_3 = Label(containerSEX, text="Sexo:",width=20,font=("bold", 10),bg=fondoGeneral)
            label_3.pack(side=LEFT)
            self.var = IntVar()
            Radiobutton(containerSEX, text="Hombre",padx = 5, variable=self.var, value=1,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerSEX, text="Mujer",padx = 20, variable=self.var, value=2,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            
            label_Act = Label(containerACT, text="Actividad: ",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Act.pack(side=LEFT)
            self.varAct = IntVar()
            Radiobutton(containerACT, text="1 ",padx = 10, variable=self.varAct, value=1,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerACT, text="2 ",padx = 10, variable=self.varAct, value=2,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerACT, text="3 ",padx = 10, variable=self.varAct, value=3,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerACT, text="4 ",padx = 10, variable=self.varAct, value=4,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerACT, text="5 ",padx = 10, variable=self.varAct, value=5,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            
            label_3 = Label(containerTIP, text="Tipo",width=20,font=("bold", 10),bg=fondoGeneral)
            label_3.pack(side=LEFT)
            self.varTipo = IntVar()
            Radiobutton(containerTIP, text="bajar",padx = 5, variable=self.varTipo, value=1,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerTIP, text="mantener",padx = 20, variable=self.varTipo, value=2,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            Radiobutton(containerTIP, text="subir",padx = 20, variable=self.varTipo, value=3,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            
            listPatologias=list(hojaPatologias.iloc[:,1])
            label_Pat =  Label(containerPAT, text="Patología: ",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Pat.pack(side=LEFT)
            usr = hojaUsuarios[hojaUsuarios.id == int(self.user)]
            patologia=tk.StringVar()
            patologia.set(listPatologias[int(usr['patologia'])])
            droplist=tk.OptionMenu(containerPAT,patologia, *listPatologias)
            droplist.config(width=90, font=('Helvetica', 12), relief=tk.GROOVE,bg=fondoGeneral)
             
            droplist.pack(expand=1,side=LEFT,fill=BOTH)
            buttonEnviar = Button(containerBut, text='Aceptar y Guardar',command=partial(ab.ComproYAlmacenamientoUsuario,hojaUsuarios,self, controller,hojaPatologias, patologia),bg=colorDetalles,relief=GROOVE).pack(fill=X)
            button = Button(containerBut, text="Cancelar",command=lambda: controller.show_frame("InfoUsuario"),relief=GROOVE,bg=colorDetalles).pack(fill=X)
            
            self.label_Error = Label(containerERR, text="",width=20,font=("bold", 10),bg=fondoGeneral,foreground="red")
            self.label_Error.pack()


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
        #Tabulación de comidas
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
        
        
        #Cara alegre
        self.imgPath ='assets/caraVerde.png'
        self.imagenVerde = Image.open( self.imgPath)
        self.imagenVerde =  self.imagenVerde.resize((25, 25), Image.ANTIALIAS)
        self.iconoV = ImageTk.PhotoImage( self.imagenVerde, master=self)   
        self.iconverde = tk.Label(self,bg=fondoGeneral)
        self.iconverde.configure(image= self.iconoV)
        
             
        self.n_opciones = 3;
        self.style.configure("black.Horizontal.TProgressbar", background='green')      
        self.barProgTotal = ttk.Progressbar(self,length=150,style='black.Horizontal.TProgressbar')
        
        #Cara triste
        self.imgPath ='assets/caraRoja.png'
        self.imagenRojo = Image.open( self.imgPath)
        self.imagenRojo =  self.imagenRojo.resize((25, 25), Image.ANTIALIAS)
        self.iconoRojo = ImageTk.PhotoImage( self.imagenRojo, master=self)   
        self.iconRojo = tk.Label(self,bg=fondoGeneral)
        self.iconRojo.configure(image= self.iconoRojo)
        
        n=0;
        calidad = 0;
        for i in menuDeHoy:
            if (i != ""):
                n+=1;
        if not (n == 0):
            calidad = datosAlimCliente[4]/n
        else:
            calidad=0;
        self.barProgTotal['value'] = (100*calidad)/5;
        vs.actualizarBarra(menuDeHoy,'alimento',self.barProgTotal,datosAlimCliente,self.listMacDiarios,self.style)
        self.banderaSelect = vs.crearArrayBandera(menuDeHoy)
        ####-COMIDAS-####
        self.desayunoF()
        self.AlmuerzoF()
        self.ComidaF()
        self.MeriendaF()
        self.CenaF()
        self.tab_control.pack(expand=1, fill='both')
        
        ###-Comun todas comidas-######
        self.iconRojo.pack(side=tk.RIGHT)
        self.barProgTotal.pack(side=RIGHT)
        self.iconverde.pack(side=tk.RIGHT)
        self.buttonInicio = tk.Button(self, text="Volver al inicio", command=lambda: self.controller.show_frame("menuPrincipal"),relief=GROOVE,bg=colorDetalles)
        self.buttonAddComida = tk.Button(self, text="Añadir Alimento", command=lambda: self.controller.show_frame("addComida"),relief=GROOVE,bg=colorDetalles)
        self.buttonInicio.pack(side=LEFT)
        self.buttonAddComida.pack(side=LEFT)

        '''
        Aqui metemos la carga inicial de datos.
        '''
    def codigo(self):
        self.user,self.pwd = vs.getUsuario();
        #Indice de la fila del usuario
        self.n_FilaUser = ab.comprobarUsuario(self.user,self.pwd);
        #Kcalorias que el usuario debe tomar al dia en base a su dieta
        self.kcal_Por_Dia = cd.calculoTMB(hojaUsuarios.iloc[self.n_FilaUser,:])
        #if (hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(self.user,hojaUsuarios),9],hojaPatologias)),2] == 'normal' or hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(self.user,hojaUsuarios),9],hojaPatologias)),2] == 'bajo azucares'):    
        #Lista en la cual se encuentran los macronutrientes que el usuario ha de comer en kcal, hidratos, proteina y grasas
        self.listMacDiarios = np.array(cd.distribuciónDeMacronutrientes(self.kcal_Por_Dia,hojaPatologias.iloc[int(ab.getFilaPatologia(hojaUsuarios.iloc[ab.getFilaUsuario(self.user,hojaUsuarios),9],hojaPatologias)),2]))
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
        umbral=1
        self.desayuno = self.desayuno.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.desayuno = cd.OrdMinimaDiferencia(self.desayuno,self.listDistribuciónKcal[0],"desayuno",datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios)
        self.filtDesayuno = self.desayuno.loc[self.desayuno["Calidad"] <= umbral]
        self.filtDesayuno = self.filtDesayuno.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabDesayuno,text="Objetivo: "+str(np.round(self.listMacDiarios[0]))+" Kcal // Objetivo Desayuno: "+str(np.round(self.listDistribuciónKcal[0])),bg=fondoGeneral)
        self.objetivo.pack()
        self.cont_comida_inf = tk.Frame(self.tabDesayuno,bg=fondoGeneral);
        self.cont_opciones_Des2 =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_comida = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_comida.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        self.LblLoQueLlevoDes = tk.Label(self.tabDesayuno, text="Llevo Comido: "+str(np.round(datosAlimCliente[0])),bg=fondoGeneral)
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
        self.btnSelDes.config( command=partial(vs.seleccionarYActualizarResto,self,"desayuno",self.botonesDes,self.btnSelDes,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtDesayuno,self.barProgTotal,self.listMacDiarios,self.style,umbral),bg=colorDetalles)
        
        self.btnRefrDes.config(command=partial(vs.refrescar,self,"desayuno",self.cont_opciones_Des2,self.filtDesayuno,umbral,self.desayuno,hojaAlimentos,self.botonesDes,self.n_opciones,self.btnSelDes,self.btnRefrDes, self.label_Informacion_comida,self.listDistribuciónKcal[0],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style),bg=colorDetalles)
        self.btnSelDes.pack(fill=X)
        self.btnRefrDes.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblDesTotal = tk.Label(self.tabDesayuno,text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]),bg=fondoGeneral)
        self.lblDesTotal.pack(anchor=tk.W)
    def AlmuerzoF(self):
        self.label = tk.Label(self.tabAlmuerzo, text="-ALMUERZO-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=1
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabAlmuerzo,bg=fondoGeneral);
        self.cont_opciones_Alm =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Alm = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Alm.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.almuerzo = self.almuerzo.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.almuerzo = cd.OrdMinimaDiferencia(self.almuerzo,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios)
        self.filtAlmuerzo = self.almuerzo.loc[self.almuerzo["Calidad"] <= umbral]
        self.filtAlmuerzo = self.filtAlmuerzo.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabAlmuerzo,text="Objetivo tital: "+str(np.round(self.listMacDiarios[0]))+" Kcal // Objetivo Almuerzo: "+str(np.round(self.listDistribuciónKcal[1])),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoAlm = tk.Label(self.tabAlmuerzo, text="Llevo Comido: "+str(np.round(datosAlimCliente[0])),bg=fondoGeneral)
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
        self.btnRefrAlm = tk.Button(self.tabAlmuerzo, text="Refrescar",bg=colorDetalles)
        if(self.banderaSelect[1]):
            self.btnRefrAlm['state']='disable'
            self.btnSelAlm = tk.Button(self.tabAlmuerzo, text="Editar",bg=colorDetalles)
        else:
            self.btnSelAlm = tk.Button(self.tabAlmuerzo, text="Seleccionar",bg=colorDetalles)
        self.btnSelAlm.config(command=partial(vs.seleccionarYActualizarResto,self,"almuerzo",self.botonesAl,self.btnSelAlm,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtAlmuerzo,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        
        
        self.btnRefrAlm.config(command=partial(vs.refrescar,self,"almuerzo",self.cont_opciones_Alm,self.filtAlmuerzo,umbral,self.almuerzo,hojaAlimentos,self.botonesAl,self.n_opciones,self.btnSelAlm,self.btnRefrAlm, self.label_Informacion_Alm,self.listDistribuciónKcal[1],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        self.btnSelAlm.pack(fill=X)
        self.btnRefrAlm.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblAlmTotal = tk.Label(self.tabAlmuerzo,text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]),bg=fondoGeneral)
        self.lblAlmTotal.pack(anchor=tk.W)
    def ComidaF(self):
        
        self.label = tk.Label(self.tabComida, text="-COMIDA-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=1
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabComida,bg=fondoGeneral);
        self.cont_opciones_Com =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Com = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Com.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.comida = self.comida.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.comida = cd.OrdMinimaDiferencia(self.comida,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios)
        self.filtComida = self.comida.loc[self.comida["Calidad"] <= umbral]
        self.filtComida = self.filtComida.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabComida,text="Objetivo: "+str(np.round(self.listMacDiarios[0]))+" Kcal // Objetivo Comida: "+str(np.round(self.listDistribuciónKcal[2])),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoCom = tk.Label(self.tabComida, text="Llevo Comido: "+str(np.round(datosAlimCliente[0])),bg=fondoGeneral)
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
        self.btnRefrCom = tk.Button(self.tabComida, text="Refrescar",bg=colorDetalles)
        if(self.banderaSelect[2]):
            self.btnRefrCom['state']='disable'
            self.btnSelCom = tk.Button(self.tabComida, text="Editar",bg=colorDetalles)
        else:
            self.btnSelCom = tk.Button(self.tabComida, text="Seleccionar",bg=colorDetalles)
        cont = self.btnSelCom.config(command=partial(vs.seleccionarYActualizarResto,self,"comida",self.botonesCom,self.btnSelCom,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        self.btnRefrCom.config(command=partial(vs.refrescar,self,"comida",self.cont_opciones_Com,self.filtComida,umbral,self.comida,hojaAlimentos,self.botonesCom,self.n_opciones,self.btnSelCom,self.btnRefrCom, self.label_Informacion_Com,self.listDistribuciónKcal[2],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        
        self.btnSelCom.pack(fill=X)
        self.btnRefrCom.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblComTotal = tk.Label(self.tabComida,text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]),bg=fondoGeneral)
        self.lblComTotal.pack(anchor=tk.W)
    def MeriendaF(self):
        self.label = tk.Label(self.tabMerienda, text="-MERIENDA-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=1
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabMerienda,bg=fondoGeneral);
        self.cont_opciones_Mer =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Mer = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Mer.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.merienda = self.merienda.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.merienda = cd.OrdMinimaDiferencia(self.merienda,self.listDistribuciónKcal[1],"almuerzo",datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios)
        self.filtMerienda = self.merienda.loc[self.merienda["Calidad"] <= umbral]
        self.filtMerienda = self.filtMerienda.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabMerienda,text="Objetivo: "+str(np.round(self.listMacDiarios[0]))+" Kcal // Objetivo Merienda: "+str(np.round(self.listDistribuciónKcal[3])),bg=fondoGeneral)
        self.objetivo.pack()
        self.LblLoQueLlevoMer = tk.Label(self.tabMerienda, text="Llevo Comido: "+str(np.round(datosAlimCliente[0])),bg=fondoGeneral)
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
        self.btnRefrMer = tk.Button(self.tabMerienda, text="Refrescar",bg=colorDetalles)
        
        if(self.banderaSelect[3]):
            self.btnRefrMer['state']='disable'
            self.btnSelMer = tk.Button(self.tabMerienda, text="Editar",bg=colorDetalles)
        else:
            self.btnSelMer = tk.Button(self.tabMerienda, text="Seleccionar",bg=colorDetalles)
        self.btnSelMer.config(command=partial(vs.seleccionarYActualizarResto,self,"merienda",self.botonesMer,self.btnSelMer,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        self.btnRefrMer.config(command=partial(vs.refrescar,self,"merienda",self.cont_opciones_Mer,self.filtMerienda,umbral,self.merienda,hojaAlimentos,self.botonesMer,self.n_opciones,self.btnSelMer,self.btnRefrMer, self.label_Informacion_Mer,self.listDistribuciónKcal[3],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        
        self.btnSelMer.pack(fill=X)
        self.btnRefrMer.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblMerTotal = tk.Label(self.tabMerienda,text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]),bg=fondoGeneral)
        self.lblMerTotal.pack(anchor=tk.W)
    def CenaF(self):
        self.label = tk.Label(self.tabCena, text="-CENA-", font=self.controller.title_font,bg=fondoGeneral)
        self.label.pack(side="top", fill="x", pady=10)
        umbral=1
        selected = IntVar()
        self.cont_comida_inf = tk.Frame(self.tabCena,bg=fondoGeneral);
        self.cont_opciones_Cen =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.cont_inf_eleccion =tk.Frame(self.cont_comida_inf,bg=fondoGeneral)
        self.label_Informacion_Cen = tk.Label(self.cont_inf_eleccion,text="INFORMACIÓN",bg=fondoGeneral)
        self.label_Informacion_Cen.pack(fill=BOTH,side=LEFT,anchor=tk.W)
        i=0;
        self.cena = self.cena.sort_values(by=['Grasa'],ascending=False).sort_values(by=['Proteina'],ascending=False).sort_values(by=['Hidratos'],ascending=False)
        self.cena = cd.OrdMinimaDiferencia(self.cena,self.listDistribuciónKcal[1],"cena",datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios)
        self.filtCena = self.cena.loc[self.cena["Calidad"] <= umbral]
        self.filtCena = self.filtCena.sort_values(by=["LRE"])
        self.objetivo = tk.Label(self.tabCena,text="Objetivo: "+str(np.round(self.listMacDiarios[0]))+" Kcal // Objetivo Cena: "+str(np.round(self.listDistribuciónKcal[4])),bg=fondoGeneral)
        self.LblLoQueLlevoCen = tk.Label(self.tabCena, text="Llevo Comido: "+str(np.round(datosAlimCliente[0])),bg=fondoGeneral)
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
        self.btnRefrCen = tk.Button(self.tabCena, text="Refrescar",bg=colorDetalles)
        if(self.banderaSelect[4]):
            self.btnRefrCen['state']='disable'
            self.btnSelCen = tk.Button(self.tabCena, text="Editar",bg=colorDetalles)  
        else:
            self.btnSelCen = tk.Button(self.tabCena, text="Seleccionar",bg=colorDetalles)
        self.btnSelCen.config(command=partial(vs.seleccionarYActualizarResto,self,"cena",self.botonesCen,self.btnSelCen,selected,self.banderaSelect,hojaAlimentos,datosAlimCliente,menuDeHoy,self.filtComida,self.barProgTotal,self.listMacDiarios,self.style,umbral))
        self.btnRefrCen.config(command=partial(vs.refrescar,self,"cena",self.cont_opciones_Cen,self.filtCena,umbral,self.cena,hojaAlimentos,self.botonesCen,self.n_opciones,self.btnSelCen,self.btnRefrCen, self.label_Informacion_Cen,self.listDistribuciónKcal[4],datosAlimCliente,self.kcal_Por_Dia,self.listMacDiarios,menuDeHoy,self.barProgTotal,self.banderaSelect,self.style))
        
        self.btnSelCen.pack(fill=X)
        self.btnRefrCen.pack(fill=X)
        textoTotal=u"Comido hoy:\n desayuno:",str(menuDeHoy[0]),"\nAmuerzo:",str(menuDeHoy[1]),"\nComida:",str(menuDeHoy[2]),"\nMerienda:",str(menuDeHoy[3]),"\nCena:",str(menuDeHoy[4])
        self.lblCenTotal = tk.Label(self.tabCena,text="Comido hoy:\n desayuno:"+str(menuDeHoy[0])+"\nAmuerzo:"+str(menuDeHoy[1])+"\nComida:"+str(menuDeHoy[2])+"\nMerienda:"+str(menuDeHoy[3])+"\nCena:"+str(menuDeHoy[4]),bg=fondoGeneral)
        self.lblCenTotal.pack(anchor=tk.W)
class addComida(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.user,self.pwd = vs.getUsuario()
            self.controller = controller
            #lista = np.aray(hojaUsuarios.iloc[int(ab.getFilaUsuario(user,hojaUsuarios)),:])
            self.c = 0;
            self.containerTit = tk.Frame(self,bg=fondoGeneral)
            self.containerNom = tk.Frame(self,bg=fondoGeneral)
            self.containerGram = tk.Frame(self,bg=fondoGeneral)
            self.containerExpl = tk.Frame(self,bg=fondoGeneral)
            self.containerKCal = tk.Frame(self,bg=fondoGeneral)
            self.containerGra = tk.Frame(self,bg=fondoGeneral)
            self.containerSat = tk.Frame(self,bg=fondoGeneral)
            self.containerHid = tk.Frame(self,bg=fondoGeneral)
            self.containerFib = tk.Frame(self,bg=fondoGeneral)
            self.containerAzu = tk.Frame(self,bg=fondoGeneral)
            self.containerPro = tk.Frame(self,bg=fondoGeneral)
            self.containerSod = tk.Frame(self,bg=fondoGeneral)
            self.containerTip = tk.Frame(self,bg=fondoGeneral)
            self.containerCal = tk.Frame(self,bg=fondoGeneral)
            self.cointainerLink = tk.Frame(self,bg=fondoGeneral)
            self.containerButt = tk.Frame(self,bg=fondoGeneral)
            label = tk.Label(self, text="Añadiendo Menu", font=controller.title_font,bg=fondoGeneral)    
            label.pack()
            self.containerTit.pack(fill=X)
            self.containerNom.pack(fill=X)
            self.containerGram.pack(fill=X)
            self.containerExpl.pack(fill=X)
            self.containerKCal.pack(fill=X)
            self.containerGra.pack(fill=X)
            self.containerSat.pack(fill=X)
            self.containerHid.pack(fill=X)
            self.containerFib.pack(fill=X)
            self.containerAzu.pack(fill=X)
            self.containerPro.pack(fill=X)
            self.containerSod.pack(fill=X)
            self.containerTip.pack(fill=X)
            self.containerCal.pack(fill=X)
            self.cointainerLink.pack(fill=X)
            self.containerButt.pack(fill=X)
            etiquetas_font = font.Font(family='Times', size=16, weight="bold")
            label = tk.Label(self.containerTit, text="\t     ", font=controller.title_font,bg=fondoGeneral)    
            label.pack(side=LEFT)
            label = tk.Label(self.containerTit, text="Alimento #1", font=etiquetas_font,bg=fondoGeneral)    
            label.pack(side=LEFT,expand=1,fill=BOTH)
            label = tk.Label(self.containerTit, text="Alimento #2", font=etiquetas_font,bg=fondoGeneral)    
            label.pack(side=LEFT,expand=1,fill=BOTH)
            label = tk.Label(self.containerTit, text="Alimento #3", font=etiquetas_font,bg=fondoGeneral)    
            label.pack(side=LEFT,expand=1,fill=BOTH)
            label = tk.Label(self.containerTit, text="Alimento #4", font=etiquetas_font,bg=fondoGeneral)    
            label.pack(side=LEFT,expand=1,fill=BOTH)
            
            label_Nom = Label(self.containerNom, text="Nombre: ",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Nom.pack(side=LEFT)
            
            self.entry_Nom = Entry(self.containerNom,bg=fondoGeneral)
            self.entry_Nom.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Nom2 = Entry(self.containerNom,bg=fondoGeneral)
            self.entry_Nom2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Nom3 = Entry(self.containerNom,bg=fondoGeneral)
            self.entry_Nom3.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Nom4 = Entry(self.containerNom,bg=fondoGeneral)
            self.entry_Nom4.pack(expand=1,fill=BOTH,side=LEFT)

            label_Gram = Label(self.containerGram, text="Gramos: ",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Gram.pack(side=LEFT)
            
            self.entry_Gram = Entry(self.containerGram,bg=fondoGeneral)
            self.entry_Gram.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Gram2 = Entry(self.containerGram,bg=fondoGeneral)
            self.entry_Gram2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Gram3 = Entry(self.containerGram,bg=fondoGeneral)
            self.entry_Gram3.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Gram4 = Entry(self.containerGram,bg=fondoGeneral)
            self.entry_Gram4.pack(expand=1,fill=BOTH,side=LEFT)
            
            label_kcal = Label(self.containerExpl, text="A continuación añada la información correspondiente a 100 gramos:",width=20,bg=fondoGeneral)
            label_kcal.pack(expand=1,fill=BOTH)
            
            label_kcal = Label(self.containerKCal, text="KiloCalorias",width=20,font=("bold", 10),bg=fondoGeneral)
            label_kcal.pack(side=LEFT)
            
            self.entry_kcal = Entry(self.containerKCal,bg=fondoGeneral)
            self.entry_kcal.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_kcal2 = Entry(self.containerKCal,bg=fondoGeneral)
            self.entry_kcal2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_kcal3 = Entry(self.containerKCal,bg=fondoGeneral)
            self.entry_kcal3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_kcal4 = Entry(self.containerKCal,bg=fondoGeneral)
            self.entry_kcal4.pack(expand=1,fill=BOTH,side=LEFT)
            
            label_gras = Label(self.containerGra, text="Grasa",width=20,font=("bold", 10),bg=fondoGeneral)
            label_gras.pack(side=LEFT)        
            
            self.entry_gras = Entry(self.containerGra,bg=fondoGeneral)
            self.entry_gras.pack(expand=1,fill=BOTH,side=LEFT)

            self.entry_gras2 = Entry(self.containerGra,bg=fondoGeneral)
            self.entry_gras2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_gras3 = Entry(self.containerGra,bg=fondoGeneral)
            self.entry_gras3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_gras4 = Entry(self.containerGra,bg=fondoGeneral)
            self.entry_gras4.pack(expand=1,fill=BOTH,side=LEFT)
            
            
            label_sat = Label(self.containerSat, text="Saturadas",width=20,font=("bold", 10),bg=fondoGeneral)
            label_sat.pack(side=LEFT)     
            
            self.entry_sat = Entry(self.containerSat,bg=fondoGeneral)
            self.entry_sat.pack(expand=1,fill=BOTH,side=LEFT)

            self.entry_sat2 = Entry(self.containerSat,bg=fondoGeneral)
            self.entry_sat2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_sat3 = Entry(self.containerSat,bg=fondoGeneral)
            self.entry_sat3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_sat4 = Entry(self.containerSat,bg=fondoGeneral)
            self.entry_sat4.pack(expand=1,fill=BOTH,side=LEFT)
            
            
            label_Hid = Label(self.containerHid, text="Hidratos",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Hid.pack(side=LEFT)       
            
            self.entry_Hid = Entry(self.containerHid,bg=fondoGeneral)
            self.entry_Hid.pack(expand=1,fill=BOTH,side=LEFT)
           
            self.entry_Hid2 = Entry(self.containerHid,bg=fondoGeneral)
            self.entry_Hid2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Hid3 = Entry(self.containerHid,bg=fondoGeneral)
            self.entry_Hid3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_Hid4 = Entry(self.containerHid,bg=fondoGeneral)
            self.entry_Hid4.pack(expand=1,fill=BOTH,side=LEFT)
 
    
            label_Fibra = Label(self.containerFib, text="Fibra",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Fibra.pack(side=LEFT)       
            
            self.entry_Fibra = Entry(self.containerFib,bg=fondoGeneral)
            self.entry_Fibra.pack(expand=1,fill=BOTH,side=LEFT)

            self.entry_Fibra2 = Entry(self.containerFib,bg=fondoGeneral)
            self.entry_Fibra2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Fibra3 = Entry(self.containerFib,bg=fondoGeneral)
            self.entry_Fibra3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_Fibra4 = Entry(self.containerFib,bg=fondoGeneral)
            self.entry_Fibra4.pack(expand=1,fill=BOTH,side=LEFT)
            
            
            label_Azuc = Label(self.containerAzu, text="Azucares",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Azuc.pack(side=LEFT)       
            
            self.entry_Azuc = Entry(self.containerAzu,bg=fondoGeneral)
            self.entry_Azuc.pack(expand=1,fill=BOTH,side=LEFT)

            self.entry_Azuc2 = Entry(self.containerAzu,bg=fondoGeneral)
            self.entry_Azuc2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Azuc3 = Entry(self.containerAzu,bg=fondoGeneral)
            self.entry_Azuc3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_Azuc4 = Entry(self.containerAzu,bg=fondoGeneral)
            self.entry_Azuc4.pack(expand=1,fill=BOTH,side=LEFT)
            

            label_Pro = Label(self.containerPro, text="Proteina",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Pro.pack(side=LEFT)       
            
            self.entry_Pro = Entry(self.containerPro,bg=fondoGeneral)
            self.entry_Pro.pack(expand=1,fill=BOTH,side=LEFT)

            self.entry_Pro2 = Entry(self.containerPro,bg=fondoGeneral)
            self.entry_Pro2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Pro3 = Entry(self.containerPro,bg=fondoGeneral)
            self.entry_Pro3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_Pro4 = Entry(self.containerPro,bg=fondoGeneral)
            self.entry_Pro4.pack(expand=1,fill=BOTH,side=LEFT)
            
            label_Sod = Label(self.containerSod, text="Sodio",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Sod.pack(side=LEFT)       
            
            self.entry_Sod = Entry(self.containerSod,bg=fondoGeneral)
            self.entry_Sod.pack(expand=1,fill=BOTH,side=LEFT)

            self.entry_Sod2 = Entry(self.containerSod,bg=fondoGeneral)
            self.entry_Sod2.pack(expand=1,fill=BOTH,side=LEFT)
            
            self.entry_Sod3 = Entry(self.containerSod,bg=fondoGeneral)
            self.entry_Sod3.pack(expand=1,fill=BOTH,side=LEFT)
                        
            self.entry_Sod4 = Entry(self.containerSod,bg=fondoGeneral)
            self.entry_Sod4.pack(expand=1,fill=BOTH,side=LEFT)
            
            
            label_Tip = Label(self.containerTip, text="Tipo",width=20,font=("bold", 10),bg=fondoGeneral)
            label_Tip.pack(side=TOP)
            self.var = IntVar()
            self.varDes = IntVar()
            Checkbutton(self.containerTip, text="Desayuno", variable=self.varDes,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            self.varAlm = IntVar()
            Checkbutton(self.containerTip, text="Almuerzo", variable=self.varAlm,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            self.varCom = IntVar()
            Checkbutton(self.containerTip, text="Comida", variable=self.varCom,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            self.varMer = IntVar()
            Checkbutton(self.containerTip, text="Merienda", variable=self.varMer,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            self.varCen = IntVar()
            Checkbutton(self.containerTip, text="Cena", variable=self.varCen,bg=fondoGeneral).pack(expand=1,side=LEFT,fill=BOTH)
            
            link = Label(self.cointainerLink, text= "Se le aconseja la siguiente página web para rellenar la información nutricional:",bg=fondoGeneral) 
            link1 = Label(self.cointainerLink, text= "Bedca",fg="blue", cursor="hand2",bg=fondoGeneral) 
            link.pack(side=LEFT)
            link1.pack(side=LEFT)
            link1.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.bedca.net/"))
            buttonEnviar = Button(self.containerButt, text='Validar',command=partial(vs.InformacionNuevaComida,hojaAlimentos,self,colorDetalles,fondoGeneral),bg=colorDetalles,relief=GROOVE).pack(fill=X)

            button = tk.Button(self.containerButt, text="Cancelar",command=lambda: controller.show_frame("MostrarDieta"),relief=GROOVE,bg=colorDetalles).pack(fill=X)
            self.label_Error = Label(self, text="",width=20,font=("bold", 10),bg=fondoGeneral,foreground="red")
            self.label_Error.pack(fill=BOTH)


if __name__ == "__main__":
        #Variable que almacena lo que lleva comido el cliente en cuanto a datos
        datosAlimCliente = np.zeros(5)
        #Array que guarda lo que ha comido hoy el cliente
        
        menuDeHoy = ["","","","",""]
        #Variable que almacena lo que tiene que comer
        listMacDiarios = np.zeros(4)
        totalKcalComidas=0;
        hojaAlimentos, hojaUsuarios, hojaPatologias,config = ab.cargarBaseDeDatos()
        fondoGeneral=config[0]
        colorDetalles=config[1]
        mensajeError = "";
        #Inicializamos la ventana.
        login = tk.Tk();
        login.resizable(0,0)
        login.geometry('220x200')
        login.title("login")
        login.iconbitmap('assets/logo.ico')
        #INICIALIZACIÓN DE FUENTES, SEPARADORES...
        fuente = font.Font(family="Helvetica",size=12, weight="bold")
        fuente2 = font.Font(family="Helvetica",size=7)
        #Menu archivo
        menu = Menu(login)
        subMenuArchivo1 = Menu(menu)
        subMenuArchivo1.add_command(label="Manual",command= lambda: os.system('assets\Manual.pdf'))
        menu.add_cascade(label='Archivo',menu=subMenuArchivo1)
        login.config(menu=menu)
        #CUERPO
        lblMensaje = ttk.Label(login,text="",foreground="red",font=fuente2)
        lblU = ttk.Label(login,text="DNI (sin letra)", font=fuente)
        txtU = ttk.Entry(login,width=10)
        txtU.focus()
        lblP = ttk.Label(login,text="Contraseña",font=fuente)
        txtP = ttk.Entry(login,width=15, show="*")
        btnInit = ttk.Button(login, text="Inicio",command=partial(vs.cambio,txtU,txtP,login,lblMensaje))
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
        frame = tk.Frame(login)
        frame.pack(fill=BOTH)
        btnRegist = ttk.Button(login, text="Registrarse ",command=partial(vs.registrarse,hojaUsuarios,hojaPatologias)) 
        
        btnRegist.pack(fill=X,side=BOTTOM);
        login.mainloop(); 
        if(vs.getBandera()):
            hojaAlimentos, hojaUsuarios, hojaPatologias,config = ab.cargarBaseDeDatos()
            app = HealthApp()
            app.mainloop()