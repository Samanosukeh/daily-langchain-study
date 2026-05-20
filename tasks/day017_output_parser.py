```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Definindo o template do prompt
prompt = ChatPromptTemplate.from_template(
    "Resuma o seguinte texto em uma única frase: {texto}"
)

# Criando o pipeline com StrOutputParser
output_parser = StrOutputParser()

# Exemplo de uso
texto = "LangChain é uma estrutura para desenvolver aplicações com modelos de linguagem de forma rápida e fácil."

chain = prompt | output_parser

resultado = chain.invoke({"texto": texto})
print(resultado)
```