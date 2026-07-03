"""
JARBAS IXC Soft Integration — Servlink Telecom
Automação Playwright para acesso ao sistema IXC (https://ixc.servlinktelecom.com.br)

Fluxo de autenticação:
  1. ixc_login()           → entra com email/senha → se 2FA pedido, retorna aviso
  2. ixc_login(code="XXX") → usa o mesmo browser em memória para submeter o 2FA
  3. Demais ferramentas usam a sessão ativa ou cookies salvos em disco
"""

import json
import os
from datetime import datetime

try:
    from playwright.async_api import async_playwright, TimeoutError as PWTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# ── Configuração ───────────────────────────────────────────────────────────

IXC_BASE = "https://ixc.servlinktelecom.com.br"
IXC_LOGIN_URL = f"{IXC_BASE}/app/login"

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Cookies salvos em disco (volume persistente no Railway)
_COOKIES_PATHS = [
    os.getenv("IXC_COOKIES_PATH", "/data/ixc_session.json"),
    "/tmp/ixc_session.json",
]

# ── Estado da sessão em memória ────────────────────────────────────────────
# Mantido entre tool calls enquanto o processo Railway estiver rodando.
_sess = {
    "playwright": None,
    "browser": None,
    "context": None,
    "page": None,
    "logged_in": False,
    "awaiting_2fa": False,
}


# ── Helpers de cookies ─────────────────────────────────────────────────────

async def _save_cookies():
    if not _sess["context"]:
        return
    cookies = await _sess["context"].cookies()
    for path in _COOKIES_PATHS:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(cookies, f)
            return  # salvo com sucesso
        except Exception:
            continue


def _load_cookies() -> list | None:
    for path in _COOKIES_PATHS:
        try:
            with open(path) as f:
                data = json.load(f)
            if data:
                return data
        except Exception:
            continue
    return None


# ── Gerenciamento do browser ───────────────────────────────────────────────

async def _close_session():
    global _sess
    try:
        if _sess["page"] and not _sess["page"].is_closed():
            await _sess["page"].close()
    except Exception:
        pass
    try:
        if _sess["context"]:
            await _sess["context"].close()
    except Exception:
        pass
    try:
        if _sess["browser"] and _sess["browser"].is_connected():
            await _sess["browser"].close()
    except Exception:
        pass
    try:
        if _sess["playwright"]:
            await _sess["playwright"].stop()
    except Exception:
        pass
    _sess.update({
        "playwright": None, "browser": None, "context": None,
        "page": None, "logged_in": False, "awaiting_2fa": False,
    })


async def _new_browser():
    """Abre um novo browser e context, salvando em _sess."""
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    context = await browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent=_UA,
    )
    page = await context.new_page()
    _sess.update({
        "playwright": pw, "browser": browser,
        "context": context, "page": page,
    })
    return page


async def _active_page():
    """Retorna a page ativa ou None se sessão inválida."""
    if _sess["page"] and not _sess["page"].is_closed():
        return _sess["page"]
    return None


# ── Login ──────────────────────────────────────────────────────────────────

