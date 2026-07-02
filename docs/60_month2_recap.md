```markdown
# **Resumo Mês 2: Memória, Parsers e Tools**

---

## **Tools**

### **1. Conceito Básico**
Tools são funções ou métodos que permitem que um agente (ou LLM) interaja com sistemas externos, APIs ou executar operações específicas. No LangChain, tools são integradas ao ecossistema para estender a funcionalidade dos agentes.

---

### **2. Estrutura Básica de uma Tool**
Uma tool no LangChain é definida como uma classe que herda de `BaseTool` ou implementa a interface `Tool`. Exemplo mínimo:

```python
from langchain_core.tools import BaseTool

class MinhaTool(BaseTool):
    name = "minha_tool"
    description = "Uma ferramenta de exemplo que retorna um valor aleatório."

    def _run(self, input: str) -> str:
        import random
        return f"Valor aleatório: {random.randint(1, 100)}"

# Uso
tool = MinhaTool()
print(tool.run("qualquer_input"))
```

---

### **3. Ferramentas Padrão do LangChain**
O LangChain fornece tools prontas para uso comum:

| **Tool**               | **Descrição**                                      | **Exemplo de Uso**                     |
|------------------------|----------------------------------------------------|-----------------------------------------|
| `SerpAPIWrapper`       | Consulta a API do Google (busca na web).            | `SerpAPIWrapper().run("LangChain 2024")` |
| `PythonREPL`           | Executa código Python em um ambiente seguro.       | `PythonREPL().run("print(2 + 2)")`      |
| `HumanInput`           | Solicita entrada do usuário.                       | `HumanInput().run("Digite algo: ")`     |
| `FileSystem`           | Operações básicas em arquivos (ler/escrever).      | `FileSystem().run("ler: dados.txt")`    |

---

### **4. Criando uma Tool Personalizada**
Exemplo: Tool para buscar dados de uma API REST.

```python
from langchain_core.tools import BaseTool
import requests

class BuscaCepTool(BaseTool):
    name = "busca_cep"
    description = "Busca informações de um CEP brasileiro usando a API ViaCEP."

    def _run(self, cep: str) -> str:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return f"Erro: CEP {cep} não encontrado."

# Uso
tool = BuscaCepTool()
print(tool.run("01310200"))  # Retorna dados do CEP
```

---

### **5. Integrando Tools a um Agente**
Tools podem ser passadas a um agente (`AgentExecutor`) para execução dinâmica.

```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
tools = [MinhaTool(), BuscaCepTool()]

agente = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

agente.run("Qual o CEP de São Paulo e qual o valor aleatório gerado?")
```

---

### **6. Boas Práticas**
- **Segurança**: Valide inputs para evitar injeção de código (ex.: `PythonREPL`).
- **Tratamento de Erros**: Implemente `try/except` em `_run` para lidar com falhas.
- **Descrição Clara**: A `description` deve explicar o propósito e formato do input/output.
- **Testes**: Teste tools isoladamente antes de integrar ao agente.

---

### **7. Ferramentas Avançadas**
- **Tools com Estado**: Use classes para manter estado entre chamadas.
  ```python
  class ContadorTool(BaseTool):
      name = "contador"
      description = "Conta quantas vezes foi chamado."
      count = 0

      def _run(self, _: str) -> str:
          self.count += 1
          return f"Chamado {self.count} vezes."
  ```
- **Tools Assíncronas**: Implemente `_arun` para suporte a async.
  ```python
  async def _arun(self, input: str) -> str:
      import asyncio
      await asyncio.sleep(1)
      return f"Async: {input}"
  ```

---

### **8. Debugging**
- At