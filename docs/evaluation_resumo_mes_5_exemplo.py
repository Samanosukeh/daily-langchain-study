```python
from datetime import datetime
from typing import List, Dict

def resumo_mes_5(avaliacoes: List[Dict]) -> Dict:
    """
    Gera resumo mensal com base em avaliações do mês 5.

    Args:
        avaliacoes: Lista de dicionários com chaves 'data' (str) e 'nota' (float)

    Returns:
        Dicionário com médias e contagem
    """
    mes_5 = [av for av in avaliacoes if datetime.strptime(av['data'], '%Y-%m-%d').month == 5]

    if not mes_5:
        return {"erro": "Nenhuma avaliação no mês 5"}

    notas = [av['nota'] for av in mes_5]
    return {
        "total": len(mes_5),
        "media": sum(notas) / len(notas),
        "maior": max(notas),
        "menor": min(notas),
        "desvio_padrao": (sum((n - sum(notas)/len(notas))**2 for n in notas) / len(notas))**0.5
    }

# Exemplo de uso
avaliacoes = [
    {"data": "2023-05-01", "nota": 8.5},
    {"data": "2023-05-15", "nota": 9.0},
    {"data": "2023-06-01", "nota": 7.0},
    {"data": "2023-05-20", "nota": 6.5},
]

print(resumo_mes_5(avaliacoes))
```