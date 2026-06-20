# JARBAS Desktop — Como Usar

## Instalacao (fazer uma vez)

1. Abrir **PowerShell como Administrador**
2. Navegar ate esta pasta:
   ```
   cd C:\caminho\para\jarbas-desktop
   ```
3. Rodar:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\instalar-windows.ps1
   ```

## Ativar o JARBAS Desktop

Abrir PowerShell em qualquer pasta e rodar:
```
claude
```

Pronto — voce tem acesso total a maquina.

---

## O que eu posso fazer quando estiver ativo

### Terminal / Sistema
- Executar qualquer comando PowerShell ou CMD
- Instalar programas, configurar o sistema
- Criar, mover, editar, deletar arquivos em qualquer lugar
- Ler e modificar o registro do Windows
- Gerenciar processos

### Navegador (Playwright)
- Abrir o Chrome e navegar em qualquer site
- Clicar em botoes, preencher formularios
- Fazer login em plataformas para voce
- Tirar screenshots de paginas
- Fazer scraping e coleta de dados
- Automatizar tarefas repetitivas no navegador
- Baixar arquivos

### Rede / HTTP
- Fazer requisicoes HTTP para qualquer API
- Integrar com webhooks e servicos externos
- Monitorar URLs e servicos

### Memoria
- Salvar informacoes importantes entre sessoes
- Lembrar de preferencias e contexto

---

## Exemplos de comandos

- "Abra o Chrome no Gmail e me diga quantos emails nao lidos tenho"
- "Crie uma pasta em D:\Projetos\Novo e mova todos os .pdf da Area de Trabalho"
- "Instale o Python via winget"
- "Faca login no Railway e me mostre o status do JARBAS"
- "Tire um screenshot do meu dashboard do Kiwify"
- "Rode um script Python e me mostre o resultado"
