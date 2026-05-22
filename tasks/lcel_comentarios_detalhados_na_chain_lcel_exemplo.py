```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Configuração mínima com comentários detalhados
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)  # Modelo leve para testes

# Template de prompt com instruções específicas
prompt = PromptTemplate.from_template(
    """Analise o seguinte código Python e comente cada linha com detalhes:

    Código:
    {codigo}

    Formato esperado:
    # [Linha 1] - [Explicação detalhada]
    # [Linha 2] - [Explicação detalhada]
    ...
    """
)

# Cadeia minimalista: prompt → LLM → parser
chain = prompt | llm | StrOutputParser()

# Execução com exemplo prático
codigo_exemplo = """
def calcular_media(numeros):
    total = sum(numeros)
    media = total / len(numeros)
    return media
"""

resultado = chain.invoke({"codigo": codigo_exemplo})
print(resultado)
```