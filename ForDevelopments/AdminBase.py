# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:36:25 2018

@author: Jesus
"""
import pandas as pd;
import datetime
from tkinter import messagebox
'''
Función que carga la base de datos completa.
Return:
    hojaAl = Base de datos de alimentos.
    hojaUs = Base de datos de usuarios.
    hojaPa = Base dedatos de las patologias.
    config = Configuración estetica de la aplicación
'''
def cargarBaseDeDatos():
    #Cargamos la base de datos
    #doc = wx.Book("BaseDeDatosDeAlimentos.xlsx")
    try:
        doc = pd.ExcelFile("Dat/BaseDeDatosDeAlimentos.xlsx")
        docU = pd.ExcelFile("Dat/BaseDeDatosUsuarios.xlsx")
        #Seleccionamos la hoja de excell que contendrá dicha información-
    
        hojaAl = pd.read_excel(doc,'Alimentos')
        hojaUs = pd.read_excel(docU,'Usuarios')
        hojaPa = pd.read_excel(doc,'Patologias')
        archivo = open('Dat/config.txt','r')
        config = str(archivo.read()).split(':')
        archivo.close()
        
        return hojaAl,hojaUs,hojaPa,config;
    except FileNotFoundError:
        messagebox.showerror("ERROR FATAL","Base da datos dañada o eliminada")
def cargaRegistro():
    try:
        docRegistro = pd.ExcelFile("Dat/RegistroMejora.xlsx")
        hojaRegistro = pd.read_excel(docRegistro,'Registro')
        return hojaRegistro
    except FileNotFoundError:
        messagebox.showerror("ERROR FATAL","Base da datos dañada o eliminada")    
def cargaRegistroUsuario(dni):
    try:
        docRegistro = pd.ExcelFile("Dat/RegistroMejora.xlsx")
        hojaRegistro = pd.read_excel(docRegistro,'Registro')
        hojaRegistro[hojaRegistro.dni == dni]
        return hojaRegistro[hojaRegistro.dni == dni]
    except FileNotFoundError:
        messagebox.showerror("ERROR FATAL","Base da datos dañada o eliminada")    
def cargarUsuarios():
    try:
        docU = pd.ExcelFile("Dat/BaseDeDatosUsuarios.xlsx")
        hojaUs = pd.read_excel(docU,'Usuarios')
        return hojaUs
    except FileNotFoundError:
        messagebox.showerror("ERROR FATAL","Base da datos dañada o eliminada")
def cargarBaseAlimentos():
    try:
        doc = pd.ExcelFile("Dat/BaseDeDatosDeAlimentos.xlsx")
        hojaAl = pd.read_excel(doc,'Alimentos')
        hojaPa = pd.read_excel(doc,'Patologias')
        return hojaAl,hojaPa;
    except FileNotFoundError:
        messagebox.showerror("ERROR FATAL","Base da datos dañada o eliminada")
'''
Función que carga el historial del usuario para futuros calculosy gráficas para ello necesita solo la id del usuario,se 
criba y se devuelve para ser almacenado.
Parametros:
    usr = Usuario actualmente logueado en la aplicación.
'''

def cargarHistorial(usr):
    try:
        hist = pd.ExcelFile("Dat/Historial.xlsx");
        hojaHisAl = pd.read_excel(hist, 'UsrAl')
        histUsr = hojaHisAl.loc[hojaHisAl.Usuario == usr]
    
        return histUsr,hojaHisAl
    except FileNotFoundError:
        messagebox.showerror("ERROR FATAL","Base da datos dañada o eliminada")
'''
Modificamos el array 'menuDeHoy' con la información de hoy si es que hay.
Parametros:
    hojaHisAl = Historial concreto del usuario actual.
    menuDeHoy = Historial del día de hoy de los menús seleccionador por el usuario actual.
    datosAlimCliente = Datos de los alimentos que ha ido consumiendo el cliente.
    hojaAlimentos = Base de datos de toda la hoja de alimentos como base de datos.
'''
def cargaHistorialHoy(hojaHisAl,menuDeHoy,datosAlimCliente,hojaAlimentos):
    hoy = str(datetime.date.today())
    if(hoy in list(hojaHisAl.Fecha)):
       diaEntero=hojaHisAl.loc[hojaHisAl.Fecha == hoy]
       if not (diaEntero.iloc[0].isnull().loc['Desayuno']):
           menuDeHoy[0] = str(diaEntero.iloc[0].loc['Desayuno'])
           fila = getFilaAlimento(menuDeHoy[0],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Almuerzo']):
           menuDeHoy[1] = str(diaEntero.iloc[0].loc['Almuerzo'])
           fila = getFilaAlimento(menuDeHoy[1],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Comida']):
           menuDeHoy[2] = str(diaEntero.iloc[0].loc['Comida'])
           fila = getFilaAlimento(menuDeHoy[2],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Merienda']):
           menuDeHoy[3] = str(diaEntero.iloc[0].loc['Merienda'])
           fila = getFilaAlimento(menuDeHoy[3],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
        
       if not (diaEntero.iloc[0].isnull().loc['Cena']):
           menuDeHoy[4] = str(diaEntero.iloc[0].loc['Cena'])    
           fila = getFilaAlimento(menuDeHoy[4],hojaAlimentos)
           datosAlimCliente[0] = hojaAlimentos["Calorias"].loc[fila] + datosAlimCliente[0]
           datosAlimCliente[1] = hojaAlimentos["Grasa"].loc[fila] + datosAlimCliente[1]
           datosAlimCliente[2] = hojaAlimentos["Hidratos"].loc[fila] + datosAlimCliente[2]
           datosAlimCliente[3] = hojaAlimentos["Proteina"].loc[fila] + datosAlimCliente[3]
           datosAlimCliente[4] = hojaAlimentos["Calidad"].loc[fila] + datosAlimCliente[4]
'''
Función que comprueba si el usuario insetado existe y coincide con la contraseña.
Parametros:
    userId = DNI del usuarios.
    passwd = Contraseña del usuario
return:
    indice = Indice del usuario actual.
'''
def comprobarUsuario(userId,passwd):
    a,u,p,c = cargarBaseDeDatos();
    indice=-1;
    bandera =True;
    if ((u.iloc[:,0]==userId).any()):
        for i in u.iloc[:,0]:
            indice+=1
            if(i == userId):
                if(str(passwd) == str(u.iloc[indice,3])):
                    bandera = False;
                    return indice;
    if(bandera):
        indice = -1;            
    return indice;
def getFilaPatologia(patologiaID,p):
    indice=0;
    for i in p.iloc[:,0]:
        if(i == patologiaID):
            break;
        indice+=1;
    return indice;
def getFilaUsuario(userId,u):
    indice=0;
    for i in u.iloc[:,0]:
        if(i == userId):
            break;
        indice+=1;
    return indice;
def getFilaAlimento(nombre,a):
    indice=0;
    for i,alimento in a.iterrows():
        if(alimento["Nombre"] == nombre):
            break;
        indice+=1;
    return i; 
'''
Función que te devuelve el id de la patología buscada por el nombre
Parametros:
    nombre= Nombre de la patología.
    P = Array de la base de datos de la patología
Return:
    resultado = id de la patología encontrada por dicho nombre.
'''
def IdPatologiaPorNombre(nombre, p):
    resultado=-1000;
    indice=0;
    for i in p.iloc[:,1]:
        if(i == nombre):
            resultado= p.iloc[indice,0]
            break;
        indice+=1;
    return resultado;
'''
Función que llama a todas las funciones de guardado para hacer un guardado general en la aplicación.
Parametros:
    usr = Usuario actual.
    menuDeHoy = Lista de los menús seleccionados hoy
    hojaAlimentos = Array modificado (o no) de la base de datos de alimentos
    hojaUsuarios = Array modificado ( o no) de los usuarios.
    hojaPatologias = Array modificado (o no) de las patologias.
    config = configuración de estilos de la aplicación.
'''
def guardaTodo(usr, menuDeHoy, historial,hojaAlimentos, hojaUsuarios, hojaPatologias,config):
    try:
        guardarHistorial (usr, menuDeHoy, historial)
        guardarUsuario(hojaUsuarios)
        guardarDatos (hojaAlimentos, hojaPatologias)
        messagebox.showinfo("Ya se ha guardado","Datos guardados ya puede cerrar el programa")
    except PermissionError:
        messagebox.showwarning("Cierre la base de datos","Imposible guardar, base de datos abierta¡")
'''
Función que te guarda los datos del usuario.
Parametros:
    hojaUsuarios = Array con los datos ya cambiados de los usuarios.
'''
def guardarUsuario(hojaUsuarios):
    try:
        writer = pd.ExcelWriter("Dat/BaseDeDatosUsuarios.xlsx")
        hojaUsuarios.to_excel(writer,'Usuarios',index=False)
        writer.save();
        
    except PermissionError:
        raise PermissionError
'''
Funcion que almacena y guarda la información diaria del usaurio.
Parametros:
    usr = Usuario
    menuDeHoy = Alimentos seleccionados durante el día de hoy.
    historial = Array con el historial completo para añadir la nueva fila.
'''
def guardarHistorial (usr, menuDeHoy, historial):
    try:
        fech = str(datetime.date.today())
        h = historial.loc[historial.Fecha == fech]
        hoy = pd.DataFrame({"Fecha":[fech],
                        "Usuario":[usr],
                        "Desayuno":[menuDeHoy[0]],
                        "Almuerzo":[menuDeHoy[1]],
                        "Comida":[menuDeHoy[2]],
                        "Merienda":[menuDeHoy[3]],
                        "Cena":[menuDeHoy[4]]})
        if(usr in list(h.Usuario)):
            lala = historial.index[(historial.Fecha == fech) & (historial.Usuario == usr)]
            historial.iloc[lala] = hoy
        else:
            historial=historial.append(hoy,sort=False)    
        writer = pd.ExcelWriter("Dat/Historial.xlsx")
        historial.to_excel(writer,'UsrAl',index=False)
        writer.save();
    except PermissionError:
        messagebox.showwarning("Cierre la base de datos","Imposible guardar, base de datos abierta¡")
'''
Función que te guarda los datos de los alimentos y patologias en BaseDeDatosAlimentos.xlsx
parametros:
    hojaAlimentos = Array de los alimentos a almacenar.
    hojaPatologias = Array de las patologias a almacenar.
'''
def guardarDatos (hojaAlimentos, hojaPatologias):
    try:
        writer = pd.ExcelWriter("Dat/BaseDeDatosDeAlimentos.xlsx")
        hojaAlimentos.to_excel(writer,'Alimentos',index=False)
        hojaPatologias.to_excel(writer,'Patologias',index=False)
        writer.save();
    except PermissionError:
        raise PermissionError
def guardaRegistroPeso(usr, registro, pesoNuevo, bandera, tipo):
    try:
        fech = str(datetime.date.today())
        if(bandera==0):
            valor=0;
            if(tipo == 'subir'):
                valor = 500;
            elif(tipo == 'bajar'):
                valor = -500
            else:
                valor = 0
            ultimoRegistro = pd.DataFrame({"Fecha":[fech],
                        "dni":[usr],
                        "peso":[pesoNuevo],
                        "valor":[valor],
                        "tipo":[tipo],
                        })
            registro = registro.append(ultimoRegistro, sort=False)
        elif(bandera==1):
            fila = registro.index[registro.dni == usr]
            ultimaFecha = pd.to_datetime(registro['Fecha'].iloc[fila])
            
            tipoAntiguo = registro['tipo'].iloc[fila]
            for i in tipoAntiguo:               
                t = i
            #Si no se ha cambiado el tipo de dieta (bajar, mantener o subir), se sigue con la progresión
            if(str(i) == str(tipo)):
                #ultimaFecha  = datetime.datetime.strptime(str(registro['Fecha'].iloc[fila]), '%Y-%m-%d')
                difFecha = datetime.date.today()-ultimaFecha.dt.date
                difFechaInt = int(difFecha.dt.components.days)
                if(difFechaInt >= 7):
                    objetivo = registro['tipo'].iloc[fila]
                    for o in objetivo:
                        objectTipo = o
                    if(objectTipo == 'bajar'):
                        kilos = -1*(3*difFechaInt/30)
                    elif(objectTipo == 'subir'):
                        kilos = 3*difFechaInt/30
                    else:
                        kilos=0;
                    difPeso = pesoNuevo - float(registro['peso'].iloc[fila]) 

                    #Si ha cambiado lo que debería haber cambiado (margen de error del 10%)
                    if (difPeso < (kilos*1.15) and difPeso > (kilos*0.85)):
                        registro['Fecha'].iloc[fila] = fech
                        registro['peso'].iloc[fila] = pesoNuevo
                    elif(difPeso> (kilos*1.15)):
                        registro['Fecha'].iloc[fila] = fech
                        registro['peso'].iloc[fila] = pesoNuevo
                        registro['valor'].iloc[fila] = float(registro['valor'].iloc[fila])-50
                    else:
                        registro['Fecha'].iloc[fila] = fech
                        registro['peso'].iloc[fila] = pesoNuevo
                        registro['valor'].iloc[fila] = float(registro['valor'].iloc[fila])+45       
            else:
                if(tipo == 'bajar'):
                    registro['Fecha'].iloc[fila] = fech
                    registro['valor'].iloc[fila] = -500
                    registro['tipo'].iloc[fila] = tipo
                elif(tipo =='subir'):
                    registro['Fecha'].iloc[fila] = fech
                    registro['valor'].iloc[fila] = 500
                    registro['tipo'].iloc[fila] = tipo
                else:
                    registro['Fecha'].iloc[fila] = fech
                    registro['valor'].iloc[fila] = 0
                    registro['tipo'].iloc[fila] = tipo
                
 
        writer = pd.ExcelWriter("Dat/RegistroMejora.xlsx")
        registro.to_excel(writer,'Registro',index=False)
        writer.save();
    except PermissionError:
        raise PermissionError
'''
Funcion que te comprueba y guarda los datos recibidos como parámetros del usuario actualmente dado de alta en la aplicación
Parametros:
    hojaUsuarios = Array de Usuarios del cual se saca y sustituye la información
    selfi = Variables locales de la clase.
    controller = Controlador de la clase padre de todas ellas.
    hojaPatologias = Array con la lista de patologias accesibles en la web
    patologia = Patologia del propio usuario.
'''
def ComproYAlmacenamientoUsuario(hojaUsuarios,selfi,controller,hojaPatologias, patologia):
    idPatologia = IdPatologiaPorNombre(patologia.get(),hojaPatologias)
    fila = getFilaUsuario(selfi.user,hojaUsuarios)
    registro = cargaRegistro()
    try:
        if(len(selfi.entry_Nom.get()) != 0):
            hojaUsuarios['nombre'].loc[fila] = selfi.entry_Nom.get()
        if(len(selfi.entry_Ape.get()) != 0):
            hojaUsuarios['apellido'].loc[fila] = selfi.entry_Ape.get()
        if(len(selfi.entry_Eda.get()) != 0):
            int(selfi.entry_Eda.get())
            hojaUsuarios['edad'].loc[fila] = int(selfi.entry_Eda.get())
        if(len(selfi.entry_Alt.get()) != 0):
            int(selfi.entry_Alt.get())
            hojaUsuarios['altura'].loc[fila] = int(selfi.entry_Alt.get())
        if(len(selfi.entry_Pes.get()) != 0):
            float(selfi.entry_Pes.get())
            guardaRegistroPeso(hojaUsuarios['id'].loc[fila], registro, float(selfi.entry_Pes.get()), 1, hojaUsuarios['tipo'].loc[fila])
            hojaUsuarios['peso'].loc[fila] = float(selfi.entry_Pes.get())
        if(selfi.var.get() != 0):
            if(selfi.var.get() == 1):
                hojaUsuarios['sexo'] .loc[fila]= 'H'
            else:
                hojaUsuarios['sexo'].loc[fila] = 'M'
        if(selfi.varTipo.get() != 0):
            if(selfi.varTipo.get() == 1):
                hojaUsuarios['tipo'].loc[fila] = "bajar"
            elif(selfi.varTipo.get() == 2):
                hojaUsuarios['tipo'].loc[fila] = "mantener"
            else:
                hojaUsuarios['tipo'].loc[fila] = "subir"     
            guardaRegistroPeso(hojaUsuarios['id'].loc[fila], registro, float(selfi.entry_Pes.get()), 1, hojaUsuarios['tipo'].loc[fila])
        if(selfi.varAct.get() != 0):
            hojaUsuarios['actividad'].loc[fila] = selfi.varAct.get()
        hojaUsuarios['patologia'].loc[fila] = idPatologia
        selfi.label_Error.config(text="")
        guardarUsuario(hojaUsuarios)
        messagebox.showinfo("Datos actualizados","Datos actualizados correctamente, veras los cambios al reiniciar el programa")
        controller.show_frame("InfoUsuario")
    except ValueError as ve:
        selfi.label_Error.config(text="ERROR: Algun dato erroneo, comprueba todo")
    except PermissionError:
        messagebox.showwarning("Cierre la base de datos","Imposible guardar, !base de datos abierta¡") 
    
'''
Función que te comprueba que los datos son correctos e inserta un nuevo menu a la base de datos
Carga el actual estado de la base de datos, además de la lista de la cual esta haciendo uso el usuario, añade el nuevo alimento a ambas, asi cuando
guarda el alimento, lo hace solo sobre ese cambio y no tiene que guardar todo su progreso, y cuando quiere guardar todo su progreso el alimento esta ya almacenado
en la lista, lo cual evita que se sobreescriba y se borren los avances.
'''
def ComrproYAlmacenamientoAlimento(hojaAlimentos,nombre, kilocalorias, grasa,saturada, hidratos,fibra, azucar, proteina,sodio, tipo, calidad):
    try:
        alimentos, patologias = cargarBaseAlimentos() 
        nuevaFila= pd.DataFrame({'Nombre':[nombre],
                                 'Calorias': [kilocalorias],
                                 'Grasa': [grasa], 
                                 'Saturadas':[saturada],
                                 'Hidratos':[hidratos],
                                 'Fibra':[fibra],
                                 'Azucares':[azucar],
                                 'Proteina':[proteina],
                                 'Sodio':[sodio],
                                 'Tipo': [tipo],
                                 'LRE':[0],
                                 'Calidad': [calidad]})
        hojaAlimentos = hojaAlimentos.append(nuevaFila)
        alimentos = alimentos.append(nuevaFila,sort=False)
        #Guardamos la 'imagen' de la base de datos sin retoques, solo con la nueva linea
        guardarDatos(alimentos,patologias)
        messagebox.showinfo("Datos actualizados","Datos actualizados correctamente, veras los cambios al reiniciar el programa")
    except PermissionError:
        messagebox.showwarning("Cierre la base de datos","Imposible guardar, !base de datos abierta¡") 
'''
Función que inserta un nuevo usuario en la base de datos, y comprueba la veracidad de los datos antes de ser insertados.
Parametros:
    ventana = Frame donde se va a depositar la aplicación.
    hojaUsuarios = Array de todos los usuarios del programa.
    dni = Objeto python que contiene el dni del usuario
    nombre = Objeto python que contiene el nombre del usuario
    apellido = Objeto python que contiene el apellido del usuario
    pwd = Objeto python que contiene el pwd del usuario
    sexo = Objeto python que contiene el sexo del usuario
    edad = Objeto python que contiene el edad del usuario
    altura = Objeto python que contiene el altura del usuario
    peso = Objeto python que contiene el peso del usuario
    actividad = Objeto python que contiene el actividad del usuario
    tipo = Objeto python que contiene el tipo del usuario
    mensajeError = Label que contiene el mensaje de error en caso de haber uno.
    patologia = Objeto python que contiene la patologia del usuario
    hojaPatologias = Array que contiene la base de datos de patologias.
'''
def NuevoUsuario(ventana,hojaUsuarios,dni, nombre, apellido, pwd, sexo, edad,altura,peso,actividad,tipo, mensajeError, patologia, hojaPatologias):   
    idPatologia = IdPatologiaPorNombre(patologia.get(),hojaPatologias)
    if(len(dni.get()) ==0 or len(nombre.get()) == 0 or len(apellido.get()) == 0 or len(pwd.get()) == 0 or len(edad.get()) == 0 or len(altura.get()) == 0 or len(peso.get()) == 0 or sexo.get() == 0 or actividad.get() == 0 or tipo.get() == 0):
            mensajeError.config(text="ERROR: Algun dato erroneo, comprueba todo")
    else:
        try:
            int(dni.get())
            int(edad.get())
            int(altura.get())
            float(peso.get())
            registro = cargaRegistro()
            if(int(dni.get()) in list(hojaUsuarios.iloc[:,0])):
                mensajeError.config(text="ERROR: Ya existe este DNI")
            else:
                if(tipo.get() == 1):
                    tip='bajar'
                elif(tipo.get() == 2):
                    tip='mantener'
                elif(tipo.get() == 3):
                    tip='subir'
                nuevaFila= pd.DataFrame({'id':[int(dni.get())],
                                     'nombre': [nombre.get()],
                                     'apellido': [apellido.get()], 
                                     'password':[pwd.get()],
                                     'sexo':[sexo.get()],
                                     'edad':[int(edad.get())],
                                     'altura':[int(altura.get())],
                                     'peso': [float(peso.get())],
                                     'actividad':[int(actividad.get())],
                                     'patologia': [int(idPatologia)],
                                     'tipo':[tip]})
        
                hojaUsuarios = hojaUsuarios.append(nuevaFila,sort=False)
                #Guardamos la 'imagen' de la base de datos sin retoques, solo con la nueva linea
                guardarUsuario(hojaUsuarios)
                guardaRegistroPeso(int(dni.get()), registro, float(peso.get()), 0,tip)
                ventana.destroy()
                messagebox.showinfo("BIENVENIDO","Se registro en nuestra APP se ha desarrollado con exito¡")
                #mensajeError.config(text=" ")       
        except ValueError:
            mensajeError.config(text="ERROR: Caracter erroneo")
        except PermissionError:
            messagebox.showwarning("Aviso no se guardo","Base de datos abierta, imposible guardar")

        