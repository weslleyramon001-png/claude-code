#!/usr/bin/env python3
"""
MailerLite MCP Server — JARBAS
Gerencia subscribers, grupos, campanhas e funis da Pony-Digital.
Token: variável MAILERLITE_API_KEY
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.mailerlite.com/api/v2"

mcp = FastMCP("mailerlite")


def _headers() -> dict:
    token = os.environ.get("MAILERLITE_API_KEY", "")
    if not token:
        raise ValueError("MAILERLITE_API_KEY não definido")
    return {"X-MailerLite-ApiKey": token, "Content-Type": "application/json"}


def _get(path: str, params: dict = None) -> dict:
    resp = httpx.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _post(path: str, body: dict) -> dict:
    resp = httpx.post(f"{BASE_URL}{path}", headers=_headers(), json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _put(path: str, body: dict) -> dict:
    resp = httpx.put(f"{BASE_URL}{path}", headers=_headers(), json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── Ferramentas ──────────────────────────────────────────────────────────────

@mcp.tool()
def mailerlite_conta() -> str:
    """Retorna informações da conta MailerLite (plano, limites, subscribers)."""
    data = _get("/me")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_subscribers_listar(limite: int = 25, pagina: int = 1) -> str:
    """
    Lista subscribers da conta.
    Args:
        limite: quantidade por página (padrão 25, máx 1000)
        pagina: número da página
    """
    data = _get("/subscribers", {"limit": limite, "page": pagina})
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_subscriber_buscar(email: str) -> str:
    """
    Busca um subscriber pelo email.
    Args:
        email: endereço de email do subscriber
    """
    data = _get(f"/subscribers/{email}")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_subscriber_adicionar(
    email: str,
    nome: str = "",
    grupo_id: str = "",
) -> str:
    """
    Adiciona ou atualiza um subscriber.
    Args:
        email: email do novo subscriber
        nome: nome completo (opcional)
        grupo_id: ID do grupo/funil para adicionar (opcional)
    """
    body: dict = {"email": email, "resubscribe": True}
    if nome:
        body["name"] = nome
    if grupo_id:
        body["groups"] = [grupo_id]
    data = _post("/subscribers", body)
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_grupos_listar() -> str:
    """Lista todos os grupos (listas/funis) da conta com IDs e contagem de subscribers."""
    data = _get("/groups")
    resultado = []
    for g in (data if isinstance(data, list) else []):
        resultado.append({
            "id": g.get("id"),
            "nome": g.get("name"),
            "total": g.get("total"),
            "ativo": g.get("active"),
        })
    return json.dumps(resultado, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_campanhas_listar(status: str = "sent") -> str:
    """
    Lista campanhas de email.
    Args:
        status: 'sent', 'draft', 'outbox' (padrão: 'sent')
    """
    data = _get("/campaigns", {"status": status})
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_campanha_stats(campanha_id: str) -> str:
    """
    Estatísticas de uma campanha: aberturas, cliques, bounces.
    Args:
        campanha_id: ID da campanha
    """
    data = _get(f"/campaigns/{campanha_id}/stats")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_automacoes_listar() -> str:
    """Lista automações/workflows (funis de email) configurados na conta."""
    data = _get("/automations")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mailerlite_funil_ativar(automacao_id: str) -> str:
    """
    Ativa uma automação/funil de email.
    Args:
        automacao_id: ID da automação
    """
    data = _put(f"/automations/{automacao_id}", {"status": "active"})
    return json.dumps(data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