async def ixc_login(ixc_email: str, ixc_password: str, two_fa_code: str = "") -> str:
    """
    Realiza login no IXC Soft.

    Fluxo:
    - Se two_fa_code vazio: abre browser, preenche email/senha, submete.
      - Sem 2FA: salva cookies, retorna OK.
      - Com 2FA: mantém browser aberto, retorna pedido do código.
    - Se two_fa_code fornecido: usa browser ainda aberto para submeter código.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return "❌ Playwright não disponível. Adicione 'playwright' ao requirements.txt."

    # ── Caso 1: Submeter código 2FA em sessão pendente ──────────────────────
    if two_fa_code and _sess["awaiting_2fa"]:
        page = await _active_page()
        if page:
            try:
                # Tenta preencher o input do código (IXC usa campos variados)
                for selector in [
                    'input[type="text"]',
                    'input[name="token"]',
                    'input[name="code"]',
                    'input[placeholder*="código"]',
                    'input[placeholder*="token"]',
                    'input',
                ]:
                    try:
                        await page.fill(selector, two_fa_code, timeout=3_000)
                        break
                    except Exception:
                        continue

                # Submete
                for btn_selector in ['button[type="submit"]', 'button:has-text("Verificar")', 'button:has-text("Entrar")', 'button']:
                    try:
                        await page.click(btn_selector, timeout=3_000)
                        break
                    except Exception:
                        continue

                await page.wait_for_timeout(4_000)
                url = page.url

                if "/login" not in url and "2fa" not in url and "token" not in url:
                    _sess["logged_in"] = True
                    _sess["awaiting_2fa"] = False
                    await _save_cookies()
                    return "✅ 2FA validado! Sessão IXC ativa. Pode usar as ferramentas IXC agora."

                return (
                    f"❌ Código inválido ou expirado. URL atual: {url}\n"
                    "Tente novamente com o novo código enviado ao e-mail."
                )
            except Exception as exc:
                return f"❌ Erro ao submeter 2FA: {exc}"
        else:
            return "⚠️ Sessão expirou. Chame ixc_login() novamente para iniciar um novo login."

    # ── Caso 2: Iniciar login do zero ──────────────────────────────────────
    await _close_session()

    # Tenta restaurar sessão via cookies salvos
    cookies = _load_cookies()
    if cookies:
        page = await _new_browser()
        await _sess["context"].add_cookies(cookies)
        try:
            await page.goto(f"{IXC_BASE}/app/dashboard", wait_until="domcontentloaded", timeout=25_000)
            await page.wait_for_timeout(2_500)
            if "/login" not in page.url:
                _sess["logged_in"] = True
                return "✅ Sessão IXC restaurada via cookies salvos. Já autenticado!"
        except Exception:
            pass
        # Cookies inválidos — fecha e recomeça
        await _close_session()

    # Login limpo
    page = await _new_browser()

    try:
        await page.goto(IXC_LOGIN_URL, wait_until="domcontentloaded", timeout=30_000)
        await page.wait_for_timeout(2_000)

        # Preenche e-mail
        for sel in ['input[type="email"]', 'input[name="email"]', 'input[name="user"]', 'input']:
            try:
                await page.fill(sel, ixc_email, timeout=3_000)
                break
            except Exception:
                continue

        # Preenche senha
        for sel in ['input[type="password"]', 'input[name="password"]', 'input[name="senha"]']:
            try:
                await page.fill(sel, ixc_password, timeout=3_000)
                break
            except Exception:
                continue

        # Submete
        for sel in ['button[type="submit"]', 'button:has-text("Entrar")', 'button:has-text("Login")', 'button']:
            try:
                await page.click(sel, timeout=3_000)
                break
            except Exception:
                continue

        await page.wait_for_timeout(5_000)
        url = page.url
        body = (await page.inner_text("body")).lower() if not page.is_closed() else ""

        # Detecta pedido de 2FA
        _2fa_signals = ["verificação", "verification", "código", "token", "2fa", "two-factor", "autenticação de dois"]
        if any(s in body for s in _2fa_signals) or any(s in url.lower() for s in ["2fa", "token", "verify", "verificacao"]):
            _sess["awaiting_2fa"] = True
            return (
                "🔐 IXC solicitou verificação em 2 etapas.\n\n"
                "Um código foi enviado para **ramon@servlink.com.br**.\n\n"
                "Quando receber o código, use:\n"
                "`ixc_login(two_fa_code='SEU_CÓDIGO')`"
            )

        if "/login" in url:
            return f"❌ Login falhou. Ainda na página de login. Verifique as credenciais."

        _sess["logged_in"] = True
        await _save_cookies()
        return "✅ Login no IXC realizado com sucesso! Sessão salva."

    except PWTimeout:
        return "❌ Timeout ao acessar o IXC. Tente novamente."
    except Exception as exc:
        return f"❌ Erro no login IXC: {exc}"


# ── ONUs — Rede Neutra ─────────────────────────────────────────────────────

async def _ensure_logged_in(ixc_email: str, ixc_password: str) -> str | None:
    """
    Garante sessão ativa. Retorna None se OK, ou mensagem de erro se falhou.
    """
    # Sessão em memória OK
    if _sess["logged_in"] and await _active_page():
        return None

    # Tenta cookies
    cookies = _load_cookies()
    if cookies:
        await _close_session()
        page = await _new_browser()
        await _sess["context"].add_cookies(cookies)
        try:
            await page.goto(f"{IXC_BASE}/app/dashboard", wait_until="domcontentloaded", timeout=25_000)
            await page.wait_for_timeout(2_000)
            if "/login" not in page.url:
                _sess["logged_in"] = True
                return None
        except Exception:
            pass

    # Login automático (sem 2FA)
    result = await ixc_login(ixc_email, ixc_password)
    if "✅" in result:
        return None
    return result  # retorna a mensagem de erro/2FA


async def ixc_get_onus_rede_neutra(ixc_email: str, ixc_password: str, limit: int = 100) -> str:
    """
    Lista ONUs da rede neutra no IXC Soft.
    Navega para o módulo de ONU, aplica filtro 'Rede Neutra' e retorna a tabela.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return "❌ Playwright não disponível."

    err = await _ensure_logged_in(ixc_email, ixc_password)
    if err:
        return err

    page = await _active_page()
    if not page:
        return "❌ Página IXC não disponível. Chame ixc_login() primeiro."

    try:
        # Candidatos de URL para o módulo ONU no IXC Soft
        onu_urls = [
            f"{IXC_BASE}/app/onu",
            f"{IXC_BASE}/app/network/onu",
            f"{IXC_BASE}/app/provedor/onu",
            f"{IXC_BASE}/app/cto/onu",
            f"{IXC_BASE}/app/onu_list",
        ]

        loaded_url = None
        for url in onu_urls:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=15_000)
                await page.wait_for_timeout(2_500)
                body = (await page.inner_text("body")).lower()
                if "onu" in body and "/login" not in page.url:
                    loaded_url = url
                    break
            except Exception:
                continue

        if not loaded_url:
            # Tenta buscar pelo menu
            await page.goto(f"{IXC_BASE}/app/dashboard", wait_until="domcontentloaded", timeout=20_000)
            await page.wait_for_timeout(2_000)

            for label in ["ONU", "Rede Neutra", "Fibra", "GPON"]:
                try:
                    elem = page.locator(f"text={label}").first
                    if await elem.is_visible(timeout=2_000):
                        await elem.click()
                        await page.wait_for_timeout(2_000)
                        break
                except Exception:
                    continue

            body = (await page.inner_text("body")).lower()
            if "onu" not in body:
                return (
                    "⚠️ Não encontrei a página de ONUs no IXC automaticamente.\n"
                    f"URL atual: {page.url}\n"
                    "Tente `ixc_screenshot()` para ver o estado atual da tela."
                )

        # Aguarda tabela carregar
        await page.wait_for_timeout(2_000)

        # Tenta filtrar por "Rede Neutra"
        filter_applied = False
        for filter_text in ["Rede Neutra", "rede_neutra", "rede neutra"]:
            try:
                # Tenta campo de filtro/busca
                for sel in ['input[placeholder*="filtrar"]', 'input[placeholder*="buscar"]', 'input[placeholder*="pesquisar"]', 'input.filter', '.search-input input']:
                    try:
                        await page.fill(sel, filter_text, timeout=2_000)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(2_000)
                        filter_applied = True
                        break
                    except Exception:
                        continue
                if filter_applied:
                    break
            except Exception:
                continue

        # Extrai dados da tabela
        data = await page.evaluate("""() => {
            const rows = [];
            const tables = document.querySelectorAll('table, .grid, [role="grid"], .datatable');

            for (const table of tables) {
                const headers = [];
                const headerCells = table.querySelectorAll('th, .header-cell, [role="columnheader"]');
                headerCells.forEach(h => headers.push(h.innerText.trim()));

                const bodyRows = table.querySelectorAll('tr, [role="row"]');
                for (const row of bodyRows) {
                    const cells = row.querySelectorAll('td, [role="cell"]');
                    if (cells.length > 2) {
                        const rowData = {};
                        cells.forEach((cell, i) => {
                            const header = headers[i] || `col_${i}`;
                            rowData[header] = cell.innerText.trim();
                        });
                        if (Object.values(rowData).some(v => v.length > 0)) {
                            rows.push(rowData);
                        }
                    }
                }
                if (rows.length > 0) break;
            }
            return rows;
        }""")

        if not data:
            page_text = await page.inner_text("body")
            return (
                f"⚠️ Tabela de ONUs não encontrada ou sem dados.\n"
                f"URL atual: {page.url}\n"
                f"Conteúdo da página (primeiros 500 chars):\n{page_text[:500]}"
            )

        # Filtra apenas registros que mencionem "rede neutra"
        rede_neutra_rows = [
            r for r in data
            if any("rede neutra" in str(v).lower() or "rede_neutra" in str(v).lower() for v in r.values())
        ]
        rows_to_show = rede_neutra_rows if rede_neutra_rows else data
        rows_to_show = rows_to_show[:limit]

        total = len(data)
        neutra_count = len(rede_neutra_rows)

        lines = [
            f"📡 **ONUs — IXC Servlink** _(atualizado {datetime.now().strftime('%d/%m %H:%M')})_\n",
            f"Total na página: **{total}** · Rede neutra: **{neutra_count}** · Exibindo: **{len(rows_to_show)}**\n",
        ]

        if rows_to_show:
            # Mostra colunas disponíveis
            cols = list(rows_to_show[0].keys())
            lines.append(f"Colunas: {', '.join(cols)}\n")
            lines.append("---")
            for r in rows_to_show[:30]:  # Máx 30 linhas em texto
                summary = " | ".join(f"{k}: {v}" for k, v in r.items() if v)
                lines.append(f"• {summary}")
            if len(rows_to_show) > 30:
                lines.append(f"\n_... e mais {len(rows_to_show) - 30} registros_")

        return "\n".join(lines)

    except PWTimeout:
        return "❌ Timeout ao carregar página de ONUs no IXC."
    except Exception as exc:
        return f"❌ Erro ao buscar ONUs: {exc}"


