import streamlit as st
import asyncio
from groq import Groq
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field
import nest_asyncio

nest_asyncio.apply()

st.set_page_config(page_title="IA Research Agent", page_icon="🔬")
st.title("🔬 Agent de Recherche Autonome")

# Structure de sortie
class AgentOutput(BaseModel):
    answer: str = Field(description="La réponse finale")
    used_tools: bool = Field(description="Est-ce que des outils ont été consultés ?")

with st.sidebar:
    st.header("Configuration")
    user_api_key = st.text_input("Clé API Groq", type="password")

if not user_api_key:
    st.warning("Veuillez entrer votre clé API Groq.")
    st.stop()

try:
    client = Groq(api_key=user_api_key)
    model = GroqModel('llama3-70b-8192', groq_client=client)
    # CORRECTIF : On crée l'agent sans le result_type ici
    agent = Agent(model=model) 
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

@agent.tool
async def search_technical_doc(ctx, topic: str) -> str:
    """Recherche dans la base de connaissance technique interne."""
    knowledge_base = {
        "rag": "Le RAG (Retrieval-Augmented Generation) permet d'injecter des données externes à un LLM.",
        "pydantic-ai": "C'est un framework de création d'agents typés, plus robuste que LangChain.",
        "vllm": "Un moteur de serving LLM haute performance utilisé pour la production."
    }
    return knowledge_base.get(topic.lower(), "Sujet non listé dans la documentation locale.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Explique moi le RAG..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'agent réfléchit..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                # CORRECTIF : On définit le type de retour ici au moment de l'exécution
                result = loop.run_until_complete(agent.run(prompt, result_type=AgentOutput))
                
                response_text = result.data.answer
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Détails de l'erreur : {type(e).__name__} - {str(e)}")
