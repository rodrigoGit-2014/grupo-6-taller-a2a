"""Christopher: grafo con messages, publicado por el servidor nativo de LangGraph."""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from src.agente_christopher.herramientas import HERRAMIENTAS
from src.agente_christopher.prompts import SYSTEM_CHRISTOPHER

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("Configura GOOGLE_API_KEY en el archivo .env local de mi-agente antes de iniciar Christopher.")
modelo = ChatGoogleGenerativeAI(model=os.environ.get("MODELO", "gemini-3.5-flash-lite"))
graph = create_agent(
    model=modelo,
    tools=HERRAMIENTAS,
    system_prompt=SYSTEM_CHRISTOPHER,
    name="agente_christopher",
).with_config({"recursion_limit": 30})
