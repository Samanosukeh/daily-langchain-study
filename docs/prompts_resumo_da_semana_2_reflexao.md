```markdown
## Resumo da semana 2: PromptTemplate e LangChain

A segunda semana foi focada em **`PromptTemplate`**, uma ferramenta essencial do LangChain para padronizar e reutilizar *prompts* em aplicações LLM. A abstração permite criar templates dinâmicos com variáveis, facilitando a integração com modelos de linguagem.

### Principais aprendizados:
1. **Estrutura básica**:
   ```python
   from langchain.prompts import PromptTemplate
   template = PromptTemplate.from_template("Diga um {adjetivo} sobre {tema}.")
   ```
   - Suporte a *f-strings* e variáveis nomeadas.
   - Validação de variáveis obrigatórias no `format()`.

2. **Flexibilidade**:
   - Integração com `ChatPromptTemplate` para modelos conversacionais.
   - Suporte a *few-shot examples* via `FewShotPromptTemplate`.

3. **Boas práticas**:
   - **Evitar *prompt injection*** com validação de inputs.
   - **Cache de prompts** para otimizar custos em chamadas repetidas.
   - **Logging** para debugar templates complexos.

### Desafios:
- **Complexidade em templates longos**: Manter clareza sem perder contexto.
- **Dependência de contexto**: Modelos podem ignorar instruções em prompts muito longos.

### Próximos passos:
Explorar **`OutputParser`** para lidar com respostas estruturadas do LLM, fechando o ciclo de *input → processamento → output*.
```