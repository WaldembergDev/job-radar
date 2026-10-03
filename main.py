from app.agents.workana_agent import criar_agent


if __name__ == '__main__':
    agent = criar_agent()
    
    response = agent.run('Tendo como base os meus dados, selecione os três melhores projetos que mais dão um match com os meus conhecimentos')

    for projeto in response.content.projetos:
        print(f'Projeto: {projeto.titulo}\n', flush=True)
