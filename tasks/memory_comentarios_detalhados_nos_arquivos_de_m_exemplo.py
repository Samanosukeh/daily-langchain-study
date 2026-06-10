```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Modelo simplificado com comentários detalhados
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key="sua_chave_api_aqui"
)

# Template de prompt com instruções claras
prompt_template = PromptTemplate.from_template(
    """
    Analise o texto abaixo e gere comentários detalhados sobre:
    1. Estrutura lógica
    2. Clareza de propósito
    3. Possíveis melhorias

    Texto: {texto}
    """
)

# Cadeia de execução minimalista
chain = prompt_template | llm | StrOutputParser()

# Execução com um texto de exemplo
texto_exemplo = "A função soma recebe dois números e retorna a soma deles."
resultado = chain.invoke({"texto": texto_exemplo})

print("Comentários detalhados:")
print(resultado)
```