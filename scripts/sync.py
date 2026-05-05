"""
scripts/sync.py
"""

import json
import os
import random
import sys
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv
from mistralai import Mistral

# Carrega variáveis do .env
load_dotenv()

REPO_ROOT  = Path(__file__).parent.parent
PLAN_PATH  = REPO_ROOT / ".meta" / "plan.json"
INIT_PATH  = REPO_ROOT / ".meta" / "init"
STATE_PATH = REPO_ROOT / ".meta" / "state.json"

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")
MODEL = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
MAX_DAY = 200

print(f"🔧 DEBUG - Variáveis de Ambiente:")
print(f"   MISTRAL_API_KEY: {'✅ Configurada' if MISTRAL_API_KEY else '❌ NÃO CONFIGURADA'}")
print(f"   MISTRAL_MODEL: {MODEL}")
print(f"   REPO_ROOT: {REPO_ROOT}")
print()

COMMIT_COUNT_WEIGHTS = [40, 30, 20, 10]
DEFAULT_SKIP_RATE = 0.2857

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


def should_skip_today(test_mode: bool) -> bool:
    if test_mode:
        return False
    skip_rate = float(os.environ.get("SKIP_RATE", str(DEFAULT_SKIP_RATE)))
    print(f"   ⏳ Probabilidade de skip: {skip_rate:.2%}")
    return random.random() < skip_rate


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
    try:
        print(f"📡 Inicializando cliente Mistral...")
        print(f"   API Key: {'✅ Configurada' if MISTRAL_API_KEY else '❌ Não configurada'}")
        print(f"   Modelo: {MODEL}")
        
        client = Mistral(api_key=MISTRAL_API_KEY)
        print(f"📡 Chamando Mistral AI...")
        
        response = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "system", "content": _SYS},
                {"role": "user", "content": prompt[:100] + "..."},  # log resumido
            ],
            temperature=0.5,
            max_tokens=1024,
        )
        content = response.choices[0].message.content.strip()
        print(f"✅ Resposta recebida ({len(content)} caracteres)")
        return content
    except Exception as e:
        print(f"❌ ERRO ao chamar Mistral: {type(e).__name__}")
        print(f"   Detalhes: {str(e)[:200]}")
        raise
    print(f"✅ Conteúdo recebido ({len(content)} caracteres)")
    return content


def write_output(file_path: str, content: str, append: bool = False) -> None:
    target = REPO_ROOT / file_path
    target.parent.mkdir(parents=True, exist_ok=True)

    if append and target.exists():
        existing = target.read_text(encoding="utf-8")
        content = existing + "\n\n---\n\n" + content
        print(f"📝 Append: {file_path}")
    else:
        print(f"✍️  Novo arquivo: {file_path}")

    target.write_text(content, encoding="utf-8")
    print(f"💾 Salvo ({len(content)} caracteres)")


def main() -> None:
    print(f"\n📍 Iniciando main()")
    
    # Validação da API Key
    if not MISTRAL_API_KEY:
        print(f"❌ ERRO: MISTRAL_API_KEY não está configurada!")
        sys.exit(1)
    
    print(f"   ✅ MISTRAL_API_KEY configurada")
    
    # Modo teste: permite executar mesmo após MAX_DAY
    test_mode = os.environ.get("TEST_MODE", "false").lower() == "true"
    test_day = os.environ.get("TEST_DAY")

    day = int(test_day) if test_day else get_current_day()
    print(f"   Dia: {day} (test_mode={test_mode})")

    if should_skip_today(test_mode):
        print("❌ EXIT: Hoje foi selecionado para não gerar commit.")
        sys.exit(0)

    if not test_mode and (day < 1 or day > MAX_DAY):
        print(f"❌ EXIT: Dia {day} fora do range 1-{MAX_DAY}")
        sys.exit(0)

    print(f"   ✅ Dia passou na validação")

    plan = load_plan()
    print(f"   📋 Plano: {len(plan)} tarefas")
    
    task = get_task(plan, day)

    if task is None:
        print(f"❌ EXIT: Nenhuma tarefa para dia {day}")
        sys.exit(0)

    print(f"   ✅ Tarefa encontrada")
    print(f"      Título: {task['title']}")
    print(f"      Tipo: {task['type']}")
    print(f"      Arquivo: {task['file']}")

    state = load_state()
    if day in state["completed"]:
        print(f"❌ EXIT: Dia {day} já foi completado")
        sys.exit(0)

    print(f"   ✅ Dia não foi completado ainda")

    # --- Commit principal ---
    main_content = call_mistral(build_main_prompt(task))
    append_main = task["type"] in ("doc", "code") and (REPO_ROOT / task["file"]).exists()
    write_output(task["file"], main_content, append=append_main)

    commits_today = [{"type": "main", "file": task["file"]}]

    # --- Commits extras ---
    n_extra = pick_commit_count() - 1
    print(f"\n📦 Gerando {n_extra} conteúdo(s) extra(s)...")

    used_types = set()
    for i in range(n_extra):
        # evita repetir o mesmo tipo no mesmo dia
        available = [t for t in MICRO_TASK_TYPES if t not in used_types]
        if not available:
            break
        micro_type = random.choice(available)
        used_types.add(micro_type)
        
        print(f"   [{i+1}/{n_extra}] Tipo: {micro_type}")
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
    print(f"\n💾 Estado salvo")

    generated = REPO_ROOT / ".meta" / "generated_today.json"
    generated.write_text(
        json.dumps(commits_today, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"✅ Sucesso! {len(commits_today)} arquivo(s) gerado(s)")


if __name__ == "__main__":
    try:
        print("=" * 60)
        print("🚀 INICIANDO SYNC")
        print("=" * 60)
        main()
        print("=" * 60)
        print("✅ SYNC FINALIZADO COM SUCESSO")
        print("=" * 60)
    except Exception as e:
        print("=" * 60)
        print(f"❌ ERRO DURANTE SYNC: {type(e).__name__}")
        print(f"   {str(e)}")
        print("=" * 60)
        sys.exit(1)
