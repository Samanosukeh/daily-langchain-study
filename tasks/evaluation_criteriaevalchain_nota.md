```markdown
# Nota Técnica: Validação de Critérios em `CriteriaEvaluator`

## Contexto
O `CriteriaEvaluator` em LangChain frequentemente requer validação de critérios personalizados para garantir consistência em avaliações de modelos. Abaixo, um exemplo prático de como validar um critério secundário: **coerência semântica** em respostas geradas.

---

## Implementação

```python
from typing import Dict, Any
from langchain.evaluation import CriteriaEvaluator
from langchain_core.prompts import PromptTemplate

class CoerenciaSemanticaEvaluator(CriteriaEvaluator):
    def __init__(self):
        self.criteria = "coerência semântica"
        self.prompt = PromptTemplate(
            input_variables=["resposta"],
            template="Avalie a coerência semântica da resposta a seguir. Responda apenas com 'Sim' ou 'Não': {resposta}"
        )

    def evaluate(self, resposta: str) -> Dict[str, Any]:
        try:
            resultado = self.prompt.format(resposta=resposta)
            # Simula uma avaliação (substitua por LLM real em produção)
            avaliacao = "Sim" if len(resposta.split()) > 3 else "Não"
            return {
                "critério": self.criteria,
                "pontuação": 1.0 if avaliacao == "Sim" else 0.0,
                "feedback": f"Resposta {'coerente' if avaliacao == 'Sim' else 'incoerente'}."
            }
        except Exception as e:
            return {"erro": str(e)}
```

---

## Pontos Chave
1. **Critério Personalizado**: A classe `CoerenciaSemanticaEvaluator` estende `CriteriaEvaluator` para validar um critério específico.
2. **Prompt Simples**: Usa um `PromptTemplate` para padronizar a entrada do avaliador.
3. **Lógica de Avaliação**: Substitui a chamada real a um LLM por uma regra simplificada (ex.: `len(resposta.split()) > 3`).
4. **Saída Estruturada**: Retorna um dicionário com `pontuação` (0.0 ou 1.0) e `feedback`.

---

## Observações
- Em produção, substitua a lógica de avaliação por uma chamada a um LLM (ex.: `ChatOpenAI`).
- Para critérios complexos, considere usar `StringEvaluator` ou `ScoreStringEvaluator`.
- Teste com casos de borda (ex.: respostas vazias ou ambíguas).

---
```