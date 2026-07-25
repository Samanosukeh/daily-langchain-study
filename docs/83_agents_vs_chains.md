```markdown
# **Agents vs Chains: Quando Usar Cada Um**

## **1. Agents (Agentes)**
Agentes são componentes autônomos que usam **LLMs (Large Language Models)** para tomar decisões dinâmicas e interagir com ferramentas ou APIs externas.

### **Características Principais**
- **Tomada de decisão dinâmica**: Avaliam o contexto em tempo real e decidem a próxima ação.
- **Uso de ferramentas**: Podem chamar funções, APIs ou outros serviços externos.
- **Loop de feedback**: Iteram até atingir um objetivo ou critério de parada.
- **Flexibilidade**: Adaptam-se a cenários complexos e não previsíveis.

### **Quando Usar Agents?**
✅ **Casos de uso ideais:**
- **Interação com sistemas externos** (ex: busca na web, consulta a banco de dados, chamadas a APIs).
- **Fluxos de trabalho dinâmicos** onde a próxima etapa depende do resultado de ações anteriores.
- **Automação de tarefas complexas** que exigem múltiplas interações (ex: pesquisa, planejamento, resolução de problemas).
- **Sistemas que precisam de adaptação** (ex: chatbots avançados, assistentes de código, análise de dados interativa).

❌ **Evite quando:**
- O fluxo é **linear e previsível** (use **Chains**).
- Não há necessidade de interação com ferramentas externas.
- A latência de múltiplas chamadas é crítica (agents podem ser mais lentos).

### **Exemplo de Código (LangChain)**
```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
tools = [...]  # Lista de ferramentas (ex: calculadora, busca na web)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent.run("Qual é a capital do Brasil e qual é sua população?")
print(response)
```

---

## **2. Chains (Cadeias)**
Chains são sequências **fixas e lineares** de etapas que processam dados de forma previsível, sem tomada de decisão dinâmica.

### **Características Principais**
- **Fluxo linear**: Cada etapa depende apenas da saída da anterior.
- **Sem interação externa**: Não chamam ferramentas ou APIs durante a execução.
- **Previsível**: Execução determinística (mesma entrada → mesma saída).
- **Eficiência**: Menor latência (nenhum overhead de decisão).

### **Quando Usar Chains?**
✅ **Casos de uso ideais:**
- **Processamento de texto simples** (ex: formatação, extração de informações, tradução).
- **Pipelines de dados estruturados** (ex: pré-processamento, classificação, sumarização).
- **Fluxos onde a ordem das etapas é fixa** (ex: "extrair → transformar → carregar").
- **Aplicações onde performance é crítica** (ex: sistemas em tempo real).

❌ **Evite quando:**
- O problema **exige adaptação** (ex: interação com APIs dinâmicas).
- Há necessidade de **tomada de decisão autônoma**.
- O fluxo **não é linear** (ex: loops ou condições).

### **Exemplo de Código (LangChain)**
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.7)

# Definir prompt template
prompt = PromptTemplate(
    input_variables=["product"],
    template="Descreva um produto {product} em 3 linhas."
)

# Criar chain
chain = LLMChain(llm=llm, prompt=prompt)

# Executar
response = chain.run(product="notebook")
print(response)
```

---

## **3. Comparação Direta**

| **Critério**          | **Agents**                          | **Chains**                          |
|-----------------------|-------------------------------------|-------------------------------------|
| **Flexibilidade**     | Alta (decisões dinâmicas)           | Baixa (fluxo fixo)                  |
| **Interação Externa** | Sim (ferramentas, APIs)             | Não                                 |
| **Complexidade**      | Alta (múltiplas iterações)          | Baixa (sequencial)                  |
| **Performance**       | Média/baixa (latência de loops)     | Alta (exec