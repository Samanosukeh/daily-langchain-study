```python
from datetime import datetime
from typing import List

def resumo_mensal(projetos: List[dict]) -> str:
    """Gera resumo mensal de projetos em andamento."""
    mes_atual = datetime.now().strftime("%B")
    total = len(projetos)
    ativos = sum(1 for p in projetos if p.get("status") == "ativo")
    progresso = sum(p.get("progresso", 0) for p in projetos) / total if total else 0

    return (
        f"Resumo {mes_atual}:\n"
        f"- Total de projetos: {total}\n"
        f"- Projetos ativos: {ativos}\n"
        f"- Progresso médio: {progresso:.1f}%"
    )

# Exemplo de uso
projetos = [
    {"nome": "Sistema X", "status": "ativo", "progresso": 75},
    {"nome": "API Y", "status": "concluido", "progresso": 100},
    {"nome": "Dashboard Z", "status": "ativo", "progresso": 40}
]

print(resumo_mensal(projetos))
```