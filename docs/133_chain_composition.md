```markdown
# **Resumo: Composição de Chains Complexas**
**Tópico:** `chains_advanced`

---

## **1. Introdução**
A composição de chains avançadas em LangChain permite criar pipelines de processamento de linguagem natural (PLN) modulares, reutilizáveis e escaláveis. Essa abordagem é essencial para resolver problemas complexos, como:
- **Encadeamento de múltiplas LLMs** (ex.: pré-processamento, geração, pós-processamento).
- **Integração com ferramentas externas** (APIs, bancos de dados, armazenamento vetorial).
- **Fluxos condicionais** (ex.: branchs baseados em lógica ou saída de modelos).
- **Pipelines dinâmicos** (ex.: ajustar comportamento em tempo de execução).

---

## **2. Conceitos-Chave**

### **2.1. `Chain` vs. `LLMChain`**
| **Componente**       | **Descrição**                                                                                     | **Uso Típico**                          |
|----------------------|---------------------------------------------------------------------------------------------------|-----------------------------------------|
| `Chain`              | Interface base para composição de componentes LangChain.                                          | Herança para chains personalizadas.     |
| `LLMChain`           | Chain específica para interagir com LLMs (usa `PromptTemplate` + `LLM`).                          | Geração de texto simples.               |

### **2.2. Tipos de Composition**
LangChain oferece mecanismos para combinar chains de forma **sequencial**, **paralela** ou **condicional**.

---

## **3. Composição Sequencial**
Encadeia chains em uma sequência linear, onde a saída de uma é entrada para a próxima.

### **3.1. Usando `SimpleSequentialChain`**
Ideal para pipelines lineares simples.

```python
from langchain.chains import SimpleSequentialChain
from langchain.llms import OpenAI

# Chain 1: Gera um título para um tema
chain1 = LLMChain(llm=OpenAI(), prompt=PromptTemplate.from_template("Crie um título para: {tema}"))

# Chain 2: Gera um resumo para o título gerado
chain2 = LLMChain(llm=OpenAI(), prompt=PromptTemplate.from_template("Resuma este título: {title_output}"))

# Composição
overall_chain = SimpleSequentialChain(
    chains=[chain1, chain2],
    verbose=True
)

output = overall_chain.run("Aprendizado de máquina")
print(output)
```

### **3.2. Usando `SequentialChain`**
Permite múltiplas entradas/saídas entre chains.

```python
from langchain.chains import SequentialChain

chain1 = LLMChain(llm=OpenAI(), prompt=PromptTemplate.from_template("Crie um título para: {tema}"), output_key="title")
chain2 = LLMChain(llm=OpenAI(), prompt=PromptTemplate.from_template("Resuma este título: {title}"), output_key="summary")

overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["tema"],
    output_variables=["title", "summary"],
    verbose=True
)

output = overall_chain({"tema": "Processamento de linguagem natural"})
print(output)
```

---

## **4. Composição Paralela**
Executa múltiplas chains **simultaneamente** e combina os resultados.

### **4.1. Usando `ParallelSequentialChain`**
Encadeia chains em paralelo dentro de uma sequência.

```python
from langchain.chains import ParallelSequentialChain

# Chain 1: Gera um título
chain1 = LLMChain(llm=OpenAI(), prompt=PromptTemplate.from_template("Crie um título para: {tema}"), output_key="title")

# Chain 2: Gera uma pergunta sobre o tema
chain2 = LLMChain(llm=OpenAI(), prompt=PromptTemplate.from_template("Crie uma pergunta sobre: {tema}"), output_key="question")

# Composição paralela
par_chain = ParallelSequentialChain(
    chains=[chain1, chain2],
    input_variables=["tema"],
    verbose=True
)

output = par_chain({"tema": "Visão computacional"})
print(output)
```

---

## **5. Composição Condicional**
Executa chains com base em **condições dinâmicas** (ex.: saída de um modelo, variáveis externas).

### **5.1. Usando `RouterChain`**
Define rotas com base em critérios (ex.: tipo de pergunta).

```python
from langchain.chains.router import MultiPromptChain
from langchain.ch