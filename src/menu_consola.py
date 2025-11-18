import os
from src.mensaje import Mensaje

class MenuConsola:
    def __init__(self, red_servidores):
        self.red = red_servidores
        self.usuario_actual = None

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pausa(self):
        input("\nPresioná ENTER para continuar...")

    def iniciar(self):
        """Ciclo principal del programa."""
        while True:
            self.limpiar_pantalla()
            if not self.usuario_actual:
                self._menu_login()
            else:
                self._menu_principal_usuario()

    # --- GESTIÓN DE SESIÓN (LOGIN) ---
    
    def _menu_login(self):
        print("=== BIENVENIDO AL SISTEMA DE CORREO ===")
        print("Seleccioná un usuario para iniciar sesión:")
        
        # Recolectamos todos los usuarios de todos los servidores
        # Estructura auxiliar: lista de tuplas (usuario_obj, nombre_servidor)
        usuarios_disponibles = []
        
        # Accedemos a los nodos protegidos (permitido por ser capa de integración)
        for nombre_srv, servidor in self.red._nodos.items():
            for correo, usuario in servidor._usuarios.items():
                usuarios_disponibles.append((usuario, nombre_srv))

        if not usuarios_disponibles:
            print("❌ No hay usuarios registrados en la red.")
            return

        for i, (user, srv) in enumerate(usuarios_disponibles, 1):
            print(f"{i}. {user.nombre} <{user.correo}> (en {srv})")
        
        print("0. Salir del programa")

        opcion = input("\nOpción: ")
        
        if opcion == "0":
            print("Gracias vuelva prontos 👋")
            exit()
        
        try:
            idx = int(opcion) - 1
            if 0 <= idx < len(usuarios_disponibles):
                self.usuario_actual, _ = usuarios_disponibles[idx]
                print(f"\n✅ Iniciaste sesión como: {self.usuario_actual.nombre}")
            else:
                print("❌ Opción inválida.")
                self.pausa()
        except ValueError:
            print("❌ Tenés que ingresar un número.")
            self.pausa()

    # --- MENÚ PRINCIPAL ---

    def _menu_principal_usuario(self):
        print(f"\n=== PANEL DE USUARIO: {self.usuario_actual.nombre} ({self.usuario_actual.correo}) ===")
        print("1. 📤 Enviar Mensaje")
        print("2. 📥 Ver Bandeja de Entrada (y todas las carpetas)")
        print("3. 📂 Gestionar Carpetas (Crear/Mover)")
        print("4. ⚙️ Configurar Filtros")
        print("5. 🚨 Ver Mensajes Urgentes")
        print("6. 🌐 Administrar Red (Simulación de Servidores)")
        print("0. 🔙 Cerrar Sesión")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            self._opcion_enviar_mensaje()
        elif opcion == "2":
            self._opcion_ver_todo()
        elif opcion == "3":
            self._opcion_gestionar_carpetas()
        elif opcion == "4":
            self._opcion_filtros()
        elif opcion == "5":
            self._opcion_ver_urgentes()
        elif opcion == "6":
            self._menu_admin_red()
        elif opcion == "0":
            self.usuario_actual = None
        else:
            print("Opción no válida.")
            self.pausa()

    # --- FUNCIONALIDADES ---

    def _opcion_enviar_mensaje(self):
        print("\n--- Nuevo Mensaje ---")
        destinatario = input("Destinatario (correo): ")
        asunto = input("Asunto: ")
        cuerpo = input("Cuerpo del mensaje: ")
        es_urgente_str = input("¿Es Urgente? (s/n): ").lower()
        es_urgente = es_urgente_str == 's'

        # Usamos el método enviar del usuario
        # NOTA: Esto solo lo pone en 'Enviados' y simula el envío en la red.
        # El destinatario NO lo recibe hasta que se procesen los servidores (Opción 6).
        self.usuario_actual.enviar(destinatario, asunto, cuerpo, self.red, es_urgente)
        print("✅ Mensaje despachado a la red (recordá procesar los servidores en el menú 6).")
        self.pausa()

    def _opcion_ver_todo(self):
        self.usuario_actual.listar_carpetas_y_mensajes()
        self.pausa()

    def _opcion_gestionar_carpetas(self):
        print("\n--- Gestión de Carpetas ---")
        print("1. Crear Carpeta")
        print("2. Mover Mensaje")
        sub_op = input("Opción: ")
        
        if sub_op == "1":
            nombre = input("Nombre de nueva carpeta: ")
            padre = input("Ruta padre (dejá vacío para Raíz): ")
            self.usuario_actual.crear_carpeta(nombre, padre)
        elif sub_op == "2":
            id_msg = input("ID del mensaje a mover: ")
            origen = input("Carpeta Origen (Ruta): ")
            destino = input("Carpeta Destino (Ruta): ")
            self.usuario_actual.mover_mensaje(id_msg, origen, destino)
        
        self.pausa()

    def _opcion_filtros(self):
        print("\n--- Configurar Filtro Automático ---")
        nombre = input("Nombre del filtro: ")
        criterio = input("Criterio (asunto/remitente): ")
        valor = input(f"Valor a buscar en {criterio}: ")
        destino = input("Carpeta destino (Ruta existente): ")
        
        self.usuario_actual.agregar_filtro(nombre, criterio, valor, destino)
        self.pausa()

    def _opcion_ver_urgentes(self):
        print("\n--- 🚨 Mensajes URGENTES en tu buzón ---")
        urgentes = self.usuario_actual.obtener_mensajes_urgentes()
        if urgentes:
            for m in urgentes:
                m.mostrar_resumen()
        else:
            print("No tenés nada urgente pendiente :)")
        self.pausa()

    # --- ADMINISTRACIÓN DE RED (TRIGGER MANUAL) ---

    def _menu_admin_red(self):
        while True:
            self.limpiar_pantalla()
            print("--- 🌐 PANEL DE CONTROL DE SERVIDORES (Simulación) ---")
            print("Acá forzamos el paso del tiempo. Los mensajes viajan cuando procesás.")
            
            servidores = list(self.red._nodos.values())
            for i, srv in enumerate(servidores, 1):
                # Mostramos cuántos mensajes tiene en cola esperando
                n_pendientes = len(srv._cola_mensajes)
                print(f"{i}. Procesar mensajes en {srv.nombre} (Pendientes: {n_pendientes})")
            
            print("9. Procesar TODOS los servidores")
            print("0. Volver al menú de usuario")
            
            op = input("\nOpción: ")
            
            if op == "0":
                break
            elif op == "9":
                for srv in servidores:
                    srv.procesar_mensajes()
                print("\n✅ Todos los servidores procesaron su tráfico.")
                self.pausa()
            else:
                try:
                    idx = int(op) - 1
                    if 0 <= idx < len(servidores):
                        servidores[idx].procesar_mensajes()
                        self.pausa()
                    else:
                        print("Servidor no válido.")
                except ValueError:
                    pass