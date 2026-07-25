```markdown
# **Agents vs Chains — Quando Usar Cada Um?**

| **Critério**          | **Chains**                          | **Agents**                          |
|-----------------------|-------------------------------------|-------------------------------------|
| **Definição**         | Sequências lineares de ações pré-definidas. | Sistemas dinâmicos que decidem ações com base em feedback (ex: execução → observação → decisão). |
| **Controle**          | Fixo: fluxo definido em código.      | Dinâmico: ajusta ações em tempo real usando ferramentas ou loops. |
| **Complexidade**      | Baixa: ideal para tarefas simples e repetitivas. | Alta: gerencia incertezas e múltiplas etapas interativas. |
| **Exemplo de Uso**    | Extrair texto de um PDF → processar → salvar em CSV. | Pesquisar na web → analisar resultados → decidir próxima ação → concluir resposta. |
| **Flexibilidade**     | Limitada: segue um roteiro rígido.   | Alta: adapta-se a mudanças no ambiente ou entrada do usuário. |
| **Ferramentas**       | Usa `LLMChain`, `SequentialChain`, ou `RouterChain`. | Usa `AgentExecutor` com ferramentas como `SerpAPI`, `PythonREPL`, ou bases de dados. |
| **Performance**       | Previsível: desempenho constante.    | Variável: depende da capacidade de decisão do agente. |
| **Caso Ideal**        | Automação de fluxos conhecidos.      | Tarefas que exigem pesquisa, raciocínio multi-step ou interação com APIs externas. |
| **Exemplo de Código** | ```python
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(input)
``` | ```python
from langchain.agents import AgentExecutor, initialize_agent
agent = initialize_agent(tools, llm, agent=..., verbose=True)
result = agent.run("Pesquise sobre o LangChain e explique suas vantagens.")
``` |
| **Vantagens**         | - Simplicidade. <br> - Baixo custo de implementação. | - Capacidade de lidar com problemas complexos. <br> - Integração com múltiplas fontes de dados. |
| **Desvantagens**      | - Não lida bem com incertezas. <br> - Requer refatoração para mudanças. | - Maior complexidade de depuração. <br> - Custo computacional mais alto (múltiplas chamadas ao LLM). |
| **Quando Escolher?**  | Use **Chains** quando: <br> - O fluxo é previsível. <br> - A tarefa é simples e repetitiva. | Use **Agents** quando: <br> - A tarefa exige múltiplas etapas de decisão. <br> - Precisa interagir com APIs ou ferramentas externas. <br> - O problema envolve incerteza ou pesquisa. |
```