async def ixc_get_onus_online_por_vlan(ixc_email: str, ixc_password: str, vlan: str = "") -> str:
    """
    Lista ONUs online da rede neutra agrupadas por VLAN.
    Se vlan for fornecida, filtra apenas essa VLAN.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return "❌ Playwright não disponível."

    err = await _ensure_logged_in(ixc_email, ixc_password)
    if err:
        return err

    page = await _active_page()
    if not page:
        return "❌ Página IXC não disponível. Chame ixc_login() primeiro."

    try:
        # Navega para a lista de ONUs (tenta URL direta)
        onu_url = f"{IXC_BASE}/app/onu"
        await page.goto(onu_url, wait_until="domcontentloaded", timeout=20_000)
        await page.wait_for_timeout(3_000)

        # Aplica filtro de status "online" se disponível
        for sel in ['select[name*="status"]', 'select[name*="estado"]']:
            try:
                await page.select_option(sel, label="Online", timeout=2_000)
                await page.wait_for_timeout(1_500)
                break
            except Exception:
                continue

        # Aplica filtro de VLAN se fornecido
        if vlan:
            for sel in ['input[name*="vlan"]', 'input[placeholder*="vlan"]', 'input[placeholder*="VLAN"]']:
                try:
                    await page.fill(sel, vlan, timeout=2_000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(2_000)
                    break
                except Exception:
                    continue

        await page.wait_for_timeout(2_000)

        # Extrai tabela
        data = await page.evaluate("""() => {
            const rows = [];
            const tables = document.querySelectorAll('table');
            for (const table of tables) {
                const headers = [...table.querySelectorAll('th')].map(h => h.innerText.trim());
                const bodyRows = [...table.querySelectorAll('tbody tr')];
                for (const row of bodyRows) {
                    const cells = [...row.querySelectorAll('td')];
                    if (cells.length > 2) {
                        const obj = {};
                        cells.forEach((c, i) => { obj[headers[i] || `col_${i}`] = c.innerText.trim(); });
                        rows.push(obj);
                    }
                }
                if (rows.length > 0) break;
            }
            return rows;
        }""")

        if not data:
            return f"⚠️ Nenhum dado encontrado. URL: {page.url}"

        # Agrupa por VLAN
        vlan_map: dict[str, list] = {}
        for row in data:
            row_vlan = ""
            for key, val in row.items():
                if "vlan" in key.lower():
                    row_vlan = str(val)
                    break
            vlan_map.setdefault(row_vlan or "sem VLAN", []).append(row)

        lines = [
            f"📡 **ONUs Online por VLAN — IXC Servlink**",
            f"_{datetime.now().strftime('%d/%m/%Y %H:%M')}_\n",
            f"Total encontrado: **{len(data)}** ONUs\n",
        ]

        if vlan:
            target_data = vlan_map.get(vlan, [])
            lines.append(f"🔍 Filtro VLAN **{vlan}**: **{len(target_data)}** ONUs\n")
            for r in target_data[:50]:
                lines.append("• " + " | ".join(f"{k}: {v}" for k, v in r.items() if v))
        else:
            for v, rows in sorted(vlan_map.items()):
                lines.append(f"\n**VLAN {v}** — {len(rows)} ONU(s)")
                for r in rows[:10]:
                    lines.append("  • " + " | ".join(f"{k}: {v}" for k, v in r.items() if v))
                if len(rows) > 10:
                    lines.append(f"  _...e mais {len(rows)-10}_")

        return "\n".join(lines)

    except PWTimeout:
        return "❌ Timeout ao carregar página de ONUs."
    except Exception as exc:
        return f"❌ Erro ao buscar ONUs por VLAN: {exc}"


async def ixc_screenshot(ixc_email: str, ixc_password: str) -> dict:
    """
    Tira screenshot da tela atual do IXC (para diagnóstico).
    Retorna dict com base64 da imagem.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return {"error": "Playwright não disponível."}

    err = await _ensure_logged_in(ixc_email, ixc_password)
    if err:
        return {"error": err}

    page = await _active_page()
    if not page:
        return {"error": "Nenhuma sessão ativa."}

    try:
        import base64
        shot = await page.screenshot(full_page=False)
        return {"base64": base64.b64encode(shot).decode(), "url": page.url}
    except Exception as exc:
        return {"error": f"Erro ao capturar screenshot: {exc}"}
