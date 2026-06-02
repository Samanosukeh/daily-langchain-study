```markdown
# **Resumo Mês 1: Do LLM Call à ChaiLangChain**

## **1. Chamada Direta ao LLM (Sem Frameworks)**
- **Exemplo Básico**:
  ```python
  from openai import OpenAI

  client = OpenAI(api_key="SUA_CHAVE")
  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": "Explique cadeias de Markov em 3 linhas."}]
  )
  print(response.choices[0].message.content)
  ```
- **Problemas**:
  - Sem persistência de contexto.
  - Sem integração com ferramentas externas.
  - Sem gerenciamento de prompts complexos.

---

## **2. Primeiros Passos com LangChain**
### **2.1. Prompts e Modelos**
- **Template de Prompt**:
  ```python
  from langchain_core.prompts import ChatPromptTemplate

  template = ChatPromptTemplate.from_messages([
      ("system", "Você é um assistente especializado em {tema}."),
      ("user", "{input}")
  ])
  chain = template | client  # Encadeamento simples
  response = chain.invoke({"tema": "Python", "input": "O que é um decorator?"})
  ```
- **Vantagens**:
  - Reutilização de prompts.
  - Separação clara entre *system* e *user*.

### **2.2. Ferramentas Externas (Tools)**
- **Exemplo com DuckDuckGo**:
  ```python
  from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

  search = DuckDuckGoSearchAPIWrapper()
  tool = search.run("Notícias sobre IA em 2024")
  ```
- **Integração com LLM**:
  ```python
  from langchain_core.tools import Tool

  tools = [Tool(
      name="Busca IA",
      func=search.run,
      description="Busca informações recentes sobre IA."
  )]
  ```

---

## **3. ChaiLangChain: Simplificação Radical**
### **3.1. Conceito**
- **Foco**: Automação de workflows com LLM + ferramentas.
- **Exemplo**:
  ```python
  from chain import Chain

  workflow = Chain(
      prompt="Resuma o artigo: {article}",
      tools=[search.run],
      output_key="resumo"
  )
  result = workflow.run(article="URL_DO_ARTIGO")
  ```

### **3.2. Vantagens sobre LangChain Puro**
| **Critério**          | **LangChain**               | **ChaiLangChain**          |
|-----------------------|----------------------------|----------------------------|
| **Complexidade**      | Alto (muitos módulos)      | Baixo (abstração simples)  |
| **Setup**             | Configuração manual        | Pronta para uso            |
| **Integrações**       | Limitadas sem config       | Nativas (ex: DuckDuckGo)   |
| **Performance**       | Overhead de inicialização  | Otimizado para flows       |

### **3.3. Quando Usar?**
- **LangChain**: Projetos complexos com múltiplas cadeias.
- **ChaiLangChain**: Scripts rápidos, automações e POCs.

---
## **4. Lições Aprendidas**
- **LangChain** é poderoso, mas exige curva de aprendizado.
- **ChaiLangChain** acelera desenvolvimento para casos simples.
- **Ferramentas externas** são essenciais para workflows dinâmicos.
```