```markdown
# Notas Técnicas: Tratamento de Comentários em LangChain

## Validação de Comentários com `pydantic`

Ao integrar comentários em pipelines LangChain, é comum validar estruturas antes de processamento. Exemplo prático com `pydantic`:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class Comentario(BaseModel):
    texto: str = Field(..., min_length=3, max_length=500)
    autor: str = Field(..., regex=r"^[a-zA-Z0-9_]{3,20}$")
    id_post: Optional[int] = None

    @validator('texto')
    def texto_sem_urls(cls, v):
        if "http" in v.lower():
            raise ValueError("Comentário não pode conter URLs")
        return v

# Uso
try:
    comentario = Comentario(
        texto="Ótima explicação!",
        autor="dev123",
        id_post=42
    )
except ValueError as e:
    print(f"Comentário inválido: {e}")
```

### Pontos-chave:
1. **Validação de campo**: Limites de tamanho e regex para `autor`
2. **Validação customizada**: Rejeita URLs no texto
3. **Tipagem**: `Optional` para campos não obrigatórios
4. **Integração**: Estrutura pronta para uso em `LangChain` como `prompt_template`

### Boas práticas:
- Armazenar schemas em módulos separados (`schemas/comentario.py`)
- Usar `Field` para documentação automática (útil em `LangSmith`)
- Validar antes de passar para LLMs para reduzir custos de tokens
```