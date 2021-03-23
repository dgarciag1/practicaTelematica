import socket
import constants

socketProductor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('*' * 50)
    print("Estás conectando una nueva aplicación productora al MOM\n")
    socketProductor.connect(("127.0.0.1", constants.PORT))
    tuplaConexion = socketProductor.getsockname()
    print("Tu dirección de conexión es: ", tuplaConexion)
    opcion = menu()

    while opcion != "SALIR":
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()
        elif (opcion == "CREAR"):
            nombreAplicacion = input("Ingresa el nombre de la aplicación ")
            claveAcceso = input("Ingresa la clave de acceso al MOM de la aplicación ")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso
            socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "LISTAR"):
        	envioMOM = opcion
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "BORRAR"):
        	nombreAplicacion = input("Ingresa el nombre de la cola a eliminar ")
        	idCola = input("Ingresa el token de identificacion de la cola a eliminar ")
        	claveAcceso = input("Ingresa la clave de acceso al MOM de la cola ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso + ' ' + idCola
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "CONECTAR"):
        	nombreAplicacion = input("Ingresa el nombre de la cola a la que te quieres conectar ")
        	idCola = input("Ingresa el token de identificacion de la cola con a la que te quieres conectar ")
        	claveAcceso = input("Ingresa la clave de acceso al MOM de la cola ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + claveAcceso + ' ' + idCola
        	socketProductor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketProductor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "DESCONECTAR"):
        	nombreAplicacion = input("Ingresa el nombre de la cola en la que vas a cerrar la sesión ")
        	idCola = input("Ingresa el token de identificacion de la cola ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola
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
        elif (opcion == "MENSAJE"):
        	nombreAplicacion = input("Ingresa el nombre de la cola correspondiente ")
        	idCola = input("Ingresa el token de identificacion de la cola ")
        	mensaje = input("Mensaje a enviar ")
        	envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola + ' ' + mensaje
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


def menu():
	print("OPCION CREAR: Crear una nueva cola")
	print("OPCION LISTAR: Listado de Colas en el MOM")
	print("OPCION BORRAR: Eliminar una Cola del MOM")
	print("OPCION CONECTAR: Conexión a una Cola del MOM")
	print("OPCION DESCONECTAR: Desconexión una Cola del MOM")
	print("OPCION MENSAJE: Envio de un mensaje")
	print("OPCION SALIR: Desconectar aplicación")
	opcion = input("Ingrece la opcion que quiere realizar ")
	return opcion


if __name__ == '__main__':
    main()
