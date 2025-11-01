# src/servidor_correo.py
from src.usuario import Usuario
import heapq # Nuevo Import

class ServidorCorreo:
    def __init__(self):
        self._usuarios = {}
        self._cola_mensajes = []

    def registrar_usuario(self, nombre, correo, contrasena):
        if correo in self._usuarios:
            print("Error: Ya existe un usuario con este correo.")
            return None
        
        nuevo_usuario = Usuario(nombre, correo, contrasena)
        self._usuarios[correo] = nuevo_usuario
        print(f"Usuario '{nombre}' registrado con éxito.")
        return nuevo_usuario

    def recibir_mensaje_entrante(self, mensaje):
        """Añade el mensaje a la cola de prioridad."""
        # Almacenamos (prioridad, ID, mensaje) para que heapq ordene por prioridad, 
        # y use el ID como desempate (para la estabilidad).
        heapq.heappush(self._cola_mensajes, (mensaje.prioridad, mensaje.id, mensaje)) 
        print(f"Mensaje ID {mensaje.id} de {mensaje.remitente} recibido en el servidor (Prioridad: {mensaje.prioridad}).")

    def procesar_mensajes(self):
        """Procesa mensajes de la cola, priorizando los de menor valor (urgentes)."""
        while self._cola_mensajes:
            # Se extrae el mensaje de mayor prioridad (menor valor numérico)
            prioridad, _, mensaje = heapq.heappop(self._cola_mensajes)
            
            destinatario_obj = self._usuarios.get(mensaje.destinatario)
            
            if destinatario_obj:
                destinatario_obj.recibir(mensaje)
            else:
                print(f"Error: El destinatario '{mensaje.destinatario}' no existe en este servidor.")