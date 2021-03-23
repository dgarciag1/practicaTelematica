
import _thread
import socket
import constants
import Aplicacion
import threading
import sys
from collections import deque

class Mom:

	def __init__(self):
		self.MOMserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.colas = {}
		self.contador = 0
		self.consumidoresConectados = {}
		self.contadorConsumidores = 0

	def envioMensaje(self):
		if (len(self.consumidoresConectados) != 0):
			valor = 0
			for cliente in self.consumidoresConectados:
				valor = valor + 1
				idCliente = cliente
				arreglo = self.consumidoresConectados[idCliente]
				conexionAplicacion = arreglo[0]
				direccionAplicacion = arreglo[1]
				nombre = arreglo[2]
				idCola = arreglo[3]
				estado = arreglo[4]

				try: 
					if (self.colas[int(idCola)].getTamañoCola() != 0):
						consumidores = self.colas[int(idCola)].getClientes()
						estados = self.colas[int(idCola)].getEstadosClientes()
						for i in range(0,len(consumidores)):
							clienteArreglo = consumidores[i]
							estadoArreglo = estados[i]
							
							if (idCliente == clienteArreglo and estadoArreglo == False and len(consumidores) == 1 and self.colas[int(idCola)].getTamañoCola() > 1):
								contadorAux = 0
								while contadorAux < self.colas[int(idCola)].getTamañoCola():
									respuesta = ""
									mensajeEnviar = self.colas[int(idCola)].cambiarIndiceEnvio()
									respuesta = f"Repsuesta para: {direccionAplicacion} Tiene un nuevo mensaje: {mensajeEnviar}\n"
									conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
							elif (idCliente == clienteArreglo and estadoArreglo == False and len(consumidores) > 1):
								respuesta = ""
								mensajeEnviar = self.colas[int(idCola)].cambiarIndiceEnvio()
								respuesta = f"Repsuesta para: {direccionAplicacion} Tiene un nuevo mensaje: {mensajeEnviar}\n"
								conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
								self.colas[int(idCola)].cambiarEstadoCliente(i)
								if (i == len(consumidores)-1):
									self.colas[int(idCola)].actualizarTodosConsumidores()
								break
							elif (idCliente == clienteArreglo and estadoArreglo == False):
								respuesta = ""
								mensajeEnviar = self.colas[int(idCola)].cambiarIndiceEnvio()
								respuesta = f"Repsuesta para: {direccionAplicacion} Tiene un nuevo mensaje: {mensajeEnviar}\n"
								conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
								if (i == len(consumidores)-1):
									self.colas[int(idCola)].actualizarTodosConsumidores()
								break

					else:
						respuesta = f"Repsuesta para: {direccionAplicacion} No hay mensajes nuevos\n"
						conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
				except:
					continue

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

	        elif (opcion == "CREAR"):
	        	print(f'{direccionAplicacion[0]} solicita: {opcion}')
	        	aplicacion = Aplicacion.Aplicacion(arreglo[1],arreglo[2],self.contador)
	        	self.colas[self.contador] = aplicacion
	        	respuesta = f'Respuesta para: {direccionAplicacion[0]} La cola fue creada correctamente\n con el nombre {arreglo[1]} No olvide el token de identificacion de la cola: {self.contador}\n'
	        	self.contador = self.contador + 1
	        	conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
	        	print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

	        elif (opcion == "LISTAR"):
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

	        	conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
	        	print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

	        elif (opcion == "BORRAR"):
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

	        elif (opcion == "CONECTAR"):
	        	print(f'{direccionAplicacion[0]} solicita: {opcion}')
	        	idCola = arreglo[3]
	        	nombreCola = arreglo[1]
	        	claveAcceso = arreglo[2]
	        	try:
		        	nombreAux = self.colas[int(idCola)].getNombre()
		        	claveAux = self.colas[int(idCola)].getClaveAcceso()
		        	idAux = self.colas[int(idCola)].getId()
		        	if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux) and str(claveAux) == str(claveAcceso)):
	        			respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión se establecio correctamente, ahora puedes enviar mensajes\n'
	        			self.colas[int(idCola)].conectar()
	        	except:
	        		respuesta = f'Respuesta para: {direccionAplicacion[0]} Los datos son incorrectos, prueba nuevamente\n'
	        	print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
	        	conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
	        
	        elif (opcion == "CONECTAR-CONSUMIDOR"):
	        	print(f'{direccionAplicacion[0]} solicita: {opcion}')
	        	nombreCola = arreglo[1]
	        	idCola = arreglo[2]
	        	respuesta = ""
	        	try:
		        	nombreAux = self.colas[int(idCola)].getNombre()
		        	idAux = self.colas[int(idCola)].getId()
		        	if (str(idCola) == str(idAux) and str(nombreCola) == str(nombreAux)):
	        			respuesta = f'Respuesta para: {direccionAplicacion[0]} La conexión se establecio correctamente, ahora puedes recibir mensajes\n'
	        			conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
	        			arregloConsumidor = [conexionAplicacion,direccionAplicacion,nombreAux,idCola,True]
	        			self.colas[int(idCola)].agregarCliente(self.contadorConsumidores)
	        			self.consumidoresConectados[self.contadorConsumidores] = arregloConsumidor
	        			self.contadorConsumidores = self.contadorConsumidores + 1
	        			threadEnvio = threading.Thread(target=self.envioMensaje)
	        			threadEnvio.start()
	        			threadEnvio.join()
	        	except:
	        		respuesta = f'Respuesta para: {direccionAplicacion[0]} No hay conexión, prueba nuevamente\n'
	        		conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
	        	print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
	        	
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
					        respuesta = respuesta + f'			Mensaje: {mensaje}\n'
	        	conexionAplicacion.sendall(respuesta.encode(constants.ENCODING_FORMAT))
	        	print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')

	        elif (opcion == "DESCONECTAR"):
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

	        elif (opcion == "MENSAJE"):
	        	print(f'{direccionAplicacion[0]} solicita: {opcion}')
	        	nombreCola = arreglo[1]
	        	idCola = arreglo[2]
	        	print("Id Cola envio mensaje desde el productor: " + str(idCola))
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
		        			threadEnvio = threading.Thread(target=self.envioMensaje)
		        			threadEnvio.start()
		        			threadEnvio.join()
			        	else:
			        		respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje. La cola está llena\n'
			        else:
			        	respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, los datos de la cola no coinciden\n'
	        	except:
	        		respuesta = f'Respuesta para: {direccionAplicacion[0]} Error al enviar el mensaje, posiblemente no estés conectado a la cola\n'
	        	print(f'Se envio respuesta a: {direccionAplicacion[0]} por la solicitud: {opcion}')
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
