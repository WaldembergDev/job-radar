from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from app.utils import extrair_qnt_propostas
from config import settings


def extrair_projetos_workana() -> list:
    """ Extrai todos os projetos das 5 primeiras páginas do site Workana 

    Returns:
        Uma lista de truplas contendo titulo, link do projeto, conteudo, quantidade de propostas do projeto, valor e análise do projeto
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--headless=new",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
                ],
            proxy=getattr(settings, 'PROXY', None)
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        Stealth().use_sync(page)

        page.goto('https://www.workana.com/jobs?category=it-programming&language=pt')

        projetos = []
        for i in range(1, 6):
            page.goto(
                f'https://www.workana.com/jobs?category=it-programming&language=pt&page={i}'
                )
            elementos = page.locator('.project-item').all()
            for elemento in elementos:
                elemento.locator('.link').click()
                link_relativo = elemento.locator('//h2[@class="h3 project-title"]//a').get_attribute('href')
                link = 'https://workana.com' + link_relativo if link_relativo else ''
                titulo = elemento.locator('.project-title').inner_text()
                conteudo = elemento.locator('.project-body').inner_text()
                texto_qnt_propostas = elemento.locator('.bids').inner_text()
                valor = elemento.locator('.values').inner_text()
                qnt_propostas = extrair_qnt_propostas(texto_qnt_propostas)
                projetos.append((titulo, link, conteudo, qnt_propostas, valor))
            page.wait_for_timeout(2000)

        page.close()

        return projetos
    