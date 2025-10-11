# main.py
from src.servidor_correo import ServidorCorreo
from src.utilidades import IDGenerator

if __name__ == "__main__":
    # Reseteamos el generador de IDs para asegurar que cada corrida sea reproducible
    IDGenerator._current_id = 0 
    servidor = ServidorCorreo()

    # 1. Registrar usuarios
    print("--- 1. Registro de Usuarios ---")
    # VE: Viviana Enriquez (vianquez5@gmail.com)
    usuario1 = servidor.registrar_usuario("VE", "vianquez5@gmail.com", "pass123")
    # RNR: Rocio Natali Rolon (rolon.rocio.natali@gmail.com)
    usuario2 = servidor.registrar_usuario("RNR", "rolon.rocio.natali@gmail.com", "pass456")

    # 2. Creación de Carpetas Recursivas para los dos usuarios
    print("\n--- 2. Creación de Carpetas Recursivas ---")
    if usuario1:
        # Carpetas de VE
        usuario1.crear_carpeta("Proyectos")
        usuario1.crear_carpeta("TP_Final", ruta_padre="Proyectos")
        usuario1.crear_carpeta("Python_Clase_4", ruta_padre="Proyectos")
        usuario1.crear_carpeta("Parciales")
        usuario1.crear_carpeta("Mails_viejos", ruta_padre="Entrada") # Subcarpeta de Entrada
        
    if usuario2:
        # Carpetas de RNR
        usuario2.crear_carpeta("Colabs")
        usuario2.crear_carpeta("Stremio", ruta_padre="Colabs")
        usuario2.crear_carpeta("Matematica")


    # 3. Envío de 10 Mensajes (se crean IDs secuenciales 0001 a 0010)
    print("\n--- 3. Envío de 10 Mensajes y Asignación de IDs ---")
    if usuario1 and usuario2:
        # Mensaje 0001 (VE -> RNR): Importante, de Stremio
        usuario1.enviar(usuario2.correo, "Error en settings de Stremio", "Revisa el readme que hay un bug con el UML de mermaid.", servidor)
        # Mensaje 0002 (RNR -> VE): Confirmación
        usuario2.enviar(usuario1.correo, "Te confirmo el meet de mañana", "Nos vemos 10 AM para repasar el TP de estructuras.", servidor)
        # Mensaje 0003 (VE -> RNR): Parcial
        usuario1.enviar(usuario2.correo, "Duda Parcial Estructuras", "No me queda claro el análisis de O(N^2).", servidor)
        # Mensaje 0004 (RNR -> VE): Proyecto
        usuario2.enviar(usuario1.correo, "Repositorio listo: TP Final", "Ya creé el repo en github fijate de aceptar el permiso como colaborador.", servidor)
        # Mensaje 0005 (VE -> RNR): Recordatorio
        usuario1.enviar(usuario2.correo, "Acordate de subir la Clase 4", "Necesito repasar la parte de recursividad en Python voy a llorar", servidor)
        # Mensaje 0006 (RNR -> VE): Sobre un lab
        usuario2.enviar(usuario1.correo, "Pregunta sobre el Colab de POO", "Pudiste revisar el punto 3? Para mi entendimos mal", servidor)
        # Mensaje 0007 (VE -> RNR): Otro mensaje importante de Stremio
        usuario1.enviar(usuario2.correo, "Configuración de Stremio", "Mirá este tutorial para usar pandas y hacer los graficos con df al toque esta genial.", servidor)
        # Mensaje 0008 (RNR -> VE): Otra confirmación
        usuario2.enviar(usuario1.correo, "MAÑANA 10 AM ACORDATE EL MEET", "Cargá la batería porq si te quedás sin luz fuimos.", servidor)
        # Mensaje 0009 (VE -> RNR): Spam o algo viejo
        usuario1.enviar(usuario2.correo, "Promo del cybermonday", "Promociones sobre cosas que estuviste googleando el otro dia!", servidor)
        # Mensaje 0010 (RNR -> VE): Proyecto Final
        usuario2.enviar(usuario1.correo, "El deadline del TP final es el viernes", "No nos colguemos con los tests unitarios.", servidor)


    # 4. Procesar los mensajes en el servidor (Distribuye los mensajes en las bandejas de entrada)
    print("\n--- 4. Procesando mensajes del Servidor ---")
    servidor.procesar_mensajes()

    # 5. Movimiento de Mensajes para organizar el árbol de ambos usuarios
    print("\n--- 5. Movimiento de Mensajes para Organización ---")
    
    # VE (vianquez5) recibió: 0002, 0004, 0006, 0008, 0010. Todos están en 'Entrada'.
    # RNR (rolon.rocio.natali) recibió: 0001, 0003, 0005, 0007, 0009. Todos están en 'Entrada'.

    # MOVIMIENTOS DE VE:
    # Mover 0004 y 0010 a Proyectos/TP_Final (mensajes de proyecto final)
    usuario1.mover_mensaje(id_mensaje="0004", ruta_origen="Entrada", ruta_destino="Proyectos/TP_Final")
    usuario1.mover_mensaje(id_mensaje="0010", ruta_origen="Entrada", ruta_destino="Proyectos/TP_Final")
    # Mover 0006 a Proyectos/Python_Clase_4 (mensaje de un lab de POO)
    usuario1.mover_mensaje(id_mensaje="0006", ruta_origen="Entrada", ruta_destino="Proyectos/Python_Clase_4")
    # Mover 0009 a Mails_viejos (mensaje de spam)
    usuario1.mover_mensaje(id_mensaje="0009", ruta_origen="Entrada", ruta_destino="Entrada/Mails_viejos") # Error: 0009 no está en VE, está en RNR!

    # Corregimos el error anterior: Movemos el 0002 (meet de mañana) a Proyectos
    usuario1.mover_mensaje(id_mensaje="0002", ruta_origen="Entrada", ruta_destino="Proyectos") 

    # MOVIMIENTOS DE RNR:
    # Mover 0001 y 0007 a Colabs/Stremio (mensajes de Stremio)
    usuario2.mover_mensaje(id_mensaje="0001", ruta_origen="Entrada", ruta_destino="Colabs/Stremio")
    usuario2.mover_mensaje(id_mensaje="0007", ruta_origen="Entrada", ruta_destino="Colabs/Stremio")
    # Mover 0003 a Entrada/Mails_viejos (creamos una subcarpeta similar a la de VE para probar)
    usuario2.crear_carpeta("Mails_viejos", ruta_padre="Entrada")
    usuario2.mover_mensaje(id_mensaje="0003", ruta_origen="Entrada", ruta_destino="Entrada/Mails_viejos")


    # 6. Listar la estructura completa para ver el árbol organizado
    print("\n\n--- 6. Revisando Estructura de Carpetas de VE (Organizado) ---")
    if usuario1:
        usuario1.listar_carpetas_y_mensajes()

    print("\n\n--- 7. Revisando Estructura de Carpetas de RNR (Organizado) ---")
    if usuario2:
        usuario2.listar_carpetas_y_mensajes()


    # 8. Pruebas de Búsqueda Recursiva
    print("\n--- 8. Pruebas de Búsqueda Recursiva ---")

    # Búsqueda 1: Buscar por Asunto "TP Final" (Debería encontrar ID 0004 y 0010 en la subcarpeta Proyectos/TP_Final de VE)
    if usuario1:
        usuario1.buscar_mensajes_recursivo(criterio="asunto", valor_buscado="TP Final")
        
    # Búsqueda 2: Buscar por Remitente "vianquez5" (Debería encontrar 0001, 0003, 0005, 0007, 0009 en las carpetas de RNR)
    if usuario2:
        usuario2.buscar_mensajes_recursivo(criterio="remitente", valor_buscado="vianquez5")

    # Búsqueda 3: Buscar por Asunto "Stremio" (Debería encontrar 0001 y 0007 en la subcarpeta Colabs/Stremio de RNR)
    if usuario2:
        usuario2.buscar_mensajes_recursivo(criterio="asunto", valor_buscado="Stremio")
        
    # Búsqueda 4: Búsqueda parcial y case-insensitive: "meet" (Debería encontrar ID 0002 en Proyectos de VE, y 0008 en Entrada de VE)
    if usuario1:
        usuario1.buscar_mensajes_recursivo(criterio="asunto", valor_buscado="meet")
        
    # Búsqueda 5: Búsqueda que no encuentra nada, vade retro Laravel
    if usuario1:
        usuario1.buscar_mensajes_recursivo(criterio="asunto", valor_buscado="Laravel")