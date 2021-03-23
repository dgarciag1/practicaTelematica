import socket
import constants

socketConsumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('*' * 50)
    print("Estás conectando una nueva aplicación consumidora al MOM\n")
    socketConsumidor.connect(("18.214.102.119", constants.PORT))
    tuplaConexion = socketConsumidor.getsockname()
    print("Tu dirección de conexión es: ", tuplaConexion)
    opcion = menu()

    while opcion != "SALIR":
        if opcion == '':
            print("Opcion invalida, intenta de nuevo\n")
            opcion = menu()
        elif (opcion == "LISTAR-COLA"):
        	envioMOM = opcion
        	socketConsumidor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
        	datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
        	print(datosRecibidos.decode(constants.ENCODING_FORMAT))
        	opcion = menu()
        elif (opcion == "LISTAR-CANAL"):
            envioMOM = opcion
            socketConsumidor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "PULL-COLA"):
            nombreAplicacion = input("Ingresa el nombre de la cola a la que te quieres conectar ")
            idCola = input("Ingresa el token de identificacion de la cola con a la que te quieres conectar ")
            envioMOM = opcion + ' ' + nombreAplicacion + ' ' + idCola
            socketConsumidor.send(bytes(envioMOM, constants.ENCODING_FORMAT))
            datosRecibidos = socketConsumidor.recv(constants.RECV_BUFFER_SIZE)
            print(datosRecibidos.decode(constants.ENCODING_FORMAT))
            opcion = menu()
        elif (opcion == "CONSUMIDOR-CANAL"):
            nombreCanal = input("Ingresa el nombre del canal que te quieres conectar ")
            idCanal = input("Ingresa el token de identificacion del canal al que te quieres conectar ")
            envioMOM = opcion + ' ' + nombreCanal + ' ' + idCanal
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
    print("OPCION LISTAR-CANAL: Listado de Canales en el MOM")
    print("OPCION LISTAR-COLA: Listado de Colas en el MOM")
    print("OPCION PULL-COLA: Conexión a una Cola del MOM")
    print("OPCION CONSUMIDOR-CANAL: Conexión a un Canal del MOM")
    print("OPCION SALIR: Desconectar aplicación")
    opcion = input("Ingrece la opcion que quiere realizar ")
    return opcion

"""def menu2():
    print("OPCION PULL: Recibir tarea")
    print("OPCION SALIR: Salir")
    opcion = input("Ingrece la opcion que quiere realizar ")
    return opcion"""


if __name__ == '__main__':
    main()
