```markdown
# Reflexão sobre `ChatPromptTemplate` com `system_message`

O uso de `ChatPromptTemplate` com `system_message` no LangChain é uma abordagem poderosa para estabelecer contexto inicial em sistemas de IA conversacional. Ao definir um `system_message`, você injeta instruções fixas que guiam o comportamento do modelo antes mesmo da interação do usuário começar. Isso é particularmente útil para:

- **Consistência**: Garantir que o modelo sempre responda dentro de um escopo pré-definido (ex.: "Você é um assistente técnico especializado em Python").
- **Eficiência**: Reduzir a necessidade de repetir instruções em cada interação, já que o contexto é mantido no template.
- **Controle**: Evitar desvios indesejados do comportamento esperado, como respostas genéricas ou fora do domínio.

Um ponto crítico é o equilíbrio entre rigidez e flexibilidade. Um `system_message` muito restritivo pode sufocar a capacidade do modelo de adaptar-se a nuances, enquanto um muito vago pode não fornecer direção suficiente. A prática recomenda:

1. **Especificidade**: Incluir exemplos de respostas esperadas ou proibições claras (ex.: "Não responda perguntas sobre política").
2. **Dinamismo**: Usar variáveis no template (ex.: `{context}`) para injetar informações dinâmicas sem perder o contexto do sistema.
3. **Testes**: Validar o impacto do `system_message` em diferentes cenários, especialmente em casos edge-case.

Exemplo prático:
```python
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

system_template = "Você é um assistente que responde apenas em português do Brasil. Contexto: {contexto}"
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    ("user", "{pergunta}")
])
```

Aqui, `{contexto}` permite ajustar a instrução base dinamicamente, enquanto o restante do comportamento é fixado pelo `system_message`. Essa combinação é essencial para aplicações que exigem tanto personalização quanto consistência.
```