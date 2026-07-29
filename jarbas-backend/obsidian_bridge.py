"""
JARBAS → Obsidian Bridge

Envia notas diretamente para o repositório cerebro-jarbas no GitHub.
O Obsidian sincroniza automaticamente via plugin Git, sem intervenção manual.
"""

import base64
import json
from datetime import datetime
import httpx
from config import config

GITHUB_API = "https://api.github.com"
REPO_OWNER = "weslleyramon001-png"
REPO_NAME = "cerebro-jarbas"
BRANCH = "main"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def _get_file_sha(client: httpx.AsyncClient, path: str) -> str | None:
    """Retorna o SHA do arquivo se ele já existir no repositório."""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    r = await client.get(url, headers=_headers(), params={"ref": BRANCH})
    if r.status_code == 200:
        return r.json().get("sha")
    return None


async def salvar_nota(
    titulo: str,
    conteudo: str,
    pasta: str = "CEREBRO DO JARBAS IA CLAUDE/99 - Sessões",
    nome_arquivo: str | None = None,
) -> dict:
    """
    Cria ou atualiza um arquivo .md no vault do Obsidian via GitHub API.

    Args:
        titulo: Título da nota (usado no commit e no nome do arquivo)
        conteudo: Conteúdo markdown completo da nota
        pasta: Caminho da pasta dentro do vault
        nome_arquivo: Nome do arquivo sem extensão (opcional)

    Returns:
        dict com status, url e mensagem
    """
    if not config.GITHUB_TOKEN:
        return {"status": "erro", "mensagem": "GITHUB_TOKEN não configurado no Railway"}

    hoje = datetime.now().strftime("%d-%m-%Y")
    nome = nome_arquivo or f"{titulo.replace(' ', '-').replace('/', '-')}-{hoje}"
    path = f"{pasta}/{nome}.md"

    conteudo_bytes = base64.b64encode(conteudo.encode("utf-8")).decode("utf-8")

    async with httpx.AsyncClient(timeout=15) as client:
        sha = await _get_file_sha(client, path)

        payload = {
            "message": f"feat: {titulo} — via JARBAS {hoje}",
            "content": conteudo_bytes,
            "branch": BRANCH,
        }
        if sha:
            payload["sha"] = sha

        url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
        r = await client.put(url, headers=_headers(), json=payload)

    if r.status_code in (200, 201):
        file_url = r.json().get("content", {}).get("html_url", "")
        acao = "atualizada" if sha else "criada"
        return {
            "status": "sucesso",
            "mensagem": f"Nota {acao} no Obsidian: {nome}.md",
            "arquivo": path,
            "url": file_url,
        }

    return {
        "status": "erro",
        "mensagem": f"Erro GitHub {r.status_code}: {r.text[:200]}",
    }


async def fechar_sessao(resumo: str, decisoes: list[str], pendencias: list[str]) -> dict:
    """
    Gera e salva automaticamente o log de sessão no Obsidian.
    Cria dois arquivos: log curto em 05-sessoes/ e memória detalhada em 99 - Sessões/.
    """
    hoje = datetime.now()
    data_br = hoje.strftime("%d/%m/%Y")
    data_iso = hoje.strftime("%Y-%m-%d")
    data_arquivo = hoje.strftime("%d-%m-%Y")

    # Log curto
    log_curto = f"""# Sessão — {data_br}

## O que foi feito
{chr(10).join(f"- {item}" for item in resumo.split(". ") if item)}

## Decisões tomadas
{chr(10).join(f"- {d}" for d in decisoes) if decisoes else "- Nenhuma decisão registrada"}

## Pendências geradas
{chr(10).join(f"- {p}" for p in pendencias) if pendencias else "- Nenhuma pendência nova"}

## Links relevantes
- [[🚀 DASHBOARD — Cockpit do JARBAS]]
"""

    # Memória detalhada
    decisoes_md = "\n".join(f"- **{d}**" for d in decisoes) if decisoes else "- Nenhuma"
    pendencias_md = "\n".join(f"- [ ] {p}" for p in pendencias) if pendencias else "- Nenhuma"

    memoria = f"""---
data: {data_iso}
tipo: sessao
tags: [sessao, jarbas, {hoje.strftime("%Y-%m")}]
---

# 📋 Memória de Sessão — {data_br}

## Resumo
> {resumo}

## O que foi feito
{chr(10).join(f"- {item}" for item in resumo.split(". ") if item)}

## Decisões Importantes
{decisoes_md}

## Pendências Geradas
{pendencias_md}

## Próxima Sessão
- [ ] Revisar pendências acima
- [ ] Abrir [[🚀 DASHBOARD — Cockpit do JARBAS]]

---
*Sessão registrada automaticamente por JARBAS em {data_br}*
"""

    resultados = []

    r1 = await salvar_nota(
        titulo=f"Sessão {data_arquivo}",
        conteudo=log_curto,
        pasta="05-sessoes",
        nome_arquivo=data_iso,
    )
    resultados.append(r1)

    r2 = await salvar_nota(
        titulo=f"Memória de Sessão {data_arquivo}",
        conteudo=memoria,
        pasta="CEREBRO DO JARBAS IA CLAUDE/99 - Sessões",
        nome_arquivo=f"📋 Memória de Sessão - {data_arquivo}",
    )
    resultados.append(r2)

    sucessos = [r for r in resultados if r["status"] == "sucesso"]
    return {
        "status": "sucesso" if sucessos else "erro",
        "arquivos_criados": len(sucessos),
        "detalhes": resultados,
    }
