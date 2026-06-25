#!/usr/bin/env python3
"""
ElevenLabs MCP Server — JARBAS
Gerencia vozes, chaves e geração TTS do ElevenLabs.
Token: variável ELEVENLABS_API_KEY
"""

import os
import json
import base64
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.elevenlabs.io/v1"
DEFAULT_VOICE_ID = "onwK4e9ZLuTAKqWW03F9"  # Daniel (voz atual do JARBAS)

mcp = FastMCP("elevenlabs")


def _headers() -> dict:
    token = os.environ.get("ELEVENLABS_API_KEY", "")
    if not token:
        raise ValueError("ELEVENLABS_API_KEY não definido")
    return {"xi-api-key": token, "Content-Type": "application/json"}


def _get(path: str) -> dict:
    resp = httpx.get(f"{BASE_URL}{path}", headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def _delete(path: str) -> int:
    resp = httpx.delete(f"{BASE_URL}{path}", headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.status_code


# ── Ferramentas ──────────────────────────────────────────────────────────────

@mcp.tool()
def elevenlabs_conta() -> str:
    """
    Status da conta ElevenLabs: plano, caracteres usados/disponíveis e status da chave API.
    Use para verificar se a chave está válida (se retornar dados = chave ok).
    """
    data = _get("/user/subscription")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def elevenlabs_vozes_listar() -> str:
    """Lista todas as vozes disponíveis na conta (incluindo clonadas)."""
    data = _get("/voices")
    vozes = []
    for v in data.get("voices", []):
        vozes.append({
            "id": v.get("voice_id"),
            "nome": v.get("name"),
            "categoria": v.get("category"),
            "descricao": v.get("description", ""),
            "preview_url": v.get("preview_url", ""),
        })
    return json.dumps(vozes, ensure_ascii=False, indent=2)


@mcp.tool()
def elevenlabs_voz_detalhes(voice_id: str = DEFAULT_VOICE_ID) -> str:
    """
    Detalhes de uma voz específica.
    Args:
        voice_id: ID da voz (padrão: Daniel, voz atual do JARBAS)
    """
    data = _get(f"/voices/{voice_id}")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def elevenlabs_tts_testar(
    texto: str,
    voice_id: str = DEFAULT_VOICE_ID,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> str:
    """
    Gera áudio TTS e retorna o tamanho em bytes (validação de que está funcionando).
    Para uso real de áudio, o endpoint /voice do JARBAS backend é mais adequado.
    Args:
        texto: texto para converter em voz
        voice_id: ID da voz (padrão: Daniel)
        stability: estabilidade da voz 0-1 (padrão 0.5)
        similarity_boost: similaridade com a voz original 0-1 (padrão 0.75)
    """
    token = os.environ.get("ELEVENLABS_API_KEY", "")
    if not token:
        raise ValueError("ELEVENLABS_API_KEY não definido")
    headers = {"xi-api-key": token, "Content-Type": "application/json"}
    body = {
        "text": texto,
        "voice_settings": {"stability": stability, "similarity_boost": similarity_boost},
    }
    resp = httpx.post(
        f"{BASE_URL}/text-to-speech/{voice_id}",
        headers=headers,
        json=body,
        timeout=60,
    )
    if resp.status_code == 401:
        return "❌ Chave inválida ou expirada (401). Precisa renovar ELEVENLABS_API_KEY."
    resp.raise_for_status()
    tamanho = len(resp.content)
    return f"✅ Áudio gerado com sucesso — {tamanho} bytes. Chave funcionando."


@mcp.tool()
def elevenlabs_modelos_listar() -> str:
    """Lista os modelos TTS disponíveis (ex: eleven_multilingual_v2)."""
    data = _get("/models")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def elevenlabs_historico_listar(limite: int = 10) -> str:
    """
    Histórico de gerações de áudio recentes.
    Args:
        limite: número de itens (padrão 10)
    """
    data = _get(f"/history?page_size={limite}")
    items = data.get("history", [])
    resultado = []
    for h in items:
        resultado.append({
            "id": h.get("history_item_id"),
            "texto": h.get("text", "")[:80] + "..." if len(h.get("text", "")) > 80 else h.get("text", ""),
            "voice_id": h.get("voice_id"),
            "voice_name": h.get("voice_name"),
            "data": h.get("date_unix"),
            "caracteres": h.get("character_count_change_from", 0),
        })
    return json.dumps(resultado, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
