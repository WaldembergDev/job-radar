from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from utils import extrair_qnt_propostas

def extrair_projetos_workana() -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
                ]
            )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport=None 
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
                titulo = elemento.locator('.project-title').inner_text()
                conteudo = elemento.locator('.project-body').inner_text()
                texto_qnt_propostas = elemento.locator('.bids').inner_text()
                qnt_propostas = extrair_qnt_propostas(texto_qnt_propostas)
                projetos.append((titulo, conteudo, qnt_propostas))
            page.wait_for_timeout(2000)

        page.close()

        return projetos
    