import smtplib
from email.message import EmailMessage
from jinja2 import Template
from app.schemas.projetos import InformacoesProjeto
from config import settings


def email_workana(projetos: list[InformacoesProjeto]) -> None:
    with open('app/templates/email_workana.html', 'r', encoding='utf-8') as arquivo:
        corpo_html = arquivo.read()

    template = Template(corpo_html)

    dados = {
        'projetos': projetos
    }

    corpo_html = template.render(dados)

    msg = EmailMessage()
    msg['Subject'] = "E-mail Diário de Projetos Workana"
    msg['From'] = getattr(settings, 'FROM_EMAIL')
    msg['To'] = getattr(settings, 'TO_EMAIL')

    # Texto alternativo obrigatório
    msg.set_content("Caso não veja o HTML, este é o texto alternativo.")

    # 2. Insere o conteúdo lido do arquivo
    msg.add_alternative(corpo_html, subtype='html')

    # Envio do e-mail
    try:
        with smtplib.SMTP_SSL(getattr(settings, 'SMTP_EMAIL'), 465) as smtp:
            smtp.login(getattr(settings,'FROM_EMAIL'), getattr(settings, 'SENHA_EMAIL'))
            smtp.send_message(msg)
        print("E-mail enviado com sucesso usando o arquivo HTML!")
    except Exception as e:
        print(f"Erro ao enviar: {e}")