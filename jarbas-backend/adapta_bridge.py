"""
Adapta Bridge — integração JARBAS ↔ Adapta One 26

Fluxo:
  1. httpx chama a API do Clerk diretamente para obter Bearer token JWT
  2. httpx faz as chamadas à API interna do Adapta (/api/chat/stream/v1)
  3. Resposta SSE é parseada para extrair text-delta → texto completo

Variáveis de ambiente necessárias no Railway:
  ADAPTA_SESSION_ID  → ID da sessão Clerk (ex: sess_3GedcbPuo3IQOFr5AVO65QYxQ6V)
  ADAPTA_CLIENT_UAT  → Timestamp de autenticação Clerk (ex: 1784336048)
"""

import asyncio
import json
import logging
import os
import struct
import time
import uuid

import httpx

logger = logging.getLogger(__name__)

ADAPTA_BASE = "https://agent.adapta.one"
CLERK_BASE = "https://clerk.agent.adapta.one"
CLERK_KEY_SUFFIX = "0GUur0zr"

ADAPTA_SESSION_ID = os.getenv("ADAPTA_SESSION_ID", "")
ADAPTA_CLIENT_UAT = os.getenv("ADAPTA_CLIENT_UAT", "")

_bearer_token: str = ""
_bearer_expires: float = 0.0
_token_lock = asyncio.Lock()


def _uuid7() -> str:
    """Gera UUID v7 compatível com o formato usado pelo Adapta."""
    ts_ms = int(time.time() * 1000)
    rand_bytes = uuid.uuid4().bytes
    b = bytearray(16)
    struct.pack_into(">Q", b, 0, ts_ms)
    b[0] = b[1] = 0
    b[6] = (b[6] & 0x0F) | 0x70
    for i in range(6, 16):
        b[i] ^= rand_bytes[i]
    b[8] = (b[8] & 0x3F) | 0x80
    h = b.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def _clerk_cookies() -> dict:
    return {
        "__client_uat": ADAPTA_CLIENT_UAT,
        f"__client_uat_{CLERK_KEY_SUFFIX}": ADAPTA_CLIENT_UAT,
        "clerk_active_context": f"{ADAPTA_SESSION_ID}:",
    }


def _clerk_headers() -> dict:
    return {
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://agent.adapta.one",
        "referer": "https://agent.adapta.one/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept": "*/*",
    }


