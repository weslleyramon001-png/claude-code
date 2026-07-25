---
tipo: mapa-de-conteudo
titulo: Produtos — Mapa de Conteúdo
tags: [moc, produtos, planos, ixc-provedor]
---

# 🗺️ Produtos — Mapa de Conteúdo

---

## Notas neste módulo

- [[📚-conhecimento/produtos/planos]] — Planos de internet disponíveis
- [[📚-conhecimento/produtos/servicos-adicionais]] — IP fixo, TV, segurança
- [[📚-conhecimento/produtos/equipamentos]] — Roteadores, ONUs
- [[📚-conhecimento/produtos/promocoes]] — Promoções e descontos

## Fluxos

```
Criação de plano
  ↓
Configuração no Radius (velocidade real)
  ↓
Disponível para venda
  ↓
Cliente contrata → Contrato criado
  ↓
OS de instalação gerada → Técnico instala
  ↓
Cobrança mensal ativada
```

## Conexões

- [[moc-financeiro]] — Plano define valor da fatura
- [[moc-suporte]] — Plano gera OS de instalação
- [[moc-fiscal]] — Código de serviço do plano
- [[moc-ixc-provedor]] — Sistema raiz

## Automações disponíveis

- Lista de planos ativos com preços
- Clientes por plano
- Planos sem nenhum cliente
