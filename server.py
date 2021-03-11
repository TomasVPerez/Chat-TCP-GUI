import threading
import socket

ip = "127.0.0.1" #La ip que si solo es en casa se usa localhost
puerto = 44444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, puerto))
server.listen() #para que el server escuche conexiones

usuarios = []
nicknames = []

def enviarATodos(mensaje): #manda mensaje del servidor a todos los usuarios
    for usuario in usuarios:
        usuario.send(mensaje)

def controlar(usuario):
    while True:
        try:
            mensaje = usuario.recv(1024)
            enviarATodos(mensaje) #recibimos mensajes de los usuarios y los enviamos a todos los demas usuarios
        except: 
            indice = usuarios.index(usuario) 
            usuarios.remove(usuario)
            usuario.close() 
            nickname = nicknames[indice] 
            enviarATodos(f'{nickname} abandonó el chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def recibir():
    while True:
        usuario, ip = server.accept() #acepta las conexiones de cualquier usuario
        print(f'Conectado desde: {str(ip)}') 

        usuario.send('NICK'.encode('ascii')) 
        nickname = usuario.recv(1024).decode('ascii') 
        nicknames.append(nickname) 
        usuarios.append(usuario) 

        print(f'El nickname del usuario es {nickname}') 
        enviarATodos(f'{nickname} se unio al chat\n'.encode('ascii')) 
        usuario.send("Conectado al servidor".encode('ascii')) 

        thread = threading.Thread(target=controlar, args=(usuario,)) #inicio un thread porque necesito controlar muchos clientes/trafico a la vez
        thread.start()  

    
print("Esperando conexiones...")
recibir() 




             
