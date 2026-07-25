---
tipo: mapa-de-conteudo
titulo: IXC Provedor — Mapa Geral
tags: [moc, ixc-provedor]
---

# 🗺️ IXC Provedor — Mapa de Conteúdo

> Visão completa de tudo que a Lyvian sabe sobre o IXC Provedor.
> Interliga todos os módulos, fluxos e automações relacionados.

---

## O que é o IXC Provedor

O **IXC Soft** é o principal ERP para provedores de internet (ISPs) do Brasil.
Gerencia desde o cadastro do cliente até a emissão de nota fiscal.

→ [[📚-conhecimento/ixc-provedor/visao-geral]]
→ [[📚-conhecimento/ixc-provedor/api-referencia]]

---

## Módulos

```
IXC Provedor
├── 💰 Financeiro     → [[moc-financeiro]]
├── 👤 Atendimento    → [[📚-conhecimento/atendimento/visao-geral]]
├── 🔧 Suporte        → [[moc-suporte]]
├── 🧾 Fiscal         → [[moc-fiscal]]
├── 📦 Estoque        → [[moc-estoque]]
└── 📡 Produtos       → [[moc-produtos]]
```

---

## Fluxos principais

| Fluxo | Módulos envolvidos |
|---|---|
| Ativação de cliente | Atendimento → Produtos → Suporte → Financeiro |
| Cobrança mensal | Financeiro → Fiscal |
| Manutenção técnica | Suporte → Estoque |
| Cancelamento | Atendimento → Financeiro → Suporte |

---

## API

- Autenticação: Basic Auth (base64)
- Base URL: `https://DOMINIO.ixcprovedor.com.br/webservice/v1`
- → [[📚-conhecimento/ixc-provedor/api-referencia]]

---

## Automações

→ [[⚡-automacoes/índice]]

---

## Conexões com outros mapas

- [[moc-financeiro]] — Cobranças geradas pelo IXC
- [[moc-suporte]] — OS abertas para clientes do IXC
- [[moc-fiscal]] — NFS-e emitidas automaticamente
