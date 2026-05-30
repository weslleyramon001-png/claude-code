---
tipo: conhecimento
titulo: IXC API — Referência Completa
tags: [ixc-provedor, api, rest]
relacionado: [visao-geral, moc-ixc-provedor]
---

# IXC API — Referência Completa

## Autenticação

```http
Authorization: Basic base64(usuario:token)
Content-Type: application/json
```

## Base URL

```
https://SEU_DOMINIO.ixcprovedor.com.br/webservice/v1/
```

## Padrão de filtros

```json
{
  "qtype": "campo_do_filtro",
  "query": "valor",
  "oper": "=",
  "page": 1,
  "rp": 20,
  "sortname": "id",
  "sortorder": "desc"
}
```

## Endpoints por módulo

### 👤 Clientes e Contratos
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/cliente` | Lista clientes |
| GET | `/cliente/{id}` | Detalhe do cliente |
| POST | `/cliente` | Criar cliente |
| PUT | `/cliente/{id}` | Atualizar cliente |
| GET | `/contrato` | Lista contratos |
| GET | `/contrato/{id}` | Detalhe do contrato |

### 💰 Financeiro
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/fin_titulo` | Lista títulos/faturas |
| GET | `/fin_titulo/{id}` | Detalhe da fatura |
| POST | `/fin_titulo` | Criar fatura |
| GET | `/fin_lancamento` | Lançamentos |
| GET | `/fin_inadimplente` | Lista inadimplentes |

### 🔧 Suporte / OS
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/su_oss_chamado` | Lista OS |
| GET | `/su_oss_chamado/{id}` | Detalhe da OS |
| POST | `/su_oss_chamado` | Criar OS |
| PUT | `/su_oss_chamado/{id}` | Atualizar OS |
| GET | `/su_oss_tipo` | Tipos de OS |
| GET | `/tecnico` | Lista técnicos |

### 🧾 Fiscal
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/fiscal_nfse` | Lista NFS-e |
| GET | `/fiscal_nfse/{id}` | Detalhe NFS-e |
| POST | `/fiscal_nfse` | Emitir NFS-e |
| GET | `/fiscal_nfe` | Lista NF-e |

### 📦 Estoque
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/estoque_produto` | Lista produtos |
| GET | `/estoque_saldo` | Saldo por produto |
| GET | `/estoque_movimentacao` | Movimentações |
| POST | `/estoque_movimentacao` | Registrar movimentação |

### 📡 Planos e Produtos
| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/plano` | Lista planos |
| GET | `/plano/{id}` | Detalhe do plano |
| POST | `/plano` | Criar plano |
| GET | `/produto` | Lista produtos |

## Relacionamentos

→ [[visao-geral]]
→ [[🗺️-mapas/moc-ixc-provedor]]
→ [[⚡-automacoes/índice]]
