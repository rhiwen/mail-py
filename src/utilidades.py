# src/utilidades.py
# Generador de IDs secuenciales de 4 cifras para los Mensajes.
# Elegimos un contador simple ya que UUIDs son complejos y excesivos
# para un proyecto de este tamaño.

class IDGenerator:
    """Clase simple para generar IDs secuenciales."""
    _current_id = 0

    @classmethod
    def get_next_id(cls):
        """
        Devuelve el siguiente ID secuencial de 4 cifras.
        Se usa un contador simple para asegurar que cada Mensaje tenga una 
        identificación única y no ambigua.
        """
        cls._current_id += 1
        # Limitamos a 4 cifras, aunque Python maneja números grandes. 
        # Es solo una convención para el ejercicio. KISS!
        return f"{cls._current_id:04d}"

# Reiniciamos el contador cada vez que se carga el módulo si fuera necesario

class ReglaFiltro:
    """
    Modelado simple de una regla de filtro (Opción A).
    Condición: Criterio/Valor (ej: Asunto='Promo')
    Acción: Ruta de destino.
    """
    def __init__(self, nombre, criterio, valor_buscado, ruta_destino):
        self._nombre = nombre
        self._criterio = criterio.lower() # 'asunto' o 'remitente'
        self._valor_buscado = valor_buscado.lower()
        self._ruta_destino = ruta_destino

    @property
    def ruta_destino(self):
        return self._ruta_destino

    def evaluar(self, mensaje):
        """Evalúa si el mensaje cumple la regla (búsqueda parcial)."""
        if self._criterio == 'asunto':
            campo_a_evaluar = mensaje.asunto
        elif self._criterio == 'remitente':
            campo_a_evaluar = mensaje.remitente
        else:
            return False

        # Búsqueda parcial y case-insensitive
        return self._valor_buscado in campo_a_evaluar.lower()