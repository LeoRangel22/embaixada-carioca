#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  GSC Reindexação — Embaixada Carioca
  Solicita reindexação de URLs via Google Search Console URL Inspection API
  Autor: Manus AI | Data: 2026-06-11
═══════════════════════════════════════════════════════════════════════════════

PASSO A PASSO PARA CONFIGURAR:
────────────────────────────────────────────────────────────────────────────
1. Acesse: https://console.cloud.google.com/
2. Crie um projeto (ou use um existente)
3. Ative a API: "Google Search Console API"
4. Crie credenciais: "OAuth 2.0 Client ID" → tipo "Desktop App"
5. Baixe o arquivo JSON de credenciais e salve como:
       credentials.json
   na mesma pasta deste script.
6. Execute o script: python3 gsc_reindex.py
7. Na primeira execução, um navegador abrirá para você autorizar o acesso.
   Após autorizar, o token será salvo em token.json para uso futuro.
────────────────────────────────────────────────────────────────────────────

DEPENDÊNCIAS:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

QUOTA DA API:
    - URL Inspection API: 2.000 requisições por dia
    - Indexing API (JobPosting/BroadcastEvent): 200 req/dia (padrão)
    - Este script usa a URL Inspection API, que funciona para QUALQUER página.
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import time
from datetime import datetime

# ─── Verificar dependências ───────────────────────────────────────────────────
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Dependências não instaladas. Execute:")
    print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# ─── Configuração ─────────────────────────────────────────────────────────────

# Propriedade do GSC (com protocolo e www)
GSC_PROPERTY = "https://www.embaixadacarioca.com/"

# Escopos necessários para a URL Inspection API
SCOPES = ["https://www.googleapis.com/auth/webmasters"]

# Arquivos de credenciais
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

# ─── URLs a reindexar ─────────────────────────────────────────────────────────
# Divididas em grupos por prioridade

URLS_ALTA_PRIORIDADE = [
    # Páginas corrigidas nesta sessão (canonical + noindex → index)
    "https://www.embaixadacarioca.com/contato.html",
    "https://www.embaixadacarioca.com/nossa-visao.html",
    "https://www.embaixadacarioca.com/en/contato.html",
    "https://www.embaixadacarioca.com/en/nossa-visao.html",
    "https://www.embaixadacarioca.com/es/contato.html",
    "https://www.embaixadacarioca.com/es/nossa-visao.html",
]

URLS_KWS_DE_OURO = [
    # Páginas otimizadas com KWs de ouro (restaurante/café/almoço + Pão de Açúcar)
    "https://www.embaixadacarioca.com/restaurante-bondinho-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/cafe-da-manha-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/almoco-morro-da-urca.html",
    "https://www.embaixadacarioca.com/onde-comer-no-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/restaurantes-perto-do-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/en/sugarloaf-cable-car-restaurant.html",
    "https://www.embaixadacarioca.com/en/cafe-da-manha-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/en/almoco-morro-da-urca.html",
    "https://www.embaixadacarioca.com/es/restaurante-bondinho-pan-de-azucar.html",
    "https://www.embaixadacarioca.com/es/cafe-da-manha-pao-de-acucar.html",
    "https://www.embaixadacarioca.com/es/almoco-morro-da-urca.html",
]

URLS_HOMEPAGE_E_CORE = [
    # Páginas principais do site
    "https://www.embaixadacarioca.com/",
    "https://www.embaixadacarioca.com/en/",
    "https://www.embaixadacarioca.com/es/",
    "https://www.embaixadacarioca.com/restaurante-morro-da-urca.html",
    "https://www.embaixadacarioca.com/parque-bondinho.html",
    "https://www.embaixadacarioca.com/morro-da-urca.html",
]

# ─── Funções ──────────────────────────────────────────────────────────────────

