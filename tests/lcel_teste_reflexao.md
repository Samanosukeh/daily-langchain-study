```markdown
# Reflexão: `RunnableParallel` retornando dicionário vazio

Ao trabalhar com `RunnableParallel` no LangChain, deparei-me com um comportamento inesperado: o retorno vazio de um dicionário quando uma das *runnables* falha ou não produz saída. Isso ocorreu em um pipeline onde uma cadeia de processamento tinha uma etapa opcional (ex: *retriever* que pode não encontrar documentos).

**Causa raiz**:
O `RunnableParallel` não propaga exceções nem falhas silenciosas por padrão. Se uma *runnable* interna lançar uma exceção ou retornar `None`, o dicionário resultante simplesmente omite aquela chave, sem alerta.

**Solução prática**:
1. **Validação explícita**: Adicionar um passo de pós-processamento para verificar chaves ausentes.
   ```python
   def validate_output(output: dict) -> dict:
       if "retriever" not in output:
           output["retriever"] = "Sem resultados"  # ou lançar exceção customizada
       return output
   ```
2. **Tratamento de exceções**: Usar `try-catch` dentro das *runnables* ou um *fallback* via `RunnablePassthrough`.
3. **Debug**: Ativar logs com `langchain.debug = True` para rastrear onde a falha ocorre.

**Lições**:
- `RunnableParallel` é "otimista": assume que todas as *runnables* executam com sucesso.
- Em pipelines críticos, sempre validar saídas intermediárias.
- A flexibilidade do LangChain exige atenção a casos de borda — o que é uma feature para alguns, pode ser um *footgun* para outros.
```