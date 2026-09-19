```python
from langchain.chains import CriteriaEvalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.fake import FakeListLLM

# Setup mock LLM para demonstração
llm = FakeListLLM(responses=["Sim, atende", "Não, não atende"])

# Definição dos critérios de avaliação
criteria = "O texto deve ser claro e conciso"

# Criação da cadeia de avaliação
eval_chain = CriteriaEvalChain.from_llm(
    llm=llm,
    criteria=criteria,
    return_scores=True
)

# Template de prompt minimalista
prompt = ChatPromptTemplate.from_messages([
    ("system", "Avalie o texto abaixo conforme os critérios: {criteria}"),
    ("user", "{text}")
])

# Execução da cadeia
text_to_evaluate = "Este é um exemplo claro."
result = eval_chain.invoke({
    "criteria": criteria,
    "text": text_to_evaluate
})

print(result)
```