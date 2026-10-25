"""
Monitoramento de arquivos de log com watchdog.
O watchdog notifica mudanças; este módulo lê apenas as linhas novas.
"""

import logging
from pathlib import Path

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from filter import extract_relevant_lines
from notifier import send_alert

logger = logging.getLogger(__name__)

class LogFileHandler(FileSystemEventHandler):
    """
    Handler do watchdog para monitorar um arquivo de log específico.
    Mantém a posição da última leitura para processar apenas linhas novas.
    """

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self._last_position: int = self._get_current_size()

    def _get_current_size(self) -> int:
        """Retorna o tamanho atual do arquivo em bytes.
        """
        try:
            return self.log_path.stat().st_size
        except FileNotFoundError:
            logger.error("Arquivo de log são encontrados: %s", self.log_path)
            return 0

    def _read_new_lines(self) -> list[str]:
        """
        Lê apenas as linhas adicionadas desde a última leitura.

        Returns:
            Lista de novas linhas de arquivo.
        """
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
                f.seek(self._last_position)
                new_lines = f.readlines()
                self._last_position = f.tell()
            return new_lines
        except FileNotFoundError:
            logger.error("Arquivo de log desapareceu durante a leitura: %s", self.log_path)
            return []
        except OSError as exc:
            logger.error("Erro ao ler arquivo de log: %s", exc)
            return []

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Chamado pelo watchdog quando o arquivo monitorado é modificado.
        Lê as novas linhas, filtra e envia alerta se necessário.
        """
        if Path(str(event.src_path)) != self.log_path:
            return

        new_lines = self._read_new_lines()
        if not new_lines:
            return

        relevant = extract_relevant_lines(new_lines)
        if relevant:
            logger.info("%d linha(s) relevante(s) detectada(s).", len(relevant))
            send_alert(relevant)

def start_monitoring(log_path: str) -> None:
    """
    Inicia o monitoramento do arquivo de log.
    Encerra corretamente quando Ctrl + C é pressionado.
    """
    path = Path(log_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo de log não encontrado: {log_path}"
        )

    handler = LogFileHandler(log_path)
    observer = Observer()
    observer.schedule(
        handler,
        path=str(path.parent),
        recursive=False,
    )

    observer.start()
    logger.info("Monitorando: %s", log_path)

    try:
        while observer.is_alive():
            observer.join(timeout=1)

    except KeyboardInterrupt:
        logger.info("Encerramento solicitado pelo usuário.")

    finally:
        observer.stop()
        observer.join()
        logger.info("Monitor encerrado com sucesso.")
