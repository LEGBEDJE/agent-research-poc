import streamlit as st
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field
import nest_asyncio

# Indispensable pour Streamlit
nest_asyncio.apply()

# 1. Configuration de la page
st.set_page_config(page_title="IA Research Agent", page_icon="🔬")
st.title("🔬 Agent de Recherche Autonome")
st.markdown("Ce projet utilise **Pydantic-AI** et **Llama 3** pour orchestrer des outils de recherche.")

# 2. Définition des structures de données (TOUJOURS EN HAUT)
class AgentOutput(BaseModel):
    answer: str = Field(description="La réponse finale")
    used_tools: bool = Field(description="Est-ce que des outils ont été consultés ?")

# 3. Sidebar pour la clé API
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Clé API Groq", type="password", help="Gratuit sur console.groq.com")

if not api_key:
    st.warning("Veuillez entrer votre clé API Groq pour activer l'agent.")
    st.stop()

# 4. Initialisation de l'Agent (seulement si la clé est présente)
try:
    model = GroqModel('llama3-70b-8192', api_key=api_key)
    agent = Agent(model=model, result_type=AgentOutput)
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

# 5. Définition des outils (Tools)
@agent.tool
async def search_technical_doc(ctx, topic: str) -> str:
    """Recherche dans la base de connaissance technique interne."""
    knowledge_base = {
        "rag": "Le RAG (Retrieval-Augmented Generation) permet d'injecter des données externes à un LLM.",
        "pydantic-ai": "C'est un framework de création d'agents typés, plus robuste que LangChain.",
        "vllm": "Un moteur de serving LLM haute performance utilisé pour la production."
    }
    return knowledge_base.get(topic.lower(), "Sujet non listé dans la documentation locale.")

# 6. Gestion du Chat (Interface utilisateur)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Posez une question technique (ex: Explique moi le RAG)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'agent réfléchit..."):
            try:
                # Création d'une boucle d'événement propre pour Streamlit
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(agent.run(prompt))
                
                # On affiche la réponse propre
                response_text = result.data.answer
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Erreur lors de l'exécution : {e}")
