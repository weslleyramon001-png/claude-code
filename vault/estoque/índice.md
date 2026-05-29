# Estoque — IXC Provedor

## Visão geral

Módulo de controle de materiais, equipamentos e almoxarifado do provedor.

## Funcionalidades principais

### Itens de Estoque
- Cadastro de produtos/materiais
- Categorias (equipamento, cabo, conector, etc.)
- Código de barras e patrimônio
- Estoque mínimo e alertas

### Movimentações
- Entrada (compra, devolução, transferência)
- Saída (OS, descarte, transferência)
- Transferência entre almoxarifados
- Histórico completo por item

### Almoxarifados
- Múltiplos almoxarifados (sede, técnicos, filiais)
- Saldo por almoxarifado
- Transferência entre locais

### Inventário
- Contagem periódica
- Ajuste de saldo
- Relatório de divergências

### Vinculação com OS
- Materiais consumidos na OS saem automaticamente do estoque
- Rastreabilidade equipamento → cliente → OS

## Fluxos mapeados

- [[_fluxos/estoque-entrada]] — Entrada de material (compra)
- [[_fluxos/estoque-saida-os]] — Saída via Ordem de Serviço
- [[_fluxos/estoque-transferencia]] — Transferência entre almoxarifados
- [[_fluxos/estoque-inventario]] — Processo de inventário

## Endpoints API

```
GET  /webservice/v1/estoque_produto      — Lista produtos no estoque
GET  /webservice/v1/estoque_produto/{id} — Detalhe do produto
GET  /webservice/v1/estoque_movimentacao — Histórico de movimentações
POST /webservice/v1/estoque_movimentacao — Registrar movimentação
GET  /webservice/v1/estoque_saldo        — Saldo atual por produto/almoxarifado
```

## Automações disponíveis

- [[_automacoes/estoque-saldo-critico]] — Alertar itens abaixo do estoque mínimo
- [[_automacoes/estoque-relatorio-mensal]] — Relatório mensal de movimentações
- [[_automacoes/estoque-consumo-os]] — Relatório de consumo por OS/técnico

## Pendências / a mapear

- [ ] Lista de almoxarifados ativos
- [ ] Produtos críticos (estoque mínimo configurado)
- [ ] Fluxo de compras (quem aprova, quem lança entrada)
- [ ] Técnicos com estoque próprio (almoxarifado móvel)
