# ============================================================
#  JARBAS DESKTOP — Setup Completo para Windows
#  Execute como Administrador no PowerShell
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  JARBAS DESKTOP — Instalacao Completa" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

# ── 1. Verificar Node.js ─────────────────────────────────────────────────

Write-Host "[1/7] Verificando Node.js..." -ForegroundColor Cyan

$nodeVersion = $null
try { $nodeVersion = node --version 2>$null } catch {}

if (-not $nodeVersion) {
    Write-Host "  Node.js nao encontrado. Instalando via winget..." -ForegroundColor Yellow
    winget install --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    Write-Host "  Node.js instalado. Reinicie o PowerShell se der erro." -ForegroundColor Green
} else {
    Write-Host "  Node.js $nodeVersion encontrado." -ForegroundColor Green
}

# ── 2. Instalar Claude Code CLI ──────────────────────────────────────────

Write-Host ""
Write-Host "[2/7] Instalando Claude Code CLI..." -ForegroundColor Cyan
npm install -g @anthropic-ai/claude-code
Write-Host "  Claude Code instalado." -ForegroundColor Green

# ── 3. Instalar MCP servers ──────────────────────────────────────────────

Write-Host ""
Write-Host "[3/7] Instalando MCP servers..." -ForegroundColor Cyan

# Filesystem — acesso total C:\ e D:\
npm install -g @modelcontextprotocol/server-filesystem
Write-Host "  [OK] Filesystem MCP" -ForegroundColor Green

# Playwright — controle de navegadores (Chrome, Firefox, WebKit)
npm install -g @playwright/mcp
Write-Host "  [OK] Playwright MCP" -ForegroundColor Green

# Puppeteer — controle alternativo do Chrome
npm install -g @modelcontextprotocol/server-puppeteer
Write-Host "  [OK] Puppeteer MCP" -ForegroundColor Green

# Memory — memoria persistente entre sessoes
npm install -g @modelcontextprotocol/server-memory
Write-Host "  [OK] Memory MCP" -ForegroundColor Green

# Fetch — requisicoes HTTP / APIs / scraping
npm install -g @modelcontextprotocol/server-fetch
Write-Host "  [OK] Fetch MCP" -ForegroundColor Green

# SQLite — banco de dados local
npm install -g @modelcontextprotocol/server-sqlite
Write-Host "  [OK] SQLite MCP" -ForegroundColor Green

# Git — operacoes git em qualquer repositorio
npm install -g @modelcontextprotocol/server-git
Write-Host "  [OK] Git MCP" -ForegroundColor Green

# Sequential Thinking — raciocinio encadeado para tarefas complexas
npm install -g @modelcontextprotocol/server-sequential-thinking
Write-Host "  [OK] Sequential Thinking MCP" -ForegroundColor Green

# ── 4. Instalar navegadores do Playwright ───────────────────────────────

Write-Host ""
Write-Host "[4/7] Instalando navegadores (Chrome, Firefox, WebKit)..." -ForegroundColor Cyan
npx playwright install chromium firefox webkit
Write-Host "  Navegadores instalados." -ForegroundColor Green

# ── 5. Criar pasta do JARBAS ─────────────────────────────────────────────

Write-Host ""
Write-Host "[5/7] Criando pasta C:\jarbas..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "C:\jarbas" | Out-Null
Write-Host "  Pasta criada." -ForegroundColor Green

# ── 6. Criar configuracao do Claude Code ────────────────────────────────

Write-Host ""
Write-Host "[6/7] Criando configuracao do Claude Code..." -ForegroundColor Cyan

$claudeDir = "$env:USERPROFILE\.claude"
New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null
$settingsPath = "$claudeDir\settings.json"

$settingsContent = @"
{
  "mcpServers": {

    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\\\", "D:\\\\"],
      "type": "stdio"
    },

    "playwright-chrome": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "chrome", "--headless"],
      "type": "stdio"
    },

    "playwright-chrome-visible": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "chrome"],
      "type": "stdio"
    },

    "playwright-firefox": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "firefox", "--headless"],
      "type": "stdio"
    },

    "playwright-firefox-visible": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "firefox"],
      "type": "stdio"
    },

    "playwright-webkit": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser", "webkit", "--headless"],
      "type": "stdio"
    },

    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
      "type": "stdio"
    },

    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "type": "stdio"
    },

    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"],
      "type": "stdio"
    },

    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "C:\\\\jarbas\\\\jarbas.db"],
      "type": "stdio"
    },

    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "C:\\\\"],
      "type": "stdio"
    },

    "sequentialthinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "type": "stdio"
    }

  },
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "Glob(*)",
      "Grep(*)",
      "mcp__filesystem__*",
      "mcp__playwright-chrome__*",
      "mcp__playwright-chrome-visible__*",
      "mcp__playwright-firefox__*",
      "mcp__playwright-firefox-visible__*",
      "mcp__playwright-webkit__*",
      "mcp__puppeteer__*",
      "mcp__memory__*",
      "mcp__fetch__*",
      "mcp__sqlite__*",
      "mcp__git__*",
      "mcp__sequentialthinking__*"
    ]
  }
}
"@

Set-Content -Path $settingsPath -Value $settingsContent -Encoding UTF8
Write-Host "  Configuracao salva em: $settingsPath" -ForegroundColor Green

# ── 7. Verificacao final ─────────────────────────────────────────────────

Write-Host ""
Write-Host "[7/7] Verificando instalacao..." -ForegroundColor Cyan

$ok = $true

if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Host "  [OK] claude CLI" -ForegroundColor Green
} else {
    Write-Host "  [ERRO] claude CLI nao encontrado — reinicie o PowerShell" -ForegroundColor Red
    $ok = $false
}

if (Test-Path $settingsPath) {
    Write-Host "  [OK] settings.json" -ForegroundColor Green
} else {
    Write-Host "  [ERRO] settings.json nao criado" -ForegroundColor Red
    $ok = $false
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta

if ($ok) {
    Write-Host "  JARBAS DESKTOP PRONTO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Para ativar:" -ForegroundColor White
    Write-Host "      claude" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  12 capacidades ativas:" -ForegroundColor White
    Write-Host "    [1] Terminal / PowerShell (Bash built-in)" -ForegroundColor Cyan
    Write-Host "    [2] Arquivos C:\ e D:\ (Filesystem MCP)" -ForegroundColor Cyan
    Write-Host "    [3] Chrome headless — automacao silenciosa" -ForegroundColor Cyan
    Write-Host "    [4] Chrome visivel — voce ve o que eu faco" -ForegroundColor Cyan
    Write-Host "    [5] Firefox headless" -ForegroundColor Cyan
    Write-Host "    [6] Firefox visivel" -ForegroundColor Cyan
    Write-Host "    [7] WebKit / Safari headless" -ForegroundColor Cyan
    Write-Host "    [8] Puppeteer — Chrome alternativo" -ForegroundColor Cyan
    Write-Host "    [9] Memoria persistente (entre sessoes)" -ForegroundColor Cyan
    Write-Host "   [10] HTTP / Fetch / APIs" -ForegroundColor Cyan
    Write-Host "   [11] SQLite — banco de dados local" -ForegroundColor Cyan
    Write-Host "   [12] Git — controle de repositorios" -ForegroundColor Cyan
} else {
    Write-Host "  Instalacao incompleta — veja os erros acima." -ForegroundColor Red
    Write-Host "  Reinicie o PowerShell como Administrador e rode novamente." -ForegroundColor Yellow
}

Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""
