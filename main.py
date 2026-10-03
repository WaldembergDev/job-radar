from services.services_agno import criar_agent
from services.services_workana import extrair_projetos_workana


if __name__ == '__main__':
    #agent = criar_agent()
    projetos = extrair_projetos_workana()

    print(projetos)

    