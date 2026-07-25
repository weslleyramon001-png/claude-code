---
tipo: indice
titulo: Automações — Catálogo
tags: [automacao, ixc-provedor]
---

# ⚡ Automações — Catálogo Completo

> Tarefas que a Lyvian executa mediante solicitação via API do IXC.
> Status: 🔴 Aguardando API · 🟡 Em desenvolvimento · 🟢 Ativa

---

## 💰 Financeiro

| Automação | Descrição | Status |
|---|---|---|
| `relatorio-recebimentos` | Recebimentos do dia/semana/mês | 🔴 |
| `lista-inadimplentes` | Clientes em atraso com detalhes | 🔴 |
| `boletos-pendentes` | Boletos gerados sem pagamento | 🔴 |
| `previsao-receita` | Receita esperada no mês | 🔴 |

## 👤 Atendimento

| Automação | Descrição | Status |
|---|---|---|
| `base-clientes` | Total ativo, bloqueado, cancelado | 🔴 |
| `novos-clientes` | Clientes ativados no período | 🔴 |
| `churn` | Clientes cancelados no período | 🔴 |

## 🔧 Suporte

| Automação | Descrição | Status |
|---|---|---|
| `os-em-aberto` | OS abertas por técnico e status | 🔴 |
| `os-fora-do-sla` | OS que ultrapassaram o prazo | 🔴 |
| `satisfacao` | Média de avaliações do período | 🔴 |

## 🧾 Fiscal

| Automação | Descrição | Status |
|---|---|---|
| `notas-do-mes` | NFS-e emitidas no mês | 🔴 |
| `notas-com-erro` | NFS-e rejeitadas pela prefeitura | 🔴 |

## 📦 Estoque

| Automação | Descrição | Status |
|---|---|---|
| `estoque-critico` | Itens abaixo do mínimo | 🔴 |
| `consumo-tecnico` | Materiais usados por técnico | 🔴 |

## 📡 Produtos

| Automação | Descrição | Status |
|---|---|---|
| `lista-planos` | Planos ativos com preços | 🔴 |
| `clientes-por-plano` | Distribuição da base | 🔴 |

---

## Como ativar

1. Forneça credenciais em [[_meta/credenciais]]
2. Solicite qualquer automação acima pelo nome
3. A Lyvian executa, exibe resultado e salva em [[💭-memorias/]]
