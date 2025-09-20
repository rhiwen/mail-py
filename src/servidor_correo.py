from src.usuario import Usuario

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
        self._cola_mensajes.append(mensaje)
        print(f"Mensaje de {mensaje.remitente} recibido por el servidor.")

    def procesar_mensajes(self):
        while self._cola_mensajes:
            mensaje = self._cola_mensajes.pop(0)
            destinatario_obj = self._usuarios.get(mensaje.destinatario)
            
            if destinatario_obj:
                destinatario_obj.recibir(mensaje)
            else:
                print(f"Error: El destinatario '{mensaje.destinatario}' no existe en este servidor.") 