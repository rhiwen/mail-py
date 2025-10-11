# src/usuario.py
from src.interfaces import IEnviable, IRecibible
from src.carpeta import Carpeta
from src.mensaje import Mensaje

class Usuario(IEnviable, IRecibible):
    def __init__(self, nombre, correo, contrasena):
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena
        
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
    
    def enviar(self, destinatario, asunto, cuerpo, servidor):
        mensaje = Mensaje(self.correo, destinatario, asunto, cuerpo)
        servidor.recibir_mensaje_entrante(mensaje)
        self._bandeja_enviados.agregar_mensaje(mensaje)

    def recibir(self, mensaje):
        print(f"[{self.nombre}] --> 📩 Tenés un mensaje nuevo.")
        # Los mensajes entrantes siempre van a la Bandeja de Entrada
        self._bandeja_entrada.agregar_mensaje(mensaje)

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
        Usamos el ID del mensaje y las rutas completas
        para evitar ambigüedades.
        """
        carpeta_origen = self._resolver_ruta_carpeta(ruta_origen)
        carpeta_destino = self._resolver_ruta_carpeta(ruta_destino)
        
        if not carpeta_origen:
            print(f"❌ Error: Carpeta de origen '{ruta_origen}' no encontrada.")
            return

        if not carpeta_destino:
            print(f"❌ Error: Carpeta de destino '{ruta_destino}' no encontrada.")
            return

        # 1. Extracción: Eliminar el mensaje de la carpeta origen
        mensaje = carpeta_origen.eliminar_mensaje_por_id(id_mensaje)
        
        if mensaje:
            # 2. Inserción: Agregar el mensaje a la carpeta destino
            carpeta_destino.agregar_mensaje(mensaje)
            print(f"↪ Mensaje ID {id_mensaje} movido de '{ruta_origen}' a '{ruta_destino}'.")
        else:
            print(f"❌ Error: No se encontró un mensaje con ID {id_mensaje} en '{ruta_origen}'.")


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