"""
Configurações centralizadas do log-monitor.
Carrega variáveis do .env e define constantes do sistema.
"""

import os
from dotenv import load_dotenv 

load_dotenv()

# — Email ————————————————————————————————————————————

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# — Monitor ——————————————————————————————————————————

LOG_PATH = os.getenv("LOG_PATH", "/var/log/syslog")
SEVERITY_LEVELS = ["ERROR", "WARNING", "CRITICAL"]

# — Rate limiting ————————————————————————————————————
# Mínimo de segundos entre dois emails consecutivos

RATE_LIMIT_SECONDS = int(os.getenv("RATE_LIMIT_SECONDS", "60"))

# — Validação de configuração obrigatória ————————————
REQUIRED_VARS = ["EMAIL_SENDER", "EMAIL_PASSWORD", "EMAIL_RECEIVER"]

def validate_config():
    """
    Garante que todas as variáveis de configuração obrigatórias estão definidas.
    """
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Variáveis de ambiente obrigatórias não definidas: {', '.join(missing)}\n"
        "Crie um arquivo .env baseado no .env.example."
        
        ) 