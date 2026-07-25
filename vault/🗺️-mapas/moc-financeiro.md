---
tipo: mapa-de-conteudo
titulo: Financeiro — Mapa de Conteúdo
tags: [moc, financeiro, ixc-provedor]
---

# 🗺️ Financeiro — Mapa de Conteúdo

---

## Notas neste módulo

- [[📚-conhecimento/financeiro/cobranca]] — Ciclo de cobrança
- [[📚-conhecimento/financeiro/inadimplencia]] — Gestão de inadimplentes
- [[📚-conhecimento/financeiro/baixa-pagamento]] — Baixa manual e automática
- [[📚-conhecimento/financeiro/conciliacao]] — Conciliação bancária
- [[📚-conhecimento/financeiro/relatorios]] — Relatórios financeiros

## Fluxos

```
Vencimento da fatura
  ↓
Envio automático (e-mail/SMS/WhatsApp)
  ↓
Pagamento? ──→ SIM → Baixa automática → NFS-e emitida
  ↓ NÃO
Atraso > X dias → Notificação de cobrança
  ↓
Atraso > Y dias → Bloqueio no Radius
  ↓
Negociação / Parcelamento
```

## Conexões

- [[moc-ixc-provedor]] — Sistema raiz
- [[moc-fiscal]] — NFS-e é gerada após pagamento
- [[📚-conhecimento/produtos/planos]] — Valor da fatura vem do plano

## Automações disponíveis

- Relatório diário de recebimentos
- Lista de inadimplentes
- Alertas de vencimento
