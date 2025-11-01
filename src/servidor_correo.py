# src/servidor_correo.py
from src.usuario import Usuario
import heapq # Nuevo Import

class ServidorCorreo:
    def __init__(self, nombre):
        self._usuarios = {}
        self._cola_mensajes = []
        self._nombre = nombre
        print(f"✅ Servidor '{self._nombre}' inicializado.")
    
    @property
    def nombre(self):
        return self._nombre

    def registrar_usuario(self, nombre, correo, contrasena):
        if correo in self._usuarios:
            print(f"❌ Error: El correo '{correo}' ya está registrado en este servidor.")
            return None
        
        # El Usuario necesita saber dónde está registrado para el enrutamiento
        nuevo_usuario = Usuario(nombre, correo, contrasena, self.nombre) 
        self._usuarios[correo] = nuevo_usuario
        print(f"👤 Usuario '{nombre}' registrado en Servidor '{self.nombre}'.")
        return nuevo_usuario

    def recibir_mensaje_entrante(self, mensaje):
        """Añade el mensaje a la cola de prioridad usando su atributo _prioridad."""
        # NOTA: Se usa el ID del mensaje como desempate si las prioridades son iguales
        heapq.heappush(self._cola_mensajes, (mensaje.prioridad, mensaje.id, mensaje)) 
        print(f"📧 Mensaje ID {mensaje.id} de {mensaje.remitente} recibido en '{self.nombre}' (Prioridad: {mensaje.prioridad}).")

    def procesar_mensajes(self):
        """Procesa mensajes de la cola, priorizando los 'urgentes' (prioridad menor)."""
        print(f"⚙️ Procesando cola de mensajes en Servidor '{self.nombre}'...")
        while self._cola_mensajes:
            prioridad, _, mensaje = heapq.heappop(self._cola_mensajes)
            
            destinatario_obj = self._usuarios.get(mensaje.destinatario)
            
            if destinatario_obj:
                destinatario_obj.recibir(mensaje)
            else:
                # Esto no debería pasar si la red funciona bien, pero porlas
                print(f"⚠️ Error: El destinatario '{mensaje.destinatario}' no está en este servidor ('{self.nombre}').")