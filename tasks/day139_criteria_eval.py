```python
from langchain.chains import CriteriaEvalChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# Definir critérios de avaliação
class EvaluationCriteria(BaseModel):
    relevancia: str = Field(description="Avalie se a resposta é relevante para a pergunta")
    precisao: str = Field(description="Avalie se a resposta é precisa e factual")
    clareza: str = Field(description="Avalie se a resposta é clara e bem estruturada")

# Criar prompt para avaliação
criteria_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="""
    Pergunta: {question}
    Resposta: {answer}

    Avalie a resposta com base nos seguintes critérios:
    1. Relevância: {relevancia}
    2. Precisão: {precisao}
    3. Clareza: {clareza}
    """
)

# Criar cadeia de avaliação
evaluation_chain = CriteriaEvalChain.from_criteria(
    criteria=EvaluationCriteria,
    llm_chain_kwargs={"prompt": criteria_prompt},
    return_scores=True
)

# Exemplo de uso
question = "Qual é a capital do Brasil?"
answer = "A capital do Brasil é Brasília."

# Avaliar a resposta
result = evaluation_chain.evaluate(
    input={"question": question, "answer": answer},
    criteria=EvaluationCriteria(
        relevancia="A resposta aborda diretamente a pergunta",
        precisao="A informação está correta",
        clareza="A resposta é direta e fácil de entender"
    )
)

print(result)
```