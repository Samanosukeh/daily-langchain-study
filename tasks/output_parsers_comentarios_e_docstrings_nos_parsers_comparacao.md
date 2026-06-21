```markdown
| **Aspecto**          | **Comentários no Código**                     | **Docstrings**                              |
|----------------------|-----------------------------------------------|---------------------------------------------|
| **Objetivo**         | Explicar trechos complexos ou decisões de código. | Documentar funções, classes e módulos para geração automática de docs. |
| **Localização**      | Qualquer lugar no código (linhas, blocos).     | Imediatamente após a definição de funções, classes ou módulos. |
| **Sintaxe**          | `# Comentário`                                | `"""Docstring aqui"""`                     |
| **Ferramentas**      | Não são processadas por ferramentas de doc.   | Suportadas por `pydoc`, `Sphinx`, `mkdocs`. |
| **Boas Práticas**    | Evitar comentários óbvios; focar em "porquês". | Seguir PEP 257 (formato Google, NumPy, etc.). |
| **Exemplo**          | `# Calcula média ponderada (evita overflow)`  | `"""Calcula média ponderada de valores.\n\nArgs:\n    valores: Lista de números.\nReturns:\n    Média ponderada.\n"""` |
| **Geração de Docs**  | Não gera documentação automática.             | Permite exportar para HTML/PDF via Sphinx. |
| **Manutenção**       | Risco de desatualização com refatorações.     | Centraliza docs junto ao código (melhor manutenção). |
| **Uso em LangChain** | Útil para explicar lógica de prompts ou chains. | Essencial para documentar `CustomLLMs`, `Chains` e `Agents`. |
```