# Fiscal — IXC Provedor

## Visão geral

Módulo responsável pela emissão de notas fiscais, obrigações fiscais e integração com a SEFAZ.

## Funcionalidades principais

### Nota Fiscal de Serviço (NFS-e)
- Emissão automática junto com a fatura
- Integração com prefeituras via webservice
- RPS (Recibo Provisório de Serviços)
- Cancelamento e substituição de NFS-e

### Nota Fiscal Eletrônica (NF-e / NFC-e)
- Emissão para venda de equipamentos/produtos
- DANFE
- Cancelamento dentro do prazo legal
- Carta de correção

### Obrigações Acessórias
- SPED Fiscal
- EFD-Contribuições
- DCTF
- Relatórios por competência

### Configurações Fiscais
- Regimes tributários (Simples Nacional, Lucro Presumido, etc.)
- CNAE do provedor
- Alíquotas ISS por município
- Código de serviço municipal

## Fluxos mapeados

- [[_fluxos/fiscal-emissao-nfse]] — Fluxo de emissão de NFS-e
- [[_fluxos/fiscal-cancelamento]] — Cancelamento de nota fiscal
- [[_fluxos/fiscal-relatorio-mensal]] — Fechamento fiscal mensal

## Endpoints API

```
GET  /webservice/v1/fiscal_nfse          — Lista NFS-e emitidas
GET  /webservice/v1/fiscal_nfse/{id}     — Detalhe da NFS-e
POST /webservice/v1/fiscal_nfse          — Emitir NFS-e manualmente
GET  /webservice/v1/fiscal_nfe           — Lista NF-e emitidas
POST /webservice/v1/fiscal_nfe           — Emitir NF-e
```

## Automações disponíveis

- [[_automacoes/fiscal-relatorio-notas]] — Relatório de notas emitidas no mês
- [[_automacoes/fiscal-pendentes]] — Verificar notas pendentes de emissão
- [[_automacoes/fiscal-erros]] — Alertar notas rejeitadas pela SEFAZ

## Pendências / a mapear

- [ ] Regime tributário do provedor
- [ ] Municípios atendidos e código de serviço de cada um
- [ ] Certificado digital (vencimento)
- [ ] Prefeituras com integração ativa
