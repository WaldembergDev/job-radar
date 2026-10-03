from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from .services_workana import extrair_projetos_workana
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.google import GeminiEmbedder


load_dotenv()

def criar_agent():

    gemini_embedder=GeminiEmbedder(id="gemini-embedding-2")

    knowledge = Knowledge(
        vector_db=ChromaDb(
            collection='docs',
            path='tmp/chromadb',
            persistent_client=True,
            embedder=gemini_embedder
        )
    )

    knowledge.insert(path='docs/')

    agent = Agent(
        model=Gemini(id='gemini-3.1-flash-lite'),
        description='Você é um especialista em análise de projetos de sistemas',
        tools=[extrair_projetos_workana],
        knowledge=knowledge,
        search_knowledge=True,
        markdown=True,
    )

    return agent

