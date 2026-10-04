from app.agents.workana_agent import criar_agent
from app.services.services_email import email_workana


if __name__ == '__main__':

    agent = criar_agent()
    response = agent.run(
        'Use a ferramenta para buscar os projetos da Workana e selecione até 3 que tenham '
        'maior aderência ao meu perfil, aplicando as regras de descarte. '
        'Se nenhum projeto passar nos critérios, retorne a lista vazia.'
    )
    projetos = response.content.projetos
    print("Número de projetos localizados: ", len(projetos), flush=True)
    email_workana(projetos)