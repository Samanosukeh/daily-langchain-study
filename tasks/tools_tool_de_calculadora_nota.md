```markdown
# Notas Técnicas: Integração de Ferramentas de Conversão de Formato em LangChain

## Contexto
LangChain permite estender suas capacidades com ferramentas externas (`tools`). Um aspecto secundário, mas útil, é a conversão de formatos de dados entre etapas de um *pipeline* de processamento.

## Implementação: Ferramenta de Conversão JSON ↔ CSV

### Dependências
```bash
pip install pandas python-dotenv langchain
```

### Código Base
```python
from langchain_core.tools import tool
import pandas as pd
import json
from typing import Union, Dict, List

@tool
def json_to_csv(json_data: Union[str, Dict, List[Dict]]) -> str:
    """Converte dados JSON para CSV.
    Args:
        json_data: JSON como string, dict ou lista de dicts.
    Returns:
        CSV como string.
    """
    df = pd.json_normalize(json_data)
    return df.to_csv(index=False)

@tool
def csv_to_json(csv_data: str) -> str:
    """Converte dados CSV para JSON.
    Args:
        csv_data: CSV como string.
    Returns:
        JSON como string.
    """
    df = pd.read_csv(pd.compat.StringIO(csv_data))
    return df.to_json(orient="records")
```

### Uso em Chain
```python
from langchain_core.runnables import RunnablePassthrough

conversor = {
    "json_input": RunnablePassthrough(),
    "csv_output": json_to_csv
} | {
    "csv_input": RunnablePassthrough(),
    "json_output": csv_to_json
}

# Exemplo de execução
resultado = conversor.invoke({"json_input": '[{"a": 1, "b": 2}]'})
print(resultado["csv_output"])  # CSV gerado
```

### Observações
1. **Tratamento de Erros**: Adicione validações para JSON/CVS inválidos.
2. **Desempenho**: Para grandes volumes, considere `polars` em vez de `pandas`.
3. **Segurança**: Sanitize inputs se origem for não confiável.

## Referências
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [Pandas I/O](https://pandas.pydata.org/docs/reference/io.html)
```