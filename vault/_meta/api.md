# API IXC Provedor — Referência

## Autenticação

A API do IXC usa autenticação via token no header HTTP:

```
Authorization: Basic base64(usuario:token)
```

Ou via parâmetro na URL:
```
?token=SEU_TOKEN&tokenkey=email@provedor.com.br
```

## URL base

```
https://SEU_DOMINIO.ixcprovedor.com.br/webservice/v1/
```

> ⚠️ Substituir `SEU_DOMINIO` pelo domínio real do provedor.

## Padrão das requisições

- **Método**: GET, POST, PUT, DELETE
- **Formato**: JSON
- **Paginação**: parâmetros `start` e `limit`
- **Filtros**: parâmetro `qtype`, `query` e `oper`

### Exemplo de requisição com filtro

```bash
curl -X GET "https://SEU_DOMINIO.ixcprovedor.com.br/webservice/v1/cliente" \
  -H "Authorization: Basic TOKEN_BASE64" \
  -H "Content-Type: application/json" \
  -d '{
    "qtype": "cli_atividade",
    "query": "A",
    "oper": "=",
    "page": 1,
    "rp": 20
  }'
```

## Endpoints por módulo

| Módulo | Endpoint base |
|---|---|
| Clientes | `/cliente` |
| Contratos | `/contrato` |
| Financeiro (títulos) | `/fin_titulo` |
| Financeiro (lançamentos) | `/fin_lancamento` |
| OS (chamados) | `/su_oss_chamado` |
| Tipos de OS | `/su_oss_tipo` |
| Planos | `/plano` |
| Produtos | `/produto` |
| Estoque | `/estoque_produto` |
| Movimentações | `/estoque_movimentacao` |
| NFS-e | `/fiscal_nfse` |
| NF-e | `/fiscal_nfe` |
| Técnicos | `/tecnico` |

## Configuração de acesso

Preencha em [[_meta/credenciais]] (nunca commitar dados reais).

## Documentação oficial

- Documentação IXC: painel do sistema em `Configurações > API`
