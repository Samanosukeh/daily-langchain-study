```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Definindo o prompt template
prompt = ChatPromptTemplate.from_template(
    "Resuma o seguinte texto em uma única frase: {text}"
)

# Inicializando o modelo de linguagem
llm = ChatOpenAI(model="gpt-4o-mini")

# Criando a chain usando LCEL
chain = prompt | llm | StrOutputParser()

# Executando a chain com um input
input_text = "A linguagem Python foi criada por Guido van Rossum em 1991. É uma linguagem de programação de alto nível, interpretada e de propósito geral."
result = chain.invoke({"text": input_text})

print(result)
```