---
tipo: mapa-de-conteudo
titulo: Estoque — Mapa de Conteúdo
tags: [moc, estoque, almoxarifado, ixc-provedor]
---

# 🗺️ Estoque — Mapa de Conteúdo

---

## Notas neste módulo

- [[📚-conhecimento/estoque/produtos-cadastro]] — Itens e categorias
- [[📚-conhecimento/estoque/movimentacoes]] — Entradas e saídas
- [[📚-conhecimento/estoque/almoxarifados]] — Locais de armazenamento
- [[📚-conhecimento/estoque/consumo-os]] — Rastreio por OS e técnico

## Fluxos

```
Compra aprovada
  ↓
Entrada no almoxarifado central
  ↓
Transferência para técnico (almox. móvel)
  ↓
OS executada → material consumido
  ↓
Saída registrada automaticamente na OS
  ↓
Saldo atualizado
```

## Conexões

- [[moc-suporte]] — OS consome estoque
- [[moc-ixc-provedor]] — Sistema raiz
- [[📚-conhecimento/produtos/planos]] — Equipamentos vinculados ao plano

## Automações disponíveis

- Itens abaixo do estoque mínimo
- Consumo por técnico no mês
- Relatório de movimentações
