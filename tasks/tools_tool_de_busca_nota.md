```markdown
# Notas Técnicas: Validação de Parâmetros em Ferramentas Customizadas do LangChain

## Introdução
Ao estender o LangChain com ferramentas customizadas (`CustomTool`), a validação de parâmetros é um aspecto secundário, mas crítico para robustez. Este documento aborda práticas para garantir integridade em ferramentas que interagem com APIs externas ou sistemas legados.

---

## Validação de Tipos e Formatos

### 1. **Uso de `pydantic.BaseModel`**
Para ferramentas com parâmetros complexos, use modelos Pydantic para validação automática:

```python
from pydantic import BaseModel, Field, validator

class UserInput(BaseModel):
    user_id: int = Field(..., gt=0, description="ID do usuário (positivo)")
    email: str = Field(..., regex=r"^[^@]+@[^@]+\.[^@]+$")

    @validator("user_id")
    def check_id(cls, v):
        if v > 1_000_000:
            raise ValueError("ID muito grande")
        return v
```

**Integração com `CustomTool`:**
```python
from langchain.tools import tool

@tool
def fetch_user_data(input: UserInput) -> dict:
    """Busca dados de usuário por ID e e-mail."""
    # input já validado automaticamente
    ...
```

---

### 2. **Validação Manual em Ferramentas Simples**
Para ferramentas com parâmetros simples, valide explicitamente:

```python
from typing import Optional
from langchain.tools import tool

@tool
def search_products(query: str, max_results: Optional[int] = 10) -> list:
    """Busca produtos por query."""
    if not query.strip():
        raise ValueError("Query não pode ser vazia")
    if max_results and max_results <= 0:
        raise ValueError("max_results deve ser positivo")
    ...
```

---

## Tratamento de Erros

### 1. **Erros Amigáveis para o Usuário Final**
Evite expor detalhes internos. Exemplo:

```python
try:
    response = api_client.get(f"/users/{user_id}")
    response.raise_for_status()
except requests.HTTPError as e:
    raise ValueError(f"Usuário não encontrado (ID: {user_id})") from None
```

### 2. **Logs para Depuração**
Registre erros internos sem expor ao usuário:

```python
import logging

logger = logging.getLogger(__name__)

try:
    ...
except Exception as e:
    logger.error(f"Falha ao buscar usuário {user_id}: {e}", exc_info=True)
    raise
```

---

## Boas Práticas Adicionais

1. **Documentação Clara:**
   - Use `Field` do Pydantic ou docstrings para descrever restrições.
   - Exemplo: `Field(..., description="Deve ser uma string não vazia")`.

2. **Testes Automatizados:**
   - Teste casos válidos e inválidos:
     ```python
     import pytest

     def test_invalid_user_id():
         with pytest.raises(ValueError):
             fetch_user_data(UserInput(user_id=-1, email="invalido"))
     ```

3. **Performance:**
   - Validações pesadas (ex: regex complexas) podem ser otimizadas com cache ou pré-processamento.

---

## Conclusão
A validação de parâmetros em ferramentas LangChain deve balancear:
- **Robustez** (evitar erros silenciosos).
- **Clareza** (mensagens de erro úteis).
- **Manutenibilidade** (código testável e documentado).
```