async def _fetch_clerk_token() -> str:
    """Obtém JWT fresco chamando a API do Clerk diretamente via httpx."""
    global _bearer_token, _bearer_expires

    params = {
        "__clerk_api_version": "2025-11-10",
        "_clerk_js_version": "5.127.1",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        url = f"{CLERK_BASE}/v1/client/sessions/{ADAPTA_SESSION_ID}/tokens"
        resp = await client.post(
            url,
            params=params,
            headers=_clerk_headers(),
            cookies=_clerk_cookies(),
        )

        logger.info(f"[AdaptaBridge] Clerk /tokens → HTTP {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            jwt = data.get("jwt", "")
            if jwt:
                _bearer_token = jwt
                _bearer_expires = time.time() + 50  # 50s cache (token dura 60s)
                logger.info("[AdaptaBridge] ✅ Bearer token obtido via Clerk API")
                return jwt

        logger.error(f"[AdaptaBridge] Clerk erro: {resp.status_code} — {resp.text[:300]}")
        raise RuntimeError(
            f"Clerk API retornou {resp.status_code}. "
            "Sessão provavelmente expirou. "
            "Atualize ADAPTA_SESSION_ID e ADAPTA_CLIENT_UAT no Railway."
        )


async def _get_token() -> str:
    """Retorna Bearer token válido, renovando via Clerk API se necessário."""
    global _bearer_token, _bearer_expires

    if _bearer_token and time.time() < _bearer_expires - 5:
        return _bearer_token

    async with _token_lock:
        if _bearer_token and time.time() < _bearer_expires - 5:
            return _bearer_token
        return await _fetch_clerk_token()


async def send_to_adapta(
    prompt: str,
    model: str = "ONE",
    context_text: str = "",
) -> str:
    """
    Envia um prompt ao Adapta One e retorna a resposta completa.

    Args:
        prompt: Mensagem do usuário
        model: Modelo Adapta ('ONE', 'GPT-5.1', 'Claude 5 Sonnet',
               'Gemini 3.5 Flash', 'ONE Image', etc.)
        context_text: Contexto adicional para prefixar ao prompt

    Returns:
        Texto completo da resposta do Adapta
    """
    if not ADAPTA_SESSION_ID:
        return "❌ ADAPTA_SESSION_ID não configurada. Adicione no Railway."

    token = await _get_token()

    chat_id = _uuid7()
    message_id = _uuid7()
    full_prompt = f"{context_text}\n\n{prompt}".strip() if context_text else prompt

    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": ADAPTA_BASE,
        "referer": f"{ADAPTA_BASE}/agentic-chat/{chat_id}",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            await client.post(
                f"{ADAPTA_BASE}/api/chat/init/v1",
                json={"chatId": chat_id, "isTemporaryChat": True},
                headers=headers,
            )
        except Exception as e:
            logger.debug(f"[AdaptaBridge] init/v1 ignorado: {e}")

    payload = {
        "mandatoryTools": [],
        "chatId": chat_id,
        "contextsIds": [],
        "meetingContextsIds": [],
        "modelAi": model,
        "preloadedData": {
            "companyGlobalSettings": None,
            "deactivatedToolNames": [],
            "chatSummary": None,
            "userProfile": None,
            "chatFiles": {"images": [], "sheets": [], "presentations": []},
            "projectAutoContext": {
                "contextsList": [], "meetingContexts": "",
                "chatFiles": {"images": [], "sheets": [], "presentations": []},
                "projectContextCount": 0, "projectFileCount": 0,
            },
            "chatDocument": {
                "activeDocument": None, "allDocuments": [],
                "activeDocumentId": None, "activeDocumentMarkdown": None,
            },
            "isMemoriesEnabled": False,
            "userDisabledTools": {},
            "userTierLimit": False,
            "snapshotToken": f"{int(time.time() * 1000)}:jarbas-bridge",
            "contextsList": [],
            "meetingContexts": "",
        },
        "amplitudeContext": {
            "deviceId": "jarbas-bridge",
            "sessionId": int(time.time() * 1000),
        },
        "id": chat_id,
        "messages": [
            {
                "id": message_id,
                "role": "user",
                "parts": [{"type": "text", "text": full_prompt}],
            }
        ],
        "trigger": "submit-message",
        "messageId": message_id,
    }

    text_parts: list[str] = []

    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                async with client.stream(
                    "POST",
                    f"{ADAPTA_BASE}/api/chat/stream/v1",
                    json=payload,
                    headers=headers,
                ) as resp:
                    if resp.status_code == 401 and attempt == 0:
                        logger.warning("[AdaptaBridge] 401 — forçando renovação de token...")
                        global _bearer_token
                        _bearer_token = ""
                        token = await _get_token()
                        headers["authorization"] = f"Bearer {token}"
                        continue

                    resp.raise_for_status()

                    async for line in resp.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        raw = line[6:]
                        if raw in ("[DONE]", ""):
                            continue
                        try:
                            chunk = json.loads(raw)
                            if chunk.get("type") == "text-delta":
                                text_parts.append(chunk.get("delta", ""))
                        except json.JSONDecodeError:
                            pass
            break

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401 and attempt == 0:
                _bearer_token = ""
                token = await _get_token()
                headers["authorization"] = f"Bearer {token}"
            else:
                logger.error(f"[AdaptaBridge] HTTP {exc.response.status_code}: {exc}")
                return f"❌ Erro ao contactar Adapta: HTTP {exc.response.status_code}"
        except Exception as exc:
            logger.error(f"[AdaptaBridge] Erro inesperado: {exc}")
            return f"❌ Erro Adapta Bridge: {exc}"

    result = "".join(text_parts)
    logger.info(f"[AdaptaBridge] ✅ Resposta recebida ({len(result)} chars) | modelo: {model}")
    return result or "⚠️ Adapta retornou resposta vazia."


async def check_status() -> dict:
    """Status da conexão com Adapta One."""
    if not ADAPTA_SESSION_ID:
        return {"connected": False, "reason": "ADAPTA_SESSION_ID não configurada"}
    try:
        tok = await _get_token()
        return {
            "connected": bool(tok),
            "session_id": f"{ADAPTA_SESSION_ID[:10]}...",
            "token_valid_seconds": max(0, int(_bearer_expires - time.time())),
        }
    except Exception as exc:
        return {"connected": False, "reason": str(exc)}
