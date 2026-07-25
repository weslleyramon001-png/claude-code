---
tipo: conhecimento
titulo: IXC Provedor — Visão Geral
tags: [ixc-provedor, erp, isp]
relacionado: [api-referencia, moc-ixc-provedor]
---

# IXC Provedor — Visão Geral

## O que é

O **IXC Soft** é um ERP (sistema de gestão) desenvolvido especificamente para **provedores de internet (ISPs)** brasileiros. É um dos mais usados no Brasil para gestão completa de provedores de pequeno, médio e grande porte.

## Tecnologia

- Interface web (browser)
- API REST própria
- App mobile para técnicos (Android/iOS)
- Integrado com Radius (PPPoE, CGNAT)
- Integrado com SEFAZ (notas fiscais)
- Integrado com bancos (CNAB, PIX, boleto)

## Arquitetura geral

```
Cliente final
  ↕ PPPoE/FTTH/Rádio
Radius (autenticação)
  ↕
IXC Provedor (ERP)
  ├── Financeiro (fatura, cobrança)
  ├── CRM (cliente, contrato)
  ├── OS (suporte, técnicos)
  ├── Fiscal (NFS-e, NF-e)
  ├── Estoque (materiais)
  └── Produtos (planos, serviços)
```

## Acesso ao sistema

- **Interface**: `https://DOMINIO.ixcprovedor.com.br`
- **API**: `https://DOMINIO.ixcprovedor.com.br/webservice/v1`
- **App técnico**: Google Play / App Store — "IXC Provedor"

## Relacionamentos

→ [[api-referencia]]
→ [[🗺️-mapas/moc-ixc-provedor]]
→ [[CEREBRO-LYVIAN]]
