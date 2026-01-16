import streamlit as st
import asyncio
import os
import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel, Field

# Indispensable pour l'exécution asynchrone dans Streamlit
nest_asyncio.apply()

# --- CONFIGURATION UI ---
st.set_page_config(page_title="AI Research Agent", page_icon="🔬", layout="centered")

st.title("🔬 Agent de Recherche Autonome")
st.markdown("""
Cette application démontre les capacités d'un **Agent IA** à utiliser des outils externes 
pour répondre à des questions techniques complexes.
""")

# --- LOGIQUE DE L'AGENT ---

# Définition de la structure de sortie pour garantir la fiabilité des données
class AgentOutput(BaseModel):
    answer: str = Field(description="La réponse finale structurée")
    used_tools: bool = Field(description="Indique si l'outil de recherche a été consulté")

# Sidebar pour la sécurité (Clé API)
with st.sidebar:
    st.header("🔑 Authentification")
    user_api_key = st.text_input("Clé API Groq", type="password", help="Obtenez une clé gratuite sur console.groq.com")
    st.info("Le modèle utilisé est **Llama-3.3-70b-Versatile**.")

if not user_api_key:
    st.warning("Veuillez entrer votre clé API Groq dans la barre latérale.")
    st.stop()

# Initialisation du modèle et de l'agent
try:
    os.environ['GROQ_API_KEY'] = user_api_key
    model = GroqModel('llama-3.3-70b-versatile')
    
    system_prompt = """Tu es un expert en R&D IA. 
    Pour toute question technique (RAG, Pydantic-AI, vLLM, Agents), utilise SYSTEMATIQUEMENT 
    l'outil 'search_technical_doc' pour garantir l'exactitude des informations."""
    
    agent = Agent(model=model, system_prompt=system_prompt)

    # Définition de l'outil de recherche (Simulated RAG)
    @agent.tool
    async def search_technical_doc(ctx, topic: str) -> str:
        """Recherche des définitions techniques dans la documentation interne."""
        knowledge_base = {
            "rag": "RAG (Retrieval-Augmented Generation) : architecture combinant recherche vectorielle et LLM pour réduire les hallucinations.",
            "pydantic-ai": "Framework Python de Pydantic pour bâtir des agents type-safe et robustes pour la production.",
            "vllm": "Moteur de serving haute performance optimisé pour le déploiement de LLM (KV cache, batching).",
            "agent": "Système autonome capable de raisonner, d'utiliser des outils et d'agir pour atteindre un objectif."
        }
        return knowledge_base.get(topic.lower(), f"Le sujet '{topic}' n'est pas documenté en interne.")

except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

# --- INTERFACE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if prompt := st.chat_input("Ex: Explique-moi les avantages du vLLM"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'agent consulte la documentation..."):
            try:
                # Exécution asynchrone de l'agent
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                enhanced_prompt = f"Utilise tes outils pour répondre à : {prompt}"
                result = loop.run_until_complete(agent.run(enhanced_prompt))
                
                response_text = str(result.output)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Erreur d'exécution : {e}")
