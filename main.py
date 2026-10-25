"""
Log Monitor — Monitor de arquivos de log em tempo real.

Detecta linhas com ERROR, WARNING e CRITICAL e envia alertas
por email com rate limiting configurável.

Uso:
    python main.py
    python main.py --log /caminho/para/arquivo.log
    python main.py --log /var/log/syslog --rate-limit 120
"""

import argparse
import logging
import sys

from config import LOG_PATH, RATE_LIMIT_SECONDS, validate_config
import config
from monitor import start_monitoring


def setup_logging() -> None:
    """Configura o formato de log do próprio monitor."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    """Parseia os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Monitor de arquivos de log com alertas por email."
    )
    parser.add_argument(
        "--log",
        default=LOG_PATH,
        help=f"Caminho do arquivo de log a monitorar (padrão: {LOG_PATH})",
    )
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=RATE_LIMIT_SECONDS,
        help=f"Segundos entre emails consecutivos (padrão: {RATE_LIMIT_SECONDS})",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    # Permite sobrescrever rate limit via argumento
    config.RATE_LIMIT_SECONDS = args.rate_limit

    try:
        validate_config()
    except EnvironmentError as exc:
        logging.critical(str(exc))
        sys.exit(1)

    try:
        start_monitoring(args.log)
    except KeyboardInterrupt:
        logging.info("Monitor encerrado pelo usuário.")
    except FileNotFoundError as exc:
        logging.critical(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()