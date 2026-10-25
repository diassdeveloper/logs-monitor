"""
Envio de alertas por email com rate limiting.
Rate limiting evita flood de emails em caso de falhas em cascata.
"""

import smtplib
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config
from config import (
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
    SMTP_HOST,
    SMTP_PORT,
)

logger = logging.getLogger(__name__)

_last_sent_at: float = 0.0

def _is_rate_limited() -> bool:
    """Verifica se o rate limit ainda está ativo."""
    elapsed = time.time() - _last_sent_at
    return elapsed < config.RATE_LIMIT_SECONDS

def _build_email(lines: list[str]) -> MIMEMultipart:
    body = "\n".join(lines)

    message = MIMEMultipart()
    message["From"] = str(EMAIL_SENDER)
    message["To"] = str(EMAIL_RECEIVER)
    message["Subject"] = f"[log-monitor] {len(lines)} alerta(s) detectado(s)"
    message.attach(MIMEText(body, "plain"))

    return message

def send_alert(lines: list[str]) -> None:
    """
    Envia email de alerta com as linhas críticas do log.
    Respeita o rate limit configurado.

    Args:
        lines: Lista de linhas relevantes detectadas.
    """
    global _last_sent_at

    if not lines:
        return

    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        logger.error("Credenciais de email não configuradas.")
        return

    if _is_rate_limited():
        remaining = int(config.RATE_LIMIT_SECONDS - (time.time() - _last_sent_at))
        logger.warning(
            "Rate limit ativo. Próximo email em %ds. "
            "%d linha(s) suprimida(s).",
            remaining,
            len(lines),
        )
        return

    message = _build_email(lines)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(str(EMAIL_SENDER), str(EMAIL_PASSWORD))
            server.sendmail(str(EMAIL_SENDER), str(EMAIL_RECEIVER), message.as_string())

        _last_sent_at = time.time()
        logger.info("Email enviado com %d alerta(s).", len(lines))

    except smtplib.SMTPAuthenticationError:
        logger.error("Falha de autenticação SMTP.")
    except smtplib.SMTPException as exc:
        logger.error("Falha ao enviar email: %s", exc)
