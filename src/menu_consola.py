import os

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
        usuarios_disponibles = []
        
        for nombre_srv, servidor in self.red._nodos.items():
            for correo, usuario in servidor._usuarios.items():
                usuarios_disponibles.append((usuario, nombre_srv))

        if not usuarios_disponibles:
            print("❌ No hay usuarios registrados en la red.")
            exit()

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
        print("4. ⚙️  Configurar Filtros")
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
        print("\n--- 📤 Nuevo Mensaje ---")
        
        # 1. SELECCIÓN DE DESTINATARIO (Lista cerrada)
        destinatario_correo = self._seleccionar_destinatario_de_red()
        if not destinatario_correo:
            return # El usuario canceló

        asunto = input("Asunto: ")
        cuerpo = input("Cuerpo del mensaje: ")
        
        # Validación simple de S/N
        while True:
            es_urgente_str = input("¿Es Urgente? (s/n): ").lower()
            if es_urgente_str in ['s', 'n']:
                es_urgente = (es_urgente_str == 's')
                break
            print("Por favor, respondé 's' o 'n'.")

        # Ejecución
        try:
            # Usamos el método enviar del usuario
            self.usuario_actual.enviar(destinatario_correo, asunto, cuerpo, self.red, es_urgente)
            print(f"✅ Mensaje despachado a la red hacia '{destinatario_correo}'.")
            print("ℹ️  Nota: El mensaje llegará cuando el servidor procese los envíos (Menú 6).")
        except Exception as e:
            print(f"❌ Error inesperado al enviar: {e}")
        
        self.pausa()

    def _opcion_ver_todo(self):
        self.usuario_actual.listar_carpetas_y_mensajes()
        self.pausa()

    def _opcion_gestionar_carpetas(self):
        print("\n--- 📂 Gestión de Carpetas ---")
        print("1. Crear Carpeta")
        print("2. Mover Mensaje")
        print("0. Volver")
        sub_op = input("Opción: ")
        
        if sub_op == "1":
            self._sub_crear_carpeta()
        elif sub_op == "2":
            self._sub_mover_mensaje()
        elif sub_op == "0":
            return
        else:
            print("Opción inválida.")
            self.pausa()

    def _opcion_filtros(self):
        print("\n--- ⚙️ Configurar Filtro Automático ---")
        nombre = input("Nombre del filtro: ")
        criterio = input("Criterio (asunto/remitente): ")
        valor = input(f"Valor a buscar en {criterio}: ")
        
        print("\nA qué carpeta mover los mensajes que coincidan?")
        ruta_destino = self._seleccionar_carpeta_del_usuario(titulo="Seleccioná carpeta destino:")
        
        if ruta_destino:
            self.usuario_actual.agregar_filtro(nombre, criterio, valor, ruta_destino)
        else:
            print("Cancelado. No se creó el filtro.")
            
        self.pausa()

    def _opcion_ver_urgentes(self):
        print("\n--- 🚨 Mensajes URGENTES en tu buzón ---")
        urgentes = self.usuario_actual.obtener_mensajes_urgentes()
        if urgentes:
            for m in urgentes:
                m.mostrar_resumen()
        else:
            print("Tranqui, no tenés nada urgente pendiente.")
        self.pausa()

    # --- SUB-RUTINAS DE GESTIÓN ---

    def _sub_crear_carpeta(self):
        print("\n--- Crear Nueva Carpeta ---")
        nombre = input("Nombre de la nueva carpeta: ")
        
        print("\n¿Dónde querés crearla?")
        # Reutilizamos el selector de carpetas para elegir el padre
        ruta_padre = self._seleccionar_carpeta_del_usuario(titulo="Seleccioná la carpeta PADRE (Opción 1 para Raíz):", permitir_raiz=True)
        
        if ruta_padre is None: 
            return # Cancelado
            
        # Si eligió Raíz (""), ruta_padre ya viene como ""
        self.usuario_actual.crear_carpeta(nombre, ruta_padre)
        self.pausa()

    def _sub_mover_mensaje(self):
        print("\n--- ↪ Mover Mensaje ---")
        id_msg = input("Ingresá el ID del mensaje (4 dígitos): ")
        
        # 1. BÚSQUEDA AUTOMÁTICA (Requiere método buscar_ubicacion_mensaje en Usuario)
        mensaje, ruta_origen = self.usuario_actual.buscar_ubicacion_mensaje(id_msg)
        
        if not mensaje:
            print(f"❌ No se encontró ningún mensaje con ID '{id_msg}' en tus carpetas.")
            self.pausa()
            return

        # 2. CONFIRMACIÓN VISUAL
        print(f"\n🔎 Mensaje encontrado en: '{ruta_origen}'")
        print(f"   Asunto: {mensaje.asunto}")
        print(f"   De: {mensaje.remitente}")
        
        confirmar = input("¿Es este el mensaje que querés mover? (s/n): ").lower()
        if confirmar != 's': # Corrección de variable local
            print("Operación cancelada.")
            self.pausa()
            return

        # 3. SELECCIÓN DE DESTINO
        print("\nA dónde lo querés mover?")
        ruta_destino = self._seleccionar_carpeta_del_usuario(titulo="Elegí la carpeta DESTINO:")
        
        if not ruta_destino:
            print("Operación cancelada.")
            self.pausa()
            return
            
        if ruta_destino == ruta_origen:
            print("⚠️ El mensaje ya está en esa carpeta.")
            self.pausa()
            return

        # 4. EJECUCIÓN
        self.usuario_actual.mover_mensaje(id_msg, ruta_origen, ruta_destino)
        self.pausa()

    # --- HELPERS DE INTERFAZ (Listados inteligentes) ---

    def _seleccionar_destinatario_de_red(self):
        """
        Muestra todos los usuarios de la red y permite elegir uno con un número.
        Devuelve el string del correo o None si cancela.
        """
        print("\n--- Seleccionar Destinatario ---")
        # Recolectamos usuarios: lista de (nombre, correo)
        opciones = []
        for servidor in self.red._nodos.values():
            for usuario in servidor._usuarios.values():
                # No mostramos al usuario actual (no auto-envío por UI)
                if usuario.correo != self.usuario_actual.correo:
                    opciones.append((usuario.nombre, usuario.correo))
        
        if not opciones:
            print("❌ No hay otros usuarios en la red.")
            return None

        for i, (nombre, correo) in enumerate(opciones, 1):
            print(f"{i}. {nombre} <{correo}>")
        print("0. Cancelar")

        while True:
            sel = input("Opción: ")
            if sel == "0": return None
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(opciones):
                    return opciones[idx][1] # Retornamos el correo
                print("Número fuera de rango.")
            except ValueError:
                print("Ingresá un número válido.")

    def _seleccionar_carpeta_del_usuario(self, titulo="Seleccioná una carpeta:", permitir_raiz=False):
        """
        Recorre recursivamente las carpetas del usuario y las muestra en una lista plana.
        Devuelve el string de la RUTA (ej: "Archivados/Recibos").
        """
        print(f"\n{titulo}")
        rutas_disponibles = []

        # Función auxiliar para aplanar el árbol
        def _recolectar_rutas(carpeta, ruta_actual):
            # Si no es la carpeta raíz interna "RAIZ_USUARIO", la agregamos
            if carpeta.nombre != "RAIZ_USUARIO":
                rutas_disponibles.append(ruta_actual)
            
            for nombre_sub, obj_sub in carpeta.subcarpetas.items():
                nueva_ruta = f"{ruta_actual}/{nombre_sub}" if ruta_actual else nombre_sub
                _recolectar_rutas(obj_sub, nueva_ruta)

        # Llenamos la lista iterando hijos directos de la raiz del usuario
        for nombre, obj in self.usuario_actual._raiz_de_carpetas.subcarpetas.items():
            _recolectar_rutas(obj, nombre)
        
        rutas_disponibles.sort() # Orden alfabético

        # Mostrar opciones
        if permitir_raiz:
            print("1. [RAÍZ / CARPETAS PRINCIPALES]") # Opción especial
            
        offset = 2 if permitir_raiz else 1
        
        for i, ruta in enumerate(rutas_disponibles):
            print(f"{i + offset}. 📂 {ruta}")
        
        print("0. Cancelar")

        # Selección
        while True:
            sel = input("Opción: ")
            if sel == "0": return None
            
            try:
                sel_int = int(sel)
                
                # Caso especial Raiz
                if permitir_raiz and sel_int == 1:
                    return "" # Ruta vacía = Raíz
                
                idx = sel_int - offset
                if 0 <= idx < len(rutas_disponibles):
                    return rutas_disponibles[idx]
                print("Número fuera de rango.")
            except ValueError:
                print("Ingresá un número válido.")

    # --- ADMINISTRACIÓN DE RED ---

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
                print("\n✅ Todos los servidores han procesado su tráfico.")
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