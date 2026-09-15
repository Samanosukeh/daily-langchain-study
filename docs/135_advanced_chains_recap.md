```markdown
# Resumo Mês 4.5: Chains Avançadas e Callbacks

## **Chains Avançadas**

### **SequentialChain**
Encadeia múltiplas chains em sequência, onde a saída de uma é a entrada da próxima.

```python
from langchain.chains import SequentialChain

# Chain 1
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="intermediate_output")

# Chain 2
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="final_output")

# Encadeamento
overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["input_var"],
    output_variables=["final_output"]
)

result = overall_chain({"input_var": "valor_inicial"})
```

---

### **RouterChain**
Define lógica de roteamento entre chains com base em condições.

```python
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser

# Definir destinos
destinations = ["math_chain", "physics_chain"]
default_destination = "default_chain"

# Roteador
router_chain = LLMRouterChain.from_llm(
    llm,
    destinations,
    default_destination
)

# Chains específicas
math_chain = LLMChain(llm=llm, prompt=math_prompt)
physics_chain = LLMChain(llm=llm, prompt=physics_prompt)
default_chain = LLMChain(llm=llm, prompt=default_prompt)

# MultiPromptChain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={"math_chain": math_chain, "physics_chain": physics_chain},
    default_chain=default_chain
)

result = chain.run("Resolva a equação quadrática x² - 5x + 6 = 0")
```

---

## **Callbacks**

### **Tipos de Callbacks**
- **`CallbackHandler`**: Classe base para handlers personalizados.
- **`LLMCallbackHandler`**: Para eventos do LLM.
- **`ChainCallbackHandler`**: Para eventos de chains.
- **`ToolCallbackHandler`**: Para ferramentas externas.

### **Implementação Básica**
```python
from langchain.callbacks import StdOutCallbackHandler

# Handler personalizado
class CustomHandler(StdOutCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"🚀 Iniciando LLM com prompts: {prompts}")

# Adicionar ao LLM ou Chain
llm = model.with_config(callbacks=[CustomHandler()])

# Ou em uma chain
chain = LLMChain(llm=llm, prompt=prompt).with_config(callbacks=[CustomHandler()])
```

---

### **Callbacks Personalizados**
```python
from langchain.callbacks.base import BaseCallbackHandler

class LoggingHandler(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"🔗 Chain iniciada com inputs: {inputs}")

    def on_chain_end(self, outputs, **kwargs):
        print(f"✅ Chain finalizada com outputs: {outputs}")

# Uso
chain = LLMChain(llm=llm, prompt=prompt).with_config(
    callbacks=[LoggingHandler()]
)
```

---

### **Callbacks para Ferramentas Externas**
```python
from langchain.callbacks.manager import CallbackManager
from langchain.tools import Tool

def search_tool(query: str) -> str:
    return f"Resultado para '{query}'"

tool = Tool(
    name="Search",
    func=search_tool,
    description="Útil para buscar informações."
)

# Callback para ferramenta
class ToolHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"🔍 Ferramenta iniciada com input: {input_str}")

# Executar com callback
result = tool.run(
    "Python 3.11",
    callbacks=[ToolHandler()]
)
```

---

## **Melhores Práticas**
1. **Isolamento de Callbacks**: Evite handlers que bloqueiem a execução.
2. **Logging Estruturado**: Use bibliotecas como `logging` para persistência.
3. **Performance**: Callbacks adicionam overhead; use-os apenas quando necessário.
4. **Integração com Observabilidade**: Integre com ferramentas como Prometheus ou Datadog.
```