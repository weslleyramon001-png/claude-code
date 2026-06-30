# Claude Code

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

Claude Code é uma ferramenta de codificação agêntica que vive no seu terminal, entende sua base de código e ajuda você a programar mais rápido ao executar tarefas rotineiras, explicar código complexo e gerenciar fluxos de trabalho git — tudo por meio de comandos em linguagem natural. Use no seu terminal, IDE, ou marque @claude no GitHub.

**Saiba mais na [documentação oficial](https://code.claude.com/docs/en/overview)**.

<img src="./demo.gif" />

## Primeiros passos
> [!NOTE]
> A instalação via npm está descontinuada. Use um dos métodos recomendados abaixo.

Para mais opções de instalação, etapas de desinstalação e solução de problemas, consulte a [documentação de configuração](https://code.claude.com/docs/en/setup).

1. Instale o Claude Code:

    **MacOS/Linux (Recomendado):**
    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Homebrew (MacOS/Linux):**
    ```bash
    brew install --cask claude-code
    ```

    **Windows (Recomendado):**
    ```powershell
    irm https://claude.ai/install.ps1 | iex
    ```

    **WinGet (Windows):**
    ```powershell
    winget install Anthropic.ClaudeCode
    ```

    **NPM (Descontinuado):**
    ```bash
    npm install -g @anthropic-ai/claude-code
    ```

2. Navegue até o diretório do seu projeto e execute `claude`.

## Plugins

Este repositório inclui vários plugins do Claude Code que ampliam funcionalidades com comandos e agentes personalizados. Consulte o [diretório de plugins](./plugins/README.md) para documentação detalhada sobre os plugins disponíveis.

## Reportando Bugs

Agradecemos seu feedback. Use o comando `/bug` para reportar problemas diretamente no Claude Code, ou abra uma [issue no GitHub](https://github.com/anthropics/claude-code/issues).

## Conecte-se no Discord

Junte-se ao [Discord dos Desenvolvedores Claude](https://anthropic.com/discord) para se conectar com outros desenvolvedores que usam o Claude Code. Obtenha ajuda, compartilhe feedback e discuta seus projetos com a comunidade.

## Coleta, uso e retenção de dados

Quando você usa o Claude Code, coletamos feedback, o que inclui dados de uso (como aceitação ou rejeição de código), dados de conversa associados e feedback do usuário enviado pelo comando `/bug`.

### Como usamos seus dados

Consulte nossas [políticas de uso de dados](https://code.claude.com/docs/en/data-usage).

### Salvaguardas de privacidade

Implementamos diversas salvaguardas para proteger seus dados, incluindo períodos de retenção limitados para informações sensíveis, acesso restrito aos dados de sessão do usuário e políticas claras contra o uso de feedback para treinamento de modelos.

Para mais detalhes, consulte nossos [Termos de Serviço Comercial](https://www.anthropic.com/legal/commercial-terms) e [Política de Privacidade](https://www.anthropic.com/legal/privacy).
