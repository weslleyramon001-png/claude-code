#!/usr/bin/env python3
"""
Obsidian MCP Server — JARBAS
Lê e escreve no vault Obsidian via plugin "Local REST API".

Variáveis de ambiente:
  OBSIDIAN_HOST    — endereço do servidor (padrão: http://100.82.120.121:27123 via Tailscale/Dell)
  OBSIDIAN_TOKEN   — token gerado nas configurações do plugin (opcional se sem auth)
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

DEFAULT_HOST = "http://100.82.120.121:27123"  # Dell via Tailscale

mcp = FastMCP("obsidian")


def _base() -> str:
    return os.environ.get("OBSIDIAN_HOST", DEFAULT_HOST).rstrip("/")


def _headers() -> dict:
    token = os.environ.get("OBSIDIAN_TOKEN", "")
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _get(path: str) -> httpx.Response:
    resp = httpx.get(f"{_base()}{path}", headers=_headers(), timeout=15, verify=False)
    resp.raise_for_status()
    return resp


def _put(path: str, content: str) -> httpx.Response:
    headers = _headers()
    headers["Content-Type"] = "text/markdown"
    resp = httpx.put(f"{_base()}{path}", headers=headers, content=content.encode(), timeout=15, verify=False)
    resp.raise_for_status()
    return resp


def _post(path: str, body: dict | str) -> httpx.Response:
    if isinstance(body, str):
        headers = _headers()
        headers["Content-Type"] = "text/markdown"
        resp = httpx.post(f"{_base()}{path}", headers=headers, content=body.encode(), timeout=15, verify=False)
    else:
        resp = httpx.post(f"{_base()}{path}", headers=_headers(), json=body, timeout=15, verify=False)
    resp.raise_for_status()
    return resp


def _delete(path: str) -> httpx.Response:
    resp = httpx.delete(f"{_base()}{path}", headers=_headers(), timeout=15, verify=False)
    resp.raise_for_status()
    return resp


# ── Ferramentas ──────────────────────────────────────────────────────────────

@mcp.tool()
def obsidian_status() -> str:
    """Verifica se o Obsidian está acessível e retorna informações do vault."""
    try:
        resp = _get("/")
        return json.dumps(resp.json(), ensure_ascii=False, indent=2)
    except Exception as e:
        return f"❌ Obsidian inacessível: {e}\nHost configurado: {_base()}\nVerifique se o Dell está ligado, Tailscale ativo e plugin Local REST API habilitado."


@mcp.tool()
def obsidian_listar(pasta: str = "") -> str:
    """
    Lista arquivos e pastas do vault.
    Args:
        pasta: caminho da pasta (vazio = raiz do vault)
    """
    path = f"/vault/{pasta}/" if pasta else "/vault/"
    resp = _get(path)
    return json.dumps(resp.json(), ensure_ascii=False, indent=2)


@mcp.tool()
def obsidian_ler(caminho: str) -> str:
    """
    Lê o conteúdo de uma nota do vault.
    Args:
        caminho: caminho do arquivo (ex: '99 - Sessões/Memória de Sessão - 25-06-2026.md')
    """
    resp = _get(f"/vault/{caminho}")
    return resp.text


@mcp.tool()
def obsidian_escrever(caminho: str, conteudo: str) -> str:
    """
    Cria ou substitui uma nota no vault.
    Args:
        caminho: caminho do arquivo (ex: '99 - Sessões/nova-nota.md')
        conteudo: conteúdo em Markdown
    """
    _put(f"/vault/{caminho}", conteudo)
    return f"✅ Nota salva: {caminho}"


@mcp.tool()
def obsidian_adicionar(caminho: str, conteudo: str) -> str:
    """
    Adiciona texto ao final de uma nota existente (append).
    Args:
        caminho: caminho do arquivo
        conteudo: texto a adicionar
    """
    _post(f"/vault/{caminho}", conteudo)
    return f"✅ Conteúdo adicionado em: {caminho}"


@mcp.tool()
def obsidian_deletar(caminho: str) -> str:
    """
    Deleta uma nota do vault.
    Args:
        caminho: caminho do arquivo a deletar
    """
    _delete(f"/vault/{caminho}")
    return f"✅ Nota deletada: {caminho}"


@mcp.tool()
def obsidian_buscar(query: str) -> str:
    """
    Busca notas no vault por texto.
    Args:
        query: texto a buscar
    """
    resp = _post("/search/simple/", {"query": query})
    resultados = resp.json()
    if not resultados:
        return "Nenhum resultado encontrado."
    saida = []
    for r in resultados:
        saida.append({
            "arquivo": r.get("filename", ""),
            "score": r.get("score", 0),
            "trecho": r.get("matches", [{}])[0].get("context", "") if r.get("matches") else "",
        })
    return json.dumps(saida, ensure_ascii=False, indent=2)


@mcp.tool()
def obsidian_memoria_sessao_salvar(data: str, conteudo: str) -> str:
    """
    Salva uma memória de sessão diretamente na pasta correta do Cérebro do JARBAS.
    Args:
        data: data no formato DD-MM-AAAA (ex: 25-06-2026)
        conteudo: conteúdo completo da memória em Markdown
    """
    caminho = f"CEREBRO DO JARBAS IA CLAUDE/99 - Sessões/📋 Memória de Sessão - {data}.md"
    _put(f"/vault/{caminho}", conteudo)
    return f"✅ Memória de sessão salva: {caminho}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
