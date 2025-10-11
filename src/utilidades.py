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