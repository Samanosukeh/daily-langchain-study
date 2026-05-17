```markdown
# 📌 Resumo da Semana 2: PromptTemplate e LangChain Expression Language (LCEL)

## 🔹 PromptTemplate
- **Objetivo**: Criar templates reutilizáveis para prompts com variáveis dinâmicas.
- **Exemplo Básico**:
  ```python
  from langchain_core.prompts import PromptTemplate

  template = "Dê um resumo de {tema} em {palavras} palavras."
  prompt = PromptTemplate.from_template(template)
  prompt.format(tema="Python", palavras=50)
  ```
- **Saída**:
  ```text
  Dê um resumo de Python em 50 palavras.
  ```
- **Boas Práticas**:
  - Use `{variaveis}` para parâmetros dinâmicos.
  - Valide a saída com `.validate()` (se necessário).

---

## 🔹 LangChain Expression Language (LCEL)
- **Objetivo**: Construir cadeias de execução de forma declarativa.
- **Exemplo Simples**:
  ```python
  from langchain_core.output_parsers import StrOutputParser
  from langchain_core.prompts import ChatPromptTemplate

  prompt = ChatPromptTemplate.from_template("Diga um fato sobre {tema}.")
  chain = prompt | model | StrOutputParser()  # Pipeline LCEL
  chain.invoke({"tema": "IA"})
  ```
- **Componentes Comuns**:
  - `|` (pipe): Encadeia operações (ex: `prompt → model → parser`).
  - `StrOutputParser()`: Converte saída do LLM para string.

---
## 🔹 Dicas Rápidas
1. **PromptTemplate**:
   - Use `from_template()` para criar templates rapidamente.
   - Combine com `ChatPromptTemplate` para modelos de chat.

2. **LCEL**:
   - Encadeie componentes com `|` para fluxos claros.
   - Use `StrOutputParser()` para padronizar saídas.

3. **Debug**:
   - Verifique templates com `.format()` antes de executar.
   - Teste cadeias pequenas antes de complexas.

---
## 🔹 Exemplo Prático
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("Explique {conceito} como se eu tivesse 5 anos.")
chain = prompt | model

response = chain.invoke({"conceito": "fotossíntese"})
print(response.content)
```
```