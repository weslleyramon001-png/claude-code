# Suporte — IXC Provedor

## Visão geral

Módulo de Ordens de Serviço (OS): abertura, acompanhamento, despacho de técnicos e encerramento de chamados.

## Funcionalidades principais

### Ordens de Serviço (OS)
- Abertura de OS por atendente ou cliente (portal)
- Tipos: instalação, manutenção, retirada, visita técnica
- Prioridade: baixa, média, alta, urgente
- Status: aberta, em andamento, agendada, encerrada, cancelada

### Agendamento
- Agenda por técnico e por região
- Janelas de atendimento
- Notificação de agendamento ao cliente
- App mobile para técnico (visualização e encerramento)

### Despacho
- Atribuição manual ou automática de técnico
- Fila de OS por região/setor
- Roteamento geográfico

### Encerramento
- Registro de solução aplicada
- Materiais utilizados (vincula ao estoque)
- Assinatura digital do cliente
- Pesquisa de satisfação pós-atendimento

## Fluxos mapeados

- [[_fluxos/suporte-abertura-os]] — Abertura de OS passo a passo
- [[_fluxos/suporte-despacho]] — Despacho e atribuição de técnico
- [[_fluxos/suporte-encerramento]] — Encerramento e pesquisa de satisfação

## Endpoints API

```
GET  /webservice/v1/su_oss_chamado       — Lista ordens de serviço
GET  /webservice/v1/su_oss_chamado/{id}  — Detalhe da OS
POST /webservice/v1/su_oss_chamado       — Criar OS
PUT  /webservice/v1/su_oss_chamado/{id}  — Atualizar OS
GET  /webservice/v1/su_oss_tipo          — Tipos de OS
GET  /webservice/v1/tecnico              — Lista técnicos
```

## Automações disponíveis

- [[_automacoes/suporte-os-abertas]] — Relatório de OS em aberto
- [[_automacoes/suporte-os-atrasadas]] — Alertar OS fora do prazo
- [[_automacoes/suporte-satisfacao]] — Consolidar pesquisas de satisfação

## Pendências / a mapear

- [ ] Tipos de OS utilizados no provedor
- [ ] SLA por tipo de OS
- [ ] Regiões e setores de atendimento configurados
- [ ] Técnicos cadastrados e suas regiões
