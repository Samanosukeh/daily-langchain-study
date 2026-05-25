```python
from langchain_core.runnables import RunnableParallel

# Exemplo básico de RunnableParallel
# Executando dois ramos em paralelo e combinando os resultados

# Definindo dois ramos simples
branch_1 = {"input": lambda x: x["texto"].upper()}
branch_2 = {"input": lambda x: x["texto"].lower()}

# Criando o RunnableParallel
parallel_runnable = RunnableParallel(branch_1=branch_1, branch_2=branch_2)

# Executando com um input
input_data = {"texto": "Hello World"}
result = parallel_runnable.invoke(input_data)

print(result)
# Saída esperada: {'branch_1': {'input': 'HELLO WORLD'}, 'branch_2': {'input': 'hello world'}}

# Exemplo mais avançado com chamadas a modelos
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Modelo
model = ChatOpenAI(model="gpt-3.5-turbo")

# Prompts diferentes para cada ramo
prompt_1 = ChatPromptTemplate.from_template("Resuma este texto em uma frase: {texto}")
prompt_2 = ChatPromptTemplate.from_template("Traduz este texto para inglês: {texto}")

# Cadeias para cada ramo
chain_1 = prompt_1 | model | StrOutputParser()
chain_2 = prompt_2 | model | StrOutputParser()

# Executando em paralelo
parallel_chain = RunnableParallel(resumo=chain_1, traducao=chain_2)

# Input
texto = "O desenvolvimento de software é uma atividade complexa que requer planejamento e execução cuidadosos."

# Invocando
resultado = parallel_chain.invoke({"texto": texto})

print("Resumo:", resultado["resumo"])
print("Tradução:", resultado["traducao"])
```