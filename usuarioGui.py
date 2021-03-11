import socket
import threading
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog

ip = "127.0.0.1"
puerto = 44444

class Usuario:
    def __init__(self, ip, puerto):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sock stream es para que sea tcp
        self.sock.connect((ip, puerto))

        mensaje = tkinter.Tk() 
        mensaje.withdraw()

        self.nombre = simpledialog.askstring("Nombre", "Elegir nombre de usuario", parent=mensaje)

        self.guiHecha = False
        self.corriendo = True

        threadGui = threading.Thread(target=self.loopGui)
        threadRecibir = threading.Thread(target=self.recibir) 

        threadGui.start()
        threadRecibir.start()

    def loopGui(self):
        self.ventana = tkinter.Tk()
        self.ventana.configure(bg="lightgray")

        self.chatGui = tkinter.Label(self.ventana, text="Chat:", bg="lightgray")
        self.chatGui.config(font=("Arial", 12))
        self.chatGui.pack(padx=20, pady=5)
        
        self.areaDeTexto = tkinter.scrolledtext.ScrolledText(self.ventana) #para scrollear en el chat
        self.areaDeTexto.pack(padx=20, pady=5)
        self.areaDeTexto.config(state="disabled")

        self.mensajeGui = tkinter.Label(self.ventana, text="Mensaje:", bg="lightgray")
        self.mensajeGui.config(font=("Arial", 12))
        self.mensajeGui.pack(padx=20, pady=5)

        self.areaDeMensaje = tkinter.Text(self.ventana, height=3)
        self.areaDeMensaje.pack(padx=20, pady=5)

        self.enviar = tkinter.Button(self.ventana, text="Enviar", command=self.escribir) #command recibe una funcion encargada de la logica del boton
        self.enviar.config(font=("Arial", 12))
        self.enviar.pack(padx=20, pady=5)

        self.guiHecha = True

        self.ventana.mainloop()
        self.ventana.protocol("WM_DELETE_WINDOW", self.terminar)

    def recibir(self):
        while self.corriendo:
            try:
                mensaje = self.sock.recv(1024).decode("utf-8")
                if mensaje == "NICK":
                    self.sock.send(self.nombre.encode("utf-8"))
                else:
                    if self.guiHecha:
                        self.areaDeTexto.config(state="normal")
                        self.areaDeTexto.insert("end", mensaje) #empezamos al final porque queremos appendear losm mensajes
                        self.areaDeTexto.yview("end") #para que la ventana vaya bajando con los mensajes
                        self.areaDeTexto.config(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print("Error al conectarse")
                self.sock.close()
                break

    def escribir(self):
        mensaje = f"{self.nombre}: {self.areaDeMensaje.get('1.0', 'end')}" #desde 1.0 hasta el final para que elija todo el texto
        self.sock.send(mensaje.encode("utf-8"))
        self.areaDeMensaje.delete("1.0", "end") #limpiamos el area de mensaje borrando el texto entero

    def terminar(self):
        self.corriendo = False
        self.ventana.destroy()
        self.sock.close()
        exit(0)

usuario = Usuario(ip, puerto)

    
