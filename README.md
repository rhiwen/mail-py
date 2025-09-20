
# 📧 Estructuras de Datos Entrega 1: Cliente de Correo en Python (Mail-Py - Grupo 33)

## Resumen del Proyecto

Este proyecto es una implementación básica de un cliente de correo electrónico, enfocado en el diseño orientado a objetos. En esta primera etapa, se definen las clases principales (`Usuario`, `Mensaje`, `Carpeta`, `ServidorCorreo`) y se implementa su encapsulamiento y las interfaces para las operaciones básicas.

> Consigna: _Sistema orientado a objetos que modele un cliente de correo electrónico, permitiendo la gestión de usuarios, mensajes, carpetas, filtros y operaciones típicas de un entorno de email._

## Integrantes

- Viviana Enriquez: vianquez5@gmail.com / vienriquez87@gmail.com (Github: DoomMetalLady)
- Rocío N. Rolón: rolon.rocio.natali@gmail.com (Github: rhiwen)

## Estructura de Carpetas

La siguiente estructura de archivos mantiene el código organizado y modular. Cada clase principal está en su propio archivo para respetar el principio de Responsabilidad Única.

```
.
├── src/
│   ├── __init__.py
│   ├── interfaces.py
│   ├── usuario.py
│   ├── mensaje.py
│   ├── carpeta.py
│   └── servidor\_correo.py
├── main.py
├── docs/
│   └── diseno\_entrega1.md
└── README.md

````

-   `src/`: Contiene todo el código fuente del proyecto.
-   `src/interfaces.py`: Módulo para definir las interfaces (clases abstractas) del proyecto.
-   `src/usuario.py`: Clase que modela al usuario del sistema.
-   `src/mensaje.py`: Clase para representar los mensajes de correo.
-   `src/carpeta.py`: Clase que gestiona los mensajes en las carpetas.
-   `src/servidor_correo.py`: Clase que simula el servidor central.
-   `main.py`: Archivo principal para la ejecución de la aplicación, donde se interactúa con las clases y se demuestra su uso.

## Instalación y Ejecución

Para levantar el proyecto localmente:

1.  Clonar el repositorio:

    ```bash
    git clone [https://github.com/rhiwen/mail-py.git)
    cd mail-py
    ```

2.  Ejecutar el programa principal:

    ```bash
    python main.py
    ```

## Diagrama de Clases

[![](https://mermaid.ink/img/pako:eNqNVU1v2zAM_SuCTlmXBHGT1h8oeul2GNBeOuxSGAgYm03V2VJAycW2IP99smXZrtO09UU2xUc-PlLynmcqR57wrACtvwnYEpSpZPbJBWFmhJLs9j6VztZ4sV-6AhKK7Z2RsZk2xNZSlRvC17ZMEaEa26Qh0Cihs-ciM3YDaIcGdGe-cQa23oDM8RnWWCNzeM_hRUCuuhBfGwNNctRGSDA17ykDXUlj16xC2tlVI72IXNGXDmZLFxtBkxKlhmfsNzJCIM904krudwuhbYox3UnrcHgt4882602j0UBNp0blVO7VqIPX6hWwbmnpAd-t3SWbu4W11GyNTfR69aofVenDOb7S4HHZO1IZauhc9Yma7tz2eDQIS2Fs9NF0DLvyesd1aDQ3Tbc620apgq0LtBJ2NEvlRCDUlWV6gqSfmvfn18l9pLQ9IbjthTiWys3AidQ_vtfzuCkGCl1dCSsMPUKG19fjue2jDGLcN237RBA_xW9Gua15fiLIiXr8JZDyIOXsbDZr3_oKEybKXYFWIAMfYPqKPgI5zHx-Zt_9sCXMCJT4tvtZ7-_7njSHwUEcaHQUj1P5qAnb1jOr_N31IbDn2B4hn9KTGUAWY0hP8xgxUK_r5FA8PuVbEjlPDFU45SVSCfUnb9qdcvNk_VKe2Ncc6HfKU3mwmB3IB6VKDyNVbZ948giFtl_VLgeD7V-ic0F72VkB7IHlyTIImhg82fM_PAmDebiKozgK4mgVXSxXU_6XJ1Ewj6PzwBrDZXgZLi8OU_6vSbqYR-HFYrEIgvh8EZ9H8eWUYy6Morv2N1Uvh_8E9Rfc?type=png)](https://mermaid.live/edit#pako:eNqNVU1v2zAM_SuCTlmXBHGT1h8oeul2GNBeOuxSGAgYm03V2VJAycW2IP99smXZrtO09UU2xUc-PlLynmcqR57wrACtvwnYEpSpZPbJBWFmhJLs9j6VztZ4sV-6AhKK7Z2RsZk2xNZSlRvC17ZMEaEa26Qh0Cihs-ciM3YDaIcGdGe-cQa23oDM8RnWWCNzeM_hRUCuuhBfGwNNctRGSDA17ykDXUlj16xC2tlVI72IXNGXDmZLFxtBkxKlhmfsNzJCIM904krudwuhbYox3UnrcHgt4882602j0UBNp0blVO7VqIPX6hWwbmnpAd-t3SWbu4W11GyNTfR69aofVenDOb7S4HHZO1IZauhc9Yma7tz2eDQIS2Fs9NF0DLvyesd1aDQ3Tbc620apgq0LtBJ2NEvlRCDUlWV6gqSfmvfn18l9pLQ9IbjthTiWys3AidQ_vtfzuCkGCl1dCSsMPUKG19fjue2jDGLcN237RBA_xW9Gua15fiLIiXr8JZDyIOXsbDZr3_oKEybKXYFWIAMfYPqKPgI5zHx-Zt_9sCXMCJT4tvtZ7-_7njSHwUEcaHQUj1P5qAnb1jOr_N31IbDn2B4hn9KTGUAWY0hP8xgxUK_r5FA8PuVbEjlPDFU45SVSCfUnb9qdcvNk_VKe2Ncc6HfKU3mwmB3IB6VKDyNVbZ948giFtl_VLgeD7V-ic0F72VkB7IHlyTIImhg82fM_PAmDebiKozgK4mgVXSxXU_6XJ1Ewj6PzwBrDZXgZLi8OU_6vSbqYR-HFYrEIgvh8EZ9H8eWUYy6Morv2N1Uvh_8E9Rfc)


# Justificación del Diseño Orientado a Objetos (Entrega 1)

## 1. Clases Principales y su Responsabilidad

-   **`Usuario`**: Responsable de la gestión del cliente de correo. Maneja la información del usuario (nombre, correo), y las operaciones de enviar y recibir mensajes, además de la gestión de carpetas. Implementa las interfaces **IEnviable** e **IRecibible**.
-   **`Mensaje`**: Objeto de datos que encapsula toda la información de un correo (remitente, destinatario, asunto, cuerpo, etc.). Almacena esta información y ofrece métodos como por ejemplo, `mostrar_resumen()`.
-   **`Carpeta`**: Contenedor para los objetos `Mensaje`. Agregar y lista los mensajes que le pertenecen. En esta primera entrega es una lista simple, pero su diseño permite que se convierta en una estructura de árbol en futuras entregas. Implementa la interfaz **IListable**.
-   **`ServidorCorreo`**: Es el punto central para la lógica del sistema. Su responsabilidad principal es gestionar la creación de usuarios y procesar el flujo de mensajes entre ellos. Es un mediador entre los objetos `Usuario`.

## 2. Encapsulamiento y Propiedades

Se decidió encapsular los atributos de las clases (`_nombre`, `_correo`, `_mensajes`, etc.) para proteger la integridad de los datos. Se usan propiedades (`@property`) para permitir el acceso controlado a estos atributos, y en algunos casos, setters (`@nombre.setter`) para validar los cambios. Esto asegura que los datos se manejen de forma segura y consistente.

## 3. Uso de Interfaces (Módulo `abc`)

Las interfaces **IEnviable**, **IRecibible** e **IListable** se definieron usando el módulo `abc` de Python. Esto fuerza a las clases a implementar ciertos métodos, lo que hace el código más claro y mantenible. Por ejemplo, al exigir que la clase `Usuario` implemente `enviar()` y `recibir()`, se asegura que cualquier objeto `Usuario` pueda realizar esas operaciones, lo que simplifica el diseño a futuro.

## 4. Principio KISS

El diseño evita la complejidad innecesaria. Las clases son simples, con responsabilidades claras. Por ejemplo, el `ServidorCorreo` solo tiene los métodos que necesita para el flujo básico de mensajes. Las carpetas son simples listas de mensajes, así se puede comprender mas facilmente y tiene escalabilidad para las próximas entregas.

