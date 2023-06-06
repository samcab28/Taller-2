"""
Instituto TecnolÃ³gico de Costa Rica
Computer Engineering
Taller de ProgramaciÃ³n

Ejemplo Consola Cliente
Implementación del módulo NodeMCU
Proyecto 2, semestre 1
2019

Profesor: Milton Villegas Lemus
Autor: Santiago Gamboa RamÃ­rez

Restricciónes: Python3.7 
Ejemplo de como usar el módudo NodeMCU de wifiConnection

"""
global volumen, Name,welcome_text 

#           _____________________________
#__________/BIBLIOTECAS
from tkinter import *               # Tk(), Label, Canvas, Photo
from threading import Thread        # p.start()
import threading                    # 
import os                           # ruta = os.path.join('')
import time                         # time.sleep(x)
from tkinter import messagebox      # AskYesNo ()
import tkinter.scrolledtext as tkscrolled
##### Biblioteca para el Carro
from WiFiClient import NodeMCU
#### Biblioteca para manipulacion de imagenes
from PIL import Image, ImageTk
#### Biblioteca para manipulacion de sonidos
import pygame
pygame.mixer.init()

Name = ""
welcome_text = ""
volumen = 0.5

#           ____________________________
#__________/Ventana Principal
root=Tk()
root.title('Proyecto 1')
root.minsize(800,600)
root.resizable(width=NO,height=NO)
root.title("Proyecto Taller 2")

#           ______________________________
#__________/Se crea un lienzo para objetos
C_root=Canvas(root, width=800,height=600, bg='white')
C_root.place(x=0,y=0)


