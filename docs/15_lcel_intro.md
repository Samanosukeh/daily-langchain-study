```markdown
# **LCEL (LangChain Expression Language)**

O **LangChain Expression Language (LCEL)** é uma linguagem declarativa projetada para facilitar a composição de cadeias de processamento (pipelines) em aplicações com modelos de linguagem (LLMs). Ela permite criar fluxos de trabalho complexos de forma simples e legível, integrando componentes como LLMs, retrievers, ferramentas e transformadores.

---

## **Características Principais**
- **Declarativo**: Define o fluxo de dados sem detalhar a execução.
- **Composicional**: Permite combinar componentes de forma modular.
- **Assíncrono**: Suporta execução assíncrona (`async/await`).
- **Streaming**: Processa dados em tempo real (útil para LLMs).
- **Invocação Flexível**: Suporta chamadas síncronas e assíncronas.

---

## **Estrutura Básica**
Um pipeline LCEL é composto por **componentes** (funções ou objetos) conectados por operadores (`|`). Exemplo:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Definindo componentes
prompt = ChatPromptTemplate.from_template("Diga-me um {adjetivo} fato sobre {tópico}.")
llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

# Pipeline LCEL
chain = prompt | llm | output_parser

# Execução
resultado = chain.invoke({"adjetivo": "curioso", "tópico": "Python"})
print(resultado)
```

---

## **Operadores LCEL**
| Operador | Descrição                          | Exemplo                     |
|----------|------------------------------------|-----------------------------|
| `|`      | Encadeia componentes.              | `chain1 | chain2`          |
| `+`      | Combina prompts ou saídas.         | `prompt1 + prompt2`         |
| `>>`     | Redireciona saída para entrada.    | `chain1 >> chain2`          |
| `*`      | Repete um componente N vezes.      | `chain * 3`                 |

---

## **Componentes Comuns**
1. **Prompts**: `ChatPromptTemplate`, `PromptTemplate`.
2. **LLMs**: `ChatOpenAI`, `ChatAnthropic`.
3. **Retrievers**: `VectorStoreRetriever`.
4. **Output Parsers**: `StrOutputParser`, `JsonOutputParser`.
5. **Ferramentas**: `Tool`, `function_tool`.

---

## **Exemplo Prático: RAG com LCEL**
```python
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings

# Carrega vetor de documentos
vetor_db = FAISS.from_texts(["Python é uma linguagem de programação.", "LangChain é uma biblioteca."], OpenAIEmbeddings())
retriever = vetor_db.as_retriever()

# Pipeline RAG
prompt = ChatPromptTemplate.from_template("Responda sobre: {pergunta}\nContexto: {contexto}")
llm = ChatOpenAI()
output_parser = StrOutputParser()

chain = (
    {"contexto": retriever, "pergunta": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

resultado = chain.invoke("O que é Python?")
print(resultado)
```

---

## **Vantagens do LCEL**
- **Simplicidade**: Sintaxe clara e intuitiva.
- **Reutilização**: Componentes podem ser reutilizados em diferentes pipelines.
- **Performance**: Otimizado para streaming e execução assíncrona.
- **Integração**: Funciona com todos os módulos do LangChain.

---
## **Quando Usar LCEL?**
- Criação de **cadeias de RAG** (Retrieval-Augmented Generation).
- **Orquestração de ferramentas** (ex: agentes).
- **Processamento sequencial** de dados (ex: pré/pós-processamento de prompts).
- **Aplicações que exigem streaming** (ex: chatbots em tempo real).

---
## **Recursos Adicionais**
- [Documentação Oficial LCEL](https://python.langchain.com/docs/expression_language/)
- [Exemplos no GitHub LangChain](https://github.com/langchain-ai/langchain/tree/master/examples)
- [Tutorial: Criando um Agente com LCE