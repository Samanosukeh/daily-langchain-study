```markdown
# Resumo: Tipos de Tools e Quando Usar Cada Um

## **1. Ferramentas de Busca (Search Tools)**
**Quando usar:**
- Quando o agente precisa buscar informações em bases de dados externas (ex: Google, Wikipedia, APIs).
- Para consultas que exigem dados atualizados ou específicos.

**Exemplos:**
```python
from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
```

---

## **2. Ferramentas de API (API Tools)**
**Quando usar:**
- Para interagir com serviços externos via HTTP (ex: APIs REST, GraphQL).
- Quando a lógica de negócio depende de dados dinâmicos.

**Exemplo:**
```python
from langchain.tools import APIOperation
api_tool = APIOperation(
    name="get_weather",
    api_wrapper=WeatherAPIWrapper(api_key="SUA_CHAVE")
)
```

---

## **3. Ferramentas de Banco de Dados (Database Tools)**
**Quando usar:**
- Para executar queries SQL ou NoSQL.
- Quando o agente precisa manipular dados estruturados.

**Exemplo:**
```python
from langchain.utilities import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///exemplo.db")
db_tool = QuerySQLDatabaseTool(db=db)
```

---

## **4. Ferramentas de Arquivos (File Tools)**
**Quando usar:**
- Para ler, gravar ou analisar arquivos locais (JSON, CSV, TXT).
- Quando o agente precisa processar dados persistentes.

**Exemplo:**
```python
from langchain.tools import FileSystemTool
file_tool = FileSystemTool(
    root_dir="./data",
    allowed_extensions=[".txt", ".csv"]
)
```

---

## **5. Ferramentas de Código (Code Tools)**
**Quando usar:**
- Para executar scripts Python ou shell.
- Quando a tarefa exige lógica computacional complexa.

**Exemplo:**
```python
from langchain.tools import PythonREPLTool
code_tool = PythonREPLTool()
```

---

## **6. Ferramentas Personalizadas (Custom Tools)**
**Quando usar:**
- Para lógica específica não coberta por tools nativas.
- Quando é necessário encapsular uma função personalizada.

**Exemplo:**
```python
from langchain.tools import StructuredTool
def minha_funcao(arg1: str, arg2: int) -> str:
    return f"Resultado: {arg1} {arg2}"

custom_tool = StructuredTool.from_function(
    func=minha_funcao,
    name="minha_funcao_customizada",
    description="Processa dados customizados."
)
```

---

## **7. Ferramentas de Memória (Memory Tools)**
**Quando usar:**
- Para armazenar ou recuperar contexto entre interações.
- Quando o agente precisa "lembrar" informações anteriores.

**Exemplo:**
```python
from langchain.memory import ConversationBufferMemory
memory_tool = ConversationBufferMemory(return_messages=True)
```

---
**Guia Rápido de Escolha:**
| **Tipo de Tool**       | **Use quando...**                          |
|-------------------------|--------------------------------------------|
| Busca (Search)          | Precisa de dados externos.                 |
| API                     | Interage com serviços web.                 |
| Banco de Dados          | Manipula dados estruturados.               |
| Arquivos                | Processa dados locais.                     |
| Código                  | Executa lógica computacional.              |
| Personalizada           | Necessita de lógica customizada.           |
| Memória                 | Precisa manter contexto entre interações.  |
```