def inside(C_root):
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='red')
    C_root.place(x=0,y=0)
    #           _____________________________________
    #__________/Se titulo de los Cuadros de texto
    L_Titulo = Label(C_root,text="Mensajes Enviados",font=('Agency FB',14),bg='white',fg='blue')
    L_Titulo.place(x=100,y=10)

    L_Titulo = Label(C_root,text="Respuesta Mensaje",font=('Agency FB',14),bg='white',fg='blue')
    L_Titulo.place(x=490,y=10)


    SentCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
    SentCarScrolledTxt.place(x=10,y=50)

    RevCarScrolledTxt = tkscrolled.ScrolledText(C_root, height=10, width=45)
    RevCarScrolledTxt.place(x=400,y=50)


    #           _____________________________________
    #__________/Creando el cliente para NodeMCU
    myCar = NodeMCU()
    myCar.start()


    def get_log():
        """
        Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
        """
        indice = 0
        # Variable del carro que mantiene el hilo de escribir.
        while(myCar.loop):
            while(indice < len(myCar.log)):
                mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
                SentCarScrolledTxt.insert(END,mnsSend)
                SentCarScrolledTxt.see("end")

                mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
                RevCarScrolledTxt.insert(END, mnsRecv)
                RevCarScrolledTxt.see('end')

                indice+=1
            time.sleep(0.200)
        
    p = Thread(target=get_log)
    p.start()
            


    L_Titulo = Label(C_root,text="Mensaje:",font=('Agency FB',14),bg='white',fg='blue')
    L_Titulo.place(x=100,y=250)

    E_Command = Entry(C_root,width=30,font=('Agency FB',14))
    E_Command.place(x=200,y=250)

    L_Titulo = Label(C_root,text="ID mensaje:",font=('Agency FB',14),bg='white',fg='blue')
    L_Titulo.place(x=100,y=300)

    E_read = Entry(C_root,width=30,font=('Agency FB',14))
    E_read.place(x=200,y=300)


    def send (event):
        """
        Ejemplo como enviar un mensaje sencillo sin importar la respuesta
        """
        mns = str(E_Command.get())
        if(len(mns)>0 and mns[-1] == ";"):
            E_Command.delete(0, 'end')
            myCar.send(mns)
        else:
            messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')") 


    def sendShowID():
        """
        Ejemplo como capturar un ID de un mensaje específico.
        """
        mns = str(E_Command.get())
        if(len(mns)>0 and mns[-1] == ";"):
            E_Command.delete(0, 'end')
            mnsID = myCar.send(mns)
            messagebox.showinfo("Mensaje pendiente", "Intentando enviar mensaje, ID obtenido: {0}\n\
    La respuesta definitiva se obtine en un máximo de {1}s".format(mnsID, myCar.timeoutLimit))
            
        else:
            messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

    def read():
        """
        Ejemplo de como leer un mensaje enviado con un ID específico
        """
        mnsID = str(E_read.get())
        if(len(mnsID)>0 and ":" in mnsID):
            mns = myCar.readById(mnsID)
            if(mns != ""):
                messagebox.showinfo("Resultado Obtenido", "El mensaje con ID:{0}, obtuvo de respuesta:\n{1}".format(mnsID, mns))
                E_read.delete(0, 'end')
            else:
                messagebox.showerror("Error de ID", "No se obtuvo respuesta\n\
    El mensaje no ha sido procesado o el ID es invalido\n\
    Asegurese que el ID: {0} sea correcto".format(mnsID))

        else:
            messagebox.showwarning("Error en formato", "Recuerde ingresar el separador (':')")

    root.bind('<Return>', send) #Vinculando tecla Enter a la función send

    #           ____________________________
    #__________/Botones de ventana principal

    Btn_ConnectControl = Button(C_root,text='Send',command=lambda:send(None),fg='white',bg='blue', font=('Agency FB',12))
    Btn_ConnectControl.place(x=450,y=250)

    Btn_Controls = Button(C_root,text='Send & Show ID',command=sendShowID,fg='white',bg='blue', font=('Agency FB',12))
    Btn_Controls.place(x=500,y=250)

    Btn_ConnectControl = Button(C_root,text='Leer Mensaje',command=read,fg='white',bg='blue', font=('Agency FB',12))
    Btn_ConnectControl.place(x=450,y=300)

    #//////////////////////////////////////////////////////////////////
    #funciones de movimiento
    #funcion para moverse a la izquierda
    def left(event): 
        mensaje = "mensaje izquierda"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)
        print("moverse izquierda")

    #funcion para moverse a la derecha 
    def right(event): 
        mensaje = "mensaje derecha"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)
        print("moverse derecha")

    #funcion para moverse hacia arriba
    def up(event): 
        mensaje = "mensaje arriba"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)       
        print("moverse adelante")

    #funcion para moverse hacia abajo 
    def down(event): 
        mensaje = "mensaje abajo"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)       
        print("moverse atras")

    #funcion para las luces izquierda
    def luz_left(event):
        mensaje = "mensaje luz izquierda"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)      
        print("luz izquierda")

    #funcion para las luces derecha
    def luz_right(event):
        mensaje = "mensaje luz derecha"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)       
        print("luz derecha")

    #funcion para las luces adelante
    def luz_up(event):
        mensaje = "mensaje luz adelante"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)      
        print("luz adelante")

    #funcion para las luces atras
    def luz_down(event):
        mensaje = "mensaje iluz atras"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)       
        print("luz atras")

    #funcion para movimiento circular 
    def circle(event):
        mensaje = "mensaje circular"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)       
        print("movimiento circular")

    #funcion para sensor luz
    def fotorresistencia(event):
        mensaje = "mensaje fotorresistencia"
        E_Command.config(state=NORMAL)
        E_Command.delete(0, END)
        E_Command.insert(0, mensaje)
        E_Command.config(state=DISABLED)    
        print("fotorresistencia ")

    def salida(event):
        menu(C_root)

    #asignacion de teclas a cada funcion 
    root.bind("<a>", left)
    root.bind("<d>", right)
    root.bind("<w>", up)
    root.bind("<s>", down)
    root.bind("<l>", luz_left)
    root.bind("<k>", luz_right)
    root.bind("<j>", luz_up)
    root.bind("<h>", luz_down)
    root.bind("<q>", circle)
    root.bind("<g>", fotorresistencia)
    root.bind("<m>", salida)

#//////////////////////////////////////////////////////
#interfaz en general
def salir(C_root):
    root.destroy()

imagen_wheel = Image.open("imagenes\wheel.png")
imagen_wheeltk = ImageTk.PhotoImage(imagen_wheel)
def controles(C_root):
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='black')
    C_root.place(x=0,y=0)

    label_imagen = Label(root, image=imagen_wheeltk)
    label_imagen.place(x=0,y=0)

    C_root.create_text(500,25, text = "INSTRUCCIONES DE MANEJO", font=("Helvetica",20),fill="white")
    C_root.create_text(500,75, text = "* OPRIMA W PARA AVANZAR", font=("Helvetica",14),fill="white")
    C_root.create_text(500,110, text = "* OPRIMA S PARA RETROCEDER", font=("Helvetica",14),fill="white")
    C_root.create_text(500,145, text = "* OPRIMA D PARA GIRAR A LA DERECHA", font=("Helvetica",14),fill="white")
    C_root.create_text(500,180, text = "* OPRIMA A PARA GIRAR A LA IZQUIERDA", font=("Helvetica",14),fill="white")
    C_root.create_text(500,215, text = "* OPRIMA Q PARA HACER UN CIRCULO", font=("Helvetica",14),fill="white")

    C_root.create_text(500,300, text = "INSTRUCCIONES DE LUCES", font=("Helvetica",20),fill="white")
    C_root.create_text(500,350, text = "* OPRIMA L PARA LA LUZ IZQUIERDA", font=("Helvetica",14),fill="white")
    C_root.create_text(500,385, text = "* OPRIMA K PARA LA LUZ DERECHA", font=("Helvetica",14),fill="white")
    C_root.create_text(500,420, text = "* OPRIMA J PARA LA LUZ DELANTERA", font=("Helvetica",14),fill="white")
    C_root.create_text(500,455, text = "* OPRIMA H PARA LA LUZ TRASERA", font=("Helvetica",14),fill="white")
    C_root.create_text(500,490, text = "* OPRIMA G PARA LA FOTORRESISTENCIA", font=("Helvetica",14),fill="white")

    C_root.create_text(500,560, text = "* OPRIMA M PARA SALIR DEL CONTROL", font=("Helvetica",14),fill="white")
    Btnvolver = Button(C_root, text = "VOLVER", command=lambda:play1(C_root))
    Btnvolver.place(x = 50, y = 525, width= 50, height= 50)

