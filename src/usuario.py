from src.interfaces import IEnviable, IRecibible
from src.carpeta import Carpeta
from src.mensaje import Mensaje

class Usuario(IEnviable, IRecibible):
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena
        self._bandeja_entrada = Carpeta("Entrada")
        self._bandeja_enviados = Carpeta("Enviados")
        self._carpetas = {"Entrada": self._bandeja_entrada, "Enviados": self._bandeja_enviados}

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo
    
    # Este setter no es ideal por motivos de seguridad, pero se incluye para cumplir con el ejercicio.
    @property
    def contrasena(self):
        return self._contrasena

    def enviar(self, destinatario, asunto, cuerpo, servidor):
        mensaje = Mensaje(self.correo, destinatario, asunto, cuerpo)
        servidor.recibir_mensaje_entrante(mensaje)
        self._bandeja_enviados.agregar_mensaje(mensaje)

    def recibir(self, mensaje):
        print(f"[{self.nombre}] Tenés un mensaje nuevo.")
        self._bandeja_entrada.agregar_mensaje(mensaje)
    
    def crear_carpeta(self, nombre_carpeta):
        if nombre_carpeta not in self._carpetas:
            self._carpetas[nombre_carpeta] = Carpeta(nombre_carpeta)
            print(f"Carpeta '{nombre_carpeta}' creada.")
        else:
            print(f"La carpeta '{nombre_carpeta}' ya existe.")
    
    def listar_bandeja_entrada(self):
        self._bandeja_entrada.listar()
