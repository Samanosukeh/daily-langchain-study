```markdown
# Notas Técnicas: Comentários em Python com LangChain

## Tratamento de Comentários Multilinha no Pré-processamento

Ao integrar LangChain com fontes de dados que incluem comentários multilinha (ex: código Python, documentação), é necessário normalizar o texto antes de repassá-lo ao modelo.

### Solução Proposta

```python
import re

def normalize_multiline_comments(text: str) -> str:
    """
    Remove ou padroniza comentários multilinha antes de processamento.
    Opções:
    1. Remover completamente (padrão):
       text = re.sub(r'#.*?$|""".*?"""|\'\'\'.*?\'\'\'', '', text, flags=re.M|re.S)
    2. Substituir por espaços (preserva estrutura):
       text = re.sub(r'(#.*?$|""".*?"""|\'\'\'.*?\'\'\')', ' ', text, flags=re.M|re.S)
    """
    # Remove comentários de linha única e blocos docstring
    cleaned = re.sub(
        r'#.*?$|""".*?"""|\'\'\'.*?\'\'\'',
        '',
        text,
        flags=re.MULTILINE | re.DOTALL
    )
    return cleaned.strip()
```

### Considerações

1. **Regex**: O padrão `#.*?$` captura comentários de linha única, enquanto `""".*?"""` e `'''.*?'''` capturam docstrings.
2. **Performance**: Para grandes volumes de texto, considere pré-compilar o regex.
3. **Edge Cases**:
   - Strings que contenham padrões de comentários (ex: `"# não é comentário"`)
   - Comentários aninhados (não suportado nativamente)

### Integração com LangChain

```python
from langchain.document_loaders import TextLoader

loader = TextLoader("codigo.py")
docs = loader.load()

for doc in docs:
    doc.page_content = normalize_multiline_comments(doc.page_content)
```

**Nota**: Para casos onde os comentários são relevantes (ex: documentação), substitua por espaços em branco para manter a estrutura do texto.
```