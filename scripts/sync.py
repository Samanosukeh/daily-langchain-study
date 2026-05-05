"""
scripts/sync.py
"""

import json
import os
import random
import sys
from datetime import date, datetime
from pathlib import Path

from mistralai.client import MistralClient

REPO_ROOT  = Path(__file__).parent.parent
PLAN_PATH  = REPO_ROOT / ".meta" / "plan.json"
INIT_PATH  = REPO_ROOT / ".meta" / "init"
STATE_PATH = REPO_ROOT / ".meta" / "state.json"

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MODEL = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
MAX_DAY = 200

COMMIT_COUNT_WEIGHTS = [40, 30, 20, 10]

MICRO_TASK_TYPES = [
    "nota",
    "exemplo",
    "dica",
    "reflexao",
    "comparacao",
]


def get_current_day() -> int:
    start = date.fromisoformat(INIT_PATH.read_text().strip())
    return (date.today() - start).days + 1


def load_plan() -> list[dict]:
    with open(PLAN_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_task(plan: list[dict], day: int) -> dict | None:
    return next((t for t in plan if t["day"] == day), None)


def load_state() -> dict:
    if STATE_PATH.exists():
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "last_run": None, "commit_log": []}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def pick_commit_count() -> int:
    return random.choices([1, 2, 3, 4], weights=COMMIT_COUNT_WEIGHTS, k=1)[0]


def pick_micro_type() -> str:
    return random.choice(MICRO_TASK_TYPES)


