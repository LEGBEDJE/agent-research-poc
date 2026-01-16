# 🔬 AI Research Agent (Pydantic-AI POC)

Ce projet est une démonstration technique d'un **Agent IA Autonome** capable d'exécuter du **Tool Calling** (appel d'outils) pour enrichir ses réponses avec une documentation technique spécifique.

## 🚀 Objectifs du projet
- Implémenter une architecture **Agentic RAG**.
- Utiliser le framework **Pydantic-AI** pour garantir la robustesse et le typage des interactions.
- Déployer une interface interactive via **Streamlit**.
- Utiliser des modèles **Open Source (Llama 3.3)** via Groq pour une performance optimale.

## 🛠 Stack Technique
- **Framework Agent** : Pydantic-AI (Modern Agentic Framework)
- **Modèle LLM** : Llama-3.3-70b-Versatile (via Groq)
- **Interface** : Streamlit
- **Runtime** : Python 3.10+ (Asynchrone via Asyncio)

## 📖 Fonctionnalités
- **Raisonnement Autonome** : L'agent décide de consulter ou non la base de connaissances interne selon la requête.
- **Base de Connaissances Technique** : Documentation intégrée sur le RAG, vLLM et Pydantic-AI.
- **Sécurité** : Gestion dynamique des clés API via l'interface utilisateur.

## 📦 Installation locale
1. Cloner le repo : `git clone https://github.com/LEGBEDJE/agent-research-poc.git`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'app : `streamlit run app.py`

-
