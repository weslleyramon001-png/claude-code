"""
JARBAS Agent Tools

All tools are async functions that Claude can invoke via tool_use.
Each tool has a corresponding entry in the Claude tools list format.
"""

import math
import re
from datetime import datetime
from typing import Any
import httpx
import pytz
from browser import take_screenshot, browse_and_read


# ── Tool implementations ───────────────────────────────────────────────────

async def get_current_datetime() -> str:
    """
    Return the current date and time in Brazilian format (America/Sao_Paulo timezone).
    """
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)

    # Brazilian weekday names
    weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    months = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]

    weekday = weekdays[now.weekday()]
    month = months[now.month - 1]

    return (
        f"{weekday}, {now.day} de {month} de {now.year} — "
        f"{now.strftime('%H:%M')} (horário de Brasília)"
    )


async def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression and return the result.

    Supports: +, -, *, /, **, %, sqrt(), abs(), round(), floor(), ceil(),
              log(), log10(), sin(), cos(), tan(), pi, e

    Args:
        expression: Math expression as a string, e.g. "2 ** 10 + sqrt(144)"

    Returns:
        Result string or error message.
    """
    # Whitelist: only allow safe characters for math
    safe_pattern = re.compile(r'^[\d\s\+\-\*/\(\)\.\,\%\*\^a-z_]+$', re.IGNORECASE)
    if not safe_pattern.match(expression):
        return "Expressão inválida. Apenas operações matemáticas são permitidas."

    # Build a restricted namespace with math functions
    safe_names: dict[str, Any] = {
        "sqrt": math.sqrt,
        "abs": abs,
        "round": round,
        "floor": math.floor,
        "ceil": math.ceil,
        "log": math.log,
        "log10": math.log10,
        "log2": math.log2,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
        "pow": pow,
        "max": max,
        "min": min,
    }

    try:
        # Replace ^ with ** for convenience
        expr_clean = expression.replace("^", "**").replace(",", ".")
        result = eval(expr_clean, {"__builtins__": {}}, safe_names)  # noqa: S307

        # Format nicely
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return f"{result:,.6f}".rstrip("0").rstrip(".")
        return str(result)
    except ZeroDivisionError:
        return "Erro: divisão por zero."
    except Exception as exc:
        return f"Erro ao calcular: {exc}"


async def web_search(query: str, api_key: str) -> str:
    """
    Search the web via the Tavily API and return formatted results.

    Args:
        query:   Search query string.
        api_key: Tavily API key.

    Returns:
        Formatted string with search results, or error/placeholder message.
    """
    if not api_key:
        return (
            "Busca na web indisponível — chave da API Tavily não configurada. "
            "Adicione TAVILY_API_KEY no arquivo .env para habilitar esta função."
        )

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "include_raw_content": False,
        "max_results": 5,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        return "Busca expirou. Tente novamente em instantes."
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 401:
            return "Chave da API Tavily inválida. Verifique o valor de TAVILY_API_KEY."
        return f"Erro na busca (HTTP {exc.response.status_code}). Tente novamente."
    except Exception as exc:
        return f"Erro inesperado na busca: {exc}"

    lines: list[str] = []

    # Include the AI-generated answer if available
    answer = data.get("answer", "").strip()
    if answer:
        lines.append(f"**Resposta direta:** {answer}\n")

    results = data.get("results", [])
    if not results:
        return "Nenhum resultado encontrado para essa busca."

    lines.append("**Fontes:**")
    for i, r in enumerate(results[:5], 1):
        title = r.get("title", "Sem título")
        url = r.get("url", "")
        snippet = r.get("content", "")[:300].strip()
        lines.append(f"{i}. **{title}**")
        if snippet:
            lines.append(f"   {snippet}")
        if url:
            lines.append(f"   {url}")
        lines.append("")

    return "\n".join(lines).strip()


async def create_file_content(filename: str, content: str, file_type: str = "text") -> str:
    """
    Format content as a 'file' to be shown to the user.
    JARBAS doesn't write to disk directly — it returns structured content
    that the UI can offer as a download.

    Args:
        filename:  Suggested filename.
        content:   File content.
        file_type: Hint for syntax highlighting (python, markdown, json, etc.)

    Returns:
        Formatted string the UI can render as a downloadable code block.
    """
    lang = file_type.lower().strip()
    return (
        f"**Arquivo: `{filename}`**\n\n"
        f"```{lang}\n{content}\n```\n\n"
        f"*Copie o conteúdo acima ou salve como `{filename}`.*"
    )


async def generate_pony_digital_content(content_type: str, topic: str) -> str:
    """
    Generate Pony-Digital specific content for Instagram or sales copy.

    Args:
        content_type: One of: hook, caption, email, cta, headline
        topic:        The subject of the content (e.g. "planilhas", "produtividade", "finanças")

    Returns:
        Generated content ready to use.
    """
    templates = {
        "hook": [
            f"Se você ainda não controla seu {topic}, você está deixando dinheiro na mesa.",
            f"Eu perdi R$3.000 por não usar {topic} certo. Hoje eu te mostro como evitar isso.",
            f"O segredo dos empreendedores que faturam mais está no {topic}. Veja o que ninguém te conta.",
            f"Para de fazer {topic} na mão. Existe uma forma mais inteligente — e gratuita.",
            f"Em 2 minutos você vai entender por que seu {topic} não está funcionando.",
        ],
        "caption": (
            f"A maioria das pessoas ignora {topic} até ser tarde demais.\n\n"
            f"Eu aprendi da forma difícil que controlar {topic} é o primeiro passo para qualquer negócio sério.\n\n"
            f"Por isso criei uma planilha que resolve isso de uma vez por todas.\n\n"
            f"👇 Link na bio para baixar agora.\n\n"
            f"#PonyDigital #Empreendedorismo #Planilhas #{topic.replace(' ', '')}"
        ),
        "email": (
            f"Assunto: Sobre o seu {topic}...\n\n"
            f"Olá,\n\n"
            f"Quero falar sobre {topic} de uma forma diferente hoje.\n\n"
            f"A maioria das pessoas só pensa nisso quando o problema já explodiu.\n\n"
            f"Mas os empreendedores que realmente crescem tratam {topic} como prioridade desde o dia 1.\n\n"
            f"É por isso que criei a planilha de {topic} — para você ter controle total, sem complicação.\n\n"
            f"Clique aqui para ver: [LINK]\n\n"
            f"Até mais,\nRamon"
        ),
        "cta": [
            f"👉 Baixe a planilha de {topic} — link na bio",
            f"✅ Acesse agora: planilha de {topic} com tudo pronto",
            f"🔗 Link na bio → Planilha de {topic} (oferta por tempo limitado)",
            f"💡 Quer dominar {topic}? Clica no link da bio",
        ],
        "headline": [
            f"Planilha de {topic.title()}: Controle Total em Menos de 5 Minutos",
            f"Chega de Perder Dinheiro com {topic.title()} — Use a Planilha Certa",
            f"O Sistema Definitivo de {topic.title()} para Empreendedores",
            f"Domine seu {topic.title()} com Esta Planilha Profissional",
        ],
    }

    ct = content_type.lower().strip()
    if ct not in templates:
        return (
            f"Tipo de conteúdo '{content_type}' não reconhecido. "
            f"Use: hook, caption, email, cta, ou headline."
        )

    result = templates[ct]
    if isinstance(result, list):
        import random
        return f"**{content_type.upper()} para '{topic}':**\n\n" + "\n\n—\n\n".join(result)
    return f"**{content_type.upper()} para '{topic}':**\n\n{result}"


async def get_weather(city: str) -> str:
    """
    Placeholder weather function.
    Returns a polite message explaining no weather API key is configured.

    Args:
        city: City name requested by the user.

    Returns:
        Polite unavailability message.
    """
    return (
        f"Previsão do tempo para {city} está indisponível no momento. "
        "A integração com API de clima ainda não foi configurada. "
        "Você pode conferir manualmente em tempo.ig.com.br ou weather.com."
    )


# ── Claude tool definitions ────────────────────────────────────────────────

def format_tools_for_claude() -> list[dict]:
    """
    Return the tools list in Claude API format (to pass as the `tools` parameter).
    Each tool maps to an async function above.
    """
    return [
        {
            "name": "get_current_datetime",
            "description": (
                "Retorna a data e hora atual no fuso horário de Brasília. "
                "Use quando o usuário perguntar que horas são, qual é a data de hoje, etc."
            ),
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        {
            "name": "calculate",
            "description": (
                "Calcula expressões matemáticas com segurança. "
                "Suporta operações básicas (+, -, *, /), potenciação (**), raiz quadrada (sqrt), "
                "logaritmos, funções trigonométricas, e constantes pi e e. "
                "Use para qualquer cálculo numérico solicitado pelo usuário."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A expressão matemática a ser calculada. Ex: '2 ** 10', 'sqrt(144) + 5 * 3'",
                    }
                },
                "required": ["expression"],
            },
        },
        {
            "name": "web_search",
            "description": (
                "Busca informações atualizadas na internet via Tavily. "
                "Use quando o usuário precisar de informações recentes, notícias, preços, "
                "tendências de mercado, ou qualquer dado que pode ter mudado após seu treinamento."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A consulta de busca em linguagem natural. Seja específico para melhores resultados.",
                    }
                },
                "required": ["query"],
            },
        },
        {
            "name": "create_file_content",
            "description": (
                "Gera conteúdo formatado como um arquivo para o usuário baixar ou copiar. "
                "Use quando o usuário pedir para criar um script, documento, template ou qualquer arquivo."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Nome sugerido para o arquivo, incluindo extensão. Ex: 'email_boas_vindas.txt'",
                    },
                    "content": {
                        "type": "string",
                        "description": "Conteúdo completo do arquivo.",
                    },
                    "file_type": {
                        "type": "string",
                        "description": "Tipo do arquivo para syntax highlight: python, markdown, json, html, text, etc.",
                        "default": "text",
                    },
                },
                "required": ["filename", "content"],
            },
        },
        {
            "name": "generate_pony_digital_content",
            "description": (
                "Gera conteúdo de marketing para o negócio Pony-Digital de Ramon: "
                "hooks para Instagram, captions, emails de vendas, CTAs e headlines. "
                "Use quando Ramon pedir para criar conteúdo, post, email ou copy relacionado ao negócio dele."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "content_type": {
                        "type": "string",
                        "description": "Tipo de conteúdo: hook, caption, email, cta, ou headline",
                        "enum": ["hook", "caption", "email", "cta", "headline"],
                    },
                    "topic": {
                        "type": "string",
                        "description": "Tema do conteúdo. Ex: 'planilhas', 'finanças', 'produtividade', 'negócios digitais'",
                    },
                },
                "required": ["content_type", "topic"],
            },
        },
        {
            "name": "get_weather",
            "description": "Consulta a previsão do tempo para uma cidade. (Placeholder — requer configuração de API)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nome da cidade. Ex: 'São Paulo', 'Rio de Janeiro'",
                    }
                },
                "required": ["city"],
            },
        },
        {
            "name": "take_screenshot",
            "description": (
                "Tira um screenshot de qualquer URL usando o browser headless. "
                "Use quando Ramon pedir para ver uma página, verificar um site, "
                "ou quando precisar visualizar conteúdo de uma URL. "
                "Retorna a imagem para análise visual."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL completa para capturar. Ex: 'https://kiwify.com.br'",
                    },
                    "full_page": {
                        "type": "boolean",
                        "description": "Se True, captura a página inteira. Padrão: False (apenas a viewport).",
                        "default": False,
                    },
                },
                "required": ["url"],
            },
        },
        {
            "name": "browse_and_read",
            "description": (
                "Abre uma URL e lê o conteúdo de texto da página. "
                "Use para extrair informações de sites, artigos, documentações, preços, etc. "
                "Mais eficiente que take_screenshot quando só precisa do texto."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL para acessar e ler o conteúdo.",
                    }
                },
                "required": ["url"],
            },
        },
    ]


# ── Tool dispatcher ────────────────────────────────────────────────────────

async def process_tool_call(tool_name: str, tool_input: dict, config: Any) -> str:
    """
    Dispatch a tool_use request from Claude to the appropriate async function.

    Args:
        tool_name:  Name of the tool as returned by Claude's tool_use block.
        tool_input: Dict of arguments from the tool_use block.
        config:     App config instance (for API keys).

    Returns:
        String result to send back as a tool_result message.
    """
    try:
        if tool_name == "get_current_datetime":
            return await get_current_datetime()

        elif tool_name == "calculate":
            return await calculate(tool_input.get("expression", ""))

        elif tool_name == "web_search":
            return await web_search(
                query=tool_input.get("query", ""),
                api_key=config.TAVILY_API_KEY,
            )

        elif tool_name == "create_file_content":
            return await create_file_content(
                filename=tool_input.get("filename", "arquivo.txt"),
                content=tool_input.get("content", ""),
                file_type=tool_input.get("file_type", "text"),
            )

        elif tool_name == "generate_pony_digital_content":
            return await generate_pony_digital_content(
                content_type=tool_input.get("content_type", "caption"),
                topic=tool_input.get("topic", "negócios digitais"),
            )

        elif tool_name == "get_weather":
            return await get_weather(tool_input.get("city", ""))

        elif tool_name == "take_screenshot":
            return await take_screenshot(
                url=tool_input.get("url", ""),
                full_page=tool_input.get("full_page", False),
            )

        elif tool_name == "browse_and_read":
            return await browse_and_read(url=tool_input.get("url", ""))

        else:
            return f"Ferramenta desconhecida: '{tool_name}'. Verifique a lista de ferramentas disponíveis."

    except Exception as exc:
        return f"Erro ao executar '{tool_name}': {exc}"
