# Job Radar

Agente de IA que monitora diariamente os projetos de programação da [Workana](https://www.workana.com), seleciona os que mais combinam com o meu perfil técnico e envia o resultado por e-mail.

Em vez de abrir a plataforma todo dia e ler dezenas de anúncios, recebo na caixa de entrada só os melhores projetos, cada um com uma análise de aderência.

## Como funciona

```
GitHub Actions (cron diário)
        │
        ▼
Playwright extrai os projetos da Workana (5 primeiras páginas)
        │
        ▼
Agente (Agno + Gemini) compara cada projeto com o perfil em docs/habilidades_workana.txt
        │
        ▼
Saída estruturada (Pydantic): título, link, descrição, propostas, valor e análise
        │
        ▼
E-mail HTML (Jinja2 + SMTP) com os projetos selecionados
```

1. **Coleta:** o Playwright, com `playwright-stealth`, abre a categoria *TI e Programação* da Workana (projetos em português) e lê título, link, descrição, quantidade de propostas e valor de cada projeto das 5 primeiras páginas. Um proxy (Webshare) pode ser usado, se configurado.
2. **Análise:** o agente, construído com [Agno](https://docs.agno.com) e o modelo Gemini, recebe o perfil do desenvolvedor e as regras de seleção. Ele descarta projetos fora do foco (por exemplo, aplicativos mobile ou tecnologias que não domino) e escolhe até 3 projetos com maior aderência.
3. **Saída estruturada:** a resposta segue o schema `ListaProjetos` (Pydantic), o que garante campos previsíveis para montar o e-mail.
4. **Envio:** um template HTML (Jinja2) é renderizado e enviado por SMTP com SSL.
5. **Automação:** um workflow do GitHub Actions executa tudo todos os dias, e também pode ser disparado manualmente.

## Estrutura do projeto

```
job-radar/
├── .github/workflows/script_workana.yml   # execução diária (cron) e manual
├── app/
│   ├── agents/workana_agent.py            # criação do agente (modelo, instruções, schema)
│   ├── schemas/projetos.py                # modelos Pydantic da saída
│   ├── services/services_workana.py       # scraping da Workana com Playwright
│   ├── services/services_email.py         # renderização e envio do e-mail
│   ├── templates/email_workana.html       # template HTML do e-mail
│   └── utils.py                           # funções auxiliares
├── config/settings.py                     # leitura das variáveis de ambiente
├── docs/habilidades_workana.txt           # perfil usado como referência pelo agente
├── main.py                                # ponto de entrada
└── pyproject.toml
```

## Tecnologias

- Python 3.12
- [Agno](https://docs.agno.com) e Google Gemini (`google-genai`)
- Playwright e playwright-stealth
- Pydantic (saída estruturada)
- Jinja2 e `smtplib` (e-mail)
- [uv](https://docs.astral.sh/uv/) (gerenciamento de dependências)
- GitHub Actions (agendamento)

## Como executar localmente

### Pré-requisitos

- Python 3.12 ou superior
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Chave de API do Google AI (Gemini)
- Conta de e-mail com acesso SMTP (SSL, porta 465)

### Instalação

```bash
git clone https://github.com/WaldembergDev/job-radar.git
cd job-radar

uv sync
uv run playwright install chromium
```

### Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
# IA
GOOGLE_API_KEY=sua_chave_do_gemini

# E-mail (SMTP com SSL, porta 465)
SMTP_EMAIL=smtp.seuprovedor.com
FROM_EMAIL=remetente@exemplo.com
SENHA_EMAIL=senha_ou_senha_de_app
TO_EMAIL=destinatario@exemplo.com

# Proxy (opcional)
SERVER_WEBSHARE=
USERNAME_WEBSHARE=
PASSWORD_WEBSHARE=
```

O proxy só é usado quando as três variáveis `*_WEBSHARE` estão preenchidas.

### Perfil

Edite `docs/habilidades_workana.txt` com as suas habilidades, lacunas e preferências. É esse arquivo que o agente usa para decidir quais projetos combinam com você.

### Execução

Execute a partir da raiz do projeto, porque o caminho do perfil é relativo:

```bash
uv run main.py
```

## Execução automática (GitHub Actions)

O workflow `.github/workflows/script_workana.yml` roda todos os dias às `12:30 UTC` (09:30 no horário de Brasília) e pode ser disparado manualmente na aba *Actions*.

Cadastre estes *secrets* no repositório (*Settings → Secrets and variables → Actions*):

| Secret | Descrição |
|---|---|
| `GOOGLE_API_KEY` | Chave de API do Gemini |
| `SMTP_EMAIL` | Servidor SMTP |
| `FROM_EMAIL` | E-mail remetente (também usado no login) |
| `SENHA_EMAIL` | Senha ou senha de app do remetente |
| `TO_EMAIL` | E-mail que recebe o relatório |
| `SERVER_WEBSHARE`, `USERNAME_WEBSHARE`, `PASSWORD_WEBSHARE` | Proxy (opcional) |
| `HOST` | Variável de e-mail reservada no workflow |

## Personalização

- **Critérios de seleção:** altere a lista `instructions` em `app/agents/workana_agent.py` (regras de descarte, prioridades e quantidade de projetos).
- **Perfil:** edite `docs/habilidades_workana.txt`.
- **Páginas e categoria:** ajuste as URLs e o intervalo de páginas em `app/services/services_workana.py`.
- **Aparência do e-mail:** edite `app/templates/email_workana.html`.
- **Horário:** altere a expressão `cron` no workflow.

## Limitações

- Depende da estrutura HTML da Workana: se o site mudar os seletores, a coleta precisa de ajuste.
- A Workana pode bloquear acessos automatizados; por isso o projeto suporta proxy e `playwright-stealth`.
- A qualidade da seleção depende do modelo e do perfil informado. A análise é um apoio à decisão, não substitui a leitura do projeto.
- Respeite os termos de uso da plataforma ao executar o monitoramento.

## Autor

**Waldemberg Pereira**
[GitHub](https://github.com/WaldembergDev) · [LinkedIn](https://www.linkedin.com/in/Waldemberg-pereira)