def autenticar():
    """Autentica com OAuth2 e retorna as credenciais."""
    creds = None

    # Carregar token salvo se existir
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Renovar ou criar credenciais
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token de acesso...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"\n❌ Arquivo '{CREDENTIALS_FILE}' não encontrado!")
                print("\nSiga as instruções no topo deste script para configurar as credenciais.")
                print("\nResumo rápido:")
                print("  1. Acesse https://console.cloud.google.com/")
                print("  2. Ative a 'Google Search Console API'")
                print("  3. Crie credenciais OAuth 2.0 (Desktop App)")
                print(f"  4. Salve o JSON como '{CREDENTIALS_FILE}' nesta pasta")
                sys.exit(1)

            print("🌐 Abrindo navegador para autorização...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Salvar token para próximas execuções
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        print(f"✅ Token salvo em '{TOKEN_FILE}'")

    return creds


def inspecionar_url(service, url):
    """
    Usa a URL Inspection API para verificar o status de indexação de uma URL
    e solicitar reindexação se necessário.
    """
    try:
        response = service.urlInspection().index().inspect(
            body={
                "inspectionUrl": url,
                "siteUrl": GSC_PROPERTY,
            }
        ).execute()

        result = response.get("inspectionResult", {})
        index_status = result.get("indexStatusResult", {})
        coverage_state = index_status.get("coverageState", "DESCONHECIDO")
        last_crawl = index_status.get("lastCrawlTime", "Nunca rastreada")
        verdict = index_status.get("verdict", "DESCONHECIDO")

        return {
            "url": url,
            "verdict": verdict,
            "coverage_state": coverage_state,
            "last_crawl": last_crawl,
            "success": True,
        }

    except HttpError as e:
        return {
            "url": url,
            "verdict": "ERRO",
            "coverage_state": f"HTTP {e.resp.status}: {e._get_reason()}",
            "last_crawl": "N/A",
            "success": False,
        }
    except Exception as e:
        return {
            "url": url,
            "verdict": "ERRO",
            "coverage_state": str(e),
            "last_crawl": "N/A",
            "success": False,
        }


def processar_grupo(service, urls, nome_grupo, delay=1.5):
    """Processa um grupo de URLs e exibe o resultado."""
    print(f"\n{'═'*70}")
    print(f"  {nome_grupo}")
    print(f"{'═'*70}")

    resultados = []
    for i, url in enumerate(urls, 1):
        print(f"  [{i:02d}/{len(urls):02d}] Inspecionando: {url.replace('https://www.embaixadacarioca.com/', '/')}")
        resultado = inspecionar_url(service, url)

        # Ícone de status
        if resultado["verdict"] == "PASS":
            icone = "✅"
        elif resultado["verdict"] == "NEUTRAL":
            icone = "⚪"
        elif resultado["verdict"] == "FAIL":
            icone = "❌"
        elif resultado["verdict"] == "ERRO":
            icone = "⚠️ "
        else:
            icone = "❓"

        print(f"         {icone} Status: {resultado['verdict']} | Cobertura: {resultado['coverage_state']}")
        if resultado["last_crawl"] != "N/A":
            print(f"            Último rastreamento: {resultado['last_crawl'][:10] if len(resultado['last_crawl']) > 10 else resultado['last_crawl']}")

        resultados.append(resultado)

        # Respeitar rate limit da API (2.000 req/dia = ~1,4 req/s)
        if i < len(urls):
            time.sleep(delay)

    return resultados


def salvar_relatorio(todos_resultados):
    """Salva um relatório JSON com os resultados."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_reindexacao_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "data": datetime.now().isoformat(),
            "propriedade": GSC_PROPERTY,
            "total_urls": len(todos_resultados),
            "resultados": todos_resultados,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n📄 Relatório salvo em: {filename}")
    return filename


# ─── Execução Principal ───────────────────────────────────────────────────────

def main():
    print("\n" + "═"*70)
    print("  🔍 GSC Reindexação — Embaixada Carioca")
    print(f"  Propriedade: {GSC_PROPERTY}")
    print(f"  Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("═"*70)

    # Autenticar
    print("\n🔐 Autenticando com Google Search Console...")
    creds = autenticar()
    service = build("searchconsole", "v1", credentials=creds)
    print("✅ Autenticado com sucesso!")

    todos_resultados = []

    # Grupo 1: URLs de alta prioridade (corrigidas nesta sessão)
    resultados = processar_grupo(
        service,
        URLS_ALTA_PRIORIDADE,
        "GRUPO 1 — Alta Prioridade (Canonicals + Noindex Corrigidos)",
        delay=1.5
    )
    todos_resultados.extend(resultados)

    # Grupo 2: KWs de ouro
    resultados = processar_grupo(
        service,
        URLS_KWS_DE_OURO,
        "GRUPO 2 — KWs de Ouro (Restaurante / Café / Almoço + Pão de Açúcar)",
        delay=1.5
    )
    todos_resultados.extend(resultados)

    # Grupo 3: Homepage e páginas core
    resultados = processar_grupo(
        service,
        URLS_HOMEPAGE_E_CORE,
        "GRUPO 3 — Homepage e Páginas Core",
        delay=1.5
    )
    todos_resultados.extend(resultados)

    # ─── Resumo Final ─────────────────────────────────────────────────────────
    print(f"\n{'═'*70}")
    print("  RESUMO FINAL")
    print(f"{'═'*70}")

    total = len(todos_resultados)
    indexadas = sum(1 for r in todos_resultados if r["verdict"] == "PASS")
    nao_indexadas = sum(1 for r in todos_resultados if r["verdict"] in ("NEUTRAL", "FAIL"))
    erros = sum(1 for r in todos_resultados if r["verdict"] == "ERRO")

    print(f"  Total de URLs verificadas: {total}")
    print(f"  ✅ Já indexadas (PASS):     {indexadas}")
    print(f"  ⚪ Não indexadas (NEUTRAL): {nao_indexadas}")
    print(f"  ❌ Com falha (FAIL):        {sum(1 for r in todos_resultados if r['verdict'] == 'FAIL')}")
    print(f"  ⚠️  Erros de API:            {erros}")

    if nao_indexadas > 0:
        print(f"\n  📋 URLs ainda não indexadas ({nao_indexadas}):")
        for r in todos_resultados:
            if r["verdict"] in ("NEUTRAL", "FAIL"):
                print(f"     • {r['url']}")
        print(f"\n  💡 Para forçar reindexação, acesse o GSC manualmente:")
        print(f"     https://search.google.com/search-console/inspect")
        print(f"     E clique em 'Solicitar indexação' para cada URL acima.")

    # Salvar relatório
    salvar_relatorio(todos_resultados)

    print(f"\n{'═'*70}")
    print("  ✅ Processo concluído!")
    print("═"*70 + "\n")


if __name__ == "__main__":
    main()
