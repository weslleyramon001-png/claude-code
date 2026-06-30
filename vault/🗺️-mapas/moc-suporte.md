---
tipo: mapa-de-conteudo
titulo: Suporte — Mapa de Conteúdo
tags: [moc, suporte, os, ixc-provedor]
---

# 🗺️ Suporte — Mapa de Conteúdo

---

## Notas neste módulo

- [[📚-conhecimento/suporte/ordens-de-servico]] — Como funciona a OS
- [[📚-conhecimento/suporte/tipos-de-os]] — Instalação, manutenção, retirada
- [[📚-conhecimento/suporte/tecnicos]] — Cadastro e regiões dos técnicos
- [[📚-conhecimento/suporte/agendamento]] — Janelas de atendimento
- [[📚-conhecimento/suporte/sla]] — Prazos e prioridades

## Fluxos

```
Cliente solicita suporte
  ↓
Atendente abre OS
  ↓
Classificação: tipo + prioridade
  ↓
Agendamento ──→ Técnico notificado (app)
  ↓
Técnico executa → usa materiais do estoque
  ↓
Encerramento → assinatura digital
  ↓
Pesquisa de satisfação enviada
```

## Conexões

- [[moc-ixc-provedor]] — Sistema raiz
- [[moc-estoque]] — Materiais consumidos nas OS
- [[📚-conhecimento/atendimento/visao-geral]] — OS nasce no atendimento
- [[moc-financeiro]] — OS de instalação gera cobrança

## Automações disponíveis

- OS em aberto por técnico
- OS fora do SLA
- Relatório de satisfação
