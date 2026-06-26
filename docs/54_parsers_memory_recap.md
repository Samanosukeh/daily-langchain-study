```markdown
# Resumo Mês 1.5: Parsers e Memória Integrados

## Output Parsers em LangChain

### 1. **Visão Geral**
Os **Output Parsers** em LangChain são responsáveis por:
- Validar a estrutura da resposta gerada pelo LLM.
- Extrair dados estruturados a partir do texto não estruturado.
- Garantir que a saída esteja no formato esperado pela aplicação.

---

### 2. **Tipos de Output Parsers**

#### 2.1. **StrOutputParser**
- **Uso**: Extrai texto bruto sem formatação.
- **Exemplo**:
  ```python
  from langchain_core.output_parsers import StrOutputParser
  from langchain_core.prompts import ChatPromptTemplate

  prompt = ChatPromptTemplate.from_template("Diga-me um fato interessante sobre {tema}.")
  output_parser = StrOutputParser()

  chain = prompt | model | output_parser
  resposta = chain.invoke({"tema": "Python"})
  print(resposta)  # Texto puro
  ```

#### 2.2. **PydanticOutputParser**
- **Uso**: Valida e extrai dados estruturados usando modelos Pydantic.
- **Exemplo**:
  ```python
  from pydantic import BaseModel, Field
  from langchain_core.output_parsers import PydanticOutputParser

  class Fato(BaseModel):
      assunto: str = Field(description="Assunto do fato")
      descricao: str = Field(description="Descrição do fato")

  parser = PydanticOutputParser(pydantic_object=Fato)

  prompt = ChatPromptTemplate.from_template(
      "Crie um fato sobre {tema}.\n{format_instructions}"
  )
  chain = prompt | model | parser

  resposta = chain.invoke({
      "tema": "Python",
      "format_instructions": parser.get_format_instructions()
  })
  print(resposta.assunto)  # "Python"
  ```

#### 2.3. **JsonOutputParser**
- **Uso**: Extrai dados no formato JSON.
- **Exemplo**:
  ```python
  from langchain_core.output_parsers import JsonOutputParser

  parser = JsonOutputParser()

  prompt = ChatPromptTemplate.from_template(
      "Liste 3 características de {tema}.\n{format_instructions}"
  )
  chain = prompt | model | parser

  resposta = chain.invoke({
      "tema": "Python",
      "format_instructions": parser.get_format_instructions()
  })
  print(resposta)  # {"caracteristicas": ["...", "...", "..."]}
  ```

#### 2.4. **CustomOutputParser**
- **Uso**: Parser personalizado para formatos específicos.
- **Exemplo**:
  ```python
  from typing import Dict
  from langchain_core.output_parsers import BaseOutputParser

  class CustomParser(BaseOutputParser[Dict]):
      def parse(self, text: str) -> Dict:
          return {"resposta": text.upper()}

  parser = CustomParser()
  resposta = parser.parse("Olá, mundo!")
  print(resposta)  # {"resposta": "OLÁ, MUNDO!"}
  ```

---

### 3. **Memória Integrada em LangChain**

#### 3.1. **Visão Geral**
A memória (`Memory`) permite que os LLMs mantenham contexto entre interações.
LangChain oferece várias opções de armazenamento de estado.

#### 3.2. **Tipos de Memória**

##### 3.2.1. **ConversationBufferMemory**
- **Uso**: Armazena histórico de conversas em memória.
- **Exemplo**:
  ```python
  from langchain.memory import ConversationBufferMemory

  memory = ConversationBufferMemory(return_messages=True)
  memory.save_context({"input": "Olá"}, {"output": "Oi, tudo bem?"})
  print(memory.load_memory_variables({}))  # {"history": [...]}
  ```

##### 3.2.2. **ConversationSummaryMemory**
- **Uso**: Resume o histórico em um texto compacto.
- **Exemplo**:
  ```python
  from langchain.memory import ConversationSummaryMemory
  from langchain.llms import OpenAI

  llm = OpenAI()
  memory = ConversationSummaryMemory(llm=llm)
  memory.save_context({"input": "Python é uma linguagem?"}, {"output": "Sim."})
  print(memory.load_memory_variables({}))  # {"history": "O usuário perguntou sobre Python..."}
  ```

##### 3.2.3. **ConversationBufferWindowMemory**
- **Uso**: Mantém apenas as últimas `k`