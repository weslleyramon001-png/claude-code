# Atendimento — IXC Provedor

## Visão geral

Módulo de relacionamento com o cliente: cadastro, contratos, histórico de contato e comunicação.

## Funcionalidades principais

### Cadastro de Clientes
- Pessoa física e jurídica
- Dados pessoais, endereço, contatos
- Documentos (CPF, CNPJ, RG)
- Status do cliente (ativo, bloqueado, cancelado, inadimplente)

### Contratos
- Planos contratados
- Data de instalação e vigência
- Endereço de instalação
- Equipamentos vinculados

### Histórico de Atendimento
- Registro de interações por cliente
- Atendimentos por telefone, chat, presencial
- Anotações internas
- Timeline do cliente

### Comunicação
- Envio de e-mail individual e em massa
- SMS para clientes
- Integração WhatsApp (via API)
- Notificações automáticas por evento

## Fluxos mapeados

- [[_fluxos/atendimento-novo-cliente]] — Cadastro e ativação de novo cliente
- [[_fluxos/atendimento-cancelamento]] — Processo de cancelamento
- [[_fluxos/atendimento-alteracao-plano]] — Mudança de plano

## Endpoints API

```
GET  /webservice/v1/cliente              — Lista clientes
GET  /webservice/v1/cliente/{id}         — Detalhe do cliente
POST /webservice/v1/cliente              — Criar cliente
PUT  /webservice/v1/cliente/{id}         — Atualizar cliente
GET  /webservice/v1/contrato             — Lista contratos
GET  /webservice/v1/contrato/{id}        — Detalhe do contrato
POST /webservice/v1/mensagem             — Enviar mensagem ao cliente
```

## Automações disponíveis

- [[_automacoes/atendimento-boas-vindas]] — Mensagem automática para novo cliente
- [[_automacoes/atendimento-aniversario]] — Felicitação de aniversário
- [[_automacoes/atendimento-relatorio-clientes]] — Relatório de base de clientes

## Pendências / a mapear

- [ ] Canais de atendimento ativos (telefone, chat, WhatsApp)
- [ ] SLA de atendimento definido
- [ ] Motivos de cancelamento mais comuns
