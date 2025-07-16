import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path # 1. Importamos 'Path' para manejar rutas de forma segura
from prometheus_fastapi_instrumentator import Instrumentator

# 2. Construimos una ruta absoluta al archivo .env, esto es mucho más robusto
# Asume que el script se corre desde la raíz 'market_place_project'
env_path = Path('.') / 'chatbot_service' / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Chatbot Service")

Instrumentator().instrument(app).expose(app)

# 3. Movemos la inicialización del modelo dentro de un evento de startup
#    para que los errores sean más claros al iniciar.
@app.on_event("startup")
async def startup_event():
    try:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("La variable de entorno GOOGLE_API_KEY no se encontró o está vacía.")
        
        genai.configure(api_key=GOOGLE_API_KEY)
        app.state.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Modelo de IA configurado y listo.")
    except Exception as e:
        app.state.model = None
        print(f"❌ Error crítico al configurar Google AI: {e}")

# ... (Tu configuración de CORS no cambia)
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/v1/chat")
async def chat_with_bot(request: ChatRequest):
    if not hasattr(app.state, 'model') or app.state.model is None:
        raise HTTPException(status_code=503, detail="Servicio de IA no disponible.")
    try:
        prompt = f"""
        Eres 'FrescoBot', un asistente amigable y servicial para un marketplace de frutas y verduras llamado 'Mercado Fresco'.
        Tu objetivo es responder preguntas sobre frutas, verduras, recetas o ayudar a los usuarios a navegar la tienda.
        Sé breve, amable y directo.
        
        El usuario pregunta: "{request.message}"
        
        Tu respuesta:
        """
        response = await app.state.model.generate_content_async(prompt)
        return {"reply": response.text}
    except Exception as e:
        # Este error ahora aparecerá en tu terminal de backend
        print(f"Error al generar respuesta de Gemini: {e}")
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con la API de IA.")

@app.get("/")
def read_root():
    return {"service": "Chatbot Service", "status": "ok"}