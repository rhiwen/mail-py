# src/red_servidores.py (nuevo entrega 3)

from collections import deque # Para BFS

class RedServidores:
    """
    Gestiona la red de servidores de correo como un grafo.
    Responsabilidad Única (SRP): solo maneja la topología y el enrutamiento.
    """
    def __init__(self):
        # {nombre_servidor: objeto_ServidorCorreo}
        self._nodos = {} 
        # {nombre_servidor: set_de_nombres_conectados}
        self._grafo = {} 

    def agregar_servidor(self, nombre_servidor, servidor_obj):
        """Añadir un servidor a la red."""
        if nombre_servidor not in self._nodos:
            self._nodos[nombre_servidor] = servidor_obj
            self._grafo[nombre_servidor] = set()
            print(f"🌐 Servidor '{nombre_servidor}' agregado a la red.")
        else:
            print(f"Advertencia: Servidor '{nombre_servidor}' ya existe.")

    def conectar_servidores(self, srv_a, srv_b):
        """Establecer una conexión bidireccional entre servidores."""
        if srv_a not in self._grafo or srv_b not in self._grafo:
            print("❌ Error: Uno o ambos servidores no existen.")
            return
        
        self._grafo[srv_a].add(srv_b)
        self._grafo[srv_b].add(srv_a)
        print(f"Conexión establecida: {srv_a} <-> {srv_b}")

    # --- Algoritmos de Búsqueda de Rutas (Enrutamiento) ---

    def buscar_ruta_bfs(self, origen, destino):
        """
        Buscar la ruta MAS CORTA entre dos servidores usando BFS.
        Retornar la lista de servidores en el camino o None.
        """
        if origen not in self._grafo or destino not in self._grafo or origen == destino:
            return None # O se retorna [origen] si origen == destino. Dejamos None para enrutamiento.

        cola = deque([origen])
        padres = {origen: None}
        visitados = {origen}

        while cola:
            actual = cola.popleft()
            
            if actual == destino:
                # Reconstruir la ruta
                ruta = []
                while actual is not None:
                    ruta.append(actual)
                    actual = padres.get(actual)
                return ruta[::-1] 

            for vecino in self._grafo[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    cola.append(vecino)
                    
        return None 
        
    def simular_envio_bfs(self, origen, destino, mensaje):
        """Simular el envío de un mensaje encontrando la ruta más corta (BFS)."""
        ruta = self.buscar_ruta_bfs(origen, destino)
        
        if not ruta:
            print(f"🚫 Imposible enviar ID {mensaje.id}: No hay ruta BFS entre {origen} y {destino}.")
            return

        print(f"Ruta óptima (BFS) para ID {mensaje.id}: {' -> '.join(ruta)}")
        
        # El mensaje se envía al servidor de destino para su procesamiento final
        servidor_destino_obj = self._nodos[destino]
        servidor_destino_obj.recibir_mensaje_entrante(mensaje)
        
    def simular_envio_dfs(self, origen, destino, mensaje):
        """
        Simular el envío buscando la primera ruta encontrada (DFS).
        Generalmente no es óptimo, pero cumple con la consigna de implementar DFS.
        """
        pila = [(origen, [origen])] 
        visitados = {origen}
        
        while pila:
            actual, camino = pila.pop()
            
            if actual == destino:
                print(f"Ruta encontrada (DFS) para ID {mensaje.id}: {' -> '.join(camino)}")
                servidor_destino_obj = self._nodos[destino]
                servidor_destino_obj.recibir_mensaje_entrante(mensaje)
                return
            
            for vecino in self._grafo[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = camino + [vecino]
                    pila.append((vecino, nuevo_camino))
                    
        print(f"🚫 Imposible enviar ID {mensaje.id}: No se encontró ruta (DFS) entre {origen} y {destino}.")