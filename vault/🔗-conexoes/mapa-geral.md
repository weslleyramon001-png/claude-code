---
tipo: conexoes
titulo: Mapa de Conexões — IXC Provedor
tags: [conexoes, mapa, ixc-provedor]
---

# 🔗 Mapa de Conexões — IXC Provedor

> Como os módulos se relacionam entre si dentro do sistema.

---

## Diagrama de dependências

```
                    ┌─────────────┐
                    │   CLIENTE   │
                    └──────┬──────┘
                           │ contrata
              ┌────────────▼────────────┐
              │         PRODUTOS        │
              │     (planos, serviços)  │
              └──┬──────────┬───────────┘
                 │          │ define
                 │     ┌────▼──────┐
                 │     │ FINANCEIRO│◄──── pagamento
                 │     │ (faturas) │────► FISCAL (NFS-e)
                 │     └───────────┘
                 │ instala
         ┌───────▼───────┐
         │    SUPORTE    │
         │  (OS técnica) │
         └───────┬───────┘
                 │ consome
         ┌───────▼───────┐
         │    ESTOQUE    │
         │  (materiais)  │
         └───────────────┘
```

---

## Relações por módulo

### Financeiro
- Recebe valor de → **Produtos** (plano do cliente)
- Gera → **Fiscal** (NFS-e após pagamento)
- Bloqueia via → **Radius** (inadimplência)

### Suporte (OS)
- Nasce de → **Atendimento** (cliente liga)
- Gera saída em → **Estoque** (materiais usados)
- Ativa → **Financeiro** (cobrança de instalação)

### Fiscal
- Depende de → **Financeiro** (pagamento confirmado)
- Código de serviço vem de → **Produtos** (plano)

### Estoque
- Movimentado por → **Suporte** (OS)
- Alertas para → gestão de compras

### Produtos
- Define valor em → **Financeiro**
- Define perfil Radius para → autenticação PPPoE

---

## Conexões com notas

- [[🗺️-mapas/moc-financeiro]]
- [[🗺️-mapas/moc-suporte]]
- [[🗺️-mapas/moc-fiscal]]
- [[🗺️-mapas/moc-estoque]]
- [[🗺️-mapas/moc-produtos]]
- [[🗺️-mapas/moc-ixc-provedor]]
