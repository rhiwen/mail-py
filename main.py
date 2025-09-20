from src.servidor_correo import ServidorCorreo

if __name__ == "__main__":
    servidor = ServidorCorreo()

    # 1. Registrar usuarios
    print("--- Registro de Usuarios ---")
    usuario1 = servidor.registrar_usuario("VE", "vianquez5@gmail.com", "pass123")
    usuario2 = servidor.registrar_usuario("RNR", "rolon.rocio.natali@gmail.com", "pass456")

    # 2. Enviar un mensaje
    print("\n--- Envío de Mensajes ---")
    if usuario1 and usuario2:
        usuario1.enviar("rolon.rocio.natali@gmail.com", "Reunion urgente!!", "Mañana a las 10", servidor)
    
    # 3. Procesar los mensajes en el servidor
    print("\n--- Procesando mensajes del Servidor ---")
    servidor.procesar_mensajes()

    # 4. Listar mensajes de los usuarios
    print("\n--- Revisando Bandejas ---")
    if usuario1:
        print(f"\n📮 {usuario1.nombre}:")
        usuario1.listar_bandeja_entrada()
    
    if usuario2:
        print(f"\n📮 {usuario2.nombre}:")
        usuario2.listar_bandeja_entrada()