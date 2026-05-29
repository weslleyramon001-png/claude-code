# Produtos — IXC Provedor

## Visão geral

Módulo de cadastro e gestão de planos de internet, serviços adicionais e produtos comercializados pelo provedor.

## Funcionalidades principais

### Planos de Internet
- Velocidade (download/upload)
- Tecnologia (fibra, rádio, cabo)
- Preço e periodicidade (mensal, semestral, anual)
- Fidelidade e multa rescisória
- Área de cobertura

### Serviços Adicionais
- IP fixo
- TV por assinatura (parceiro)
- Segurança (antivírus, backup em nuvem)
- E-mail profissional
- Suporte prioritário

### Produtos para Venda
- Equipamentos (roteadores, ONUs, decodificadores)
- Cabos e acessórios
- Kits de instalação

### Promoções e Descontos
- Desconto por período
- Cashback
- Indicação de clientes
- Combo (internet + serviço adicional)

### Configurações de Plano
- Perfil Radius (velocidade real entregue)
- Bloqueio por inadimplência (Radius)
- Regras de QoS
- Franquia de dados (se aplicável)

## Fluxos mapeados

- [[_fluxos/produtos-novo-plano]] — Criação de novo plano
- [[_fluxos/produtos-alteracao-plano]] — Cliente migrando de plano
- [[_fluxos/produtos-promocao]] — Aplicação de promoção

## Endpoints API

```
GET  /webservice/v1/plano                — Lista planos disponíveis
GET  /webservice/v1/plano/{id}           — Detalhe do plano
POST /webservice/v1/plano                — Criar plano
PUT  /webservice/v1/plano/{id}           — Atualizar plano
GET  /webservice/v1/produto              — Lista produtos
GET  /webservice/v1/produto/{id}         — Detalhe do produto
POST /webservice/v1/produto              — Criar produto
```

## Automações disponíveis

- [[_automacoes/produtos-lista-planos]] — Listar todos os planos ativos com preços
- [[_automacoes/produtos-clientes-por-plano]] — Quantos clientes por plano
- [[_automacoes/produtos-planos-sem-cliente]] — Planos sem nenhum cliente ativo

## Pendências / a mapear

- [ ] Lista completa de planos ativos
- [ ] Tecnologias disponíveis na área de atuação
- [ ] Serviços adicionais comercializados
- [ ] Política de fidelidade e reajuste