imagen_hamilton = Image.open("imagenes//hamilton.png")
imagen_hamiltontk = ImageTk.PhotoImage(imagen_hamilton)
def play1(C_root):
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='black')
    C_root.place(x=0,y=0)

    label_imagen = Label(root, image=imagen_hamiltontk)
    label_imagen.place(x=0,y=0)

    Texto1 = C_root.create_text(550, 100, text=Name + ", SI ESTAS PREPARADO", font=("Helvetica", 18), fill="white")
    Texto2 = C_root.create_text(550, 150, text="HAZ CLIC EN INGRESAR!!", font=("Helvetica", 18), fill="white")
    BtnComojugar = Button(C_root, text = "CONTROLES", command=lambda:controles(C_root))
    BtnComojugar.place(x = 500, y = 400, width= 100, height= 100)

    BtnPlay2 = Button(C_root, text="INGRESO", command=lambda: inside(C_root))
    BtnPlay2.place(x =500, y = 200, width=100, height=100)

    Btnvolver = Button(C_root, text = "VOLVER", command=lambda:menu(C_root))
    Btnvolver.place(x = 700, y = 525, width= 50, height= 50)

imagen_integrantes = Image.open("imagenes//prueba (1).png")
imagen_integrantestk = ImageTk.PhotoImage(imagen_integrantes)
def acercade(C_root):
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='black')
    C_root.place(x=0,y=0)

    C_root.create_text(400,50, text="INSTITUTO TECNOLOGICO DE COSTA RICA, ESCUELA DE COMPUTADORES", font=("Helvetica",16),fill="white")
    C_root.create_text(400,120, text="TALLER DE PROGRMACION, PRIMER SEMESTRE DEL 2023", font=("Helvetica",12),fill="white")
    C_root.create_text(400,150, text="SEGUNDO PROYECTO DE TALLER DE PROGRAMACION, CARRO A CONTROL REMOTO", font=("Helvetica",12),fill="white")
    C_root.create_text(400,180, text="PROFESOR: MILTON VILLEGAS LEMUS", font=("Helvetica",12),fill="white")
    C_root.create_text(400,210, text="ESTUDIANTES: ", font=("Helvetica",12),fill="white")
    C_root.create_text(400,240, text="ESTUDIANTES: CABRERA TABASH SAMIR, 2022161229", font=("Helvetica",12),fill="white")
    C_root.create_text(400,270, text="ESTUDIANTES: CAMPOS ABARCA ESTEBAN, 2022207705 ", font=("Helvetica",12),fill="white")
    C_root.create_text(400,300, text="PAIS DE PRODUCCION: COSTA RICA", font=("Helvetica",12),fill="white")
    C_root.create_text(400,330, text="PROGRAMA EJECUTADO EN PYTHON 3.11.2", font=("Helvetica",12),fill="white")

    Btnvolver = Button(C_root, text = "VOLVER", command=lambda:menu(C_root))
    Btnvolver.place(x = 700, y = 525, width= 50, height= 50)

    label_imagen = Label(root, image=imagen_integrantestk)
    label_imagen.place(x=10,y=350)
    #label_imagen.pack()

def bajarvolumen():
    #funcion para bajar el volumen
    global volumen
    volumen -= 0.1
    pygame.mixer.music.set_volume(volumen)

def subirvolumen():
    #funcion para subir el volumen 
    global volumen
    volumen += 0.1
    pygame.mixer.music.set_volume(volumen)

def activarvolumen():
    #funcion para activar el volumen, se inicia en el 50% del sonido
    pygame.mixer.music.set_volume(0.5)

