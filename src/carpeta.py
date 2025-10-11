# src/carpeta.py
from src.interfaces import IListable

class Carpeta(IListable):
    """
    Representa un nodo en el árbol general de carpetas.
    Ahora contiene mensajes Y referencias a sus subcarpetas (recursividad).
    """
    def __init__(self, nombre):
        self._nombre = nombre
        self._mensajes = []
        # El conjunto de subcarpetas es la clave de la recursividad (árbol general)
        self._subcarpetas = {}

    @property
    def nombre(self):
        return self._nombre

    @property
    def subcarpetas(self):
        """Permite acceder al diccionario de subcarpetas."""
        return self._subcarpetas

    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje directamente a esta carpeta (nodo)."""
        self._mensajes.append(mensaje)
        
    def eliminar_mensaje_por_id(self, id_mensaje):
        """
        Busca y elimina un mensaje de la colección de mensajes de esta carpeta.
        Se usa el ID para evitar ambigüedades.
        """
        # Se usa una lista por comprensión para eliminar de forma segura
        mensaje_encontrado = None
        
        # Iterar y buscar el mensaje por ID (string)
        for i, mensaje in enumerate(self._mensajes):
            if mensaje.id == id_mensaje:
                mensaje_encontrado = self._mensajes.pop(i)
                break
        
        return mensaje_encontrado

    # --- Métodos del Árbol General ---

    def agregar_subcarpeta(self, carpeta_hija):
        """Añade una subcarpeta (nodo hijo) a este nodo."""
        if carpeta_hija.nombre in self._subcarpetas:
            raise ValueError(f"Ya existe la subcarpeta '{carpeta_hija.nombre}' en '{self.nombre}'.")
        self._subcarpetas[carpeta_hija.nombre] = carpeta_hija

    def obtener_subcarpeta(self, nombre_subcarpeta):
        """Devuelve un objeto Carpeta hijo por su nombre."""
        return self._subcarpetas.get(nombre_subcarpeta)

    def resolver_ruta(self, ruta_relativa):
        """
        Navega recursivamente por el árbol para encontrar la carpeta destino
        dada una ruta relativa (ej. "Personal/Recibos").
        
        El usuario nos indicó que usaremos rutas absolutas, la implementación 
        siempre comenzará desde la Raíz (Usuario) y usará esta función con 
        la ruta que le quede a partir de allí.
        """
        # Limpiamos la ruta para obtener los nombres de las carpetas
        nombres_carpetas = [n for n in ruta_relativa.split('/') if n]
        
        if not nombres_carpetas:
            # Si la ruta es vacía, devolvemos la carpeta actual
            return self

        carpeta_actual = self
        for nombre in nombres_carpetas:
            siguiente_carpeta = carpeta_actual.obtener_subcarpeta(nombre)
            if not siguiente_carpeta:
                return None  # No se encontró la carpeta en la ruta
            carpeta_actual = siguiente_carpeta
            
        return carpeta_actual


    # --- Operación Clave: Búsqueda Recursiva (DFS) ---

    def buscar_mensajes(self, criterio, valor_buscado):
        """
        Implementa Búsqueda en Profundidad (DFS) para buscar mensajes de forma recursiva.
        
        Recorre todos los mensajes de esta carpeta y luego llama recursivamente 
        a la búsqueda en sus subcarpetas (O(N+M) en el peor caso).
        """
        resultados = []
        valor_buscado_lower = valor_buscado.lower() # Para búsqueda case-insensitive

        # 1. Procesar los mensajes de la carpeta actual (Nodo)
        for mensaje in self._mensajes:
            # Evaluamos el criterio de búsqueda (asunto o remitente)
            if criterio == 'asunto':
                campo_a_evaluar = mensaje.asunto
            elif criterio == 'remitente':
                campo_a_evaluar = mensaje.remitente
            else:
                # Caso no contemplado, se devuelve una lista vacía
                print(f"Advertencia: Criterio de búsqueda '{criterio}' no soportado.")
                return []
            
            # Búsqueda Parcial y Case-Insensitive (decisión acordada)
            if valor_buscado_lower in campo_a_evaluar.lower():
                resultados.append(mensaje)

        # 2. Llamada Recursiva para las Subcarpetas (Nodos Hijos)
        for subcarpeta in self._subcarpetas.values():
            # Extendemos la lista de resultados con los resultados de la subcarpeta
            resultados.extend(subcarpeta.buscar_mensajes(criterio, valor_buscado))
            
        return resultados


    # --- Implementación de IListable ---

    def listar(self, nivel=0):
        """
        Muestra la estructura recursiva de carpetas y sus mensajes.
        Se usa para visualizar el árbol (DFS).
        """
        indentacion = "  " * nivel
        print(f"{indentacion}📂 {self.nombre} ({len(self._mensajes)} mensajes):")
        
        # Muestra los mensajes de esta carpeta
        for mensaje in self._mensajes:
            mensaje.mostrar_resumen()

        # Llamada recursiva a las subcarpetas
        for subcarpeta in self._subcarpetas.values():
            subcarpeta.listar(nivel + 1) # Aumentamos el nivel de indentación