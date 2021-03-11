import threading
import socket

ip = "127.0.0.1" #La ip que si solo es en casa se usa localhost
puerto = 55555

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
        except: #si hay un error al recibir el mensaje o conexion con el usuario cortamos la conexion y lo removemos de la lista
            indice = usuarios.index(usuario) #conseguimos su posicion en la lista
            usuarios.remove(usuario)
            usuario.close() 
            nickname = nicknames[indice] #lo buscamos con ese indice en la lista de nicknames y lo borramos
            enviarATodos(f'{nickname} abandonó el chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def recibir():
    while True:
        usuario, ip = server.accept() #acepta las conexiones de cualquier usuario
        print(f'Conectado desde: {str(ip)}') #me dice desde donde se conectaron

        usuario.send('NICK'.encode('ascii')) #le envio una palabra clave para esperar una respuesta especifica(su nick en este caso)
        nickname = usuario.recv(1024).decode('ascii') #recibo el nickname
        nicknames.append(nickname) #lo agrego a la lista de nicks
        usuarios.append(usuario) #lo agrego a la lsta de usuarios

        print(f'El nickname del usuario es {nickname}') #me muestra el nick q eligio
        enviarATodos(f'{nickname} se unio al chat\n'.encode('ascii')) 
        usuario.send("Conectado al servidor".encode('ascii')) #le mando un mensaje a ese usuario

        thread = threading.Thread(target=controlar, args=(usuario,)) #inicio un thread porque necesito controlar muchos clientes/trafico a la vez
        thread.start()  

    
print("Esperando conexiones...")
recibir() #corro el main




             