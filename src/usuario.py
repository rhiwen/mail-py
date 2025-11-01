# src/usuario.py
from src.interfaces import IEnviable, IRecibible
from src.carpeta import Carpeta
from src.mensaje import Mensaje
from src.utilidades import ReglaFiltro # Nuevo Import

class Usuario(IEnviable, IRecibible):
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena
        # Nuevo: Diccionario de filtros automáticos
        self._filtros = {} # {nombre_filtro: ReglaFiltro}
        
        # Implementamos el Árbol General. El Usuario es el gestor de la Raíz
        # Creamos una Carpeta Raíz contenedora
        self._raiz_de_carpetas = Carpeta("RAIZ_USUARIO")
        
        # Las carpetas iniciales son subcarpetas de la Raíz
        self._bandeja_entrada = Carpeta("Entrada")
        self._bandeja_enviados = Carpeta("Enviados")
        
        # Agregamos las carpetas principales a la Raíz
        self._raiz_de_carpetas.agregar_subcarpeta(self._bandeja_entrada)
        self._raiz_de_carpetas.agregar_subcarpeta(self._bandeja_enviados)


    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo
    
    @property
    def contrasena(self):
        return self._contrasena

    # --- Métodos de Mensajería ---
    
    def enviar(self, destinatario, asunto, cuerpo, servidor, es_urgente=False):
        mensaje = Mensaje(self.correo, destinatario, asunto, cuerpo, es_urgente)
        servidor.recibir_mensaje_entrante(mensaje)
        self._bandeja_enviados.agregar_mensaje(mensaje)

    def recibir(self, mensaje):
        print(f"[{self.nombre}] --> 📩 Tenés un mensaje nuevo.")
        # 1. Intentar aplicar filtros
        fue_filtrado = self.aplicar_filtros_a_mensaje(mensaje)

        if not fue_filtrado:
            # 2. Si no fue filtrado, va a la Bandeja de Entrada por defecto
            self._bandeja_entrada.agregar_mensaje(mensaje)
            print(f"[{self.nombre}] Mensaje ID {mensaje.id} agregado a 'Entrada'.")

    # --- Métodos de Gestión del Árbol de Carpetas ---

    def _resolver_ruta_carpeta(self, ruta_relativa):
        """
        Función utilitaria para encontrar una carpeta a partir de su ruta.
        Se usa la ruta absoluta (decisión acordada) desde el nivel de las carpetas principales.
        """
        # La RAÍZ tiene el método para resolver la ruta a partir de sus hijos
        return self._raiz_de_carpetas.resolver_ruta(ruta_relativa)


    def crear_carpeta(self, nombre_nueva_carpeta, ruta_padre=""):
        """
        Crea una nueva subcarpeta dentro de la ruta padre especificada.
        Si la ruta padre es vacía, se crea directamente bajo la Raíz (junto a Entrada/Enviados).
        """
        carpeta_padre = self._raiz_de_carpetas.resolver_ruta(ruta_padre)

        if carpeta_padre:
            nueva_carpeta = Carpeta(nombre_nueva_carpeta)
            try:
                carpeta_padre.agregar_subcarpeta(nueva_carpeta)
                print(f"✅ Carpeta '{nombre_nueva_carpeta}' creada en la ruta: {ruta_padre}.")
            except ValueError as e:
                print(f"❌ Error al crear carpeta: {e}")
        else:
            print(f"❌ Error: La carpeta padre en la ruta '{ruta_padre}' no existe.")

    
    def mover_mensaje(self, id_mensaje, ruta_origen, ruta_destino):
        """
        Mover un mensaje entre carpetas.
        Busca el mensaje de forma recursiva en la ruta_origen y lo extrae.
        """
        carpeta_origen = self._resolver_ruta_carpeta(ruta_origen)
        carpeta_destino = self._resolver_ruta_carpeta(ruta_destino)
        
        if not carpeta_origen:
            print(f"❌ Error: Carpeta de origen '{ruta_origen}' no encontrada.")
            return

        if not carpeta_destino:
            print(f"❌ Error: Carpeta de destino '{ruta_destino}' no encontrada.")
            return

        # 1. Extracción RECURSIVA del mensaje de la ruta de origen (o subcarpeta)
        mensaje = carpeta_origen.extraer_mensaje_recursivo_por_id(id_mensaje)
        
        if mensaje:
            # 2. Inserción: Agregar el mensaje a la carpeta destino
            carpeta_destino.agregar_mensaje(mensaje)
            print(f"↪ Mensaje ID {id_mensaje} movido de (Búsqueda en) '{ruta_origen}' a '{ruta_destino}'.")
        else:
            print(f"❌ Error: No se encontró un mensaje con ID {id_mensaje} en el árbol de '{ruta_origen}'.")


    def buscar_mensajes_recursivo(self, criterio, valor_buscado):
        """
        Inicia la Búsqueda Recursiva desde la Raíz para encontrar mensajes 
        en cualquier parte del árbol.
        """
        # La búsqueda se delega a la Raíz, que hace el recorrido DFS
        print(f"\nBuscando '{valor_buscado}' por {criterio} en todas las carpetas...")
        resultados = self._raiz_de_carpetas.buscar_mensajes(criterio, valor_buscado)
        
        if resultados:
            print(f"--- {len(resultados)} Mensaje(s) Encontrado(s) ---")
            for mensaje in resultados:
                mensaje.mostrar_resumen()
        else:
            print("No se encontraron mensajes que coincidan con el criterio.")
            
        return resultados

    # --- Implementación de IListable ---

    def listar_carpetas_y_mensajes(self):
        """
        Muestra la estructura completa de carpetas y mensajes del usuario, 
        comenzando desde la Raíz (DFS).
        """
        print(f"--- Estructura de Correo de {self.nombre} ---")
        # Listamos solo a partir de las carpetas principales (Entrada, Enviados, etc.)
        for carpeta_principal in self._raiz_de_carpetas.subcarpetas.values():
            carpeta_principal.listar(nivel=0)
    
    # --- Métodos de Gestión de Filtros (Nuevos entrega 3) ---

    def agregar_filtro(self, nombre, criterio, valor_buscado, ruta_destino):
        """Define una nueva regla de filtrado y la almacena."""
        # Se verifica que la ruta de destino exista antes de crear la regla
        if not self._resolver_ruta_carpeta(ruta_destino):
            print(f"❌ Error: La carpeta destino '{ruta_destino}' no existe. Filtro no creado.")
            return
            
        nueva_regla = ReglaFiltro(nombre, criterio, valor_buscado, ruta_destino)
        self._filtros[nombre] = nueva_regla
        print(f"✅ Filtro '{nombre}' creado: {criterio}='{valor_buscado}' -> '{ruta_destino}'.")

    def aplicar_filtros_a_mensaje(self, mensaje):
        """Evalúa el mensaje contra todas las reglas y lo mueve si coincide."""
        for regla in self._filtros.values():
            if regla.evaluar(mensaje):
                # OBTENER LA CARPETA DESTINO
                carpeta_destino = self._resolver_ruta_carpeta(regla.ruta_destino)
                
                # El mensaje todavía no está en ninguna carpeta del usuario, 
                # simplemente lo agregamos a la carpeta de destino del filtro.
                carpeta_destino.agregar_mensaje(mensaje)
                print(f"[{self.nombre}] 🧠 Mensaje ID {mensaje.id} filtrado a '{regla.ruta_destino}'.")
                
                return True # El mensaje fue filtrado y ubicado.
                
        return False # El mensaje no coincidió con ningún filtro.