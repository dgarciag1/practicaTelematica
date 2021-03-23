import socket
import constants

socketProductor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('*' * 50)
    print("Estás conectando una nueva aplicación productora al MOM\n")
    socketProductor.connect(("18.214.102.119", constants.PORT))
    tuplaConexion = socketProductor.getsockname()
    print("Tu dirección de conexión es: ", tuplaConexion)

    opcion = menuInicial()
    while opcion != "SALIR":
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menuInicial()
        elif (opcion == "CREAR-SESION"):
            usuario = input("Ingrese el usuario ")
            contrasena = input("Ingrese la contraseña ")
            envioMOM = opcion + ' ' + usuario + ' ' + contrasena
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menuInicial()
        elif (opcion == "INICIAR-SESION"):
            usuario = input("Ingrese el usuario ")
            contrasena = input("Ingrese la contraseña ")
            envioMOM = opcion + ' ' + usuario + ' ' + contrasena
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            validar = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            validar = str(validar)
            if (validar[2:len(validar)-1] == "Ok"):
                opcion = menu()
            else:
                opcion = menuInicial()
        elif (opcion == "CREAR-COLA"):
            nombreAplicacion = input("Ingresa el nombre de la cola ")
            claveAcceso = input("Ingresa la clave de acceso al MOM de la cola ")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "CREAR-CANAL"):
            nombreAplicacion = input("Ingresa el nombre del canal ")
            claveAcceso = input("Ingresa la clave de acceso al MOM del canal ")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "LISTAR-COLA"):
        	envioMOM = opcion
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "LISTAR-CANAL"):
            envioMOM = opcion
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "BORRAR-COLA"):
        	nombreAplicacion = input("Ingresa el nombre de la cola a eliminar ")
        	idCola = input("Ingresa el token de identificacion de la cola a eliminar ")
        	claveAcceso = input("Ingresa la clave de acceso al MOM de la cola ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso + ' ' + idCola
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "BORRAR-CANAL"):
            nombreAplicacion = input("Ingresa el nombre del canal a eliminar ")
            idCola = input("Ingresa el token de identificacion del canal a eliminar ")
            claveAcceso = input("Ingresa la clave de acceso al MOM del canal")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso + ' ' + idCola
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "CONECTAR-COLA"):
        	nombreAplicacion = input("Ingresa el nombre de la cola a la que te quieres conectar ")
        	idCola = input("Ingresa el token de identificacion de la cola con a la que te quieres conectar ")
        	claveAcceso = input("Ingresa la clave de acceso al MOM de la cola ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso + ' ' + idCola
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "CONECTAR-CANAL"):
            nombreAplicacion = input("Ingresa el nombre del canal al que te quieres conectar ")
            idCola = input("Ingresa el token de identificacion del canal al que te quieres conectar ")
            claveAcceso = input("Ingresa la clave de acceso al MOM del canal ")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso + ' ' + idCola
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "DESCONECTAR-COLA"):
        	nombreAplicacion = input("Ingresa el nombre de la cola en la que vas a cerrar la sesión ")
        	idCola = input("Ingresa el token de identificacion de la cola ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "DESCONECTAR-CANAL"):
            nombreCanal = input("Ingresa el nombre del canal del que vas a cerrar la sesión ")
            idCola = input("Ingresa el token de identificacion del canal ")
            envioMOM = opcion + ' ' + nombreCanal + ' ' + idCola
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "VER"):
            envioMOM = opcion
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "MENSAJE-COLA"):
        	nombreAplicacion = input("Ingresa el nombre de la cola correspondiente ")
        	idCola = input("Ingresa el token de identificacion de la cola ")
        	mensaje = input("Mensaje a enviar ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola + ' ' + mensaje
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "MENSAJE-CANAL"):
            nombreCanal = input("Ingresa el nombre del canal correspondiente ")
            idCanal = input("Ingresa el token de identificacion del canal ")
            mensaje = input("Mensaje a enviar ")
            envioMOM = opcion + ' ' + nombreCanal + ' ' + idCanal + ' ' + mensaje
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        else:
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()

    socketProductor.send(bytes(opcion, constants.ENCODING_FORMAT))
    datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
    print(datosRecibidos.decode(constants.ENCODING_FORMAT))
    socketProductor.close()

def menuInicial():
    print("CREAR-SESION: Crear la sesión")
    print("INICIAR-SESION: Inicio de sesión")
    print("OPCION SALIR: Desconectar aplicación")
    opcion = input("Ingrece la opcion que quiere realizar ")
    return opcion

def menu():
    print("OPCION CREAR-COLA: Crear una nueva cola")
    print("OPCION LISTAR-COLA: Listado de Colas en el MOM")
    print("OPCION BORRAR-COLA: Eliminar una Cola del MOM")
    print("OPCION CONECTAR-COLA: Conexión a una Cola del MOM")
    print("OPCION DESCONECTAR-COLA: Desconexión una Cola del MOM")
    print("OPCION MENSAJE-COLA: Envio de un mensaje")

    print("OPCION CREAR-CANAL: Crear una nueva cola")
    print("OPCION LISTAR-CANAL: Listado de Colas en el MOM")
    print("OPCION BORRAR-CANAL: Eliminar una Cola del MOM")
    print("OPCION CONECTAR-CANAL: Conexión a una Cola del MOM")
    print("OPCION DESCONECTAR-CANAL: Desconexión una Cola del MOM")
    print("OPCION MENSAJE-CANAL: Envio de un mensaje")

    print("OPCION SALIR: Desconectar aplicación")
    opcion = input("Ingrece la opcion que quiere realizar ")
    return opcion

if __name__ == '__main__':
    main()
