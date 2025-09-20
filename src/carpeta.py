from src.interfaces import IListable

class Carpeta(IListable):
    def __init__(self, nombre):
        self._nombre = nombre
        self._mensajes = []

    @property
    def nombre(self):
        return self._nombre

    def agregar_mensaje(self, mensaje):
        self._mensajes.append(mensaje)

    def listar(self):
        print(f"Contenido de la Carpeta '{self.nombre}':")
        for mensaje in self._mensajes:
            mensaje.mostrar_resumen()