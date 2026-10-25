"""
Filtragem de linhas de log por severidade.
Mantém separado da lógica de monitaramento para facilitar testes.
"""

from config import SEVERITY_LEVELS

def is_relevant(line: str) -> bool:
    """
    Verifica se uma linha de log contém algum nível de severidade relevante.
    
    Args:
        line: Linha do arquivo de log.
    
    Returns:
        True se a linha contiver ERROR, WARNING ou CRITICAL
    """
    line_upper = line.upper()
    return any(level in line_upper for level in SEVERITY_LEVELS)

def extract_relevant_lines(lines: list[str]) -> list[str]:
    """
    Filtra uma lista de linhas retornando apenas as relevantes.

    Args:
        lines: Lista de linhas brutas do log.

    Returns:
        Lista de linhas que contêm níveis de severidade relevantes.
    """
    return [line.strip() for line in lines if is_relevant(line)] 


