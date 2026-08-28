```python
from langchain.callbacks import StdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Configuração inicial
llm = OpenAI(temperature=0.9)
prompt = PromptTemplate.from_template("Diga-me um fato interessante sobre {topic}.")

# Instância do callback handler
handler = StdOutCallbackHandler()

# Criação da cadeia com o callback
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])

# Execução com saída detalhada no terminal
chain.run(topic="Python")
```