# src/mensaje.py
from src.utilidades import IDGenerator

class Mensaje:
    def __init__(self, remitente, destinatario, asunto, cuerpo, es_urgente=False):
        # Generamos un ID único para el mensaje
        self._id = IDGenerator.get_next_id()
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._cuerpo = cuerpo
        self._leido = False
        # Prioridad: -1 (Urgente/Alta) y 0 (Normal/Baja). 
        # Usamos valores negativos para que heapq (Min-Heap) priorice.
        self._prioridad = -1 if es_urgente else 0

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
    
    @property
    def prioridad(self):
        return self._prioridad

    def marcar_leido(self):
        self._leido = True

    def mostrar_resumen(self):
        estado = "✅ Leído" if self._leido else "📧 No leído"
        prioridad_tag = "🔺 URGENTE" if self._prioridad == -1 else ""
        # Incluimos el ID para testeo y uso en las operaciones
        print(f"    [{self.id}] [{estado}] {prioridad_tag} De: {self.remitente} - Asunto: {self.asunto}")