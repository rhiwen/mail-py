# Documentación Técnica - Entrega Final (Integración)

## 1. Adiciones y Cambios de la Entrega 4

En esta etapa final nos enfocamos en la **orquestación** de todo el sistema. El backend ya estaba solido con las entregas anteriores (árboles, grafos, colas), pero faltaba una forma "humana" de usarlo.

### Evolución de la Interfaz (`src/menu_consola.py`)

Lo mas importante fue la creación de la clase `MenuConsola`. Al principio la idea era simple: pedir inputs de texto para todo. Pero probando el flujo nos dimos cuenta que era inusable:

-   **Problema:** Para mover un mensaje tenias que escribir la ruta exacta (ej: `Archivados/Recibos`). Si le pifiabas a una letra, el sistema tiraba error.
    
-   **Solución:** Refactorizamos para usar menús numéricos. En vez de escribir el email del destinatario o la ruta de la carpeta, el sistema te lista las opciones disponibles (tomadas de los objetos vivos en memoria) y vos elegís el índice.
    

### Ajustes en el Backend (`src/usuario.py` y `main.py`)

Para soportar esta nueva interfaz, tuvimos que tocar el modelo de `Usuario`:

-   **Búsqueda de Mensajes:** Antes solo podíamos buscar por contenido. Agregamos `buscar_ubicacion_mensaje(id)` que recorre recursivamente el árbol y te devuelve no solo el mensaje, sino en qué carpeta está. Esto es clave para la UX de "Mover mensaje", así el usuario solo mete el ID y listo.
    
-   **Bootstrapping en `main.py`:** Limpiamos todo el código de prueba sucio y lo encapsulamos en una función `inicializar_escenario_demo()`. Esto carga usuarios, servidores y mensajes "pre-enviados" para que al abrir el programa ya haya cosas para ver y tocar.

## 2. Análisis de Eficiencia y Complejidad

Como se comportan las funcionalidades principales ahora que está todo integrado.

| **Operación** 	| **Estructura** 	| **Complejidad Temporal** 	| **Análisis** 	|
|---	|---	|---	|---	|
| Enrutamiento (BFS) 	| Grafo (Red) 	| $O(V + E)$ 	| Donde V son servidores y E conexiones. Es óptimo para encontrar la ruta más corta. 	|
| Buscar Mensaje (Recursivo) 	| Árbol N-ario 	| $O(N)$ 	| Recorre todas las carpetas y subcarpetas (DFS). N es el total de carpetas+mensajes. 	|
| Procesar Cola de Mensajes 	| Min-Heap (PriorityQueue) 	| $O(\log M)$ 	| Insertar o sacar un mensaje cuesta logaritmicamente respecto a la cantidad de mensajes en cola ($M$). 	|
| Mover Mensaje 	| Árbol 	| $O(N)$ 	| Primero hace una búsqueda ($O(N)$) para encontrarlo y sacarlo, la inserción es $O(1)$ en la lista destino. 	|
| Listar Carpetas 	| Árbol 	| $O(N)$ 	| Tiene que visitar cada nodo para imprimirlo. |


----------

## 3. Diagrama de Clases (Mermaid)

Este diagrama refleja como quedó la arquitectura final con la capa de presentación (`MenuConsola`) separada del dominio.

