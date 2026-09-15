```markdown
# Notas Técnicas: Extração de Entidades em Resumos com LangChain

## Contexto
Ao implementar um pipeline de resumo com LangChain, a extração de entidades (NER) pode ser um aspecto secundário útil para:
- Categorizar tópicos-chave
- Melhorar a busca semântica
- Validar a coerência do resumo

## Implementação Prática

### 1. Pipeline Básico
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

prompt = ChatPromptTemplate.from_template(
    """Extraia entidades do seguinte texto em formato JSON:

    Texto: {texto}

    Formato esperado:
    {{
        "entidades": [
            {{"tipo": "pessoa", "valor": "..."}},
            {{"tipo": "organização", "valor": "..."}},
            ...
        ]
    }}"""
)

chain = prompt | llm | StrOutputParser()
```

### 2. Integração com Resumo
```python
from langchain.chains import SequentialChain

resumo_chain = ...  # Seu chain de resumo existente

full_chain = SequentialChain(
    chains=[resumo_chain, chain],
    input_variables=["texto_original"],
    output_variables=["resumo", "entidades"]
)
```

### 3. Validação de Saída
```python
import json
from typing import List, Dict

def validar_entidades(entidades: str) -> List[Dict]:
    try:
        dados = json.loads(entidades)
        return dados["entidades"]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro na extração: {e}")
        return []
```

## Observações
- **Performance**: Modelos menores (7B) podem perder precisão em NER
- **Custo**: Adicionar +20-30% de tempo de execução
- **Alternativa**: Usar spaCy como fallback para entidades críticas

## Exemplo de Saída
```json
{
    "entidades": [
        {"tipo": "pessoa", "valor": "Elon Musk"},
        {"tipo": "organização", "valor": "Tesla"},
        {"tipo": "local", "valor": "Berlim"}
    ]
}
```