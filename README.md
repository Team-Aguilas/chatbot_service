# Microservicio de Chatbot para Marketplace

Este es un microservicio construido con **FastAPI** que actúa como un intermediario seguro entre la aplicación de frontend y la **API de Google AI (Gemini)**. Su único propósito es recibir mensajes de los usuarios, consultar al modelo de IA y devolver las respuestas.

## Arquitectura

El servicio expone un único endpoint que evita exponer la clave de API de Google en el lado del cliente (navegador), lo cual es una práctica de seguridad fundamental.

- **Endpoint**: `POST /api/v1/chat`
- **Modelo de IA**: `gemini-1.5-flash`

## Tecnologías Utilizadas

- **Framework**: FastAPI
- **Servidor ASGI**: Uvicorn
- **Lenguaje**: Python 3.11+
- **Integración IA**: `google-generativeai`
- **Variables de Entorno**: `python-dotenv`, `pydantic-settings`

## Prerrequisitos

- Python 3.11 o superior
- `pip` (el gestor de paquetes de Python)

## Guía de Instalación y Configuración

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone <url-del-repositorio-del-chatbot>
    cd marketplace-chatbot
    ```

2.  **Crear y Activar un Entorno Virtual:**
    Es altamente recomendable trabajar dentro de un entorno virtual.
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en Windows (PowerShell)
    .\venv\Scripts\Activate

    # Activar en Linux o macOS
    # source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    Instala todas las librerías necesarias con el siguiente comando:
    ```bash
    pip install -r chatbot_service/requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    Este paso es **crucial**. Debes crear un archivo `.env` dentro de la carpeta `chatbot_service/`.
    -   **Crea el archivo**: `chatbot_service/.env`
    -   **Añade el siguiente contenido** y reemplaza `TU_API_KEY_DE_GOOGLE_AI` con tu clave real.

    ```env
    PROJECT_NAME="Servicio de Chatbot"
    GOOGLE_API_KEY="AIzaSy...tu_clave_real_aqui"
    ```

## Cómo Ejecutar el Servicio

Una vez configurado, puedes iniciar el servidor de desarrollo. La forma en que lo ejecutas depende de en qué carpeta te encuentres en la terminal.

**Método Recomendado (Desde la raíz del repositorio `marketplace-chatbot`):**

Este método es el más claro.
```bash
# Estando en la carpeta marketplace-chatbot/
uvicorn chatbot_service.app.main:app --reload --port 8003
```
* `chatbot_service.app.main:app`: Le indica a Uvicorn la ruta completa al objeto `app` de FastAPI.

## Endpoint de la API

### Enviar un Mensaje al Chatbot

-   **URL**: `/api/v1/chat`
-   **Método**: `POST`
-   **Cuerpo de la Petición (Request Body)**:
    ```json
    {
      "message": "Hola, ¿qué tipo de manzanas venden?"
    }
    ```
-   **Respuesta Exitosa (Response Body)**:
    ```json
    {
      "reply": "¡Hola! En Mercado Fresco tenemos una gran variedad de manzanas, como la Gala, Fuji y Granny Smith. ¿Te gustaría saber más sobre alguna de ellas?"
    }
    ```
