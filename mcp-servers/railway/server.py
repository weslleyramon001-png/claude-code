#!/usr/bin/env python3
"""
Railway MCP Server — JARBAS
Gerencia deploys, variáveis e logs do Railway via GraphQL API.
Token: variável RAILWAY_API_TOKEN
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

RAILWAY_API = "https://backboard.railway.app/graphql/v2"

mcp = FastMCP("railway")


def _headers() -> dict:
    token = os.environ.get("RAILWAY_API_TOKEN", "")
    if not token:
        raise ValueError("RAILWAY_API_TOKEN não definido")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _gql(query: str, variables: dict = None) -> dict:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = httpx.post(RAILWAY_API, json=payload, headers=_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"Railway API erro: {data['errors']}")
    return data.get("data", {})


# ── Ferramentas ──────────────────────────────────────────────────────────────

@mcp.tool()
def railway_projetos() -> str:
    """Lista todos os projetos Railway do usuário com IDs e status."""
    data = _gql("""
    query {
      me {
        projects {
          edges {
            node {
              id
              name
              description
              environments {
                edges { node { id name } }
              }
              services {
                edges { node { id name } }
              }
            }
          }
        }
      }
    }
    """)
    projetos = data.get("me", {}).get("projects", {}).get("edges", [])
    resultado = []
    for p in projetos:
        n = p["node"]
        servicos = [s["node"]["name"] for s in n.get("services", {}).get("edges", [])]
        envs = [e["node"]["name"] for e in n.get("environments", {}).get("edges", [])]
        resultado.append({
            "id": n["id"],
            "nome": n["name"],
            "descricao": n.get("description", ""),
            "servicos": servicos,
            "ambientes": envs,
        })
    return json.dumps(resultado, ensure_ascii=False, indent=2)


@mcp.tool()
def railway_status(project_id: str) -> str:
    """
    Status atual de um projeto: serviços e último deployment de cada um.
    Args:
        project_id: ID do projeto Railway
    """
    data = _gql("""
    query Status($id: String!) {
      project(id: $id) {
        id
        name
        services {
          edges {
            node {
              id
              name
              deployments(first: 3) {
                edges {
                  node {
                    id
                    status
                    createdAt
                    url
                    meta
                  }
                }
              }
            }
          }
        }
      }
    }
    """, {"id": project_id})
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def railway_logs(deployment_id: str, limit: int = 100) -> str:
    """
    Logs de um deployment específico.
    Args:
        deployment_id: ID do deployment
        limit: número máximo de linhas (padrão 100)
    """
    data = _gql("""
    query Logs($deploymentId: String!, $limit: Int) {
      deploymentLogs(deploymentId: $deploymentId, limit: $limit) {
        timestamp
        message
        severity
      }
    }
    """, {"deploymentId": deployment_id, "limit": limit})
    logs = data.get("deploymentLogs", [])
    linhas = [f"[{l.get('severity','INFO')}] {l.get('timestamp','')} — {l.get('message','')}" for l in logs]
    return "\n".join(linhas) if linhas else "Nenhum log encontrado."


@mcp.tool()
def railway_variaveis_listar(project_id: str, service_id: str, environment_id: str) -> str:
    """
    Lista variáveis de ambiente de um serviço.
    Args:
        project_id: ID do projeto
        service_id: ID do serviço
        environment_id: ID do ambiente (ex: production)
    """
    data = _gql("""
    query Vars($projectId: String!, $serviceId: String!, $environmentId: String!) {
      variables(projectId: $projectId, serviceId: $serviceId, environmentId: $environmentId)
    }
    """, {"projectId": project_id, "serviceId": service_id, "environmentId": environment_id})
    variaveis = data.get("variables", {})
    # Ocultar valores de chaves sensíveis
    sensiveis = {"API_KEY", "TOKEN", "SECRET", "PASSWORD", "PASS"}
    resultado = {}
    for k, v in variaveis.items():
        if any(s in k.upper() for s in sensiveis):
            resultado[k] = "***oculto***"
        else:
            resultado[k] = v
    return json.dumps(resultado, ensure_ascii=False, indent=2)


@mcp.tool()
def railway_variavel_definir(
    project_id: str,
    service_id: str,
    environment_id: str,
    nome: str,
    valor: str,
) -> str:
    """
    Define ou atualiza uma variável de ambiente no Railway.
    Args:
        project_id: ID do projeto
        service_id: ID do serviço
        environment_id: ID do ambiente
        nome: nome da variável (ex: ELEVENLABS_API_KEY)
        valor: valor da variável
    """
    data = _gql("""
    mutation SetVar($input: VariableUpsertInput!) {
      variableUpsert(input: $input)
    }
    """, {
        "input": {
            "projectId": project_id,
            "serviceId": service_id,
            "environmentId": environment_id,
            "name": nome,
            "value": valor,
        }
    })
    sucesso = data.get("variableUpsert", False)
    if sucesso:
        return f"✅ Variável '{nome}' definida com sucesso."
    return f"⚠️ Retorno inesperado: {data}"


@mcp.tool()
def railway_redeploy(service_id: str, environment_id: str) -> str:
    """
    Força um novo deploy de um serviço no Railway.
    Args:
        service_id: ID do serviço
        environment_id: ID do ambiente
    """
    data = _gql("""
    mutation Redeploy($serviceId: String!, $environmentId: String!) {
      serviceInstanceRedeploy(serviceId: $serviceId, environmentId: $environmentId)
    }
    """, {"serviceId": service_id, "environmentId": environment_id})
    return f"✅ Redeploy disparado: {json.dumps(data, ensure_ascii=False)}"


@mcp.tool()
def railway_deployment_cancelar(deployment_id: str) -> str:
    """
    Cancela um deployment em andamento.
    Args:
        deployment_id: ID do deployment a cancelar
    """
    data = _gql("""
    mutation Cancel($id: String!) {
      deploymentCancel(id: $id)
    }
    """, {"id": deployment_id})
    return f"✅ Deployment cancelado: {json.dumps(data, ensure_ascii=False)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
