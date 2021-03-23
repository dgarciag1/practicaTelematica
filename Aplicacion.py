from collections import deque
from cryptography.fernet import Fernet
import constants

class Aplicacion:

	def __init__(self, nombre, claveAcceso, idCola):
		self.id = idCola
		self.nombre = nombre
		#self.claveAcceso = claveAcceso
		self.estado = False
		self.clientes = []
		self.estadoClientes = []
		self.cola = deque()
		
		self.genera_clave()

		self.clave = self.cargar_clave()

		claveEncriptada = claveAcceso.encode(constants.ENCODING_FORMAT)
		self.f = Fernet(self.clave)

		self.claveAcceso = self.f.encrypt(claveEncriptada)

	def getClaveAcceso(self):
		#self.genera_clave()
		#clave = self.cargar_clave()
		#mensaje = "mensaje".encode()
		#f = Fernet(clave)
		desencriptado = self.f.decrypt(self.claveAcceso)
		return str(desencriptado.decode())

	def genera_clave(self):
	    clave = Fernet.generate_key()
	    with open("clave.key","wb") as archivo_clave:
	        archivo_clave.write(clave)


	def cargar_clave(self):
	    return open("clave.key","rb").read()



	def getClientes(self):
		return self.clientes

	def setConsumidores(self, arreglo):
		self.clientes = arreglo

	def actualizarTodosConsumidores(self):
		for i in range(0,len(self.estadoClientes)):
			self.estadoClientes[i] = False

	def agregarCliente(self, cliente):
		self.clientes.append(cliente)
		self.estadoClientes.append(False)

	def cambiarEstadoCliente(self,i):
		self.estadoClientes[i] = True

	def getEstadosClientes(self):
		return self.estadoClientes

	def setEstados(self, arreglo):
		self.estadoClientes = arreglo


	def cambiarIndiceEnvio(self):
		mensaje = self.cola.popleft()
		return mensaje

	#def getClaveAcceso(self):
	#	return self.claveAcceso

	def getId(self):
		return self.id

	def getNombre(self):
		return self.nombre

	def getCola(self):
		return self.cola

	def enviarMensaje(self, mensaje):
		if (len(self.cola) < 2):
			self.cola.append(mensaje)
			return 1
		else:
			return 0

	def conectar(self):
		self.estado = True

	def desconectar(self):
		self.estado = False

	def getEstado(self):
		return self.estado

	def getTamañoCola(self):
		return len(self.cola)

	def vaciarCola(self):
		self.cola = deque()


"""juan = Aplicacion("cesar","123",1)
#print(juan.getNombre())
juan.enviarMensaje("hola")
juan.enviarMensaje("calvo")
#print(juan.getAplicacion())
print(juan.getCola())
valor = juan.cambiarIndiceEnvio()
print(valor)
print(juan.getCola())"""


"""arreglo = [1,True]
juan = Aplicacion("cesar","123",1)

juan.agregarCliente(arreglo)

print("pasa")

print(juan.getClientes())"""
