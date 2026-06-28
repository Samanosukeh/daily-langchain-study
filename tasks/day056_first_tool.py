```python
from langchain_core.tools import tool

@tool
def buscar_produto_por_id(id_produto: str) -> dict:
    """Busca um produto no banco de dados pelo ID.

    Args:
        id_produto: ID único do produto.

    Returns:
        Dicionário com os dados do produto ou mensagem de erro.
    """
    # Simulação de busca em banco de dados
    produtos = {
        "1": {"nome": "Notebook Gamer", "preco": 4500.00, "estoque": 10},
        "2": {"nome": "Mouse sem fio", "preco": 89.90, "estoque": 50},
    }

    return produtos.get(id_produto, {"erro": "Produto não encontrado"})

@tool
def calcular_desconto(valor: float, percentual: float) -> float:
    """Aplica um desconto percentual sobre um valor.

    Args:
        valor: Valor original.
        percentual: Percentual de desconto (0-100).

    Returns:
        Valor com desconto aplicado.
    """
    if percentual < 0 or percentual > 100:
        raise ValueError("Percentual deve estar entre 0 e 100")
    return valor * (1 - percentual / 100)

# Exemplo de uso
if __name__ == "__main__":
    print(buscar_produto_por_id("1"))
    print(calcular_desconto(100.0, 15.0))
```