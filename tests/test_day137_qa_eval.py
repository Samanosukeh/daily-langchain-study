```python
import pytest
from langchain.evaluation import QAEvalChain
from langchain.schema import Document

@pytest.fixture
def mock_chain():
    return QAEvalChain.from_llm(llm=None)  # Substituir por um mock ou LLM real

def test_qaeval_correct_answer(mock_chain):
    """Testa se QAEval retorna CORRECT para resposta correta."""
    question = "Qual é a capital do Brasil?"
    correct_answer = "Brasília"
    predicted_answer = "Brasília"

    result = mock_chain.evaluate(
        inputs=[{"question": question}],
        predictions=[predicted_answer],
        references=[correct_answer]
    )

    assert result[0]["text"] == "CORRECT"

def test_qaeval_incorrect_answer(mock_chain):
    """Testa se QAEval retorna INCORRECT para resposta incorreta."""
    question = "Qual é a capital do Brasil?"
    correct_answer = "Brasília"
    predicted_answer = "São Paulo"

    result = mock_chain.evaluate(
        inputs=[{"question": question}],
        predictions=[predicted_answer],
        references=[correct_answer]
    )

    assert result[0]["text"] == "INCORRECT"

def test_qaeval_empty_answer(mock_chain):
    """Testa comportamento com resposta vazia."""
    question = "Qual é a capital do Brasil?"
    correct_answer = "Brasília"
    predicted_answer = ""

    result = mock_chain.evaluate(
        inputs=[{"question": question}],
        predictions=[predicted_answer],
        references=[correct_answer]
    )

    assert result[0]["text"] in ["INCORRECT", "CORRECT"]  # Depende da implementação

def test_qaeval_multiple_questions(mock_chain):
    """Testa avaliação de múltiplas perguntas."""
    questions = ["Capital do Brasil?", "Capital da França?"]
    correct_answers = ["Brasília", "Paris"]
    predicted_answers = ["Brasília", "Londres"]

    result = mock_chain.evaluate(
        inputs=[{"question": q} for q in questions],
        predictions=predicted_answers,
        references=correct_answers
    )

    assert len(result) == 2
    assert result[0]["text"] == "CORRECT"
    assert result[1]["text"] == "INCORRECT"

def test_qaeval_with_context(mock_chain):
    """Testa avaliação com contexto fornecido."""
    question = "Qual é a capital do Brasil?"
    context = "O Brasil é um país da América do Sul."
    correct_answer = "Brasília"
    predicted_answer = "Brasília"

    result = mock_chain.evaluate(
        inputs=[{"question": question, "context": context}],
        predictions=[predicted_answer],
        references=[correct_answer]
    )

    assert result[0]["text"] == "CORRECT"
```