``` mermaid
classDiagram
    class MenuConsola {
        -red: RedServidores
        -usuario_actual: Usuario
        +iniciar()
        -_seleccionar_destinatario()
        -_seleccionar_carpeta()
    }

    class RedServidores {
        -nodos: Dict
        -grafo: Dict
        +simular_envio_bfs()
        +conectar_servidores()
    }

    class ServidorCorreo {
        -nombre: str
        -cola_mensajes: Heap
        -usuarios: Dict
        +procesar_mensajes()
        +registrar_usuario()
    }

    class Usuario {
        -nombre: str
        -filtros: Dict
        -raiz_carpetas: Carpeta
        +enviar()
        +mover_mensaje()
        +buscar_ubicacion_mensaje()
    }

    class Carpeta {
        -nombre: str
        -subcarpetas: Dict
        -mensajes: List
        +agregar_mensaje()
        +extraer_mensaje_recursivo()
    }

    class Mensaje {
        -id: str
        -prioridad: int
        -asunto: str
    }

    class IEnviable { <<Interface>> }
    class IListable { <<Interface>> }

    MenuConsola --> RedServidores : usa
    RedServidores o-- ServidorCorreo : agrupa
    ServidorCorreo *-- Usuario : contiene
    Usuario *-- Carpeta : compone
    Carpeta *-- Mensaje : almacena
    Carpeta o-- Carpeta : recursividad
    Usuario ..|> IEnviable : implementa
    Carpeta ..|> IListable : implementa

```

----------

## 4. Decisiones de Diseño

| **TEMA** 	| **OPCIONES CONSIDERADAS** 	| **DECISIÓN TOMADA** 	| **JUSTIFICACIÓN** 	|
|---	|---	|---	|---	|
| Interfaz de Usuario 	| GUI (Tkinter/Qt) vs CLI (Consola) 	| CLI (Consola Interactiva) 	| Respetar principio KISS. Una GUI barata consume tiempo. Una CLI bien hecha es más coherente con el tiempo que tuvimos y la complejidad que queríamos alcanzar. 	|
| Input de Datos 	| Texto Libre vs Menú Numérico 	| Menú Numérico 	| El texto libre es propenso a errores humanos (typos). Ir a buscar y listar las opciones existentes es mas seguro y menos trabajo para el usuario. 	|
| Datos Iniciales 	| Base de datos real vs Hardcode en memoria 	| Seed Data en Memoria 	| No requerimos persistencia entre ejecuciones. Cargar un escenario predefinido al inicio permite testear rápido. 	|
| Manejo de Rutas 	| Rutas Relativas vs Rutas Absolutas 	| Rutas Absolutas simuladas 	| Para el usuario es confuso saber dónde está parado. Siempre mostramos y operamos desde la raíz del usuario para simplificar. 	|

----------

## 5. Manejo de Casos de Borde

| **CASO POTENCIAL** 	| **CLASE AFECTADA** 	| **MECANISMO DE CONTROL** 	|  	|
|---	|---	|---	|---	|
| Envío a usuario inexistente 	| MenuConsola / Usuario 	| El menú directamente no te deja escribir el correo; te obliga a elegir de una lista de usuarios validos en la red. 	|  	|
| Mover mensaje a la misma carpeta 	| Usuario 	| Chequeo previo: si ruta_origen == ruta_destino, se cancela la operación y avisa al usuario. 	|  	|
| Usuario intenta acceder a opción inválida 	| MenuConsola 	| Bloques try-except ValueError en todos los inputs numéricos para atrapar letras o enters vacíos. 	|  	|
| Mover mensaje con ID incorrecto 	| Usuario 	| El método buscar_ubicacion_mensaje retorna None si no existe, y el menú avisa "No encontrado" antes de intentar mover nada. 	|  	|
| Ruteo entre servidores desconectados 	| RedServidores 	| El algoritmo BFS retorna None si no hay camino. El sistema avisa "Imposible enviar" y no crashea. 	|  	|

----------

**Otros casos que no implementamos pero tuvimos en cuenta:**

1.  _Persistencia:_ Si cerrás el programa, perdés todo.
2.  _Concurrencia:_ El sistema es monohilo. La simulación de red es por turnos, no tiempo real.
3.  _Borrado:_ No implementamos borrar carpetas porque si tienen mensajes adentro hay que decidir si borrarlos o moverlos a la madre (complejidad innecesaria para el TP).
4.  _IDs Duplicados:_ Si reiniciás el contador `IDGenerator` manualmente sin limpiar los mensajes viejos, podría haber colisiones. En el flujo normal no pasa.
