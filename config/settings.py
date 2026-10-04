from dotenv import load_dotenv
import os


load_dotenv()

USERNAME_WEBSHARE = os.getenv('USERNAME_WEBSHARE', default=None)
PASSWORD_WEBSHARE = os.getenv('PASSWORD_WEBSHARE', default=None)
SERVER_WEBSHARE = os.getenv('SERVER_WEBSHARE', default=None)

if all([USERNAME_WEBSHARE, PASSWORD_WEBSHARE, SERVER_WEBSHARE]):
    PROXY = {
        'server': SERVER_WEBSHARE,
        'username': USERNAME_WEBSHARE,
        'password': PASSWORD_WEBSHARE
    }

# configurações de e-mail
FROM_EMAIL=os.getenv('FROM_EMAIL')
SENHA_EMAIL=os.getenv('SENHA_EMAIL')
HOST=os.getenv('HOST')
SMTP_EMAIL=os.getenv('SMTP_EMAIL')
TO_EMAIL=os.getenv('TO_EMAIL')