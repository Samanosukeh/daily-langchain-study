```python
# Lições aprendidas: 6 - Validação de dados é crucial antes de processar com LLM

from typing import List, Dict
from pydantic import BaseModel, ValidationError

class UserInput(BaseModel):
    nome: str
    idade: int
    interesses: List[str]

def processar_dados_entrada(raw_data: Dict) -> UserInput:
    try:
        # Validação automática com Pydantic
        validated = UserInput(**raw_data)
        return validated
    except ValidationError as e:
        print(f"Erro de validação: {e}")
        raise ValueError("Dados de entrada inválidos")

# Exemplo de uso
if __name__ == "__main__":
    entrada_ruim = {"nome": "Ana", "idade": "30", "interesses": ["Python"]}
    entrada_bom = {"nome": "João", "idade": 25, "interesses": ["AI", "ML"]}

    try:
        user = processar_dados_entrada(entrada_bom)
        print(f"Dados validados: {user.model_dump()}")
    except ValueError:
        print("Falha ao processar dados")
```