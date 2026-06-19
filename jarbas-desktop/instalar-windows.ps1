# ============================================================
#  JARBAS DESKTOP — Setup Completo para Windows
#  Execute como Administrador no PowerShell
#  Instala: Node.js, Claude Code CLI, MCP servers, Playwright
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "  JARBAS DESKTOP — Instalacao Completa" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""

# ── 1. Verificar Node.js ─────────────────────────────────────────────────

Write-Host "[1/6] Verificando Node.js..." -ForegroundColor Cyan

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
Write-Host "[2/6] Instalando Claude Code CLI..." -ForegroundColor Cyan
npm install -g @anthropic-ai/claude-code
Write-Host "  Claude Code instalado." -ForegroundColor Green

# ── 3. Instalar MCP servers ──────────────────────────────────────────────

Write-Host ""
Write-Host "[3/6] Instalando MCP servers..." -ForegroundColor Cyan

# Filesystem MCP — acesso a qualquer pasta/arquivo
npm install -g @modelcontextprotocol/server-filesystem
Write-Host "  [OK] Filesystem MCP" -ForegroundColor Green

# Playwright MCP — controle total do navegador
npm install -g @playwright/mcp
Write-Host "  [OK] Playwright MCP" -ForegroundColor Green

# Memory MCP — memoria persistente local
npm install -g @modelcontextprotocol/server-memory
Write-Host "  [OK] Memory MCP" -ForegroundColor Green

# Fetch MCP — requisicoes HTTP / scraping
npm install -g @modelcontextprotocol/server-fetch
Write-Host "  [OK] Fetch MCP" -ForegroundColor Green

# ── 4. Instalar navegadores do Playwright ───────────────────────────────

Write-Host ""
Write-Host "[4/6] Instalando Chromium para Playwright..." -ForegroundColor Cyan
npx playwright install chromium
Write-Host "  Chromium instalado." -ForegroundColor Green

# ── 5. Criar configuracao do Claude Code ────────────────────────────────

Write-Host ""
Write-Host "[5/6] Criando configuracao do Claude Code..." -ForegroundColor Cyan

$claudeDir = "$env:USERPROFILE\.claude"
New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null

$settingsPath = "$claudeDir\settings.json"

# Pega drives disponiveis
$drives = (Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root } | Select-Object -ExpandProperty Root) -join '", "'
$drivesJson = '"' + $drives + '"'

$settingsContent = @"
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\\\",
        "D:\\\\"
      ],
      "type": "stdio"
    },
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser",
        "chrome",
        "--headless"
      ],
      "type": "stdio"
    },
    "playwright-visible": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser",
        "chrome"
      ],
      "type": "stdio"
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "type": "stdio"
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ],
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
      "mcp__playwright__*",
      "mcp__playwright-visible__*",
      "mcp__memory__*",
      "mcp__fetch__*"
    ]
  }
}
"@

Set-Content -Path $settingsPath -Value $settingsContent -Encoding UTF8
Write-Host "  Configuracao salva em: $settingsPath" -ForegroundColor Green

# ── 6. Verificacao final ─────────────────────────────────────────────────

Write-Host ""
Write-Host "[6/6] Verificando instalacao..." -ForegroundColor Cyan

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
    Write-Host "  Para ativar, abra o PowerShell em qualquer pasta e rode:" -ForegroundColor White
    Write-Host "      claude" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Acesso total disponivel:" -ForegroundColor White
    Write-Host "    - Terminal / PowerShell (comandos diretos)" -ForegroundColor Cyan
    Write-Host "    - Sistema de arquivos (C:\ D:\)" -ForegroundColor Cyan
    Write-Host "    - Navegador Chrome (controle visual + headless)" -ForegroundColor Cyan
    Write-Host "    - Requisicoes HTTP / rede" -ForegroundColor Cyan
    Write-Host "    - Memoria persistente local" -ForegroundColor Cyan
} else {
    Write-Host "  Instalacao incompleta — veja os erros acima." -ForegroundColor Red
    Write-Host "  Reinicie o PowerShell como Administrador e rode novamente." -ForegroundColor Yellow
}

Write-Host "============================================" -ForegroundColor Magenta
Write-Host ""
