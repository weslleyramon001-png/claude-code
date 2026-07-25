# Credenciais de Acesso — IXC Provedor

> ⚠️ **NUNCA commitar dados reais neste arquivo.**
> Use variáveis de ambiente ou um gerenciador de segredos.

## Template de configuração

```env
IXC_BASE_URL=https://SEU_DOMINIO.ixcprovedor.com.br/webservice/v1
IXC_TOKEN=SEU_TOKEN_AQUI
IXC_USER=email@provedor.com.br
```

## Como obter o token

1. Acesse o painel IXC como administrador
2. Vá em **Configurações > Usuários > seu usuário**
3. Aba **Token API**
4. Copie o token gerado

## Ambientes

| Ambiente | URL | Status |
|---|---|---|
| Produção | — | A configurar |
| Homologação | — | A configurar |

## Permissões necessárias na API

O usuário de API deve ter acesso de leitura/escrita aos módulos:
- Clientes e Contratos
- Financeiro
- OS/Suporte
- Fiscal
- Estoque
- Produtos/Planos
