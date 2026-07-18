"""
Adapta Bridge — integração JARBAS ↔ Adapta One 26

Fluxo:
  1. Playwright headless abre agent.adapta.one com cookies da sessão
  2. Captura Bearer token (Clerk JWT) automaticamente via interceptação de rede
  3. httpx faz as chamadas à API interna do Adapta (/api/chat/stream/v1)
  4. Resposta SSE é parseada para extrair text-delta → texto completo

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
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

logger = logging.getLogger(__name__)

ADAPTA_BASE = "https://agent.adapta.one"
ADAPTA_CHAT_URL = f"{ADAPTA_BASE}/agentic-chat"

ADAPTA_SESSION_ID = os.getenv("ADAPTA_SESSION_ID", "")
ADAPTA_CLIENT_UAT = os.getenv("ADAPTA_CLIENT_UAT", "")

_pw = None
_browser: Browser = None
_context: BrowserContext = None
_page: Page = None

_bearer_token: str = ""
_bearer_expires: float = 0.0
_initialized: bool = False
_init_lock = asyncio.Lock()


def _uuid7() -> str:
    """Gera UUID v7 compatível com o formato usado pelo Adapta."""
    ts_ms = int(time.time() * 1000)
    rand_bytes = uuid.uuid4().bytes
    # 48 bits timestamp | 4 bits versão (7) | 12 bits rand | 2 bits variante | 62 bits rand
    b = bytearray(16)
    struct.pack_into(">Q", b, 0, ts_ms)
    b[0] = b[1] = 0
    b[6] = (b[6] & 0x0F) | 0x70  # version 7
    for i in range(6, 16):
        b[i] ^= rand_bytes[i]
    b[8] = (b[8] & 0x3F) | 0x80  # variant
    h = b.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


async def _start_playwright():
    """Inicializa browser headless e adiciona cookies da sessão."""
    global _pw, _browser, _context, _page

    logger.info("[AdaptaBridge] Iniciando Playwright headless...")
    _pw = await async_playwright().start()
    _browser = await _pw.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
              "--disable-setuid-sandbox", "--single-process"],
    )
    _context = await _browser.new_context(
        user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )

    if ADAPTA_SESSION_ID and ADAPTA_CLIENT_UAT:
        cookies = [
            {"name": "__client_uat",
             "value": ADAPTA_CLIENT_UAT,
             "domain": ".agent.adapta.one", "path": "/"},
            {"name": "__client_uat_0GUur0zr",
             "value": ADAPTA_CLIENT_UAT,
             "domain": ".agent.adapta.one", "path": "/"},
            {"name": "clerk_active_context",
             "value": f"{ADAPTA_SESSION_ID}:",
             "domain": ".agent.adapta.one", "path": "/"},
        ]
        await _context.add_cookies(cookies)
        logger.info("[AdaptaBridge] Cookies da sessão carregados.")

    _page = await _context.new_page()


async def _refresh_bearer_token() -> str:
    """Navega para o Adapta e captura o Bearer token renovado via Clerk."""
    global _bearer_token, _bearer_expires

    captured = asyncio.Event()

    async def on_response(response):
        global _bearer_token, _bearer_expires
        if "clerk" in response.url and "/tokens" in response.url:
            try:
                body = await response.json()
                jwt = body.get("jwt", "")
                if jwt:
                    _bearer_token = jwt
                    _bearer_expires = time.time() + 240  # 4 min cache
                    logger.info("[AdaptaBridge] Bearer token capturado.")
                    captured.set()
            except Exception:
                pass

    _page.on("response", on_response)
    try:
        await _page.goto(ADAPTA_CHAT_URL, wait_until="domcontentloaded", timeout=25000)
        await asyncio.wait_for(captured.wait(), timeout=12.0)
    except asyncio.TimeoutError:
        logger.warning("[AdaptaBridge] Timeout ao capturar token JWT.")
    finally:
        _page.remove_listener("response", on_response)

    if "/sign-in" in _page.url:
        raise RuntimeError(
            "Adapta One: sessão expirada. "
            "Atualize ADAPTA_SESSION_ID e ADAPTA_CLIENT_UAT no Railway."
        )

    if not _bearer_token:
        raise RuntimeError(
            "Adapta One: não conseguiu obter Bearer token. "
            "Verifique ADAPTA_SESSION_ID e ADAPTA_CLIENT_UAT."
        )

    return _bearer_token


async def _get_token() -> str:
    """Retorna Bearer token válido, renovando se necessário."""
    global _initialized

    if _bearer_token and time.time() < _bearer_expires - 30:
        return _bearer_token

    async with _init_lock:
        if _bearer_token and time.time() < _bearer_expires - 30:
            return _bearer_token

        if not _initialized:
            await _start_playwright()
            _initialized = True

        return await _refresh_bearer_token()


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
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    # Inicializa o chat
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
