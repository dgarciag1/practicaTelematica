import socket
import constants

socketConsumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('*' * 50)
    print("Estás conectando una nueva aplicación consumidora al MOM\n")
    socketConsumidor.connect(("127.0.0.1", constants.PORT))
    tuplaConexion = socketConsumidor.getsockname()
    print("Tu dirección de conexión es: ", tuplaConexion)
    opcion = menu()

    while opcion != "SALIR":
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()
        elif (opcion == "LISTAR"):
        	envioMOM = opcion
        	socketConsumidor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "CONECTAR-CONSUMIDOR"):
            nombreAplicacion = input("Ingresa el nombre de la cola a la que te quieres conectar ")
            idCola = input("Ingresa el token de identificacion de la cola con a la que te quieres conectar ")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola
            socketConsumidor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            while True:
                datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
                mensaje = datosRecibidos.decode(constants.ENCODING_FORMAT)
                print(mensaje)
                if (mensaje[len(mensaje)-10:] == "nuevamente"):
                    break

            	
        else:
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()

    socketConsumidor.send(bytes(opcion, constants.ENCODING_FORMAT))
    datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
    print(datosRecibidos.decode(constants.ENCODING_FORMAT))
    socketConsumidor.close()


def menu():
	print("OPCION LISTAR: Listado de Colas en el MOM")
	print("OPCION CONECTAR-CONSUMIDOR: Conexión a una Cola del MOM")
	print("OPCION SALIR: Desconectar aplicación")
	opcion = input("Ingrece la opcion que quiere realizar ")
	return opcion


if __name__ == '__main__':
    main()
