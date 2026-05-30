---
tipo: mapa-de-conteudo
titulo: Fiscal — Mapa de Conteúdo
tags: [moc, fiscal, nfse, ixc-provedor]
---

# 🗺️ Fiscal — Mapa de Conteúdo

---

## Notas neste módulo

- [[📚-conhecimento/fiscal/nfse]] — Nota Fiscal de Serviço Eletrônica
- [[📚-conhecimento/fiscal/nfe]] — Nota Fiscal Eletrônica (produtos)
- [[📚-conhecimento/fiscal/regime-tributario]] — Simples, Lucro Presumido
- [[📚-conhecimento/fiscal/obrigacoes]] — SPED, EFD, DCTF

## Fluxos

```
Pagamento confirmado
  ↓
IXC gera NFS-e automaticamente
  ↓
Envio para prefeitura (webservice)
  ↓
Aprovada? ──→ SIM → PDF enviado ao cliente
  ↓ NÃO
Erro registrado → Alerta para equipe fiscal
  ↓
Correção e reenvio
```

## Conexões

- [[moc-financeiro]] — NFS-e é gerada após pagamento
- [[moc-produtos]] — Código de serviço vem do plano
- [[moc-ixc-provedor]] — Sistema raiz

## Automações disponíveis

- Notas emitidas no mês
- Notas com erro (rejeitadas)
- Alertas de vencimento do certificado digital
