# src/mensaje.py
from src.utilidades import IDGenerator

class Mensaje:
    def __init__(self, remitente, destinatario, asunto, cuerpo):
        # Generamos un ID único para el mensaje
        self._id = IDGenerator.get_next_id()
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._cuerpo = cuerpo
        self._leido = False

    @property
    def id(self):
        return self._id

    @property
    def remitente(self):
        return self._remitente

    @property
    def destinatario(self):
        return self._destinatario

    @property
    def asunto(self):
        return self._asunto

    def marcar_leido(self):
        self._leido = True

    def mostrar_resumen(self):
        estado = "Leído" if self._leido else "No leído"
        # Incluimos el ID para testeo y uso en las operaciones
        print(f"    [{self.id}] [{estado}] De: {self.remitente} - Asunto: {self.asunto}")