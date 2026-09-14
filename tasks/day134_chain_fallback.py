```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# Modelo primário (ex: GPT-4)
primary_model = ChatOpenAI(model="gpt-4", temperature=0.7)

# Modelo alternativo (ex: Llama2 via API local ou outro provedor)
alternative_model = ChatOpenAI(model="llama2", base_url="http://localhost:11434/v1", api_key="ollama")

# Template de prompt
prompt = ChatPromptTemplate.from_template(
    "Resuma em 3 linhas o seguinte texto:\n{text}"
)

# Chain principal com fallback
chain = (
    {"text": RunnablePassthrough()}
    | prompt
    | primary_model
    | StrOutputParser()
).with_fallbacks([alternative_model])

# Execução
texto = """
LangChain é uma estrutura para desenvolver aplicações com LLMs.
Ela permite encadear chamadas a modelos de linguagem de forma modular.
Também suporta integração com diversas fontes de dados e APIs.
"""

resultado = chain.invoke(texto)
print(resultado)
```