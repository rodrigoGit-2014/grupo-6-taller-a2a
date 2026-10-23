"""Agente de Rodrigo · se expone por A2A de forma NATIVA con el servidor de LangGraph.

Rodrigo es un especialista en arquitectura backend (Java/Spring Boot, microservicios,
APIs REST) y construcción de agentes de IA. No hay código de servidor aquí: `langgraph dev`
(o un deploy de LangGraph Platform) lee `langgraph.json`, levanta este grafo y publica
automáticamente:
  · la Agent Card  →  GET  /.well-known/agent-card.json?assistant_id=agente_rodrigo
  · el endpoint    →  POST /a2a/agente_rodrigo   (message/send, message/stream, tasks/get, tasks/cancel)

Requisito único: el estado del grafo debe tener la clave `messages` (MessagesState la trae).
El `contextId` de A2A se convierte en `thread_id`: la memoria por conversación viene gratis.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware

from src.agente_rodrigo.herramientas import HERRAMIENTAS
from src.agente_rodrigo.prompts import SYSTEM_RODRIGO

load_dotenv()

modelo = ChatGoogleGenerativeAI(model=os.environ.get("MODELO", "gemini-3.5-flash-lite"))

# Agente ReAct (LangChain 1.x): el modelo decide qué herramienta llamar, la llama, lee el resultado y responde.
# Su estado tiene la clave `messages`: eso es lo único que A2A necesita para mapear sus `parts` de texto.
parametros_agente = {
    "model": modelo,
    "tools": HERRAMIENTAS,
    "system_prompt": SYSTEM_RODRIGO,
    "name": "agente_rodrigo",
}
if os.environ.get("DEEPSEEK_API_KEY"):
    from langchain_deepseek import ChatDeepSeek

    respaldo = ChatDeepSeek(model=os.environ.get("MODELO_RESPALDO", "deepseek-chat"))
    parametros_agente["middleware"] = [ModelFallbackMiddleware(respaldo)]

graph = create_agent(**parametros_agente)
