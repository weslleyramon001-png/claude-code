# Financeiro — IXC Provedor

## Visão geral

Módulo responsável por toda a gestão financeira do provedor: cobranças, recebimentos, inadimplência e relatórios financeiros.

## Funcionalidades principais

### Cobranças
- Geração de boletos bancários
- Cobrança via PIX (QR Code e chave)
- Cartão de crédito (recorrente)
- Envio automático de faturas por e-mail/SMS
- Régua de cobrança configurável

### Contas a Receber
- Listagem de títulos em aberto
- Baixa manual e automática de pagamentos
- Conciliação bancária
- Importação de retorno bancário (CNAB 240/400)

### Inadimplência
- Relatório de inadimplentes por período
- Bloqueio automático por inadimplência
- Notificações automáticas (e-mail, SMS, WhatsApp)
- Negociação e parcelamento de dívidas

### Relatórios
- DRE (Demonstrativo de Resultado)
- Fluxo de caixa
- Receita por plano/produto
- Churn financeiro

## Fluxos mapeados

- [[_fluxos/financeiro-cobranca]] — Fluxo completo de cobrança
- [[_fluxos/financeiro-inadimplencia]] — Processo de inadimplência e bloqueio
- [[_fluxos/financeiro-baixa]] — Baixa de pagamentos

## Endpoints API

```
GET  /webservice/v1/fin_lancamento       — Lançamentos financeiros
GET  /webservice/v1/fin_titulo           — Títulos (faturas)
POST /webservice/v1/fin_titulo           — Criar novo título
GET  /webservice/v1/fin_titulo/{id}      — Detalhe do título
PUT  /webservice/v1/fin_titulo/{id}      — Atualizar título
GET  /webservice/v1/fin_inadimplente     — Lista de inadimplentes
```

## Automações disponíveis

- [[_automacoes/financeiro-relatorio-diario]] — Relatório diário de recebimentos
- [[_automacoes/financeiro-inadimplentes]] — Lista atualizada de inadimplentes
- [[_automacoes/financeiro-boleto]] — Geração de boletos em lote

## Pendências / a mapear

- [ ] Integração com gateway de pagamento atual
- [ ] Regras de bloqueio configuradas no sistema
- [ ] Planos com cobrança diferenciada
