# main.py
from src.servidor_correo import ServidorCorreo
from src.utilidades import IDGenerator
from src.red_servidores import RedServidores 
from src.menu_consola import MenuConsola # Importamos la nueva UI
from src.mensaje import Mensaje

def inicializar_escenario_demo():
    """
    Configura la red, servidores, usuarios y datos de prueba iniciales.
    Devuelve el objeto red_global listo para usar.
    """
    # Reseteamos el generador de IDs
    IDGenerator._current_id = 0
    
    print("⏳ Inicializando simulación y cargando datos de prueba...")
    
    # 1. Configuración de la Red
    red_global = RedServidores()
    
    servidor_a = ServidorCorreo("Servidor_A") 
    servidor_b = ServidorCorreo("Servidor_B") 
    servidor_c = ServidorCorreo("Servidor_C")
    
    red_global.agregar_servidor("Servidor_A", servidor_a)
    red_global.agregar_servidor("Servidor_B", servidor_b)
    red_global.agregar_servidor("Servidor_C", servidor_c)
    
    red_global.conectar_servidores("Servidor_A", "Servidor_B")
    red_global.conectar_servidores("Servidor_A", "Servidor_C")
    red_global.conectar_servidores("Servidor_C", "Servidor_B")

    # 2. Registrar usuarios
    usuario1 = servidor_a.registrar_usuario("VE", "vianquez5@gmail.com", "pass123")
    usuario2 = servidor_b.registrar_usuario("RNR", "rolon.rocio.natali@hmail.com", "pass456")
    usuario3 = servidor_a.registrar_usuario("HB", "anung.un.rama@gmail.com", "pass789")

    # 3. Creación de Carpetas y Filtros (Datos precargados)
    if usuario1:
        usuario1.crear_carpeta("Proyectos")
        usuario1.crear_carpeta("TP_Final", ruta_padre="Proyectos")
        usuario1.crear_carpeta("Urgentes_Trabajo") 
        usuario1.crear_carpeta("Archivados")
        usuario1.crear_carpeta("Recibos", ruta_padre="Archivados") 
        usuario1.crear_carpeta("Spam")
        
        usuario1.agregar_filtro("Filtro_TP_RNR", "remitente", usuario2.correo, "Proyectos/TP_Final")
        usuario1.agregar_filtro("Filtro_Urgente", "asunto", "URGENTE", "Urgentes_Trabajo")
        usuario1.agregar_filtro("Filtro_Spam", "asunto", "promo", "Spam")
        
    if usuario2:
        usuario2.crear_carpeta("Universidad")
        usuario2.crear_carpeta("Parciales", ruta_padre="Universidad")
        usuario2.crear_carpeta("Finales", ruta_padre="Universidad")
        usuario2.crear_carpeta("Bugs_Criticos")
        usuario2.agregar_filtro("Filtro_Bugs", "asunto", "BUG", "Bugs_Criticos")

    if usuario3:
        usuario3.crear_carpeta("Misiones")
        usuario3.crear_carpeta("Clases")
        usuario3.crear_carpeta("TPs", ruta_padre="Clases")
        usuario3.crear_carpeta("Investigar")
        usuario3.crear_carpeta("Spam")
        usuario3.agregar_filtro("Filtro_raro", "asunto", "raro", "Investigar")
        usuario3.agregar_filtro("Filtro_SPAM_HB", "asunto", "promo", "Spam")

    # 4. Inyectar tráfico inicial (Los 15 mensajes de prueba)
    # Solo los enviamos a la red, NO los procesamos todavía para que 
    # se pueda ver en el menú de Admin como "Pendientes".
    if usuario1 and usuario2 and usuario3:
        # Rutina de envío masivo (Tu código original)
        usuario1.enviar(usuario2.correo, "Error readme Stremio URGENTE", "Revisa el readme...", red_global, es_urgente=True) 
        usuario2.enviar(usuario1.correo, "URGENTE: Falta documentación", "Falta algun video...", red_global, es_urgente=False)
        usuario1.enviar(usuario2.correo, "Curso de Python avanzado", "oferta 24hs...", red_global, es_urgente=False)
        usuario2.enviar(usuario1.correo, "Revisa el TP de Estructuras", "lo de la clase...", red_global, es_urgente=False)
        usuario3.enviar(usuario1.correo, "MAÑANA 10 AM ACORDATE EL MEET", "cargá la batería", red_global, es_urgente=True)
        usuario1.enviar(usuario2.correo, "Configuración de Stremio para Linux", "pasate a linux...", red_global, es_urgente=False)
        usuario3.enviar(usuario1.correo, "¡Ganá una promo de viajes!", "sorteo...", red_global, es_urgente=False)
        usuario3.enviar(usuario1.correo, "URGENTE: El deadline del TP final", "No colguemos...", red_global, es_urgente=True)
        usuario2.enviar(usuario3.correo, "Consulta de la Clase 4", "Recursividad...", red_global, es_urgente=False)
        usuario1.enviar(usuario2.correo, "Trabajo en Python", "proyecto nuevo...", red_global, es_urgente=False)
        usuario2.enviar(usuario3.correo, "BUG en el mermaid otra vez!", "Se rompe...", red_global, es_urgente=True)
        usuario3.enviar(usuario2.correo, "Ayuda código en estructuras", "debuggear...", red_global, es_urgente=False)
        usuario3.enviar(usuario1.correo, "TP de Clases — ayuda", "no entendi...", red_global, es_urgente=False)
        usuario1.enviar(usuario3.correo, "Recursividad - práctica", "firewall...", red_global, es_urgente=False)
        usuario2.enviar(usuario1.correo, "promo notebook reacondicionada", "precio...", red_global, es_urgente=False)

    # Procesamos ALGUNOS mensajes para que las bandejas no estén vacías al iniciar,
    # pero dejamos otros en cola para jugar con el admin.
    # Procesamos solo Servidor A (VE y HB tendrán mails). Servidor B queda pendiente.
    print("⚙️  Procesando carga inicial del Servidor A...")
    servidor_a.procesar_mensajes()
    
    print("✅ Carga de datos completa.\n")
    return red_global

if __name__ == "__main__":
    # 1. Inicializamos el "Mundo"
    red = inicializar_escenario_demo()
    
    # 2. Arrancamos la Interfaz
    app = MenuConsola(red)
    app.iniciar()