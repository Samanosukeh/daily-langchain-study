```markdown
# **Resumo Mês 4.5: Chains Avançadas em LangChain**

## **1. Chains Personalizadas**
- Use `RunnablePassthrough` para passar dados sem modificação:
  ```python
  from langchain_core.runnables import RunnablePassthrough
  chain = {"input": RunnablePassthrough()} | llm
  ```
- Combine múltiplas chains com `SequentialChain` ou `SimpleSequentialChain`.

## **2. Chains com Memória**
- Adicione memória (`ConversationBufferMemory`) para contexto:
  ```python
  from langchain.memory import ConversationBufferMemory
  memory = ConversationBufferMemory(return_messages=True)
  chain = prompt | llm | output_parser
  ```
- Use `ConversationChain` para diálogos contínuos.

## **3. Chains com Ferramentas (Tools)**
- Integre ferramentas externas com `Tool` e `LLMChain`:
  ```python
  from langchain.tools import Tool
  tool = Tool.from_function(func=buscar_dados, name="BuscarDados")
  chain = llm.bind_tools([tool])
  ```
- Use `AgentExecutor` para chains orientadas a ações.

## **4. Chains com Saída Estruturada**
- Valide saídas com `PydanticOutputParser`:
  ```python
  from langchain.output_parsers import PydanticOutputParser
  parser = PydanticOutputParser(pydantic_object=Resposta)
  chain = prompt | llm | parser
  ```

## **5. Chains Paralelas**
- Execute múltiplas chains em paralelo com `RunnableParallel`:
  ```python
  from langchain_core.runnables import RunnableParallel
  parallel_chain = RunnableParallel({"resposta1": chain1, "resposta2": chain2})
  ```

## **6. Chains com Condicionais**
- Use `RunnableBranch` para lógica condicional:
  ```python
  from langchain_core.runnables import RunnableBranch
  branch = RunnableBranch(
      (condição1, chain1),
      (condição2, chain2),
      default_chain
  )
  ```

## **7. Otimização de Performance**
- Cache resultados com `cache=True` em `LLMChain`.
- Use `async` para chains não-bloqueantes:
  ```python
  async for chunk in chain.astream({"input": "..."}):
      print(chunk)
  ```

---
**Dica Final:** Sempre teste chains com `debug=True` para inspecionar fluxos:
```python
chain.invoke({"input": "..."}, config={"verbose": True})
```
```