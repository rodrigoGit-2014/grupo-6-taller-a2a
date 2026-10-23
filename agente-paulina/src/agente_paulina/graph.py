"""Paulina: grafo con messages, publicado por el servidor nativo de LangGraph."""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agente_paulina.herramientas import HERRAMIENTAS
from src.agente_paulina.prompts import SYSTEM_PAULINA

load_dotenv()

modelo = ChatGoogleGenerativeAI(model=os.environ.get("MODELO", "gemini-3.5-flash-lite"))
parametros_agente = {
    "model": modelo,
    "tools": HERRAMIENTAS,
    "system_prompt": SYSTEM_PAULINA,
    "name": "agente_paulina",
}
if os.environ.get("DEEPSEEK_API_KEY"):
    from langchain_deepseek import ChatDeepSeek

    respaldo = ChatDeepSeek(model=os.environ.get("MODELO_RESPALDO", "deepseek-chat"))
    parametros_agente["middleware"] = [ModelFallbackMiddleware(respaldo)]

graph = create_agent(**parametros_agente).with_config({"recursion_limit": 30})
