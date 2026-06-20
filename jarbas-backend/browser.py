"""
JARBAS Browser Tools — Playwright headless browser automation.
"""
import base64

try:
    from playwright.async_api import async_playwright, TimeoutError as PWTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

_UNAVAILABLE = (
    "Playwright não instalado no servidor. "
    "Adicione 'playwright' ao requirements.txt e execute 'playwright install chromium'."
)
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


async def take_screenshot(url: str, full_page: bool = False) -> dict:
    """
    Take a screenshot of the given URL using headless Chromium.
    Returns {"base64": str, "url": str} on success, {"error": str} on failure.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return {"error": _UNAVAILABLE}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                viewport={"width": 1280, "height": 720},
                user_agent=_USER_AGENT,
            )
            await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            await page.wait_for_timeout(1_500)
            screenshot = await page.screenshot(full_page=full_page)
            await browser.close()
        return {"base64": base64.b64encode(screenshot).decode(), "url": url}
    except PWTimeout:
        return {"error": f"Timeout ao carregar {url} (>30s)."}
    except Exception as exc:
        return {"error": f"Erro ao capturar screenshot: {exc}"}


async def browse_and_read(url: str) -> str:
    """
    Open a URL and extract its main text content (up to 6000 chars).
    """
    if not PLAYWRIGHT_AVAILABLE:
        return _UNAVAILABLE
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(user_agent=_USER_AGENT)
            await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            title = await page.title()
            text = await page.evaluate("""() => {
                document.querySelectorAll(
                    'script,style,nav,footer,header,aside,[role="navigation"]'
                ).forEach(el => el.remove());
                const root = document.querySelector('main,article,.content,#content,body');
                return (root || document.body).innerText
                    .replace(/\\n{3,}/g, '\\n\\n')
                    .trim()
                    .substring(0, 6000);
            }""")
            await browser.close()
        return f"**Título:** {title}\n\n**Conteúdo:**\n{text}"
    except PWTimeout:
        return f"Timeout ao carregar {url}."
    except Exception as exc:
        return f"Erro ao ler página: {exc}"