def quitarvolumen():
    #funcion para quitar el volumen 
    pygame.mixer.music.set_volume(0)

def config(C_root): 
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='black')
    C_root.place(x=0,y=0)


    C_root.create_text(400,100, text="MENU DE CONFIGURACIONES", font=("Helvetica",20),fill="white")

    #llamada a los diversos botones de volumen, cada uno con una funcion respectiva asignada
    volumen = Button(C_root, text= "BAJAR VOLUMEN", command=bajarvolumen)
    volumen.place(x=100,y=200, width=100, height=100)

    volumen = Button(C_root, text= "SUBIR VOLUMEN", command=subirvolumen)
    volumen.place(x=250,y=200, width=100, height=100)

    volumen = Button(C_root, text= "ACTIVAR VOLUMEN", command=activarvolumen)
    volumen.place(x=400,y=200, width=120, height=100)

    volumen = Button(C_root, text= "QUITAR VOLUMEN", command=quitarvolumen)
    volumen.place(x=570,y=200, width=120, height=100)

    volver = Button(C_root, text = "VOLVER", command=lambda:menu(C_root))
    volver.place(x = 725, y = 525, width= 50, height= 50)

imagen_carro = Image.open("imagenes\senna.png")
imagen_carrotk = ImageTk.PhotoImage(imagen_carro)
def menu(C_root):
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='black')
    C_root.place(x=0,y=0)

    label_imagen = Label(root, image=imagen_carrotk)
    label_imagen.place(x=400,y=0)

    C_root.create_text(400,180, text = "BIENVENIDO", font=("Helvetica",20),fill="black")

    BtnAcercade = Button(C_root, text="ACERCA DE", command=lambda: acercade(C_root))
    BtnAcercade.place(x =100, y = 250, width=100, height=100)

    BtnPlay1 = Button(C_root, text="PLAY", command=lambda: play1(C_root))
    BtnPlay1.place(x =100, y = 50, width=100, height=100)

    BtnConfig = Button(C_root, text="CONFIGURACION", command=lambda: config(C_root))
    BtnConfig.place(x =100, y = 450, width=100, height=100)

    BtnSalir= Button(C_root, text="SALIR", command=lambda: salir(C_root))
    BtnSalir.place(x = 700, y = 525, width= 50, height= 50)

imagen_schumi = Image.open("imagenes\schumi.png")
imagen_schumitk = ImageTk.PhotoImage(imagen_schumi)
def inicio(C_root):
    C_root.destroy()

    C_root=Canvas(root, width=800,height=600, bg='black')
    C_root.place(x=0,y=0)

    label_imagen = Label(root, image=imagen_schumitk)
    label_imagen.place(x=0,y=0)

    #Guardar nombre del usuario
    C_root.create_text(500,75, text="DIGITE SU NOMBRE, PILOTO", font=("Helvetica",20),fill="white")
    #entry para la digitacion del usuario
    Nombreplayer = Entry(C_root)
    Nombreplayer.place(x = 400, y = 125, height=50, width=100)
    #funcion para guardar el nombre del usuario 
    def Guardarnombre():
        global Name
        global welcome_text  #Agregar una variable global para almacenar la referencia al objeto de texto

        # Eliminar el objeto de texto anterior si existe
        if welcome_text is not None:
            C_root.delete(welcome_text)

        Name = Nombreplayer.get()
        # Guardar la referencia al nuevo objeto de texto creado
        welcome_text = C_root.create_text(525, 250, text="BIENVENIDO PILOTO DE CARRERAS: " + Name, font=("Helvetica", 18), fill="white")

    #boton para guardar el nombre 
    Guardarnombre = Button(C_root, text = "GUARDAR NOMBRE", command= Guardarnombre)
    Guardarnombre.place(x = 550, y = 125, width= 130, height= 50)

    BtnEntrada= Button(C_root, text="COMENZAR", command=lambda: menu(C_root))
    BtnEntrada.place(x = 450, y = 300, width= 100, height= 100)

    BtnSalir= Button(C_root, text="SALIR", command=lambda: salir(C_root))
    BtnSalir.place(x = 700, y = 525, width= 50, height= 50)

#"""
# Cargar el primer sonido
pygame.mixer.music.load("sonidos//f1_sonido.mp3")

# Reproducir el primer sonido una vez
pygame.mixer.music.play()

# Esperar hasta que se complete la reproducción del primer sonido
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# Reproducir el segundo sonido indefinidamente
pygame.mixer.music.load("sonidos//Real_Gone.mp3")
pygame.mixer.music.play(-1)
#"""
inicio(C_root)
root.mainloop()
