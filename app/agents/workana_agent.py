from agno.agent import Agent
from agno.models.google import Gemini
from ..services.services_workana import extrair_projetos_workana
from app.schemas.projetos import ListaProjetos
from pathlib import Path


PERFIL = Path('docs/habilidades_workana.txt').read_text(encoding='utf-8')

def criar_agent():    
    
    agent = Agent(
        model=Gemini(id='gemini-3.1-flash-lite'),
        description='Você é um especialista em análise de projetos de sistemas',
        instructions=[
            "Selecione os projetos com maior aderência ao PERFIL abaixo.",
            "DESCARTE o projeto se: pedir aplicativo mobile (Android, iOS, Flutter, "
            "React Native, Kotlin, Swift, app nativo ou híbrido); exigir alguma "
            "tecnologia da seção LACUNAS; for focado em front-end, design ou UX/UI; "
            "tiver escopo vago ou orçamento incompatível com o escopo.",
            "Priorize Python, Django, automação, dados e IA aplicada, com escopo claro e trabalho remoto.",
            "Se menos de 3 projetos passarem nos critérios, retorne apenas os que passaram. "
            "Nunca complete a lista com projetos fracos.",
            "No campo análise, cite as tecnologias que casam com o perfil e o principal risco ou gap.",
            f"PERFIL DO DESENVOLVEDOR:\n{PERFIL}",
        ],
        tools=[extrair_projetos_workana],
        markdown=True,
        output_schema=ListaProjetos,
        retries=3,
        delay_between_retries=30,
    )

    return agent

