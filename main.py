from services.services_workana import extrair_projetos_workana

if __name__ == '__main__':
    projetos = extrair_projetos_workana()

    for projeto in projetos:
        print(projeto)