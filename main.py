# main.py
from src.servidor_correo import ServidorCorreo
from src.utilidades import IDGenerator
from src.red_servidores import RedServidores 

if __name__ == "__main__":
    # Reseteamos el generador de IDs para asegurar que cada corrida sea reproducible
    IDGenerator._current_id = 0
    
    # 1. Configuración de la Red de Servidores
    print("--- 1. Configuración de la Red y Servidores ---")
    
    red_global = RedServidores()
    
    # Creamos TRES servidores para hacer el grafo mejor
    servidor_a = ServidorCorreo("Servidor_A") 
    servidor_b = ServidorCorreo("Servidor_B") 
    servidor_c = ServidorCorreo("Servidor_C") # Nuevo servidor
    
    red_global.agregar_servidor("Servidor_A", servidor_a)
    red_global.agregar_servidor("Servidor_B", servidor_b)
    red_global.agregar_servidor("Servidor_C", servidor_c)
    
    # Topología del Grafo: A <-> B, A <-> C, C <-> B (Ruta A->B puede ser A-B o A-C-B)
    red_global.conectar_servidores("Servidor_A", "Servidor_B")
    red_global.conectar_servidores("Servidor_A", "Servidor_C")
    red_global.conectar_servidores("Servidor_C", "Servidor_B")
    print("\n")


    # 2. Registrar usuarios
    print("--- 2. Registro de Usuarios ---")
    # VE se registra en el Servidor A (gmail.com)
    usuario1 = servidor_a.registrar_usuario("VE", "vianquez5@gmail.com", "pass123")
    # RNR se registra en el Servidor B (Hmail.com)
    usuario2 = servidor_b.registrar_usuario("RNR", "rolon.rocio.natali@hmail.com", "pass456")
    # HB se registra en el Servidor A (gmail.com)
    usuario3 = servidor_a.registrar_usuario("HB", "anung.un.rama@gmail.com", "pass789")


    # 3. Creación de Carpetas Recursivas y Filtros
    print("\n--- 3. Creación de Carpetas y Filtros ---")
    if usuario1:
        # Carpetas de VE
        usuario1.crear_carpeta("Proyectos")
        usuario1.crear_carpeta("TP_Final", ruta_padre="Proyectos")
        usuario1.crear_carpeta("Urgentes_Trabajo") 
        usuario1.crear_carpeta("Archivados")
        usuario1.crear_carpeta("Recibos", ruta_padre="Archivados") 
        usuario1.crear_carpeta("Spam") # Destino para un nuevo filtro
        
        # Filtros de VE:
        usuario1.agregar_filtro("Filtro_TP_RNR", criterio="remitente", 
                                valor_buscado=usuario2.correo, ruta_destino="Proyectos/TP_Final")
        usuario1.agregar_filtro("Filtro_Urgente", criterio="asunto", 
                                valor_buscado="URGENTE", ruta_destino="Urgentes_Trabajo")
        usuario1.agregar_filtro("Filtro_Spam", criterio="asunto", 
                                valor_buscado="promo", ruta_destino="Spam") # Nuevo filtro
        
    if usuario2:
        # Más carpetas de RNR
        usuario2.crear_carpeta("Universidad")
        usuario2.crear_carpeta("Parciales", ruta_padre="Universidad")
        usuario2.crear_carpeta("Finales", ruta_padre="Universidad")
        usuario2.crear_carpeta("Bugs_Criticos")

        # Filtro para bugs urgentes
        usuario2.agregar_filtro("Filtro_Bugs", criterio="asunto", 
                                valor_buscado="BUG", ruta_destino="Bugs_Criticos")

    if usuario3:
        # Hellboy (HB) - ahora sí carpetas
        usuario3.crear_carpeta("Misiones")
        usuario3.crear_carpeta("Clases")
        usuario3.crear_carpeta("TPs", ruta_padre="Clases")
        usuario3.crear_carpeta("Investigar")
        usuario3.crear_carpeta("Spam")

        # Filtros de HB
        usuario3.agregar_filtro("Filtro_raro", criterio="asunto", valor_buscado="raro", ruta_destino="Investigar")
        usuario3.agregar_filtro("Filtro_SPAM_HB", criterio="asunto", valor_buscado="promo", ruta_destino="Spam")

    
    # 4. Envío de Mensajes (15 mensajes para testeo de Entrega3)
    print("\n--- 4. Envío de 10 Mensajes (Prioridad y Filtros en el Servidor) ---")

    if usuario1 and usuario2 and usuario3:
        # 0001 (VE -> RNR): Cross-servidor, con FILTRO de Asunto (Stremio), Urgente
        usuario1.enviar(usuario2.correo, "Error readme Stremio URGENTE", "Revisa el readme que hay un bug con el Mermaid.", red_global, es_urgente=True) 
        
        # 0002 (RNR -> VE): Cross-servidor, con FILTRO de Asunto (URGENTE)
        usuario2.enviar(usuario1.correo, "URGENTE: Falta documentación", "Falta algun video o infografia", red_global, es_urgente=False) # Prioridad 0 (Error del remitente)

        # 0003 (VE -> RNR): Cross-servidor, con FILTRO de Asunto (Python)
        usuario1.enviar(usuario2.correo, "Curso de Python avanzado", "fijate que hay una oferta por 24 horas", red_global, es_urgente=False)
        
        # 0004 (RNR -> VE): Cross-servidor, con FILTRO de Remitente (RNR)
        usuario2.enviar(usuario1.correo, "Revisa el TP de Estructuras", "lo que te dije hoy en clase.", red_global, es_urgente=False)
        
        # 0005 (HB -> VE): Mismo servidor, sin Filtro, URGENTE
        usuario3.enviar(usuario1.correo, "MAÑANA 10 AM ACORDATE EL MEET", "cargá la batería", red_global, es_urgente=True)
        
        # 0006 (VE -> RNR): Cross-servidor, con FILTRO de Asunto (Stremio), NO Urgente
        usuario1.enviar(usuario2.correo, "Configuración de Stremio para Linux", "con toda la cosa del win10 capaz nos pasamos a linux y chau", red_global, es_urgente=False)

        # 0007 (HB -> VE): Mismo servidor, con FILTRO de Asunto (PROMO)
        usuario3.enviar(usuario1.correo, "¡Ganá una promo de viajes!", "te reenvio el sorteo", red_global, es_urgente=False) # -> Spam

        # 0008 (HB -> VE): Mismo servidor, sin Filtro, URGENTE
        usuario3.enviar(usuario1.correo, "URGENTE: El deadline del TP final es el viernes", "No colguemos con la documentacion.", red_global, es_urgente=True) # -> Urgentes_Trabajo

        # 0009 (RNR -> HB): Cross-servidor, sin Filtro
        usuario2.enviar(usuario3.correo, "Consulta de la Clase 4", "Pudiste repasar recursividad? fijate q estan los videos del año pasado", red_global, es_urgente=False)

        # 0010 (VE -> RNR): Cross-servidor, con FILTRO de Asunto (Python)
        usuario1.enviar(usuario2.correo, "Trabajo en Python", "fijate que tenemos que pensar un proyecto que aplique los temas de la clase, ojala no sea servidor de correo.", red_global, es_urgente=False)

        # 0011 (RNR -> HB): cross-server, "BUG"
        usuario2.enviar(usuario3.correo, "BUG en el mermaid otra vez!", "Se rompe siempre ya ni se que pasa mejor lo hacemos con drawio", red_global, es_urgente=True)

        # 0012 (HB -> RNR):
        usuario3.enviar(usuario2.correo, "Ayuda código en estructuras", "intenté debuggear con fuyi y fuego... no funcionó.", red_global, es_urgente=False)

        # 0013 (HB -> VE): clase y TP
        usuario3.enviar(usuario1.correo, "TP de Clases — ayuda", "no entendi la correccion, vos entendiste algo?", red_global, es_urgente=False)

        # 0014 (VE -> HB):
        usuario1.enviar(usuario3.correo, "Recursividad - práctica", "no, eso no cuenta como firewall", red_global, es_urgente=False)

        # 0015 (RNR -> VE): spam para probar filtro
        usuario2.enviar(usuario1.correo, "promo notebook reacondicionada", "te reenvio esta promo q parece a buen precio para q dejes de renegar con la del gobierno", red_global, es_urgente=False)

    # 5. Procesar los mensajes en los servidores (La Cola de Prioridad actúa acá)
    print("\n--- 5. Procesando mensajes del Servidor A (Prioridad) ---")
    # Los mensajes 0002, 0004, 0005, 0007, 0008 van a VE (Servidor A)
    # El mensaje 0009 va a HB (Servidor A)
    servidor_a.procesar_mensajes() 

    print("\n--- 5. Procesando mensajes del Servidor B (Prioridad) ---")
    # Los mensajes 0001, 0003, 0006, 0010 van a RNR (Servidor B)
    servidor_b.procesar_mensajes() 
    
    # El servidor C no tiene usuarios, solo es nodo de tránsito


    # 6. Listar y verificar filtros con Emojis
    print("\n\n--- 6. Revisando Estructura de Carpetas de VE (Filtros Aplicados) ---")
    # VE: 0002(Urgentes), 0004(TP_Final), 0005(Entrada), 0007(Spam), 0008(Urgentes)
    if usuario1:
        usuario1.listar_carpetas_y_mensajes()
        
    print("\n--- 6. Revisando Estructura de Carpetas de RNR (Filtros Aplicados) ---")
    # RNR: 0001(Stremio), 0003(Cursos_Python), 0006(Stremio), 0010(Cursos_Python)
    if usuario2:
        usuario2.listar_carpetas_y_mensajes()


    # 7. Test de Corrección: Movimiento Recursivo (E2)
    print("\n--- 7. Prueba de Movimiento Recursivo (Corrección E2) ---")

    # Mover el mensaje 0005 de Entrada a la subcarpeta Archivados/Recibos
    # El mensaje 0005 ahora está en 'Entrada'.
    usuario1.mover_mensaje(id_mensaje="0005", ruta_origen="Entrada", ruta_destino="Archivados")
    
    # Intentamos moverlo de 'Archivados' a 'Recibos'. La búsqueda debe ser recursiva
    # en 'Archivados' para encontrar el 0005. (Falla, porque Archivados no tiene mensajes,
    # el mensaje está en una subcarpeta de Archivados. Corrijo: lo muevo directamente a Recibos)
    
    # Mover 0005 que ahora está en 'Archivados' a 'Archivados/Recibos'
    usuario1.mover_mensaje(id_mensaje="0005", ruta_origen="Archivados", ruta_destino="Archivados/Recibos")
    
    # Listamos para confirmar el movimiento
    print("\n--- Estructura de VE después del movimiento recursivo ---")
    if usuario1:
        usuario1.listar_carpetas_y_mensajes()


    # 8. Pruebas de Algoritmos (BFS/DFS) sobre la Red
    print("\n--- 8. Prueba de Algoritmos de Enrutamiento (BFS/DFS) ---")
    
    # 8.1. Configuración adicional para rutas alternativas (Servidor C ya está conectado)
    
    # Creamos un nuevo mensaje (0011) desde TP (Servidor A) a RNR (Servidor B)
    # 🚨 NOTA: Para esta prueba, no usamos Usuario.enviar, sino que creamos un mensaje
    # y usamos los ruteadores directamente para SIMULAR el camino que tomaría.
    
    # El IDGenerator ya está en 0011 si se enviaron 10 mensajes antes
    IDGenerator._current_id += 1 # Aseguramos un ID nuevo (ej: 0012)
    
    # Creamos el objeto Mensaje manualmente para la simulación de ruteo
    from src.mensaje import Mensaje
    mensaje_ruteo = Mensaje(
        remitente=usuario3.correo, 
        destinatario=usuario2.correo, 
        asunto="TEST: Simulación de Ruteo", 
        cuerpo="Este mensaje va por el grafo.", 
        es_urgente=False
    )
    
    # 8.2. Simulación de Ruteo Óptimo (BFS)
    print("\n- Usando BFS (Ruta más corta, ej: Servidor_A -> Servidor_B):")
    # BFS debe elegir la ruta directa (A -> B) ya que tiene 1 salto, la más corta.
    red_global.simular_envio_bfs("Servidor_A", usuario2.correo, mensaje_ruteo)

    # 8.3. Simulación de Ruteo DFS (Cualquier ruta)
    print("\n- Usando DFS (Ruta no necesariamente óptima, ej: Servidor_A -> Servidor_B):")
    # DFS podría elegir A -> C -> B (2 saltos) o A -> B (1 salto) dependiendo del set.
    red_global.simular_envio_dfs("Servidor_A", usuario2.correo, mensaje_ruteo)
    
    # 8.4. Simulación de Entrega Local (TP a VE, ambos en Servidor_A)
    IDGenerator._current_id += 1 
    mensaje_local = Mensaje(
        remitente=usuario3.correo, 
        destinatario=usuario1.correo, 
        asunto="TEST: Entrega Local", 
        cuerpo="Este mensaje no sale del servidor.", 
        es_urgente=False
    )
    print("\n- Usando BFS (Entrega Local: Servidor_A -> Servidor_A):")
    red_global.simular_envio_bfs("Servidor_A", usuario1.correo, mensaje_local)
    
    # 8.5. Procesar Mensajes de Ruteo
    print("\n--- Procesando Mensajes de Ruteo ---")
    # Servidor B procesará el mensaje 0012 (Ruteo BFS) y el 0013 (Ruteo DFS).
    # Servidor A procesará el mensaje 0014 (Entrega Local).
    servidor_b.procesar_mensajes()
    servidor_a.procesar_mensajes()