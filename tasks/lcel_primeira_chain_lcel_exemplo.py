```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Configuração mínima
llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Responda de forma direta e objetiva."),
    ("user", "{input}")
])

# Chain LCEL
chain = prompt | llm | StrOutputParser()

# Execução
response = chain.invoke({"input": "Qual a capital da França?"})
print(response)
```