def slugify(text: str) -> str:
    """Converte título em slug simples para nome de arquivo."""
    import re
    text = text.lower()
    # remove acentos básicos
    replacements = {
        "ã": "a", "â": "a", "á": "a", "à": "a",
        "ê": "e", "é": "e", "è": "e",
        "í": "i", "î": "i",
        "õ": "o", "ô": "o", "ó": "o",
        "ú": "u", "û": "u",
        "ç": "c",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text[:40]  # limita tamanho


def extra_file_path(task: dict, micro_type: str) -> str:
    """Gera caminho descritivo para arquivo de micro-tarefa."""
    base = Path(task["file"])
    parent = str(base.parent)
    topic_slug = slugify(task["topic"])
    type_slug = slugify(task["title"].split(":")[0])  # pega só a primeira parte do título

    ext_map = {
        "nota":      ".md",
        "dica":      ".md",
        "reflexao":  ".md",
        "comparacao":".md",
        "exemplo":   ".py",
    }
    ext = ext_map.get(micro_type, ".md")
    return f"{parent}/{topic_slug}_{type_slug}_{micro_type}{ext}"


_SYS = """Você é um desenvolvedor Python estudando LangChain de forma progressiva.
Escreva conteúdo técnico em português brasileiro, de forma direta e prática.
Não inclua explicações sobre o que você vai fazer — apenas gere o conteúdo."""


def build_main_prompt(task: dict) -> str:
    if task["type"] == "doc":
        return f"""Gere documentação Markdown sobre: "{task['title']}"
Tópico: {task['topic']} | Arquivo: {task['file']}

- Markdown estruturado com headers, exemplos de código e notas práticas
- Entre 150 e 300 linhas
- LangChain >= 0.2, exemplos Python funcionais
- Se o tópico for MCP, use langchain-mcp-adapters e FastMCP
- Seção "## Resumo" ao final
- Apenas o conteúdo Markdown, sem nada mais."""

    elif task["type"] == "code":
        mcp_note = ""
        if task["topic"] == "mcp":
            mcp_note = """- Para servidores MCP: use FastMCP (pip install fastmcp)
- Para clientes MCP: use langchain-mcp-adapters (MultiServerMCPClient)
- Código assíncrono com asyncio quando necessário\n"""

        return f"""Gere código Python sobre: "{task['title']}"
Tópico: {task['topic']} | Arquivo: {task['file']}

- Python funcional, 40-120 linhas
- LangChain >= 0.2 com imports corretos
- LLM via env MISTRAL_API_KEY, modelo "mistral-small-latest"
{mcp_note}- Docstring no topo explicando o arquivo
- Comentários inline nos blocos importantes
- Bloco if __name__ == "__main__": com exemplo de uso
- Apenas o código Python, sem markdown."""

    elif task["type"] == "test":
        return f"""Gere testes pytest sobre: "{task['title']}"
Tópico: {task['topic']} | Arquivo: {task['file']}

- 3 a 6 funções de teste
- Mocks com unittest.mock para não chamar APIs reais
- Testes rápidos (< 1s cada)
- Fixtures quando apropriado
- Docstring em cada função de teste
- Apenas o código Python, sem markdown."""

    return f"Gere conteúdo sobre: {task['title']}"


def build_micro_prompt(task: dict, micro_type: str) -> str:
    title = task["title"]
    topic = task["topic"]

    prompts = {
        "nota": f"""Escreva uma nota técnica curta (20-40 linhas) em Markdown sobre um aspecto secundário de: "{title}"
Tópico: {topic}

- Pode ser uma ressalva, um gotcha, um detalhe de implementação ou observação de performance
- Tom informal, como anotação de caderno de estudos
- No máximo 1 bloco de código pequeno
- Apenas o conteúdo Markdown""",

        "exemplo": f"""Gere um exemplo Python alternativo e minimalista (15-35 linhas) relacionado a: "{title}"
Tópico: {topic}

- Caso de uso diferente do exemplo principal
- Comentários inline explicando cada parte
- Bloco if __name__ == "__main__"
- Apenas o código Python, sem markdown""",

        "dica": f"""Escreva um arquivo Markdown de dicas rápidas (15-30 linhas) sobre: "{title}"
Tópico: {topic}

- Lista de 3-5 dicas práticas com título curto e explicação de 1-2 linhas cada
- Foco em erros comuns ou atalhos úteis
- Tom direto, sem introdução longa
- Apenas o conteúdo Markdown""",

        "reflexao": f"""Escreva uma reflexão técnica curta (15-30 linhas) em Markdown sobre: "{title}"
Tópico: {topic}

- Questione quando usar ou não usar esse recurso
- Compare com abordagens alternativas
- Tom de quem está estudando e pensando em voz alta
- Apenas o conteúdo Markdown""",

        "comparacao": f"""Gere uma mini comparação em Markdown (20-35 linhas) relacionada a: "{title}"
Tópico: {topic}

- Compare dois aspectos, abordagens ou opções relacionadas ao tema
- Use uma pequena tabela ou lista paralela
- Conclua com recomendação de quando usar cada um
- Apenas o conteúdo Markdown""",
    }

    return prompts.get(micro_type, prompts["nota"])


def call_mistral(prompt: str) -> str:
    client = MistralClient(api_key=MISTRAL_API_KEY)
    response = client.chat.complete(
        model=MODEL,
        messages=[
            {"role": "system", "content": _SYS},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def write_output(file_path: str, content: str, append: bool = False) -> None:
    target = REPO_ROOT / file_path
    target.parent.mkdir(parents=True, exist_ok=True)

    if append and target.exists():
        existing = target.read_text(encoding="utf-8")
        content = existing + "\n\n---\n\n" + content

    target.write_text(content, encoding="utf-8")


def main() -> None:
    day = get_current_day()

    if day < 1 or day > MAX_DAY:
        sys.exit(0)

    plan = load_plan()
    task = get_task(plan, day)

    if task is None:
        sys.exit(0)

    state = load_state()
    if day in state["completed"]:
        sys.exit(0)

    # --- Commit principal ---
    main_content = call_mistral(build_main_prompt(task))
    append_main = task["type"] in ("doc", "code") and (REPO_ROOT / task["file"]).exists()
    write_output(task["file"], main_content, append=append_main)

    commits_today = [{"type": "main", "file": task["file"]}]

    # --- Commits extras ---
    n_extra = pick_commit_count() - 1

    used_types = set()
    for _ in range(n_extra):
        # evita repetir o mesmo tipo no mesmo dia
        available = [t for t in MICRO_TASK_TYPES if t not in used_types]
        if not available:
            break
        micro_type = random.choice(available)
        used_types.add(micro_type)

        prompt = build_micro_prompt(task, micro_type)
        content = call_mistral(prompt)
        file_path = extra_file_path(task, micro_type)
        write_output(file_path, content, append=False)
        commits_today.append({"type": micro_type, "file": file_path})

    # --- Estado ---
    state["completed"].append(day)
    state["last_run"] = datetime.now().isoformat()
    state["last_task"] = {
        "day": day,
        "type": task["type"],
        "title": task["title"],
        "file": task["file"],
        "commits_today": len(commits_today),
    }
    if "commit_log" not in state:
        state["commit_log"] = []
    state["commit_log"].append({
        "day": day,
        "date": str(date.today()),
        "commits": commits_today,
    })
    save_state(state)

    generated = REPO_ROOT / ".meta" / "generated_today.json"
    generated.write_text(
        json.dumps(commits_today, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
