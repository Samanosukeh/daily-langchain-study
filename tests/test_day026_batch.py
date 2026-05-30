```python
import pytest
from typing import List, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def test_batch_retorna_lista_mesmo_tamanho_input():
    """Teste: batch retorna lista com mesmo tamanho do input"""
    # Setup
    template = ChatPromptTemplate.from_messages([
        ("system", "Responda em português: {input}"),
        ("user", "{input}")
    ])
    chain = template | StrOutputParser()

    inputs = ["Olá", "Como você está?", "Qual é o seu nome?"]

    # Execução
    outputs = chain.batch(inputs)

    # Assertions
    assert isinstance(outputs, list), "O output deve ser uma lista"
    assert len(outputs) == len(inputs), "O tamanho da lista de output deve ser igual ao do input"
    assert all(isinstance(output, str) for output in outputs), "Todos os outputs devem ser strings"
```