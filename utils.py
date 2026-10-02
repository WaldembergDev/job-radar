import re


def extrair_qnt_propostas(texto: str) -> int | None:
    match = re.search(r'\d+', texto)
    qnt_propostas = None
    if match:
        qnt_propostas = int(match.group())
    return qnt_propostas