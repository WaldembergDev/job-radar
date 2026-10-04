from app.agents.workana_agent import criar_agent
from app.services.services_email import email_workana


if __name__ == '__main__':

    agent = criar_agent()
    response = agent.run('Tendo como base os meus dados, selecione os três melhores projetos que mais dão um match com os meus conhecimentos')
    projetos = response.content.projetos
    
    email_workana(projetos)