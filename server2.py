import _thread
import socket
import constants
import Aplicacion
import threading
import sys
from collections import deque
import os
import os.path as path

class Mom:

        def __init__(self):
                self.MOMserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.colas = {}
                self.canales = {}
                self.contadorColas = 0
                self.contadorCanales = 0
                self.consumidoresConectados = {}
                self.contadorConsumidores = 0

        def envioMensaje(self):
                if (len(self.consumidoresConectados) != 0):
                        value = 0
                        for cliente in self.consumidoresConectados:
                                idCliente = cliente
                                arreglo = self.consumidoresConectados[idCliente]
                                conexionAplicacion = arreglo[0]
                                direccionAplicacion = arreglo[1]
                                self.consumidoresConectados[idCliente][4] = self.canales[int(self.consumidoresConectados[idCliente][3])].getCola()
                                auxIndex = 0
                                while auxIndex < len(self.consumidoresConectados[idCliente][4]):
                                        respuesta = ""
                                        mensajeEnviar = self.consumidoresConectados[idCliente][4][auxIndex]
                                        respuesta = f"Repsuesta para: {direccionAplicacion} Tiene un nuevo mensaje: {mensajeEnviar}\n"
                                        conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                        print(mensajeEnviar)
                                        auxIndex = auxIndex + 1
                                if (value == len(self.consumidoresConectados)-1):
                                       self.canales[int(self.consumidoresConectados[idCliente][3])].vaciarCola()
                                value = value+1


        def threaded(self, conexionAplicacion, direccionAplicacion):
                while True:
                        datosRecibidos = conexionAplicacion.recv(1024)
                        datosRecibidos = str(datosRecibidos.decode("utf-8"))
                        arreglo = datosRecibidos.split()
                        opcion = arreglo[0]

                        if (opcion == "SALIR"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Vuelva pronto\n'
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'La aplicación {direccionAplicacion[0]}:{direccionAplicacion[1]} se desconectó correctamente')
                                break

                        elif (opcion == "CREAR-COLA"):
                                print("prueba")
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                aplicacion = Aplicacion.Aplicacion(arreglo[1],arreglo[2],self.contadorColas)
                                self.colas[self.contadorColas] = aplicacion
                                respuesta = f'Respuesta para: {direccionAplicacion[0]} La cola fue creada correctamente\n con el nombre {arreglo[1]} No olvide el token de identificacion de la cola: {self.contadorColas}\n'
                                self.contadorColas = self.contadorColas + 1
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

                        elif (opcion == "CREAR-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                aplicacion = Aplicacion.Aplicacion(arreglo[1],arreglo[2],self.contadorCanales)
                                self.canales[self.contadorCanales] = aplicacion
                                respuesta = f'Respuesta para: {direccionAplicacion[0]} El canal fue creado correctamente\n con el nombre {arreglo[1]} No olvide el token de identificacion del canal: {self.contadorCanales}\n'
                                self.contadorCanales = self.contadorCanales + 1
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

                        elif (opcion == "LISTAR-COLA"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Listado de colas\n'
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                respuesta = ''
                                if (len(self.colas) == 0):
                                        respuesta = 'No hay colas en el MOM\n'
                                else:
                                        else:
                                        for cola in self.colas:
                                                idCola = cola
                                                respuesta = respuesta + f'Cola, Token de identificación: {self.colas[idCola].getId()}: {self.colas[idCola].getNombre()} estado: {self.colas[idCola].getEstado()}\n'

                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

                        elif (opcion == "LISTAR-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Listado de canales\n'
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                respuesta = ''
                                if (len(self.canales) == 0):
                                        respuesta = 'No hay canales en el MOM\n'
                                else:
                                        for canal in self.canales:
                                                idCanal = canal
                                                respuesta = respuesta + f'Canal, Token  de identificacion: {self.canales[idCanal].getId()}: {self.canales[idCanal].getNombre()} estado: {self.canale[idCanal].getEstado()}\n'

                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

                        elif (opcion == "BORRAR-COLA"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                idCola = arreglo[3]
                                nombreCola = arreglo[1]
                                claveAcceso = arreglo[2]
                                try:
                                        nombreAux = self.colas[int(idCola)].getNombre()
                                        claveAux = self.colas[int(idCola)].getClaveAcceso()
                                        idAux = self.colas[int(idCola)].getId()
                                        if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux) and str(claveAux) == str(claveAcceso)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} La cola fue eliminada correctamente\n'
                                                self.colas.pop(int(idCola))
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "BORRAR-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                idCanal = arreglo[3]
                                nombreCanal = arreglo[1]
                                claveAcceso = arreglo[2]
                                try:
                                        nombreAux = self.canales[int(idCanal)].getNombre()
                                        claveAux = self.canales[int(idCanal)].getClaveAcceso()
                                        idAux = self.canales[int(idCanal)].getId()
                                        claveAux = str(claveAux)
                                        claveAux = claveAux[2:len(claveAux)-1]
                                        if (str(idCanal) == str(idAux) and str(nombreCanal) == str(nombreAux) and str(claveAux) == str(claveAcceso)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} El canal fue eliminado correctamente\n'
                                                self.canales.pop(int(idCanal))
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "CONECTAR-COLA"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                idCola = arreglo[3]
                                nombreCola = arreglo[1]
                                claveAcceso = arreglo[2]
                                claveAux = self.colas[int(idCola)].getClaveAcceso()
                                try:
                                        nombreAux = self.colas[int(idCola)].getNombre()
                                        claveAux = self.colas[int(idCola)].getClaveAcceso()
                                        idAux = self.colas[int(idCola)].getId()
                                        print(f'Clave ingresada: {str(claveAcceso)}')
                                        print(f'Clave cola: {str(claveAux)}')
                                        if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux) and str(claveAux) == str(claveAcceso)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión se establecio correctamente, ahora puedes enviar mensajes\n'
                                                self.colas[int(idCola)].conectar()
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))         

                        elif (opcion == "CONECTAR-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                idCanal = arreglo[3]
                                nombreCanal = arreglo[1]
                                claveAcceso = arreglo[2]
                                try:
                                        nombreAux = self.canales[int(idCanal)].getNombre()
                                        claveAux = self.canales[int(idCanal)].getClaveAcceso()
                                        idAux = self.canales[int(idCanal)].getId()
                                        if (str(idCanal) == str(idAux) and str(nombreCanal) == str(nombreAux) and str(claveAux) == str(claveAcceso)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión se establecio correctamente, ahora puedes enviar mensajes\n'
                                                self.canales[int(idCanal)].conectar()
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "PULL-COLA"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                nombreCola = arreglo[1]
                                idCola = arreglo[2]
                                respuesta = ""
                                nombreAux = self.colas[int(idCola)].getNombre()
                                idAux = self.colas[int(idCola)].getId()
                                if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                                        if (self.colas[int(idCola)].getTamañoCola() == 0):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} No hay mensajes\n'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                        else:
                                                mensajeEnviar = self.colas[int(idCola)].cambiarIndiceEnvio()
                                                respuesta = f"Repsuesta para: {direccionAplicacion} Tiene un nuevo mensaje: {mensajeEnviar}\n"
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                else:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al hacer Pull de la cola, los datos de acceso son erroneos\n'
                                        conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))


                        elif (opcion == "VER"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Listado de colas\n'
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                respuesta = ''
                                if (len(self.colas) == 0):
                                        respuesta = 'No hay colas en el MOM\n'
                                else:
                                        for cola in self.colas:
                                                idCola = cola
                                                respuesta = respuesta + f'Aplicacion {self.colas[idCola].getId()}: {self.colas[idCola].getNombre()} estado: {self.colas[idCola].getEstado()}\n'
                                                mensajes = list(self.colas[int(idCola)].getCola())
                                                for mensaje in mensajes:
                                                        respuesta = respuesta + f'                      Mensaje: {mensaje}\n'
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

                        elif (opcion == "DESCONECTAR-COLA"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                idCola = arreglo[2]
                                nombreCola = arreglo[1]
                                try:
                                        nombreAux = self.colas[int(idCola)].getNombre()
                                        idAux = self.colas[int(idCola)].getId()
                                        if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} la conexión con el MOM para el envio de mensajes se cerró correctamente\n'
                                                self.colas[int(idCola)].desconectar()
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Ocurrio un error, prueba nuevamente\n'
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "DESCONECTAR-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                idCanal = arreglo[2]
                                nombreCanal = arreglo[1]
                                try:
                                        nombreAux = self.canales[int(idCanal)].getNombre()
                                        idAux = self.canales[int(idCanal)].getId()
                                        if (str(idCanal) == str(idAux) and str(nombreCanal) == str(nombreAux)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} la conexión con el MOM para el envio de mensajes se cerró correctamente\n'
                                                self.canales[int(idCanal)].desconectar()
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Ocurrio un error, prueba nuevamente\n'
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "MENSAJE-COLA"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                nombreCola = arreglo[1]
                                idCola = arreglo[2]
                                mensaje = ""
                                for i in range(3,len(arreglo)):
                                        mensaje = mensaje + arreglo[i] + " "
                                try:
                                        nombreAux = self.colas[int(idCola)].getNombre()
                                        idAux = self.colas[int(idCola)].getId()
                                        estado = self.colas[int(idCola)].getEstado()
                                        if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux) and estado == True):
                                                if (self.colas[int(idCola)].enviarMensaje(mensaje) == 1):
                                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} El mensaje fue enviado correctamente\n'
                                                else:
                                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje. La cola está llena\n'
                                        else:
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, los datos de la cola no coinciden\n'
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, posiblemente no estés conectado a la cola\n'

                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "MENSAJE-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                nombreCanal = arreglo[1]
                                idCanal = arreglo[2]
                                mensaje = ""
                                for i in range(3,len(arreglo)):
                                        mensaje = mensaje + arreglo[i] + " "
                                try:
                                        nombreAux = self.canales[int(idCanal)].getNombre()
                                        idAux = self.canales[int(idCanal)].getId()
                                        estado = self.canales[int(idCanal)].getEstado()
                                        if (str(idCanal) == str(idAux) and str(nombreCanal) == str(nombreAux) and estado == True):
                                                if (self.canales[int(idCanal)].enviarMensaje(mensaje) == 1):
                                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} El mensaje fue enviado correctamente\n'
                                                        threadEnvio = threading.Thread(target=self.envioMensaje)
                                                        threadEnvio.start()
                                                        threadEnvio.join()
                                                else:
                                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje. El canal está llena\n'
                                        else:
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, los datos de la cola no coinciden\n'
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, posiblemente no estés conectado al canal\n'

                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "CONSUMIDOR-CANAL"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                nombreCanal = arreglo[1]
                                idCanal = arreglo[2]
                                respuesta = ""
                                try:
                                        nombreAux = self.canales[int(idCanal)].getNombre()
                                        idAux = self.canales[int(idCanal)].getId()
                                        print(f'agregar consumidor: {self.canales[int(idCanal)].getCola()}')
                                        if (str(idCanal) == str(idAux) and str(nombreCanal) == str(nombreAux)):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión se establecio correctamente, ahora puedes recibir mensajes\n'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                                arregloConsumidor = [conexionAplicacion,direccionAplicacion,nombreAux,idCanal,deque()]
                                                self.canales[int(idCanal)].agregarCliente(self.contadorConsumidores)
                                                self.consumidoresConectados[self.contadorConsumidores] = arregloConsumidor
                                                self.contadorConsumidores = self.contadorConsumidores + 1
                                                threadEnvio = threading.Thread(target=self.envioMensaje)
                                                threadEnvio.start()
                                                threadEnvio.join()
                                except:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} No hay conexión, prueba nuevamente\n'
                                        conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

                        elif (opcion == "CREAR-SESION"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                usuario = arreglo[1]
                                contrasena = arreglo[2]
                                if (path.exists("usuarios.txt")):
                                        file = open("usuarios.txt", "r")
                                        lineas = file.readlines()
                                        if (usuario+"\n" in lineas):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} El usuario ya existe\n'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                        else:
                                                file = open("usuarios.txt", "a")
                                                file.write(usuario+"\n"+contrasena+"\n")
                                                file.close()
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Sesión Creada\n'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                else:
                                        file = open("usuarios.txt", "w")
                                        file.write(usuario+"\n"+contrasena+"\n")
                                        file.close()
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Sesión Creada\n'
                                        conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))

                        elif (opcion == "INICIAR-SESION"):
                                print(f'{direccionAplicacion[0]} solicita: {opcion}')
                                usuario = arreglo[1]
                                contrasena = arreglo[2]
                                file = open("usuarios.txt", "r")
                                lineas = file.readlines()
                                if (usuario+"\n" in lineas):
                                        posicion = lineas.index(usuario+"\n")
                                        if (contrasena+"\n" == lineas[posicion+1]):
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Sesión Iniciada\n'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                                respuesta = f'Ok'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                        else:
                                                respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al iniciar la sesión 1\n'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                                respuesta = f'No'
                                                conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                else:
                                        respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al iniciar la sesión 2\n'
                                        conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
                                        respuesta = f'No'
                                        conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))


                try:
                        print_lock.release()
                except BaseException:
                        pass
                conexionAplicacion.close()


        def main(self):
                print('*' * 50)
                print('El MOM está encendido\n')
                print('La dirección IP del servidor MOM es: ', constants.SERVER_ADDRESS)
                print('El puerto por el cual está corriendo el servidor MOM es: ', constants.PORT)
                tuplaConexion = (constants.SERVER_ADDRESS, constants.PORT)
                self.MOMserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.MOMserver.bind(tuplaConexion)
                self.MOMserver.listen(constants.BACKLOG)
                while True:
                        conexionAplicacion, direccionAplicacion = self.MOMserver.accept()

                        print(f'Nueva aplicación conectada desde la dirección IP: {direccionAplicacion[0]}')
                        _thread.start_new_thread(self.threaded, (conexionAplicacion, direccionAplicacion))
                self.MOMserver.close()



def mom():
        mom = Mom()
        mom.main()

if __name__ == '__main__':
    mom()